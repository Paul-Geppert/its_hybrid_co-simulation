#!/bin/sh

until ip a show cv2x > /dev/null 2>&1
do
  echo 'waiting for network connection ...'
  sleep 1
done

exec "$@"
