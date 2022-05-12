#!/bin/sh

until ip a show i_conv_recv > /dev/null 2>&1
do
  echo 'waiting for network connection i_conv_recv ...'
  sleep 1
done

until ip a show i_conv_send > /dev/null 2>&1
do
  echo 'waiting for network connection i_conv_send ...'
  sleep 1
done

exec "$@"
