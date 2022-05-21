FROM ubuntu:20.04

RUN apt update \
    && DEBIAN_FRONTEND=noninteractive apt install -y \
    python3 \
    # Debugging
    tcpdump iproute2 iputils-ping \
    && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]

COPY delay/ /delay/

CMD [ "python3", "-m", "delay" ]
