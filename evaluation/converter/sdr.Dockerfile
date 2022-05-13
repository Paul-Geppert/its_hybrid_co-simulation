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
# Converter APP
                tshark \
                python3.8 \
                python3-pip \
                iputils-ping \
            && rm -rf /var/lib/apt/lists/*

RUN pip3 install pyshark paho-mqtt

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

# Add Application

COPY ./converter/__main__.py /converter/
COPY ./converter/config.json /converter/
COPY ./converter/converter.py /converter/
COPY ./converter/cv2x_helper.py /converter/
COPY ./converter/mqtt_client.py /converter/
COPY ./converter/mqtt_sender.py /converter/
COPY ./converter-so/converter /converter-so/

ENV USING_SDR="TRUE"

COPY ./sdr/entrypoint.sh /
ENTRYPOINT [ "/entrypoint.sh" ]

COPY ./converter.sh /converter.sh
CMD [ "/converter.sh" ]
