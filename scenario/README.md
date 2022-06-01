# V2X Level Crossing

## Important

This test scenario models a level crossing using ITS services and functionality. The following setup is used:

```
   \ street  \        / railway /
    \         \      /         /
     \    \    \    /---------/     Direction train: North-East (NE) to South-West (SW)
      \    \    \  /         /      Direction car: both NW -> SE and SE to NW
       \    \    \/---------/
        \   /    /\        /
         \ /    /  \------/             x Receiver
          \    /    \    /              x MQTT-Server
           \  /      \--/
            \/ level  \/  x Converter
            /\ crossing  x RSU
           /  \      /  \
          /----\    /   /\
         /      \  /   /  \
        /--------\/   /    \
       /         /\    \    \
      /---------/  \    \    \
     /         /    \         \
    /---------/      \    \    \

```

* 1 train sending CAM messages via ITS-G5
* 1 RSU receiving the CAM messages and sending SPATEM messages via ITS-G5 to indicate the state of the level crossing
* 1 converter to send the SPATEM messages to an MQTT server backend
* a variable number of cars driving on the street (the number can be configured). Start/Stop and speed is controlled by the car.
* 1 MQTT server
* 1 receiver which subsribes to the MQTT server and prints the incoming messages.

## How to run

0. Adapt the paths and environment variables in `start-evaluation-simulation.sh`.
1. Execute `start-evaluation-simulation.sh`.

## Troubleshooting

Containers might have problems to access services bound on `docker0` interface. If this is the case, you might want to check your firewall and routing rules. This command might fix the problem: `iptables -A INPUT -i docker0 -j ACCEPT`. Find more information here: [https://stackoverflow.com/questions/31324981/how-to-access-host-port-from-docker-container](https://stackoverflow.com/questions/31324981/how-to-access-host-port-from-docker-container)
