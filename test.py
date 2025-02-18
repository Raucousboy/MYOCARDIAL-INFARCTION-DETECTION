import serial
import matplotlib.pyplot as plt
import numpy as np

# Set up the serial connection (adjust 'COM3' and baud rate as needed)
ser = serial.Serial('COM5', 9600)
plt.ion()  # Enable interactive mode

# Set up the plot
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'b-')
plt.title('ECG Signal')
plt.xlabel('Time (s)')
plt.ylabel('ECG Value')

# Function to update the plot
def update_plot(xdata, ydata):
    ln.set_data(xdata, ydata)
    ax.relim()
    ax.autoscale_view()
    plt.draw()
    plt.pause(0.01)

# Read data from the serial port and update the plot
try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            try:
                hr, hrv, ecg_value = map(int, line.split(','))
                xdata.append(len(xdata))
                ydata.append(ecg_value)
                update_plot(xdata, ydata)
            except ValueError:
                pass  # Ignore lines that can't be parsed
except KeyboardInterrupt:
    pass  # Stop the loop on Ctrl+C

ser.close()
plt.ioff()
plt.show()
