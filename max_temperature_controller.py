# Function declarations

def record_keystrokes():
    esc_is_pressed = False
    while esc_is_pressed == False:
        if keyboard.is_pressed('+'):
            send_to_arduino('+')
            print('Max temperature increased')
            receive_from_arduino()
            time.sleep(0.5)
        if keyboard.is_pressed('-'):
            send_to_arduino('-')
            print('Max temperature decreased')
            receive_from_arduino()
            time.sleep(0.5)
        if keyboard.is_pressed('esc'):
            esc_is_pressed = True

def send_to_arduino(keystroke):
    ser.write(keystroke)  

def receive_from_arduino():
    global start_marker, end_marker
    message = ""
    x = "z" # any value that is not end_marker
    byteCount = -1

    # read only until star_marker
    while  ord(x) != start_marker: 
        x = ser.read()

    # record message until end_marker
    while ord(x) != end_marker:
        if ord(x) != start_marker:
            message = message + x 
            byteCount += 1
        x = ser.read()

    print(message)
    print('-------------------------')

# Program

import keyboard
import serial
import time

serialPort = "COM3"
baudRate = 9600

start_marker = 60
end_marker = 62

print("--------------------------------------")
print("--- Maximum temperature controller ---")
print("--------------------------------------")
print("Press + to increase value")
print("Press - to decrease value")
print("Press Esc to exit controller")
print("--------------------------------------")

ser = serial.Serial(serialPort, baudRate)
record_keystrokes()