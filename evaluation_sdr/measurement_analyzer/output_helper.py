import os

import matplotlib.pyplot as plt

class OutputHelper:
    def __init__(self, output_dir) -> None:
        self.output_dir = output_dir

        self.average_latency_python = output_dir + "/sdr_average_latency_python.csv"
        self.average_latency_python_img = output_dir + "/sdr_average_latency_python.pdf"

        self.packet_delivery_rate = output_dir + "/sdr_pdr.csv"
        self.packet_delivery_rate_img = output_dir + "/sdr_pdr.pdf"
        
        self.distance = 0
        self.gain = 0

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if not os.path.exists(self.average_latency_python):
            with open(self.average_latency_python, "w") as result_file:
                result_file.write("distance,gain,avg_latency\n")

        if not os.path.exists(self.packet_delivery_rate):
            with open(self.packet_delivery_rate, "w") as pdr_file:
                pdr_file.write("distance,gain,pdr\n")


    def log_latency(self, message_ids, latencies):
        result_file = open(self.output_dir + f"/dist_{self.distance}_gain_{self.gain}_latency_python.csv", "w")
        avg_result_file = open(self.average_latency_python, "a")
        
        result_file.write("message_id,latency\n")
        for id, latency in zip(message_ids, latencies):
            result_file.write(f"{id},{latency}\n")

        if len(latencies) > 0:
            avg_latency = sum(latencies) / len(latencies)
        else:
            avg_latency = -1
        avg_result_file.write(f"{self.distance},{self.gain},{avg_latency}\n")

        result_file.close()
        avg_result_file.close()


    def log_pdr(self, num_packets_sent, num_packets_received):
        if num_packets_sent > 0:
            pdr = num_packets_received / num_packets_sent
        else:
            pdr = -1

        with open(self.packet_delivery_rate, "a") as pdr_file:
            pdr_file.write(f"{self.distance},{self.gain},{pdr}\n")

    def create_average_graphics(self):
        self._create_graphic_average_latency_python()
        self._create_graphic_packet_delivery_rate()

    def _create_graphic_average_latency_python(self):
        with open(self.average_latency_python, "r") as result_file:
            lines = result_file.read().splitlines()
        lines = lines[1:]

        self._plot_average_data(
            lines,
            title="Avg. Packet Transmission Time - Application (Python)",
            label_y="Zeit in ms",
            output_file=self.average_latency_python_img
        )

    def _create_graphic_packet_delivery_rate(self):
        with open(self.packet_delivery_rate, "r") as result_file:
            lines = result_file.read().splitlines()
        lines = lines[1:]

        self._plot_average_data(
            lines,
            title="PDR",
            label_y="PDR",
            output_file=self.packet_delivery_rate_img
        )

    def _plot_average_data(self, lines, title=None, label_x="Distanz in m", label_y=None, prefix_legend="Gain", unit_legend="dB", output_file=None):
        distinct_tx_powers = set(list(map(lambda l: l.split(",")[1], lines)))
        distinct_tx_powers = sorted(distinct_tx_powers, key=lambda p: float(p))

        all_data_series = []
        labels = []

        for tx_power in distinct_tx_powers:
            experiments_with_tx_power = list(filter(lambda l: l.split(",")[1] == tx_power, lines))
            data_series = []
            for m in experiments_with_tx_power:
                distance, _, avg_value = m.split(",")
                if avg_value == "-1":
                    continue
                distance = int(distance)
                avg_value = float(avg_value)
                data_series.append([distance, avg_value])
            data_series = sorted(data_series, key=lambda m: m[0])   # Sort by distance
            all_data_series.append(data_series)

            label = str(int(tx_power))
            if prefix_legend:
                label = f"{prefix_legend} {label}"
            if unit_legend:
                label = f"{label} {unit_legend}"
            labels.append(label)
        
        for idx, data_series in enumerate(all_data_series):
            data_x = list(map(lambda d: d[0], data_series))
            data_y = list(map(lambda d: d[1], data_series))

            plt.plot(data_x, data_y, label=labels[idx])

        if label_x:
            plt.xlabel(label_x)
        if label_y:
            plt.ylabel(label_y)
        
        plt.legend()

        if output_file:
            plt.savefig(output_file, format="pdf", bbox_inches="tight")

        if title:
            plt.title(title)
        plt.show()

    def create_boxplot(self, configs=[], print_to_file=True):
        box_data = []
        labels=[]

        for c in configs:
            distance, gain = c["distance"], c["gain"]
            with open(self.output_dir + f"/dist_{distance}_gain_{gain}_latency_python.csv", "r") as result_file:
                lines = result_file.read().splitlines()
            lines = lines[1:]

            data_y_python = list(map(lambda l: float(l.split(",")[1]), lines))
            label = f"{distance} m,\n{gain} dB"

            box_data.append(data_y_python)
            labels.append(label)

        # plt.figure(figsize=(3, 4.8))
        plt.boxplot(box_data, labels=labels)
        plt.ylabel("Zeit in ms")

        # ax = plt.gca()
        # ax.get_yaxis().set_ticklabels("")

        if print_to_file:
            plt.savefig(f"{self.output_dir}/sdr_latency_boxplot.pdf", format="pdf", bbox_inches="tight")

        plt.title("Combined boxplot for L_python")
        plt.show()
