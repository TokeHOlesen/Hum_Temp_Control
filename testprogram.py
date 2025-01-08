from guizero import App, Text, PushButton
from gpiozero import LED
from threading import Thread, Event
import time
import os
import board
import adafruit_dht
import RPi.GPIO as GPIO

# ========== DATA CONTAINERS ==========

class SensorData:
    """Each property corresponds to data from one sensor."""
    def __init__(self):
        self.current_temp_dht = None
        self.current_hum_dht = None
        self.current_temp_1 = None
        self.current_temp_2 = None


sensor_data_all = SensorData()

stop_flag = Event()

# ========== HARDWARE SETUP ==========

# Initializes the DHT22 sensor
dht22_sensor = adafruit_dht.DHT22(board.D18)

# Instatiates an LED object for each relay, corresponding to the respective GPIO pin.
# Using LED objects allows to quickly set them to high or low voltage.
relay_ch1 = LED(5)
relay_ch2 = LED(6)
relay_ch3 = LED(13)
relay_ch4 = LED(26)
relay_ch5 = LED(12)
relay_ch6 = LED(16)

# Initializes the DS18B20 temperature probes
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
temp_sensor_1_file = base_dir + '28-0000006a045f/w1_slave'
temp_sensor_2_file = base_dir + '28-00000085eccb/w1_slave'


def read_temp(sensor_device_file: str):
    """
    Reads data from the given device file; accepts an argument that is the path to a DS18B20 probe device file.
	Returns a float with 1 decimal place if data is found, else None.
    """
    with open(sensor_device_file, 'r') as file:
        temp_data_lines = file.readlines()
    temp_data_start_pos = temp_data_lines[1].find('t=')
    if temp_data_start_pos != -1:
        temp_string = temp_data_lines[1][temp_data_start_pos + 2:]
        return round(float(temp_string) / 1000.0, 1)
    return None


# ========== THREADING ==========

def read_sensors_in_thread(sensor_data, stop_event):
    """
    Runs in a background thread. Reads sensor data and stores it in
    global variables, but does not update the GUI directly.
    """
    while not stop_event.is_set():
        try:
            # Read from DHT22
            sensor_data.current_temp_dht = dht22_sensor.temperature
            sensor_data.current_hum_dht = dht22_sensor.humidity
            # Read from DS18B20 probes
            sensor_data.current_temp_1 = read_temp(temp_sensor_1_file)
            sensor_data.current_temp_2 = read_temp(temp_sensor_2_file)
        except Exception as e:
            print("Sensor read error:", e)

        # Adjust sleep interval as needed
        time.sleep(0.5)


# Called when the window is closed; cleans up.
def close_gui():
    stop_flag.set()
    thread.join()
    GPIO.cleanup()
    app.destroy()

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
PushButton(app, relay_ch1.on,  text="Ch.1 ON",  width=10, height=2, grid=[4,1])
PushButton(app, relay_ch1.off, text="Ch.1 OFF", width=10, height=2, grid=[5,1])
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

def update_gui(sensor_data):
    """
    This function runs in the main thread. It reads the global sensor
    variables and updates the GUI labels. It then schedules itself
    to run again after 500ms.
    """
    if sensor_data.current_temp_dht is not None:
        text_temp_dht.value = sensor_data.current_temp_dht
    if sensor_data.current_hum_dht is not None:
        text_hum_dht.value = sensor_data.current_hum_dht
    if sensor_data.current_temp_1 is not None:
        text_temp1.value = sensor_data.current_temp_1
    if sensor_data.current_temp_2 is not None:
        text_temp2.value = sensor_data.current_temp_2

    # Schedule the next update in 500ms
    app.after(500, lambda: update_gui(sensor_data))

# ========== START BACKGROUND THREAD & GUI LOOP ==========

# Create and start the sensor-reading thread
thread = Thread(target=read_sensors_in_thread, args=(sensor_data_all, stop_flag,))
thread.start()

# Kick off periodic GUI updates
app.after(500, lambda: update_gui(sensor_data_all))

# Start the GUI event loop (blocks until closed)
app.display()
