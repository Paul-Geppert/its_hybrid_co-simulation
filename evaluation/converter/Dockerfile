FROM ubuntu:20.04

RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install --no-install-recommends -y tshark && \
    apt install --no-install-recommends -y \
    python3.8 python3-pip iproute2 iputils-ping

RUN pip3 install pyshark paho-mqtt

COPY ./converter/__main__.py /converter/
COPY ./converter/config.json /converter/
COPY ./converter/converter.py /converter/
COPY ./converter/cv2x_helper.py /converter/
COPY ./converter/mqtt_client.py /converter/
COPY ./converter/mqtt_sender.py /converter/
COPY ./converter-so/converter /converter-so/

COPY ./entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]

COPY ./converter.sh /converter.sh
CMD [ "/converter.sh" ]
