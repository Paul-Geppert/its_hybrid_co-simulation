from itertools import product
from multiprocessing import Process

from marvis.channel.cv2x import CV2XChannel
from marvis import ArgumentParser, Network, DockerNode, Scenario

def run_scenario(distance, tx_power):
    conf_file = open("evaluation_delay_ns3_configs.log", "a")

    scenario = Scenario()

    # ns-3 helper for C-V2X block the following IP ranges:
    # 7.0.0.0 / 255.0.0.0
    # 10.0.0.0 / 255.255.255.252
    # 12.0.0.0 / 255.255.255.252
    net = Network("15.0.0.0", "255.255.0.0")

    ns3_delay_sender = DockerNode('ns3_delay_sender', docker_build_dir='./delay', environment_variables={"DELAY_ROLE": "SENDER"})
    ns3_delay_receiver = DockerNode('ns3_delay_receiver', docker_build_dir='./delay', environment_variables={"DELAY_ROLE": "RECEIVER"})

    ns3_delay_sender.set_position(0, 0, 0)
    ns3_delay_receiver.set_position(0, distance, 0)

    cv2x_channel = net.create_channel(channel_type=CV2XChannel, tx_power=tx_power)

    cv2x_channel.connect(ns3_delay_sender, ifname="cv2x")
    cv2x_channel.connect(ns3_delay_receiver, ifname="cv2x")

    scenario.add_network(net)
    
    with scenario as sim:
        print("Log directory is", sim.log_directory)
        conf_file.write(f"{distance},{tx_power},{sim.log_directory}\n")
        sim.simulate(simulation_time=60)

    conf_file.close()

def main():

    with open("evaluation_delay_ns3_configs.log", "w") as conf_file:
        conf_file.write("distance,tx_power,log_directory\n")

    distances = [10, 100, 150, 250, 500, 1000]
    tx_powers = [5, 10, 15, 20, 23]

    # We have to create a new process to run the simulation to cleanup ns-3
    # Otherwise all elements and settings from the previous run would still be present
    for distance, tx_power in product(distances, tx_powers):
        print(f"Now simulating with distance {distance} and tx_power {tx_power}")
        p = Process(target=run_scenario, args=(distance, tx_power,))
        p.start()
        p.join()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.run(main)
