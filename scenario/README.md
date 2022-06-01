# V2X Level Crossing (DiAK)

This use case scenario was derived from the DiAK project ([https://reallab-hamburg.de/en/projekte/digital-st-andrews-cross/](https://reallab-hamburg.de/en/projekte/digital-st-andrews-cross/)). More information is provided below.

## Derived use case

This test scenario models a level crossing using ITS services and functionality. The following setup is used:

![alt text](/scenario/images/scenario_overview.png "Title")

* 1 train sending CAM messages via ITS-G5
* 1 RSU receiving the CAM messages and sending SPATEM messages via ITS-G5 to indicate the state of the level crossing
* 1 converter to send the SPATEM messages to an MQTT server backend
* a variable number of cars driving on the street (the number can be configured). Start/Stop and speed is controlled by the car.
* 1 MQTT server
* 1 receiver which subscribes to the MQTT server and prints the incoming messages.
* Optional: The converter and one vehicle are equipped with SDRs to use real/physical C-V2X

## How to run

Variant 1:

0. Adapt the paths and environment variables in `start-evaluation-simulation.sh` (in the project root).
1. Execute `start-evaluation-simulation.sh`.

Variant 2:

0. Adapt the paths and environment variables in `launch.json` to execute from VSCode
1. Run `Scenario` in VSCode.

## Troubleshooting

Containers might have problems to access services bound on `docker0` interface. If this is the case, you might want to check your firewall and routing rules. This command might fix the problem: `iptables -A INPUT -i docker0 -j ACCEPT`. Find more information here: [https://stackoverflow.com/questions/31324981/how-to-access-host-port-from-docker-container](https://stackoverflow.com/questions/31324981/how-to-access-host-port-from-docker-container)
