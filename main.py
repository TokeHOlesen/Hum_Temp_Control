import tkinter as tk
from datetime import date, datetime
from gpiozero import LED
from threading import Thread, Event
import csv
import time
import os
import board
import adafruit_dht
import RPi.GPIO as GPIO

import constants
from user_input_class import UserInput
from time_controller_class import TimeController


# ========== DATA CONTAINERS ==========

class SensorData:
    """Each property corresponds to data from one sensor."""
    def __init__(self):
        self.current_temp_dht = None
        self.current_hum_dht = None
        self.current_temp_1 = None
        self.current_temp_2 = None


sensor_data_all = SensorData()
entered_user_input = UserInput()
time_controller_all = TimeController(entered_user_input)


# Sensor readings will continue being taken for as long as this flag is not set
stop_flag = Event()


# ========== HARDWARE SETUP ==========

# Initializes the DHT22 sensor
dht22_sensor = adafruit_dht.DHT22(board.D18)

# Instatiates an LED object for each relay, corresponding to the respective GPIO pin.
# Using LED objects allows to quickly set them to high or low voltage.
ventilator_ch1 = LED(5)
varmer_ch2 = LED(6)
affugter_ch3 = LED(13)
damp_ch4 = LED(26)
running_ch5 = LED(12)
error_ch6 = LED(16)

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


def reset_all_channels() -> None:
    ventilator_ch1.off()
    varmer_ch2.off()
    affugter_ch3.off()
    damp_ch4.off()
    running_ch5.off()
    error_ch6.off()


# ========== CONTINUOUS SENSOR READING ==========

