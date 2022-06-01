#!/bin/sh

echo "CAR started"

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

exec "$@"
