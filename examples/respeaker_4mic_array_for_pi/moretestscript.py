from gpiozero import LED
from gpiozero import Buzzer
from time import sleep
"""
buzzer1 = LED(17)
buzzer2 = LED(27)
buzzer3 = LED(22)
buzzer4 = LED(23)
"""

buzzer1 = Buzzer(17)
buzzer2 = Buzzer(26)
buzzer3 = Buzzer(24)
buzzer4 = Buzzer(1)

while True:
	buzzer1.on()
	buzzer2.on()
	buzzer3.on()
	buzzer4.on()
	sleep(0.5)
	buzzer1.off()
	buzzer2.off()
	buzzer3.off()
	buzzer4.off()
	sleep(1)
