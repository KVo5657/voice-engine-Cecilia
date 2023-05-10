"""
Search the keyword "Ceclia".
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
S0 = 16
S1 = 24
S2 = 25


bit1 = Buzzer(S0)
bit2 = Buzzer(S1)
bit3 = Buzzer(S2)

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

        if(dir >= 337.5 or dir < 22.5): #12:00 (follows the direction of a clock face, 12:00 is straight forward)
            bit1.off() #binary 0
            bit2.off()
            bit3.off()
            print("12:00 motor\n")
        elif(22.5 <= dir < 67.5): #1:30
            bit1.on() #binary 1
            bit2.off()
            bit3.off()
            print("1:30 motor\n")
        elif(67.5 <= dir < 112.5): #3:00
            bit1.off() #binary 2
            bit2.on()
            bit3.off()
            print("3:00 motor\n") #4:30
        elif(112.5 <= dir < 157.5):
            bit1.on() #binary 3
            bit2.on()
            bit3.off()
            print("4:30 motor\n")
        #elif(157.5 <= dir < 202.5): #6:00 UNUSED
        #    bit1.off() 
        #    bit2.off()
        #    bit3.on()
        #    print("6:00 motor\n")
        elif(202.5 <= dir < 247.5): #7:30
            bit1.off() #binary 4
            bit2.off()
            bit3.on()
            print("7:30 motor\n")
        elif(247.5 <= dir < 292.5): #9:00
            bit1.on() #binary 5
            bit2.off()
            bit3.on()
            print("9:00 motor\n")
        elif(292.5 <= dir < 337.5): #10:30
            bit1.off() #binary 6
            bit2.on()
            bit3.on()
            print("10:30 motor\n")
        else:
            bit1.on() #binary 7, off
            bit2.on()
            bit3.on()
            print("OFF\n")
        time.sleep(1)
        bit1.on() #binary 7, off
        bit2.on()
        bit3.on()
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
