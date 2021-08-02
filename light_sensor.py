#!/usr/local/bin/python

import RPi.GPIO as GPIO
import time

__author__ = 'Gus (Adapted from Adafruit)'
__license__ = "GPL"
__maintainer__ = "pimylifeup.com"



#define the pin that goes to the circuit


def rc_time (pin_to_circuit):
    count = 0
  
    #Output on the pin for 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1

    return count

#Catch when script is interupted, cleanup correctly
def Openornot():
    try:
        pin_to_circuit = 7
        GPIO.setmode(GPIO.BOARD)
        tmp=rc_time(pin_to_circuit)
        if tmp>100000: #closed
            return 0
        else:
            return 1
    except:
        pass
    finally:
        GPIO.cleanup()
