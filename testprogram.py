from guizero import App, Text, PushButton
from gpiozero import LED
from threading import Thread, Event
import time
import os
import glob
import sys
import board
import adafruit_dht
import RPi.GPIO as GPIO

# ========== GLOBALS ==========
# Variables to hold sensor data
current_temp_dht = None
current_hum_dht = None
current_temp1 = None
current_temp2 = None

stopFlag = Event()

# ========== SETUP HARDWARE ==========

sensor = adafruit_dht.DHT22(board.D18)

relay_ch1 = LED(5)
relay_ch2 = LED(6)
relay_ch3 = LED(13)
relay_ch4 = LED(26)
relay_ch5 = LED(12)
relay_ch6 = LED(16)

# Setup 1-Wire for DS18B20 probes
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

sn1 = '28-0000006a045f'
sn2 = '28-00000085eccb'

base_dir = '/sys/bus/w1/devices/'
device_file1 = glob.glob(base_dir + sn1)[0] + '/w1_slave'
device_file2 = glob.glob(base_dir + sn2)[0] + '/w1_slave'

def read_temp_raw1():
    with open(device_file1, 'r') as f:
        return f.readlines()

def read_temp1():
    lines1 = read_temp_raw1()
    equals_pos = lines1[1].find('t=')
    if equals_pos != -1:
        temp_string1 = lines1[1][equals_pos+2:]
        return round(float(temp_string1) / 1000.0, 1)
    return None

def read_temp_raw2():
    with open(device_file2, 'r') as f:
        return f.readlines()

def read_temp2():
    lines2 = read_temp_raw2()
    equals_pos = lines2[1].find('t=')
    if equals_pos != -1:
        temp_string2 = lines2[1][equals_pos+2:]
        return round(float(temp_string2) / 1000.0, 1)
    return None

# ========== THREADING ==========

def read_sensors_in_thread(stop_event):
    """
    Runs in a background thread. Reads sensor data and stores it in
    global variables, but does NOT update the GUI directly.
    """
    global current_temp_dht, current_hum_dht, current_temp1, current_temp2

    while not stop_event.is_set():
        try:
            # Read from DHT22
            current_temp_dht = sensor.temperature
            current_hum_dht = sensor.humidity

            # Read from DS18B20 probes
            current_temp1 = read_temp1()
            current_temp2 = read_temp2()
        except Exception as e:
            # You might get occasional read errors from the DHT sensor
            print("Sensor read error:", e)

        # Adjust sleep interval as needed
        time.sleep(0.5)


# Close button
def close_gui():
    stopFlag.set()      # Signal the thread to stop
    GPIO.cleanup()      # Clean up GPIO
    sys.exit()          # Exit the entire program

# ========== GUI ==========

app = App(title="Temperature/Humidity test", layout="grid")
app.when_closed = close_gui

# Text labels for input readouts
Text(app, text="Input", width=10, grid=[1,0])
Text(app, text="Output", width=10, grid=[4,0])

# Title labels
Text(app, text="Temperature", width=15, height=3, grid=[0,1])
Text(app, text="Humidity",    width=15, height=3, grid=[0,2])
Text(app, text="Temperature 2", width=15, height=3, grid=[0,3])
Text(app, text="Temperature 3", width=15, height=3, grid=[0,4])

# Dynamic texts that we'll update
text_temp_dht = Text(app, text="", grid=[1,1])
Text(app, text="*C", grid=[2,1])
text_hum_dht = Text(app, text="", grid=[1,2])
Text(app, text="%", grid=[2,2])
text_temp1 = Text(app, text="", grid=[1,3])
Text(app, text="*C", grid=[2,3])
text_temp2 = Text(app, text="", grid=[1,4])
Text(app, text="*C", grid=[2,4])

# Buttons to control relays
PushButton(app, relay_ch1.on, text="Start", width=10, height=2, grid=[4,1])
PushButton(
    app,
    command=lambda: [
        relay_ch1.off(), relay_ch2.off(), relay_ch3.off(),
        relay_ch4.off(), relay_ch5.off(), relay_ch6.off()
    ],
    text="Stop", width=10, height=2, grid=[5,1]
)

PushButton(app, relay_ch2.on,  text="Ch.2 ON",  width=10, height=2, grid=[4,2])
PushButton(app, relay_ch2.off, text="Ch.2 OFF", width=10, height=2, grid=[5,2])
PushButton(app, relay_ch3.on,  text="Ch.3 ON",  width=10, height=2, grid=[4,3])
PushButton(app, relay_ch3.off, text="Ch.3 OFF", width=10, height=2, grid=[5,3])
PushButton(app, relay_ch4.on,  text="Ch.4 ON",  width=10, height=2, grid=[4,4])
PushButton(app, relay_ch4.off, text="Ch.4 OFF", width=10, height=2, grid=[5,4])
PushButton(app, relay_ch5.on,  text="Ch.5 ON",  width=10, height=2, grid=[4,5])
PushButton(app, relay_ch5.off, text="Ch.5 OFF", width=10, height=2, grid=[5,5])
PushButton(app, relay_ch6.on,  text="Ch.6 ON",  width=10, height=2, grid=[4,6])
PushButton(app, relay_ch6.off, text="Ch.6 OFF", width=10, height=2, grid=[5,6])

PushButton(app, close_gui, text="Close", grid=[1,5])

# ========== PERIODIC GUI UPDATE ==========

def update_gui():
    """
    This function runs in the main thread. It reads the global sensor
    variables and updates the GUI labels. It then schedules itself
    to run again after 500ms.
    """
    if current_temp_dht is not None:
        text_temp_dht.value = current_temp_dht
    if current_hum_dht is not None:
        text_hum_dht.value = current_hum_dht
    if current_temp1 is not None:
        text_temp1.value = current_temp1
    if current_temp2 is not None:
        text_temp2.value = current_temp2

    # Schedule the next update in 500ms
    app.after(500, update_gui)

# ========== START BACKGROUND THREAD & GUI LOOP ==========

# Create and start the sensor-reading thread
thread = Thread(target=read_sensors_in_thread, args=(stopFlag,))
thread.start()

# Kick off periodic GUI updates
app.after(500, update_gui)

# Start the GUI event loop (blocks until closed)
app.display()
