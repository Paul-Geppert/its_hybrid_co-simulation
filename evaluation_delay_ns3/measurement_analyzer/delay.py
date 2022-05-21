import logging
import matplotlib
import matplotlib.pyplot as plt

from .measurement_helper import extract_measurement_data, extract_time_for_messages_lteUeNetDevice, extract_time_for_raw_message_hash_lteSpectrumPhy, Measurement
from .output_helper import ResultType

logger = logging.getLogger("Delay Analyzer")

def analyze_delay_python_end_to_end(filename, output_helper):
    measurement_data = extract_measurement_data(filename, Measurement.RECEIVE)

    message_ids = list(map(lambda d: int(d.split(",")[0]), measurement_data))
    delay = list(map(lambda d: float(d.split(",")[1]) / 1000, measurement_data))

    output_helper.log_delay(message_ids, delay, ResultType.PYTHON)

def analyze_delay_pcap_LteUeNetDevice_end_to_end(filename_sender, filename_receiver, cv2x_udp_port, output_helper):
    message_timestamp_dict_sender = extract_time_for_messages_lteUeNetDevice(filename_sender, cv2x_udp_port)
    message_timestamp_dict_receiver = extract_time_for_messages_lteUeNetDevice(filename_receiver, cv2x_udp_port)

    message_ids = []
    delays = []

    for message, recv_timestamp_in_sec in message_timestamp_dict_receiver.items():
        send_timestamp_in_sec = message_timestamp_dict_sender[message]
        delay = recv_timestamp_in_sec * 1000 - send_timestamp_in_sec * 1000

        message_id = int(message.split(";")[0])
        message_ids.append(message_id)
        delays.append(delay)

    output_helper.log_delay(message_ids, delays, ResultType.LTE_UE_NET_DEVICE)

def analyze_delay_pcap_LteSpectrumPhy_end_to_end(filename_sender, filename_receiver, output_helper):
    message_hash_timestamp_dict_sender = extract_time_for_raw_message_hash_lteSpectrumPhy(filename_sender)
    message_hash_timestamp_dict_receiver = extract_time_for_raw_message_hash_lteSpectrumPhy(filename_receiver)

    sent_messages = list(message_hash_timestamp_dict_sender.keys())

    message_ids = []
    delays = []

    for message, recv_timestamp_in_sec in message_hash_timestamp_dict_receiver.items():
        send_timestamp_in_sec = message_hash_timestamp_dict_sender[message]
        delay = recv_timestamp_in_sec * 1000 - send_timestamp_in_sec * 1000

        message_id = sent_messages.index(message)
        message_ids.append(message_id)
        delays.append(delay)

    output_helper.log_delay(message_ids, delays, ResultType.LTE_SPECTRUM_PHY)
