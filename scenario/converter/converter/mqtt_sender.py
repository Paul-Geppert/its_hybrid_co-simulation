from .mqtt_client import MQTTClient

class MQTTSender:
    def __init__(self, config):
        self.configured_clients = []

        for client_config in config['servers']:
            client = MQTTClient(client_config, config['mqtt_settings'])
            self.configured_clients.append(client)

    def send_mapem(self, message):
        self._send("mapem", message)

    def send_spatem(self, message):
        self._send("spatem", message)

    def _send(self, topic_key, message):
        for client in self.configured_clients:
            client.publish(topic_key=topic_key, payload=message)
