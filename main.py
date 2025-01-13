from threading import Thread
import RPi.GPIO as GPIO

import constants
from user_input_class import UserInput
from time_controller_class import TimeController
from relays_class import Relays
from sensors_class import Sensors
from gui_class import Gui
from data_logging_function import log_data


def main():
    # Starts the thread that reads the sensors continuously
    sensor_thread.start()
    # Updates the GUI for the first time - after initially called, the update_gui() function will call itself
    # periodically until the program is terminated
    gui.window.after(constants.UPDATE_FREQUENCY, lambda: update_gui_and_relays(sensors, relays, time_controller))
    # Sets the initial GUI focus to temperature entry
    gui.target_temperature_textentry.focus_set()
    # Runs the cleanup function close_gui() when the window is closed
    gui.window.protocol("WM_DELETE_WINDOW", close_gui)
    # Starts the GUI event loop
    gui.window.mainloop()    


# Object initialization

relays = Relays()
sensors = Sensors()
user_input = UserInput()
time_controller = TimeController(user_input)
gui = Gui(user_input, relays, time_controller)
sensor_thread = Thread(target=sensors.read_sensors_in_thread, args=(sensors,))



# ========== PERIODIC GUI AND RELAY UPDATE ==========

def update_gui_and_relays(sensor_data, relay_data, timer):
    """Updates the state of the relays and the GUI labels."""
    if sensor_data.current_temp_dht is not None:
        gui.actual_temperature_label.config(text=str(sensor_data.current_temp_dht) + "°C")
    if sensor_data.current_hum_dht is not None:
        gui.actual_humidity_label.config(text=str(sensor_data.current_hum_dht) + "%")
        
    relay_data.update_relay_channels(sensor_data, user_input)
    
    gui.ventilator_label.config(text="ON", fg="Green") if relay_data.ventilator_ch1.is_lit else gui.ventilator_label.config(text="OFF", fg="Red")
    gui.varmer_label.config(text="ON", fg="Green") if relay_data.varmer_ch2.is_lit else gui.varmer_label.config(text="OFF", fg="Red")
    gui.affugter_label.config(text="ON", fg="Green") if relay_data.affugter_ch3.is_lit else gui.affugter_label.config(text="OFF", fg="Red")
    gui.damp_label.config(text="ON", fg="Green") if relay_data.damp_ch4.is_lit else gui.damp_label.config(text="OFF", fg="Red")
    gui.status_label.config(text="Kører.") if relay_data.running_ch5.is_lit else gui.status_label.config(text="Stoppet.")
    gui.error_label.config(text="Fejl", fg="Red") if relay_data.error_ch6.is_lit else gui.error_label.config(text="Ingen fejl.", fg="Green")
    if timer.start is not None:
        gui.elapsed_time_label.config(text=str(timer.get_elapsed() // 60) + " min.")
        gui.remaining_time_label.config(text=str(timer.get_remaining() // 60) + " min.") if timer.get_remaining() > 0 else gui.remaining_time_label.config(text="N/A")
    
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
            gui.on_cancel_button_press()

    # Schedule the next update
    gui.window.after(constants.UPDATE_FREQUENCY, lambda: update_gui_and_relays(sensor_data, relay_data, timer))


# Called when the window is closed; cleans up.
def close_gui() -> None:
    sensors.stop_flag.set()
    sensor_thread.join()
    GPIO.cleanup()
    gui.window.destroy()


if __name__ == "__main__":
    main()
