#!/usr/bin/env python
import RPi.GPIO as GPIO
from time import sleep

# Pin configuration
SIA = 40
SIB = 38
SW = 36 

# GPIO setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(SIA, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(SIB, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(SW, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def button_callback(channel):
    print("Button pressed!")

GPIO.add_event_detect(SW, GPIO.FALLING, callback=button_callback, bouncetime=200)

# Track the last state of both pins
last_state = (GPIO.input(SIA), GPIO.input(SIB))
counter = 0

try:
    while True:
        current_state = (GPIO.input(SIA), GPIO.input(SIB))

        if current_state != last_state:  # Detect state change
            if last_state == (0, 0) and current_state == (0, 1):
                # Clockwise step detected
                counter += 1
                print(f"Clockwise rotation, Counter: {counter}")
            elif last_state == (0, 0) and current_state == (1, 0):
                # Anti-clockwise step detected
                counter -= 1
                print(f"Anti-clockwise rotation, Counter: {counter}")
        
        # Update the last state
        last_state = current_state
        sleep(0.001)  # Debounce delay
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
