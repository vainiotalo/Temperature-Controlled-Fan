# Function declarations

def record_keystrokes():
    global esc_is_pressed, temp_max
    if keyboard.is_pressed('+'):
        send_to_arduino('+')
        print('Max temperature increased')
        temp_max = receive_from_arduino()
        print('Current value: ' + temp_max + ' C')
        print('-------------------------')
        time.sleep(0.5)
    if keyboard.is_pressed('-'):
        send_to_arduino('-')
        print('Max temperature decreased')
        temp_max = receive_from_arduino()
        print('Current value: ' + temp_max + ' C')
        print('-------------------------')
        time.sleep(0.5)
    if keyboard.is_pressed('esc'):
        esc_is_pressed = True

def send_to_arduino(keystroke):
    ser.write(keystroke)  

def receive_from_arduino():
    global start_marker, end_marker
    temp = ""
    x = "z" # any value that is not end_marker
    byteCount = -1

    # read only until start_marker
    while  ord(x) != start_marker: 
        x = ser.read()

    # record until end_marker
    while ord(x) != end_marker:
        if ord(x) != start_marker:
            temp = temp + x
            byteCount += 1
        x = ser.read()

    return temp

def read_temperature():
    global temp_start, temp_end
    temp = ""
    x = "y" # any value that is not temp_end
    byteCount = -1

    # read only until temp_start
    while  ord(x) != temp_start: 
        x = ser.read()

    # record message until temp_end
    while ord(x) != temp_end:
        if ord(x) != temp_start:
            temp = temp + x 
            byteCount += 1
        x = ser.read()

    return temp

def animate(i, xs, ys, x2, y2):
    global temp_max

    # Read temperature in celsius
    temp = float(read_temperature())

    # Max allowed temperature in celsius
    temp_max = float(temp_max)

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(temp)
    x2.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    y2.append(temp_max)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]
    x2 = x2[-20:]
    y2 = y2[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys, label = "temp")
    ax.plot(x2, y2, label = "max temp")
    ax.legend()

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('DS18B20 temperature and fan switch-on point')
    plt.ylabel('Temperature in C')

# Program

import keyboard
import serial
import time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

print("\nEnter your serial port name \nExample: COM3")
serialPort = raw_input() # Entering an invalid port will cause a crash
baudRate = 9600

start_marker = 60
end_marker = 62
temp_start = 96
temp_end = 39
esc_is_pressed = False

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []
x2 = []
y2 = []

print("\n--------------------------------------")
print("--- Maximum temperature controller ---")
print("--------------------------------------")
print("Press + to increase value")
print("Press - to decrease value")
print("Press Esc to exit controller")
print("--------------------------------------")

ser = serial.Serial(serialPort, baudRate)
temp_max = receive_from_arduino()
print('Current value: ' + temp_max + ' C')
print('Current temperature: ' + read_temperature() + ' C')
print('-------------------------')

ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, x2, y2), interval=2000) 
while esc_is_pressed == False:
    plt.ion()
    plt.show()
    record_keystrokes()
    plt.pause(0.001)