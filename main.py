import tkinter as tk
from gpiozero import LED
from threading import Thread
import RPi.GPIO as GPIO

import constants
from user_input_class import UserInput
from time_controller_class import TimeController
from sensors_class import Sensors
from data_logging_function import log_data


# ========== OBJECT INITIALIZATION ==========

sensors = Sensors()
entered_user_input = UserInput()
time_controller_all = TimeController(entered_user_input)


# ========== HARDWARE SETUP ==========

# Instatiates an LED object for each relay, corresponding to the respective GPIO pin.
# Using LED objects allows to quickly set them to high or low voltage.
ventilator_ch1 = LED(5)
varmer_ch2 = LED(6)
affugter_ch3 = LED(13)
damp_ch4 = LED(26)
running_ch5 = LED(12)
error_ch6 = LED(16)


def reset_all_channels() -> None:
    ventilator_ch1.off()
    varmer_ch2.off()
    affugter_ch3.off()
    damp_ch4.off()
    running_ch5.off()
    error_ch6.off()


# Called when the window is closed; cleans up.
def close_gui() -> None:
    sensors.stop_flag.set()
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

def update_gui_and_relays(sensors, time_controller):
    """Updates the state of the relays and the GUI labels."""
    if sensors.current_temp_dht is not None:
        actual_temperature_label.config(text=str(sensors.current_temp_dht) + "°C")
    if sensors.current_hum_dht is not None:
        actual_humidity_label.config(text=str(sensors.current_hum_dht) + "%")
        
    update_relay_channels(sensors, entered_user_input)
    
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
                    sensors.current_temp_dht,
                    entered_user_input.target_humidity,
                    sensors.current_hum_dht,
                    int(ventilator_ch1.is_lit),
                    int(varmer_ch2.is_lit),
                    int(affugter_ch3.is_lit),
                    int(damp_ch4.is_lit),
                    int(error_ch6.is_lit)
                    )
        
        if time_controller.stop_condition():
            on_cancel_button_press()

    # Schedule the next update
    window.after(constants.UPDATE_FREQUENCY, lambda: update_gui_and_relays(sensors, time_controller)) 
    
    
# ========== START BACKGROUND THREAD & GUI LOOP ==========

# Create and start the thread that reads the sensors continuously
thread = Thread(target=sensors.read_sensors_in_thread, args=(sensors,))
thread.start()

# Updates the GUI for the first time - after initially called, the update_gui() function will call itself periodically
# until the program is terminated
window.after(constants.UPDATE_FREQUENCY, lambda: update_gui_and_relays(sensors, time_controller_all))

# Starts the GUI event loop
target_temperature_textentry.focus_set()
window.protocol("WM_DELETE_WINDOW", close_gui)
window.mainloop()
