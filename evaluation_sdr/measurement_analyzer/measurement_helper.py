import pyshark

from enum import Enum

class Measurement(Enum):
    SEND = 0
    RECEIVE = 1

def extract_measurement_data(filename, mode: Measurement = Measurement.RECEIVE):
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
