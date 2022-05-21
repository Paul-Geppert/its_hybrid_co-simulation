import argparse
import logging
import matplotlib
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f',
            help='the file to extract and analyze delay times from.')
    parser.add_argument('--num-cold-run', '-c',
            default=10,
            help='the number of cold runs which will be ignored in the evaluation. Default: 10')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%y-%m-%d %H:%M:%S')

    logger = logging.getLogger("Delay_Evaluator")

    if (args.file is None):
        logger.error("Please specify an input file")
        exit(1)

    with open(args.file, "r") as f:
        lines = f.read().splitlines()
    
    lines_with_data = list(filter(lambda l: "DELAY:" in l, lines))
    data_x = list(map(lambda l: int((l.split("DELAY:")[1]).split(",")[0]), lines_with_data))[args.num_cold_run:]
    data_y = list(map(lambda l: int((l.split("DELAY:")[1]).split(",")[1]) / 1000, lines_with_data))[args.num_cold_run:]

    fig, ax = plt.subplots()
    ticker = matplotlib.ticker.EngFormatter(unit='')
    ax.axes.set_title("Delay of C-V2X messages")
    ax.axes.set_ylabel("delay in ms")
    ax.get_yaxis().set_major_formatter(ticker)
    ax.plot(data_x, data_y)
    plt.show()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
