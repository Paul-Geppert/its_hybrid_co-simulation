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

RUN wget https://1.eu.dl.wireshark.org/src/wireshark-3.6.5.tar.xz
RUN tar -xf wireshark-3.6.5.tar.xz

RUN mkdir wireshark-3.6.5/build

WORKDIR /wireshark-3.6.5/build
RUN cmake -DBUILD_wireshark=OFF ..
RUN make -j 4
RUN make install

RUN pip3 install pyshark

WORKDIR /

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]

COPY car/ /car/
CMD ["python3", "-u", "-m", "car", "-i", "v2x"]
