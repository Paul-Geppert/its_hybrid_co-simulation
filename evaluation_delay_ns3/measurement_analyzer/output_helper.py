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

        self.average_delay_python = output_dir + "/average_delay_python.csv"
        self.average_delay_lteUeNetDevice = output_dir + "/average_delay_lteUeNetDevice.csv"
        self.average_delay_lteSpectrumPhy = output_dir + "/average_delay_lteSpectrumPhy.csv"

        self.packet_reception_rate = output_dir + "/prr.csv"
        
        self.distance = 0
        self.tx_power = 0

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if not os.path.exists(self.average_delay_python):
            with open(self.average_delay_python, "w") as result_file:
                result_file.write("distance,tx_power,avg_delay\n")
        if not os.path.exists(self.average_delay_lteUeNetDevice):
            with open(self.average_delay_lteUeNetDevice, "w") as result_file:
                result_file.write("distance,tx_power,avg_delay\n")
        if not os.path.exists(self.average_delay_lteSpectrumPhy):
            with open(self.average_delay_lteSpectrumPhy, "w") as result_file:
                result_file.write("distance,tx_power,avg_delay\n")

        if not os.path.exists(self.packet_reception_rate):
            with open(self.packet_reception_rate, "w") as prr_file:
                prr_file.write("distance,tx_power,prr\n")


    def log_delay(self, message_ids, delays, type: ResultType):
        if type == ResultType.PYTHON:
            result_file = open(self.output_dir + f"/dist_{self.distance}_txPower_{self.tx_power}_delay_python.csv", "w")
            avg_result_file = open(self.average_delay_python, "a")
        elif type == ResultType.LTE_UE_NET_DEVICE:
            result_file = open(self.output_dir + f"/dist_{self.distance}_txPower_{self.tx_power}_delay_lteUeNetDevice.csv", "w")
            avg_result_file = open(self.average_delay_lteUeNetDevice, "a")
        elif type == ResultType.LTE_SPECTRUM_PHY:
            result_file = open(self.output_dir + f"/dist_{self.distance}_txPower_{self.tx_power}_delay_lteSpectrumPhy.csv", "w")
            avg_result_file = open(self.average_delay_lteSpectrumPhy, "a")
        else:
            return

        hot_message_ids = message_ids[self.num_cold_run:]
        hot_delays = delays[self.num_cold_run:]
        
        result_file.write("message_id,delay\n")
        for id, delay in zip(hot_message_ids, hot_delays):
            result_file.write(f"{id},{delay}\n")

        if len(hot_delays) > 0:
            avg_delay = sum(hot_delays) / len(hot_delays)
        else:
            avg_delay = -1
        avg_result_file.write(f"{self.distance},{self.tx_power},{avg_delay}\n")

        result_file.close()
        avg_result_file.close()


    def log_prr(self, packets_send, packets_received):
        num_packets_sent = len(packets_send[self.num_cold_run:])
        num_packets_received = len(packets_received[self.num_cold_run:])

        if num_packets_sent > 0:
            prr = num_packets_received / num_packets_sent
        else:
            prr = -1

        with open(self.packet_reception_rate, "a") as prr_file:
            prr_file.write(f"{self.distance},{self.tx_power},{prr}\n")

    def create_average_graphics(self):
        self._create_graphic_average_delay_python()
        self._create_graphic_average_delay_lteUeNetDevice()
        self._create_graphic_packet_reception_rate()

    def _create_graphic_average_delay_python(self):
        with open(self.average_delay_python, "r") as result_file:
            lines = result_file.read().splitlines()
        lines = lines[1:]

        self._plot_average_data(lines)

    def _create_graphic_average_delay_lteUeNetDevice(self):
        with open(self.average_delay_lteUeNetDevice, "r") as result_file:
            lines = result_file.read().splitlines()
        lines = lines[1:]

        self._plot_average_data(lines)

    def _create_graphic_packet_reception_rate(self):
        with open(self.packet_reception_rate, "r") as result_file:
            lines = result_file.read().splitlines()
        lines = lines[1:]

        self._plot_average_data(lines)

    def _plot_average_data(self, lines):
        distinct_tx_powers = set(list(map(lambda l: l.split(",")[1], lines)))

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
            labels.append(int(tx_power))
        
        for idx, data_series in enumerate(all_data_series):
            data_x = list(map(lambda d: d[0], data_series))
            data_y = list(map(lambda d: d[1], data_series))

            plt.plot(data_x, data_y, label=labels[idx])
        
        plt.legend()
        plt.show()
        # plt.savefig("myImagePDF.pdf", format="pdf", bbox_inches="tight")

    def create_delay_graphic(self, distance, tx_power):
        with open(self.output_dir + f"/dist_{distance}_txPower_{tx_power}_delay_python.csv", "r") as result_file:
            lines = result_file.read().splitlines()
        lines = lines[1:]

        data_x = list(map(lambda l: int(l.split(",")[0]), lines))
        data_y = list(map(lambda l: float(l.split(",")[1]), lines))

        plt.plot(data_x, data_y, label="e2e Python")

        with open(self.output_dir + f"/dist_{distance}_txPower_{tx_power}_delay_lteUeNetDevice.csv", "r") as result_file:
            lines = result_file.read().splitlines()
        lines = lines[1:]

        data_x = list(map(lambda l: int(l.split(",")[0]), lines))
        data_y = list(map(lambda l: float(l.split(",")[1]), lines))

        plt.plot(data_x, data_y, label="e2e LteUeNetDevice")
        
        plt.legend()
        plt.show()
        # plt.savefig("myImagePDF.pdf", format="pdf", bbox_inches="tight")
