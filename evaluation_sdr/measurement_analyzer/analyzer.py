import argparse
import logging
import os

from .measurement_helper import extract_measurement_data
from .output_helper import OutputHelper

def gather_directories(distance, gain):
    log_dir = os.path.join(os.getcwd(), "simulation-logs-client")
    result_dirs = os.listdir(log_dir)
    result_dirs = list(filter(lambda l: f"_dist_{distance}_gain_{gain}" in l, result_dirs))
    result_dirs = list(map(lambda l: os.path.join(log_dir, l), result_dirs))
    return result_dirs

def main():
    def analyze_results(log_directories, output_helper):
        all_hot_message_ids = []
        all_hot_latencies = []

        total_hot_sent_packets = len(log_directories) * (args.num_packets_sent - args.num_cold_run)

        for log_dir in log_directories:
            data_file = os.path.join(log_dir, "client.log")
            measurement_data = extract_measurement_data(data_file)

            message_ids = list(map(lambda d: int(d.split(",")[0]), measurement_data))
            hot_message_ids = message_ids[args.num_cold_run:]
            latencies = list(map(lambda d: float(d.split(",")[1]) / 1000, measurement_data))
            hot_latencies = latencies[args.num_cold_run:]

            all_hot_message_ids.extend(hot_message_ids)
            all_hot_latencies.extend(hot_latencies)

        output_helper.log_latency(all_hot_message_ids, all_hot_latencies)
        output_helper.log_pdr(total_hot_sent_packets, len(all_hot_message_ids))

    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', '-o',
        default="measurement_results",
        help='the directory to write the results to.')
    parser.add_argument('--num-packets-sent', '-n',
        default=160,
        help='the number of total packets sent (including cold runs). Default: 160')
    parser.add_argument('--num-cold-run', '-c',
        default=10,
        help='the number of cold runs. Default: 10')
    args = parser.parse_args()

    output_helper = OutputHelper(args.output_dir)

    configs = [
        { "distance": 1, "gain": 50 },
        { "distance": 1, "gain": 60 },
        { "distance": 1, "gain": 90 },
        { "distance": 4, "gain": 60 },
        { "distance": 4, "gain": 90 },
        { "distance": 6, "gain": 60 },
        { "distance": 6, "gain": 75 },
        { "distance": 6, "gain": 90 },
        { "distance": 8, "gain": 60 },
        { "distance": 8, "gain": 75 },
        { "distance": 8, "gain": 90 },
    ]
    
    # for c in configs:
    #     distance, gain = c["distance"], c["gain"]

    #     output_helper.distance = distance
    #     output_helper.gain = gain

    #     log_directories = gather_directories(distance, gain)
        
    #     analyze_results(log_directories, output_helper)

    output_helper.create_average_graphics()
    output_helper.create_boxplot(configs=[
        # { "distance": 1, "gain": 60 },
        # { "distance": 4, "gain": 60 },
        # { "distance": 6, "gain": 60 },
        # { "distance": 8, "gain": 60 }
        { "distance": 1, "gain": 50 },
        { "distance": 1, "gain": 60 },
        { "distance": 1, "gain": 90 },
        { "distance": 4, "gain": 60 },
        { "distance": 4, "gain": 90 },
        { "distance": 6, "gain": 60 },
        { "distance": 6, "gain": 75 },
        { "distance": 6, "gain": 90 },
        { "distance": 8, "gain": 60 },
        { "distance": 8, "gain": 75 },
        { "distance": 8, "gain": 90 },
    ])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