def read_sensors_in_thread(sensor_data, stop_event) -> None:
    """
    Runs in a background thread. Reads sensor data and stores it in the sensor_data object.
    Runs until stop_event is set.
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

        # Time between each reading (in seconds)
        time.sleep(constants.SENSOR_PROBING_INTERVAL)


# Called when the window is closed; cleans up.
def close_gui() -> None:
    stop_flag.set()
    thread.join()
    GPIO.cleanup()
    window.destroy()


# ========== CLEARING USER INPUT DATA ==========

def clear_text_entry_fields():
    target_temperature_textentry.delete(0, tk.END)
    target_humidity_textentry.delete(0, tk.END)
    running_time_textentry.delete(0, tk.END)


# ========== SETTING RELAY CHANNELS ==========

def update_relay_channels(sensor_data, user_input):
    global ventilator_ch1, varmer_ch2, affugter_ch3, damp_ch4, running_ch5, error_ch6

    if running_ch5.is_lit:
        ventilator_ch1.on()
        
        if ventilator_ch1.is_lit:
            # Only turns the heater on if the temperature is lower than target, minus acceptable tolerance
            if sensor_data.current_temp_dht <= user_input.target_temp - constants.TEMPERATURE_TOLERANCE:
                varmer_ch2.on()
            else:
                varmer_ch2.off()
            
            # Checks if the current temperature is within a set range of temperatures from target
            # Humidifier and dehumidifier won't be turned on otherwise
            if abs(sensor_data.current_temp_dht - user_input.target_temp) <= constants.HUMIDITY_CONTROL_THRESHOLD:
                if sensor_data.current_hum_dht < user_input.target_humidity - constants.HUMIDITY_TOLERANCE:
                    affugter_ch3.off()
                    damp_ch4.on()
                elif sensor_data.current_hum_dht > user_input.target_humidity + constants.HUMIDITY_TOLERANCE:
                    affugter_ch3.on()
                    damp_ch4.off()
            else:
                affugter_ch3.off()
                damp_ch4.off()
        else:
            varmer_ch2.off()
            affugter_ch3.off()
            damp_ch4.off()
            running_ch5.off()
            

# ========== DATA LOGGING ==========
        
def log_data(target_temp,
            current_temp,
            target_humidity,
            current_humidity,
            ventilator,
            varmer,
            affugter,
            dampgenerator,
            fejl):
    
    field_names = [
        "tidspunkt",
        "ønsket temperatur",
        "faktisk temperatur",
        "ønsket fugtighed",
        "faktisk fughtighed",
        "ventilator",
        "varmer",
        "affugter",
        "dampgenerator",
        "fejl"
    ]
    
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    
    current_date = date.today()
    filename = f"./Logfiler/{current_date}"
    day_log_exists = os.path.exists(filename)
    
    with open(filename, mode='a' if day_log_exists else 'w', newline='') as log_file:
        writer = csv.DictWriter(log_file, fieldnames=field_names, delimiter=";")
    
        if not day_log_exists:
            writer.writeheader()
        
        writer.writerow({
            "tidspunkt": timestamp,
            "ønsket temperatur": target_temp,
            "faktisk temperatur": current_temp,
            "ønsket fugtighed": target_humidity,
            "faktisk fughtighed": current_humidity,
            "ventilator": ventilator,
            "varmer": varmer,
            "affugter": affugter,
            "dampgenerator": dampgenerator,
            "fejl": fejl
        })
            

# ========== GUI ==========

def on_start_button_press():
    entered_user_input.read(target_temperature_textentry.get(),
                            target_humidity_textentry.get(),
                            running_time_textentry.get())
    if entered_user_input.is_correct:
        running_ch5.on()
        time_controller_all.start_timer()
        clear_text_entry_fields()
        target_temperature_label.config(text=str(entered_user_input.target_temp) + "°C")
        target_humidity_label.config(text=str(entered_user_input.target_humidity) + "%")
        target_temperature_textentry.focus_set()
    

def on_cancel_button_press():
    reset_all_channels()
    time_controller_all.reset()
    entered_user_input.reset()
    target_temperature_label.config(text="N/A")
    target_humidity_label.config(text="N/A")
    elapsed_time_label.config(text="N/A")
    remaining_time_label.config(text="N/A")
    target_temperature_textentry.focus_set()


window = tk.Tk()
window.title("Temperatur- og luftfugtighedsstyring")
window.geometry("428x380")

# Data entry frame

target_entry_frame = tk.Frame(window)
target_entry_frame.grid(row=0, column=0, padx=90, pady=10, sticky="nw")

# Target temperature entry
tk.Label(target_entry_frame, text="Ønsket temperatur:").grid(row=0, column=0, sticky="w")
target_temperature_textentry = tk.Entry(target_entry_frame, width=7)
target_temperature_textentry.grid(row=0, column=1, padx=(12, 0))
tk.Label(target_entry_frame, text="°C").grid(row=0, column=2, sticky="w", padx=(5, 0))

# Target humidity entry
tk.Label(target_entry_frame, text="Ønsket luftfugtighed:").grid(row=1, column=0, sticky="w")
target_humidity_textentry = tk.Entry(target_entry_frame, width=7)
target_humidity_textentry.grid(row=1, column=1, padx=(12, 0))
tk.Label(target_entry_frame, text="%").grid(row=1, column=2, sticky="w", padx=(5, 0))

# Running time entry
tk.Label(target_entry_frame, text="Behandlingstid:").grid(row=2, column=0, sticky="w")
running_time_textentry = tk.Entry(target_entry_frame, width=7)
running_time_textentry.grid(row=2, column=1, padx=(12, 0))
tk.Label(target_entry_frame, text="min.").grid(row=2, column=2, sticky="w", padx=(5, 0))


# Data display frame

data_display_frame = tk.Frame(window, borderwidth=1, relief="sunken")
data_display_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

# Temperature
tk.Label(data_display_frame, text="Ønsket temperatur:").grid(row=0, column=0, sticky="w", padx=(5, 0), pady=(5, 0))
target_temperature_label = tk.Label(data_display_frame, text="N/A", width=5)
target_temperature_label.grid(row=0, column=1, sticky="w", padx=(0, 20), pady=(5, 0))

tk.Label(data_display_frame, text="Faktisk temperatur:").grid(row=0, column=2, sticky="w", pady=(5, 0))
actual_temperature_label = tk.Label(data_display_frame, text="N/A", width=5)
actual_temperature_label.grid(row=0, column=3, sticky="w", padx=(0, 5),  pady=(5, 0))

# Humidity
tk.Label(data_display_frame, text="Ønsket luftfugtighed:").grid(row=1, column=0, sticky="w", padx=(5, 0))
target_humidity_label = tk.Label(data_display_frame, text="N/A", width=5)
target_humidity_label.grid(row=1, column=1, sticky="w", padx=(0, 20))

tk.Label(data_display_frame, text="Faktisk luftfugtighed:").grid(row=1, column=2, sticky="w")
actual_humidity_label = tk.Label(data_display_frame, text="N/A", width=5)
actual_humidity_label.grid(row=1, column=3, sticky="w", padx=(0, 5))

# Fan and heater
tk.Label(data_display_frame, text="Ventilator:").grid(row=2, column=0, sticky="w", padx=(5, 0), pady=(10, 0))
ventilator_label = tk.Label(data_display_frame, text="N/A", width=5)
ventilator_label.grid(row=2, column=1, sticky="w", padx=(0, 20), pady=(10, 0))

tk.Label(data_display_frame, text="Varmer:").grid(row=2, column=2, sticky="w", pady=(10, 0))
varmer_label = tk.Label(data_display_frame, text="N/A", width=5)
varmer_label.grid(row=2, column=3, sticky="w", padx=(0, 5), pady=(10, 0))

# Dehumidifier and steam generator
tk.Label(data_display_frame, text="Affugter:").grid(row=3, column=0, sticky="w", padx=(5, 0))
affugter_label = tk.Label(data_display_frame, text="N/A", width=5)
affugter_label.grid(row=3, column=1, sticky="w", padx=(0, 20))

tk.Label(data_display_frame, text="Damp Generator:").grid(row=3, column=2, sticky="w")
damp_label = tk.Label(data_display_frame, text="N/A", width=5)
damp_label.grid(row=3, column=3, sticky="w", padx=(0, 5))

# Time elapsed and remaining
tk.Label(data_display_frame, text="Tid gået:").grid(row=4, column=0, sticky="w", padx=(5, 0), pady=(10, 5))
elapsed_time_label = tk.Label(data_display_frame, text="N/A", width=5)
elapsed_time_label.grid(row=4, column=1, sticky="w", pady=(10, 5))

tk.Label(data_display_frame, text="Tid tilbage:").grid(row=4, column=2, sticky="w", pady=(10, 5))
remaining_time_label = tk.Label(data_display_frame, text="N/A", width=5)
remaining_time_label.grid(row=4, column=3, sticky="w", pady=(10, 5))


# Button frame

button_frame = tk.Frame(window)
button_frame.grid(row=2, column=0, padx=90, pady=10, sticky="nw")

# Left spacer
tk.Label(button_frame, text="").grid(row=0, column=0)

# Start button
start_button = tk.Button(button_frame, text="Start", width=8, command=on_start_button_press)
start_button.grid(row=0, column=1)

# Middle spacer
tk.Label(button_frame, text="").grid(row=0, column=2, padx=20)

# Cancel button
cancel_button = tk.Button(button_frame, text="Afbryd", width=8, command=on_cancel_button_press)
cancel_button.grid(row=0, column=3)

# Right spacer
tk.Label(button_frame, text="").grid(row=0, column=4)


# Status frame

status_frame = tk.Frame(window)
status_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nw")
status_frame.grid_columnconfigure(0, weight=0)
status_frame.grid_columnconfigure(1, weight=1)

# Current operating status
tk.Label(status_frame, text="Status:").grid(row=0, column=0, sticky="w")
status_label = tk.Label(status_frame, text="Stoppet")
status_label.grid(row=0, column=1, sticky="w")

# Error message, if any
error_label = tk.Label(status_frame, fg="red", text="This is a sample error message")
error_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=(0, 20), pady=(10, 0))


# ========== PERIODIC GUI AND RELAY UPDATE ==========

def update_gui_and_relays(sensor_data, time_controller):
    """Updates the state of the relays and the GUI labels."""
    if sensor_data.current_temp_dht is not None:
        actual_temperature_label.config(text=str(sensor_data.current_temp_dht) + "°C")
    if sensor_data.current_hum_dht is not None:
        actual_humidity_label.config(text=str(sensor_data.current_hum_dht) + "%")
        
    update_relay_channels(sensor_data_all, entered_user_input)
    
    ventilator_label.config(text="ON", fg="Green") if ventilator_ch1.is_lit else ventilator_label.config(text="OFF", fg="Red")
    varmer_label.config(text="ON", fg="Green") if varmer_ch2.is_lit else varmer_label.config(text="OFF", fg="Red")
    affugter_label.config(text="ON", fg="Green") if affugter_ch3.is_lit else affugter_label.config(text="OFF", fg="Red")
    damp_label.config(text="ON", fg="Green") if damp_ch4.is_lit else damp_label.config(text="OFF", fg="Red")
    status_label.config(text="Kører.") if running_ch5.is_lit else status_label.config(text="Stoppet.")
    error_label.config(text="Fejl", fg="Red") if error_ch6.is_lit else error_label.config(text="Ingen fejl.", fg="Green")
    if time_controller.start is not None:
        elapsed_time_label.config(text=str(time_controller.get_elapsed() // 60) + " min.")
        remaining_time_label.config(text=str(time_controller.get_remaining() // 60) + " min.") if time_controller.get_remaining() > 0 else remaining_time_label.config(text="N/A")
    
    # When running, updates the log file periodically
    if running_ch5.is_lit:
        if time_controller.log_condition():
            log_data(entered_user_input.target_temp,
                    sensor_data.current_temp_dht,
                    entered_user_input.target_humidity,
                    sensor_data.current_hum_dht,
                    int(ventilator_ch1.is_lit),
                    int(varmer_ch2.is_lit),
                    int(affugter_ch3.is_lit),
                    int(damp_ch4.is_lit),
                    int(error_ch6.is_lit)
                    )
        
        if time_controller.stop_condition():
            on_cancel_button_press()

    # Schedule the next update
    window.after(constants.UPDATE_FREQUENCY, lambda: update_gui_and_relays(sensor_data, time_controller)) 
    
    
# ========== START BACKGROUND THREAD & GUI LOOP ==========

# Create and start the thread that reads the sensors continuously
thread = Thread(target=read_sensors_in_thread, args=(sensor_data_all, stop_flag,))
thread.start()

# Updates the GUI for the first time - after initially called, the update_gui() function will call itself periodically
# until the program is terminated
window.after(500, lambda: update_gui_and_relays(sensor_data_all, time_controller_all))

# Starts the GUI event loop
target_temperature_textentry.focus_set()
window.protocol("WM_DELETE_WINDOW", close_gui)
window.mainloop()
