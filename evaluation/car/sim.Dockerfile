# Prepare the Docker container for CAR
# In case the car does not use SDRs use this Dockerfile

FROM ubuntu:20.04

# We need to manually build TShark and not install it via apt, because the version on apt is to old.

RUN apt update \
    && DEBIAN_FRONTEND=noninteractive apt install -y \
    # TShark
    bison cmake wget xz-utils \
    gcc \
    g++ \
    libglib2.0-dev \
    libc-ares-dev \
    libpcap-dev \
    libpcre2-dev \
    flex \
    make \
    python3.8 \
    perl \
    libgcrypt-dev \
    # Application Car
    python3-pip iproute2 iputils-ping \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://1.eu.dl.wireshark.org/src/wireshark-3.6.5.tar.xz \
    && tar -xf wireshark-3.6.5.tar.xz

RUN mkdir wireshark-3.6.5/build \
    && cd /wireshark-3.6.5/build \
    && cmake -DBUILD_wireshark=OFF .. \
    && make -j 4 \
    && make install \
    && rm /wireshark-3.6.5.tar.xz \
    && rm -r /wireshark-3.6.5

RUN pip3 install pyshark

WORKDIR /

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]

COPY car/ /car/
CMD ["python3", "-u", "-m", "car", "-i", "v2x"]
