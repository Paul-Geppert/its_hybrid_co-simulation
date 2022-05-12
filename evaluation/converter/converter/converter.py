import argparse
import json
import logging
import pyshark
import socket

from pyshark.packet.packet import Packet
from ctypes import CDLL, c_char_p, c_int, c_void_p, Structure, POINTER

from .mqtt_sender import MQTTSender

class ConversionResult(Structure):
    _fields_ = [("size", c_int), ("buffer", c_void_p)]

def get_sidelink_ip(cv2x_ip_base, ifname):
    import fcntl
    import ipaddress
    import struct

    def get_ip_address(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    def get_netmask(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x891b,
            struct.pack('256s', ifname)
        )[20:24])

    iface_ip = get_ip_address(ifname)
    netmask = get_netmask(ifname)

    cv2x_iface = ipaddress.ip_interface(f"{iface_ip}/{netmask}")
    base = int(cv2x_iface.ip) - int(cv2x_iface.network.network_address)

    sidelink_network = ipaddress.ip_network(f"{cv2x_ip_base}/{netmask}")
    sidelink_ip = ipaddress.ip_address(int(sidelink_network.network_address) + base)
    return str(sidelink_ip)

def main():
    def encode_and_print_as_xml(enc_functions, packet, message_id, protocol_version):
        encoding_function = enc_functions.encodeToXer
        encoding_function.argtypes = (c_int, c_int, c_char_p, c_int)
        encoding_function.restype = POINTER(ConversionResult)

        data = bytes.fromhex(packet.its_raw.value)

        data_pointer = c_char_p(data)
        data_length = len(data)

        encoding_result = encoding_function(message_id, protocol_version, data_pointer, data_length)

        if encoding_result.contents.size < 0:
            # Failed to encode
            enc_functions.freeConversionResult(encoding_result)
            return

        # Encoded successfully!
        xml_message = c_char_p(encoding_result.contents.buffer)
        # Last symbol will be a new line, we don't need it
        xml_message = xml_message.value.decode()[:-1]

        enc_functions.freeConversionResult(encoding_result)

        return xml_message

    def resend_as_cv2x_and_forward_to_mqtt(packet):
        packet: Packet = packet

        if packet.highest_layer != 'ITS_RAW':
            logger.info(f"This message is not a ITS message: {packet.highest_layer}")
            return

        # Send packet on C-V2X
        cv2x_socket.sendto(bytes.fromhex(packet.its_raw.value), (cv2x_sidelink_addr, cv2x_udp_port))

        # Convert supported messages to XMl and send them to the MQTT server
        message_type_id = packet.its.ItsPduHeader_element.messageID.main_field.int_value
        if message_type_id not in message_id_send_map:
            logger.info(f"This message type (id {message_type_id}) supported yet")
            return

        protocol_version = packet.its.ItsPduHeader_element.protocolVersion.main_field.int_value

        xml_message = encode_and_print_as_xml(my_functions, packet, message_type_id, protocol_version)

        # send message according to type
        message_id_send_map[message_type_id](xml_message)

    ########## main ##########

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--interface-itsg5', '-ii',
            default='v2x',
            help='the interface to read messages from. Default: v2x')
    parser.add_argument('--interface-cv2x', '-ic',
            default='cv2x',
            help='the interface to send cv2x messages to. Default: cv2x')
    parser.add_argument('--log-file', '-l',
            default='',
            help='the location of the log file. If not specified, stderr is used. Default: stderr is used')
    parser.add_argument('--config-file', '-c',
            default='./config.json',
            help='the config file containing application settings')

    args = parser.parse_args()

    if len(args.log_file) > 0:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d-%y %H:%M:%S',
                            filename=args.log_file,
                            filemode='w')
    else:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d-%y %H:%M:%S')

    logger = logging.getLogger("Converter")

    with open(args.config_file, 'r') as config_file:
        config = json.load(config_file)

    sender = MQTTSender(config['mqtt_config'])

    message_id_send_map = {
        4: sender.send_spatem,
        5: sender.send_mapem
    }

    my_functions = CDLL(config['app_config']['converter_file_path'])

    # Open socket to send C-V2X messages to
    cv2x_ip_base = config['app_config']['cv2x_ip_base']
    cv2x_udp_port = config['app_config']['cv2x_udp_port']
    cv2x_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    cv2x_sidelink_addr = get_sidelink_ip(cv2x_ip_base, args.interface_cv2x.encode())

    capture = pyshark.LiveCapture(interface=args.interface_itsg5, include_raw=True, use_json=True)
    capture.apply_on_packets(resend_as_cv2x_and_forward_to_mqtt)
