import argparse
import datetime
import logging
import os
import socket
from time import sleep

from .cv2x_helper import get_sidelink_ip

def main():
    def enterSendingLoop(num_packets):
        id = 0
        for _ in range(num_packets):
            message = str(id).zfill(3) + ";"
            message = message + datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%dT%H:%M:%S.%f")
            cv2x_socket_ns3.sendto(message.encode(), (cv2x_sidelink_addr_ns3, args.cv2x_udp_port))
            logger.info(f"MEASUREMENT_SENT:{id}")
            id = (id + 1) % 1000
            sleep(0.5)

    def enterReceivingLoop(num_packets):
        cv2x_socket_ns3.bind(('', args.cv2x_udp_port))

        num_received = 0

        while num_received < num_packets:
            message = cv2x_socket_ns3.recv(1024)
            recv_time = datetime.datetime.now()

            num_received = num_received + 1

            message = message.decode()
            id, send_time_str = message.split(";")
            send_time = datetime.datetime.fromisoformat(send_time_str)

            # We expect time diff to not be less than 1 minute
            time_diff = recv_time - send_time
            time_diff_in_usec = time_diff.seconds * 1e6 + time_diff.microseconds
            
            # Log measurement, prefix with MEASUREMENT_RECEIVE to filter it from the output file later
            logger.info(f"MEASUREMENT_RECEIVE:{id},{time_diff_in_usec}")


    parser = argparse.ArgumentParser()
    parser.add_argument('--interface-cv2x', '-i',
            default='cv2x',
            help='the interface to send cv2x messages to. Default: cv2x')
    parser.add_argument('--cv2x-ip-base', '-b',
            default='225.0.0.0',
            help='the CV2X SL IP base to calculate Sidelink IP address. Default: 225.0.0.0')
    parser.add_argument('--cv2x-udp-port', '-p',
            default=20001,
            help='the port to send C-V2X UDP messages. Default: 20001')
    parser.add_argument('--num-packets', '-n',
            default=160,
            help='the number of packets to send')
    parser.add_argument('--log-file', '-l',
            default='',
            help='the location of the log file. If not specified, stderr is used. Default: stderr is used')

    args = parser.parse_args()

    if len(args.log_file) > 0:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%y-%m-%d %H:%M:%S',
                            filename=args.log_file,
                            filemode='w')
    else:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%y-%m-%d %H:%M:%S')

    logger = logging.getLogger(f"ns_3_Latency_{os.environ['LATENCY_ROLE']}")

    logger.info("Using C-V2X via ns-3")
    cv2x_socket_ns3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    cv2x_sidelink_addr_ns3 = get_sidelink_ip(args.cv2x_ip_base, args.interface_cv2x.encode())

    if os.environ["LATENCY_ROLE"] == "SENDER":
        enterSendingLoop(args.num_packets)
    else:
        enterReceivingLoop(args.num_packets)

