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


#signal input pins
S0 = 17
S1 = 24
S2 = 25

#common input pin
Z = 1

bit1 = Buzzer(S0)
bit2 = Buzzer(S1)
bit3 = Buzzer(S2)
sig = Buzzer(Z)

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
        sig.on()
        if(338 <= dir < 23):
            choose0.off() #binary 0
            choose1.off()
            choose2.off()
        elif(23 <= dir < 68):
            choose0.on() #binary 1
            choose1.off()
            choose2.off()
        elif(68 <= dir < 113):
            choose0.off() #binary 2
            choose1.on()
            choose2.off()
        elif(113 <= dir < 158):
            choose0.on() #binary 3
            choose1.on()
            choose2.off()
        elif(158 <= dir < 203):
            choose0.off() #binary 4
            choose1.off()
            choose2.on()
        elif(203 <= dir < 248):
            choose0.on() #binary 5
            choose1.off()
            choose2.on()
        elif(248 <= dir < 293):
            choose0.off() #binary 6
            choose1.on()
            choose2.on()
        elif(293 <= dir < 338):
            choose0.on() #binary 7
            choose1.on()
            choose2.on()
        time.sleep(1)
        sig.off
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
