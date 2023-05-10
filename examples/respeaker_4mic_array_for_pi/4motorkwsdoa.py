"""
Search the keyword "snowboy".
After finding the keyword, Direction Of Arrival (DOA) is estimated.

for ReSpeaker 4 Mic Array for Raspberry Pi
"""

import sys
import time
from voice_engine.source import Source
from voice_engine.channel_picker import ChannelPicker
from voice_engine.kws import KWS
from voice_engine.doa_respeaker_4mic_array import DOA

from gpiozero import Buzzer
from time import sleep


#signal output pins

FrontRightPin = 23
FrontLeftPin = 26
BackRightPin = 6
BackLeftPin = 16 

FRmotor = Buzzer(FrontRightPin)
FLmotor = Buzzer(FrontLeftPin)
BRmotor = Buzzer(BackRightPin)
BLmotor = Buzzer(BackLeftPin)

def main():
    src = Source(rate=16000, channels=4)
    ch0 = ChannelPicker(channels=src.channels, pick=0)
    kws = KWS(model='Cecilia.pmdl', sensitivity=0.5, verbose=True)
    doa = DOA(rate=16000)

    src.link(ch0)
    ch0.link(kws)
    src.link(doa)
    

    def on_detected(keyword):
        dir = doa.get_direction()
        print('detected {} at direction {}'.format(keyword, dir))

        if(0 <= dir < 90):
            FRmotor.on()
            print("FrontRight")
        elif(91 <= dir < 180):
            BRmotor.on()
            print("BackRight")
        elif(181 <= dir < 270):
            BLmotor.on()
            print("BackLeft")
        elif(271 <= dir < 360):
            FLmotor.on()
            print("FrontLeft")
        time.sleep(1)
        FRmotor.off()
        FLmotor.off()
        BRmotor.off()
        BLmotor.off()
    kws.set_callback(on_detected)

    src.recursive_start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    src.recursive_stop()

    # wait a second to allow other threads to exit
    time.sleep(1)


if __name__ == '__main__':
    main()
