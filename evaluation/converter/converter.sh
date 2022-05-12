#!/bin/sh

cd /

python3 -m converter -ii i_conv_recv -ic i_conv_send -c /converter/config.json

while true
do
    sleep 1
done
