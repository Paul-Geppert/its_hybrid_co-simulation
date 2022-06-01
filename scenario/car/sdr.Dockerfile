# Prepare the Docker container for CAR
# In case the car does use SDRs use this Dockerfile


# Adapted from https://github.com/EttusResearch/ettus-docker/blob/master/ubuntu-uhd/Dockerfile
# Provides a base Ubuntu (20.04) image with latest UHD installed

FROM        ubuntu:20.04

# This will make apt-get install without question
ARG         DEBIAN_FRONTEND=noninteractive
ARG         MAKEWIDTH=6

# Add software-properties-common for add-apt-repository
RUN         apt-get update && \
            apt-get -y install -q software-properties-common

# Install security updates and required packages
RUN         add-apt-repository ppa:ettusresearch/uhd && \
            apt-get update && \
            apt-get -y install -q \
                build-essential \
                ccache \
                git \
                python3-dev \
                python3-pip \
                curl \
# Install UHD
                libuhd-dev \
                libuhd4.2.0 \
                uhd-host \
# Sidelink dependencies
                cmake \
                libfftw3-dev \
                libmbedtls-dev \
                libboost-program-options-dev \
                libconfig++-dev \
                libsctp-dev \
                libboost-all-dev \
                libusb-1.0-0-dev \
                libudev-dev \
                libulfius-dev \
                libjansson-dev \
                libmicrohttpd-dev \
                cpufrequtils \
# Waiting for network
                iproute2 \
# Tshark
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
                python3-pip iputils-ping \
            && rm -rf /var/lib/apt/lists/*

# Prepare Sidelink for SDRs

RUN         uhd_images_downloader
ENV         UHD_IMAGES_DIR=/usr/share/uhd/images
WORKDIR     /

COPY        ./sdr/sidelink /sidelink

RUN         cd /sidelink/ && \
            mkdir -p build && \
            cd build && \
            cmake .. && \
            make -j $MAKEWIDTH

# Add SDR scripts

COPY sdr/sdrHandling/start_master.sh /sidelink
COPY sdr/sdrHandling/start_client.sh /sidelink

# We need to manually build TShark and not install it via apt, because the version on apt is to old.

RUN wget https://1.eu.dl.wireshark.org/src/wireshark-3.6.5.tar.xz \
    && tar -xf wireshark-3.6.5.tar.xz

RUN mkdir wireshark-3.6.5/build \
    && cd /wireshark-3.6.5/build \
    && cmake -DBUILD_wireshark=OFF .. \
    && make -j $MAKEWIDTH \
    && make install \
    && rm /wireshark-3.6.5.tar.xz \
    && rm -r /wireshark-3.6.5

RUN pip3 install pyshark

WORKDIR /

COPY ./sdr/entrypoint.sh /
ENTRYPOINT [ "/entrypoint.sh" ]

COPY car/ /car/
CMD ["python3", "-u", "-m", "car", "-i", "tun_srssl_c"]
