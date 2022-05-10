import logging
from socket import gaierror
from time import sleep
import threading
import paho.mqtt.client as mqtt

logger = logging.getLogger("MQTT-Client")

class MQTTClient:
    def __init__(self, client_config, mqtt_config):
        def on_connect_gen(name):
            """
            Return a function to log the connect event, incorperating the client name
            """
            def on_connect(client, userdata, flags, rc):
                if rc == 0:
                    logger.info("%s: %s", name, mqtt.connack_string(rc))
                else:
                    logger.error("%s: %s Will try to reconnect during execution.", name, mqtt.connack_string(rc))

            return on_connect

        self.client_config = client_config
        self.connection_initialized = False

        self.client = mqtt.Client(mqtt_config['client_id'])
        self.client.on_connect = on_connect_gen(client_config['id'])
        self.client.max_queued_messages_set(mqtt_config['max_queue_size'])
        self.client.username_pw_set(client_config['user'], client_config['pw'])

        ca_certs = f"{mqtt_config['auth_path']}/{client_config['auth']['ca_certs']}" if 'ca_certs' in client_config['auth'] else None
        keyfile = f"{mqtt_config['auth_path']}/{client_config['auth']['keyfile']}" if 'keyfile' in client_config['auth'] else None
        certfile = f"{mqtt_config['auth_path']}/{client_config['auth']['certfile']}" if 'certfile' in client_config['auth'] else None

        if any([ca_certs, keyfile, certfile]):
            self.client.tls_set(
                ca_certs=ca_certs,
                keyfile=keyfile,
                certfile=certfile,
            )

        # Start a new thread to handle establishment of connection to not block the execution
        threading.Thread(
            target=self._connect_and_start_loop,
            args=(mqtt_config,),
            daemon=True
        ).start()

    def _connect_and_start_loop(self, mqtt_config):
        logger.info("%s: Connecting", self.client_config['id'])
        self._connect_with_retry(mqtt_config)
        self.connection_initialized = True
        self.client.loop_start()

    def _connect_with_retry(self, mqtt_config):
        """
        Try to connect the client to the given host and port.
        On error: try again after some time. Time doubles with each round, until it reaches configured `reconnect_seconds_max`
        """

        next_reconnect_wait_time = mqtt_config['reconnect_seconds_min']

        reconnect_info_text = lambda t: f"Trying to connect again in {t} seconds."
        successfully_connected = False

        while not successfully_connected:
            try:
                logger.info(f"Connecting on ${self.client_config['host']} port=${self.client_config['port']}")
                self.client.connect(self.client_config['host'], port=self.client_config['port'])
                successfully_connected = True
                return
            except ConnectionRefusedError as e:
                logger.warning("%s: Server rejected connection: %s. %s",
                    self.client_config['id'],
                    e,
                    reconnect_info_text(next_reconnect_wait_time))
            except gaierror as e:
                logger.warning("%s: Not connected. Error in getaddrinfo: %s. %s",
                    self.client_config['id'],
                    e,
                    reconnect_info_text(next_reconnect_wait_time))
            except Exception as e:
                logger.warning("%s: Could not connect to server: %s. %s",
                    self.client_config['id'],
                    e,
                    reconnect_info_text(next_reconnect_wait_time))

            sleep(next_reconnect_wait_time)
            next_reconnect_wait_time = min(2 * next_reconnect_wait_time, mqtt_config['reconnect_seconds_max'])

    def publish(self, topic_key, payload):
        if not self.connection_initialized:
            logger.warning("%s: Message can not be published, client is not yet initialized", self.client_config['id'])
            return None

        logger.info("%s: Publishing message on %s",
                self.client_config['id'],
                self.client_config['topics'][topic_key])
        return self.client.publish(self.client_config['topics'][topic_key], payload=payload)
