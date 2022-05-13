#!/bin/sh

# Start the SDR
if [ "$SDR_MASTER" = "True" ]; then
  echo "I am SDR master"
  /sidelink/start_master.sh &
  IFNAME="tun_srssl_m"
else
  echo "I am SDR client"
  /sidelink/start_client.sh &
  IFNAME="tun_srssl_c"
fi

# Wait for the SDR interface to be available
until ip a show $IFNAME > /dev/null 2>&1
do
  echo "waiting for network connection $IFNAME ..."
  sleep 1
done

# Wait for the ITS-G5 interface to be available
until ip a show i_conv_recv > /dev/null 2>&1
do
  echo 'waiting for network connection i_conv_recv ...'
  sleep 1
done

# Wait for the ETH interface to be available
until ip a show i_conv_eth > /dev/null 2>&1
do
  echo 'waiting for network connection i_conv_eth ...'
  sleep 1
done

exec "$@"
