from marvis.channel.wifi import WiFiChannel
from marvis.channel.csma import CSMAChannel
from marvis import ArgumentParser, Network, DockerNode, Scenario

def main():
    scenario = Scenario()

    net = Network("10.0.0.0", "255.255.255.0")
    net_2 = Network("20.0.0.0", "255.255.255.0")

    mqtt_server = DockerNode('mqtt_server', docker_build_dir='./mqtt_server', exposed_ports={1883:1884})

    sender = DockerNode('sender', docker_build_dir='./sender')

    # Will not work
    # converter = DockerNode('converter', docker_build_dir='./converter_old')
    # Will not work
    # converter = DockerNode('converter', docker_build_dir='./converter_medium')
    # Will work
    converter = DockerNode('converter', docker_build_dir='./converter_current')
    
    receiver = DockerNode('receiver', docker_build_dir='./receiver')

    csma_channel = net.create_channel(channel_type=WiFiChannel)
    csma_channel.connect(sender, ifname="i_sender")
    csma_channel.connect(converter, ifname="i_conv_recv")

    wifi_channel = net_2.create_channel(delay='10ms', channel_type=CSMAChannel)
    wifi_channel.connect(converter, ifname="i_conv_send")
    wifi_channel.connect(mqtt_server, ifname="i_mqtt")
    wifi_channel.connect(receiver, ifname="i_receiver")

    scenario.add_network(net)
    scenario.add_network(net_2)

    @scenario.workflow
    def disconnect_mqtt(workflow):
        mqtt_server.go_offline()
        print("MQTT server is offline now")
        workflow.sleep(20)
        print("MQTT server is online now")
        mqtt_server.go_online()
        while (True):
            workflow.sleep(20)
            print("MQTT server going offline now")
            mqtt_server.go_offline()
            workflow.sleep(20)
            print("MQTT server going online now")
            mqtt_server.go_online()
    
    with scenario as sim:
        # To simulate forever, just do not specifiy the simulation_time parameter.
        # sim.simulate(simulation_time=60)
        sim.simulate()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.run(main)
