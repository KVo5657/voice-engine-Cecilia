from gpiozero import LED
from time import sleep

testPin = 16 #change this number to match the pin

led = LED(testPin) #initialize led object, also works with motors

while True: #the motor/LED should blink on/off once a second
    led.on()
    sleep(1)
    led.off()
    sleep(1)
