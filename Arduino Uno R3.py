from pyfirmata2 import Arduino, util
import time

# Establish a connection to the Arduino
board = Arduino('COM4')  # replace 'COM3' with the port where your Arduino is connected

# Define the pin where the LED is connected
led_pin = board.get_pin('d:13:o')

while True:
    led_pin.write(1)  # turn the LED on
    time.sleep(1)  # wait for 1 second
    led_pin.write(0)  # turn the LED off
    time.sleep(1)  # wait for 1 second
