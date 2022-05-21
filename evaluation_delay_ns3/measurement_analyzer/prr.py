import logging

from .measurement_helper import extract_measurement_data, Measurement

logger = logging.getLogger("PRR Analyzer")

def analyze_prr(sender_filename, receiver_filename, output_helper):
    packets_sent = extract_measurement_data(sender_filename, Measurement.SEND)
    packets_received = extract_measurement_data(receiver_filename, Measurement.RECEIVE)

    output_helper.log_prr(packets_sent, packets_received)
