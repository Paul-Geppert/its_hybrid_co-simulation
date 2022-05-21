import argparse
import logging

from .delay import analyze_delay_python_end_to_end, analyze_delay_pcap_LteUeNetDevice_end_to_end, analyze_delay_pcap_LteSpectrumPhy_end_to_end
from .prr import analyze_prr
from .output_helper import OutputHelper

def main():
    def analyze_results(log_directory, cv2x_udp_port, output_helper):
        sender_log = log_directory + "/ns3_delay_sender.stderr.log"
        receiver_log = log_directory + "/ns3_delay_receiver.stderr.log"

        # Analyze delay in Python end-to-end
        analyze_delay_python_end_to_end(receiver_log, output_helper)

        # Analyze delay from PCAP-Files (End-to-End LteUeNetDevice and End-to-End LteSpectrumPhy)
        senderLteUeNetDevice_pcap = log_directory + "/simple-ns3_delay_sender.cv2x.pcap"
        receiverLteUeNetDevice_pcap = log_directory + "/simple-ns3_delay_receiver.cv2x.pcap"
        analyze_delay_pcap_LteUeNetDevice_end_to_end(senderLteUeNetDevice_pcap, receiverLteUeNetDevice_pcap, cv2x_udp_port, output_helper)

        senderLteSpectrumPhy_pcap = log_directory + "/ns3_delay_sender.cv2x.pcap"
        receiverLteSpectrumPhy_pcap = log_directory + "/ns3_delay_receiver.cv2x.pcap"
        analyze_delay_pcap_LteSpectrumPhy_end_to_end(senderLteSpectrumPhy_pcap, receiverLteSpectrumPhy_pcap, output_helper)

        # Analyze Packet Reception Rate (PRR)
        analyze_prr(sender_log, receiver_log, output_helper)

    parser = argparse.ArgumentParser()
    parser.add_argument('--results-file', '-f',
        default="evaluation_delay_ns3_configs.log",
        help='the file to extract and analyze delay times from.')
    parser.add_argument('--output-dir', '-o',
        default="measurement_results",
        help='the directory to write the results to.')
    parser.add_argument('--cv2x-udp-port', '-p',
        default=20001,
        help='the port C-V2X UDP messages will be sent to. Default: 20001')
    parser.add_argument('--num-cold-run', '-c',
        default=10,
        help='the number of cold runs which will be ignored in the evaluation. Default: 10')
    args = parser.parse_args()

    logger = logging.getLogger("Results Analyzer")

    if (args.results_file is None):
        logger.error("Please specify an input file")
        exit(1)

    with open(args.results_file, "r") as result_file:
        results = result_file.read().splitlines()
        # Skip header
        results = results[1:]

    output_helper = OutputHelper(args.num_cold_run, args.output_dir)
    
    for r in results:
        distance, tx_power, log_directory = r.split(",")

        output_helper.distance = distance
        output_helper.tx_power = tx_power
        
        analyze_results(log_directory, args.cv2x_udp_port, output_helper)

    output_helper.create_average_graphics()
    output_helper.create_delay_graphic(distance=100, tx_power=20)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
