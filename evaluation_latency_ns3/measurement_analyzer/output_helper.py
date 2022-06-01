import os

import matplotlib.pyplot as plt

from enum import Enum

class ResultType(Enum):
    PYTHON = 0
    LTE_UE_NET_DEVICE = 1
    LTE_SPECTRUM_PHY = 2

class OutputHelper:
    def __init__(self, num_cold_run, output_dir) -> None:
        self.num_cold_run = num_cold_run
        self.output_dir = output_dir

        self.average_latency_python = output_dir + "/average_latency_python.csv"
        self.average_latency_python_img = output_dir + "/average_latency_python.pdf"
        
        self.average_latency_lteUeNetDevice = output_dir + "/average_latency_lteUeNetDevice.csv"
        self.average_latency_lteUeNetDevice_img = output_dir + "/average_latency_lteUeNetDevice.pdf"

        self.average_latency_lteSpectrumPhy = output_dir + "/average_latency_lteSpectrumPhy.csv"
        self.average_latency_lteSpectrumPhy_img = output_dir + "/average_latency_lteSpectrumPhy.pdf"

        self.packet_reception_rate = output_dir + "/pdr.csv"
        self.packet_reception_rate_img = output_dir + "/pdr.pdf"
        
        self.distance = 0
        self.tx_power = 0

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if not os.path.exists(self.average_latency_python):
            with open(self.average_latency_python, "w") as result_file:
                result_file.write("distance,tx_power,avg_latency\n")
        if not os.path.exists(self.average_latency_lteUeNetDevice):
            with open(self.average_latency_lteUeNetDevice, "w") as result_file:
                result_file.write("distance,tx_power,avg_latency\n")
        if not os.path.exists(self.average_latency_lteSpectrumPhy):
            with open(self.average_latency_lteSpectrumPhy, "w") as result_file:
                result_file.write("distance,tx_power,avg_latency\n")

        if not os.path.exists(self.packet_reception_rate):
            with open(self.packet_reception_rate, "w") as pdr_file:
                pdr_file.write("distance,tx_power,pdr\n")


    def log_latency(self, message_ids, latencies, type: ResultType):
        if type == ResultType.PYTHON:
            result_file = open(self.output_dir + f"/dist_{self.distance}_txPower_{self.tx_power}_latency_python.csv", "w")
            avg_result_file = open(self.average_latency_python, "a")
        elif type == ResultType.LTE_UE_NET_DEVICE:
            result_file = open(self.output_dir + f"/dist_{self.distance}_txPower_{self.tx_power}_latency_lteUeNetDevice.csv", "w")
            avg_result_file = open(self.average_latency_lteUeNetDevice, "a")
        elif type == ResultType.LTE_SPECTRUM_PHY:
            result_file = open(self.output_dir + f"/dist_{self.distance}_txPower_{self.tx_power}_latency_lteSpectrumPhy.csv", "w")
            avg_result_file = open(self.average_latency_lteSpectrumPhy, "a")
        else:
            return

        hot_message_ids = message_ids[self.num_cold_run:]
        hot_latencies = latencies[self.num_cold_run:]
        
        result_file.write("message_id,latency\n")
        for id, latency in zip(hot_message_ids, hot_latencies):
            result_file.write(f"{id},{latency}\n")

        if len(hot_latencies) > 0:
            avg_latency = sum(hot_latencies) / len(hot_latencies)
        else:
            avg_latency = -1
        avg_result_file.write(f"{self.distance},{self.tx_power},{avg_latency}\n")

        result_file.close()
        avg_result_file.close()


    def log_pdr(self, packets_send, packets_received):
        num_packets_sent = len(packets_send[self.num_cold_run:])
        num_packets_received = len(packets_received[self.num_cold_run:])

        if num_packets_sent > 0:
            pdr = num_packets_received / num_packets_sent
        else:
            pdr = -1

        with open(self.packet_reception_rate, "a") as pdr_file:
            pdr_file.write(f"{self.distance},{self.tx_power},{pdr}\n")

    def create_average_graphics(self):
        self._create_graphic_average_latency_python()
        self._create_graphic_average_latency_lteUeNetDevice()
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

    def _create_graphic_average_latency_lteUeNetDevice(self):
        with open(self.average_latency_lteUeNetDevice, "r") as result_file:
            lines = result_file.read().splitlines()
        lines = lines[1:]

        self._plot_average_data(
            lines,
            title="Avg. Packet Transmission Time - LteUeNetDevice",
            label_y="Zeit in ms",
            output_file=self.average_latency_lteUeNetDevice_img
        )

    def _create_graphic_packet_delivery_rate(self):
        with open(self.packet_reception_rate, "r") as result_file:
            lines = result_file.read().splitlines()
        lines = lines[1:]

        self._plot_average_data(
            lines,
            title="PDR",
            label_y="PDR",
            output_file=self.packet_reception_rate_img
        )

    def _plot_average_data(self, lines, title=None, label_x="Distanz in m", label_y=None, unit_legend="dBm", output_file=None):
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

    def create_latency_graphic(self, distance, tx_power, print_to_file=True):
        with open(self.output_dir + f"/dist_{distance}_txPower_{tx_power}_latency_lteUeNetDevice.csv", "r") as result_file:
            lines = result_file.read().splitlines()
        lines = lines[1:]

        data_x_lteUeNetDevice = list(map(lambda l: int(l.split(",")[0]), lines))
        data_y_lteUeNetDevice = list(map(lambda l: float(l.split(",")[1]), lines))

        plt.plot(data_x_lteUeNetDevice, data_y_lteUeNetDevice, label="L_lteUeNetDevice (ns-3_c-v2x)")

        with open(self.output_dir + f"/dist_{distance}_txPower_{tx_power}_latency_python.csv", "r") as result_file:
            lines = result_file.read().splitlines()
        lines = lines[1:]

        data_x_python = list(map(lambda l: int(l.split(",")[0]), lines))
        data_y_python = list(map(lambda l: float(l.split(",")[1]), lines))

        plt.plot(data_x_python, data_y_python, label="L_simKnoten (Python)")

        plt.xlabel("message_id")
        plt.ylabel("Zeit in ms")

        plt.legend()

        if print_to_file:
            plt.savefig(f"{self.output_dir}/dist_{distance}_txPower_{tx_power}_latency.pdf", format="pdf", bbox_inches="tight")

        plt.title("Latenz pro Paket für ns-3_c-v2x (LteUeNetDevice) und Simulationsknoten (Python)")
        plt.show()


        plt.close()

        plt.figure(figsize=(3, 4.8))
        plt.boxplot([data_y_lteUeNetDevice, data_y_python], labels=["L_lteUeNetDevice", "L_simKnoten"], )
        # plt.ylabel("Zeit in ms")
        ax = plt.gca()
        ax.get_yaxis().set_ticklabels("")

        if print_to_file:
            plt.savefig(f"{self.output_dir}/dist_{distance}_txPower_{tx_power}_latency_boxplot.pdf", format="pdf", bbox_inches="tight")

        plt.show()
