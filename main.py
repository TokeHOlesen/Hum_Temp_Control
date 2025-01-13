import tkinter as tk
from threading import Thread
import RPi.GPIO as GPIO

import constants
from user_input_class import UserInput
from time_controller_class import TimeController
from relays_class import Relays
from sensors_class import Sensors
from data_logging_function import log_data


def main():
    # Starts the thread that reads the sensors continuously
    sensor_thread.start()
    # Updates the GUI for the first time - after initially called, the update_gui() function will call itself
    # periodically until the program is terminated
    window.after(constants.UPDATE_FREQUENCY, lambda: update_gui_and_relays(sensors, relays, time_controller))
    # Sets the initial GUI focus to temperature entry
    target_temperature_textentry.focus_set()
    # Runs the cleanup function close_gui() when the window is closed
    window.protocol("WM_DELETE_WINDOW", close_gui)
    # Starts the GUI event loop
    window.mainloop()    


# ========== OBJECT INITIALIZATION ==========

relays = Relays()
sensors = Sensors()
user_input = UserInput()
time_controller = TimeController(user_input)
sensor_thread = Thread(target=sensors.read_sensors_in_thread, args=(sensors,))


# ========== PERIODIC GUI AND RELAY UPDATE ==========

def update_gui_and_relays(sensor_data, relay_data, timer):
    """Updates the state of the relays and the GUI labels."""
    if sensor_data.current_temp_dht is not None:
        actual_temperature_label.config(text=str(sensor_data.current_temp_dht) + "°C")
    if sensor_data.current_hum_dht is not None:
        actual_humidity_label.config(text=str(sensor_data.current_hum_dht) + "%")
        
    relay_data.update_relay_channels(sensor_data, user_input)
    
    ventilator_label.config(text="ON", fg="Green") if relay_data.ventilator_ch1.is_lit else ventilator_label.config(text="OFF", fg="Red")
    varmer_label.config(text="ON", fg="Green") if relay_data.varmer_ch2.is_lit else varmer_label.config(text="OFF", fg="Red")
    affugter_label.config(text="ON", fg="Green") if relay_data.affugter_ch3.is_lit else affugter_label.config(text="OFF", fg="Red")
    damp_label.config(text="ON", fg="Green") if relay_data.damp_ch4.is_lit else damp_label.config(text="OFF", fg="Red")
    status_label.config(text="Kører.") if relay_data.running_ch5.is_lit else status_label.config(text="Stoppet.")
    error_label.config(text="Fejl", fg="Red") if relay_data.error_ch6.is_lit else error_label.config(text="Ingen fejl.", fg="Green")
    if timer.start is not None:
        elapsed_time_label.config(text=str(timer.get_elapsed() // 60) + " min.")
        remaining_time_label.config(text=str(timer.get_remaining() // 60) + " min.") if timer.get_remaining() > 0 else remaining_time_label.config(text="N/A")
    
    # When running, updates the log file periodically
    if relay_data.running_ch5.is_lit:
        if timer.log_condition():
            log_data(user_input.target_temp,
                    sensor_data.current_temp_dht,
                    user_input.target_humidity,
                    sensor_data.current_hum_dht,
                    int(relay_data.ventilator_ch1.is_lit),
                    int(relay_data.varmer_ch2.is_lit),
                    int(relay_data.affugter_ch3.is_lit),
                    int(relay_data.damp_ch4.is_lit),
                    int(relay_data.error_ch6.is_lit)
                    )
        
        if timer.stop_condition():
            on_cancel_button_press()

    # Schedule the next update
    window.after(constants.UPDATE_FREQUENCY, lambda: update_gui_and_relays(sensor_data, relay_data, timer))


# Called when the window is closed; cleans up.
def close_gui() -> None:
    sensors.stop_flag.set()
    sensor_thread.join()
    GPIO.cleanup()
    window.destroy()


# ========== CLEARING USER INPUT DATA ==========

def clear_text_entry_fields():
    target_temperature_textentry.delete(0, tk.END)
    target_humidity_textentry.delete(0, tk.END)
    running_time_textentry.delete(0, tk.END)


# ========== GUI ==========

def on_start_button_press():
    user_input.read(target_temperature_textentry.get(),
                            target_humidity_textentry.get(),
                            running_time_textentry.get())
    if user_input.is_correct:
        relays.running_ch5.on()
        time_controller.start_timer()
        clear_text_entry_fields()
        target_temperature_label.config(text=str(user_input.target_temp) + "°C")
        target_humidity_label.config(text=str(user_input.target_humidity) + "%")
        target_temperature_textentry.focus_set()
    

def on_cancel_button_press():
    relays.reset_all_channels()
    time_controller.reset()
    user_input.reset()
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


if __name__ == "__main__":
    main()
