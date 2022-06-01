import pyshark

from enum import Enum

class Measurement(Enum):
    SEND = 0
    RECEIVE = 1

def extract_measurement_data(filename, mode: Measurement):
    with open(filename, "r") as measurement_file:
        lines = measurement_file.read().splitlines()
    
    if mode == Measurement.SEND:
        log_key = "MEASUREMENT_SENT:"
    elif mode == Measurement.RECEIVE:
        log_key = "MEASUREMENT_RECEIVE:"
    else:
        print("Unknown measurement type. Returning empty data")
        return []
    
    measurement_lines = filter(lambda l: log_key in l, lines)
    measurement_results = list(map(lambda l: l.split(log_key)[1], measurement_lines))
    return measurement_results

def extract_time_for_messages_lteUeNetDevice(filename, cv2x_udp_port):
    cap = pyshark.FileCapture(filename, display_filter=f'udp.port=={cv2x_udp_port}')
    cap.load_packets()

    results = {}

    for p in cap:
        results[bytes.fromhex(p.data.data).decode()] = float(p.sniff_timestamp)

    return results

def extract_time_for_raw_message_hash_lteSpectrumPhy(filename):
    cap = pyshark.FileCapture(filename, include_raw=True, use_json=True)
    cap.load_packets()

    results = {}

    for p in cap:
        results[hash(p.get_raw_packet())] = float(p.sniff_timestamp)

    return results
