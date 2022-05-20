import argparse
import logging
import os

from multiprocessing import Process
from multiprocessing.sharedctypes import Value

from .driving import enterDrivingLoop, LevelCrossingState

import pyshark
from pyshark.packet.packet import Packet

MovementPhaseState_permissive_Movement_Allowed = 5
MovementPhaseState_caution_Conflicting_Traffic = 9

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--interface', '-i',
            default='v2x',
            help='the interface to read messages from. Default: v2x')
    parser.add_argument('--cv2x-udp-port', '-p',
            default=20001,
            help='the UDP port C-V2X messages will be sent to. Default: 20001 ')
    parser.add_argument('--log-file', '-l',
            default='',
            help='the location of the log file. If not specified, stderr is used. Default: stderr is used')

    return parser.parse_args()

def main():
    def handleV2XMessage(packet):
        spatem_type_id = 4

        packet: Packet = packet

        # Filter for SPATEM

        if packet.highest_layer != 'ITS':
            # logger.info(f"This message is not a ITS message: {packet.highest_layer}")
            return

        message_type_id = packet.its.messageid.main_field.int_value
        if message_type_id != spatem_type_id:
            # logger.info(f"This message is not of type SPATEM (but type id {message_type_id})")
            return

        # Update LCState

        sharedLCState.eventState = int(packet.its.dsrc_eventstate)
        
        sharedLCState.minEndTime = int(packet.its.dsrc_minendtime) if 'dsrc_minendtime' in packet.its.field_names else -1
        sharedLCState.maxEndTime = int(packet.its.dsrc_maxendtime) if 'dsrc_maxendtime' in packet.its.field_names else -1

        # logger.info(f"New sharedLCState: {sharedLCState.eventState} {sharedLCState.minEndTime} {sharedLCState.maxEndTime}")

    logger = logging.getLogger("CAR")
    args = parseArgs()

    if len(args.log_file) > 0:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%y-%m-%d %H:%M:%S',
                            filename=args.log_file,
                            filemode='w')
    else:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%y-%m-%d %H:%M:%S')

    if "MOBILITY_ID" not in os.environ:
        logger.error("Could not find MOBILITY_ID in environment variables.")
        exit(1)

    mobility_id = os.environ["MOBILITY_ID"]
    
    sharedLCState = Value(LevelCrossingState,
        -1, # eventState
        -1, # minEndTime
        -1, # maxEndTime
        lock=False
    )

    p = Process(target=enterDrivingLoop, args=(mobility_id, sharedLCState))
    p.start()

    using_cv2x = os.environ["USING_CV2X"] == "True"

    if using_cv2x:
        logger.info("Vehicle uses CV2X")
        capture = pyshark.LiveCapture(interface=args.interface, decode_as={f'udp.port=={args.cv2x_udp_port}':'its'})
    else:
        logger.info("Vehicle uses ITS-G5")
        capture = pyshark.LiveCapture(interface=args.interface)
    
    capture.apply_on_packets(handleV2XMessage)
