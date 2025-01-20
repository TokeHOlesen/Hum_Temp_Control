import RPi.GPIO as GPIO

import constants
from user_input_class import UserInput
from time_controller_class import TimeController
from relays_class import Relays
from sensors_class import Sensors
from gui_class import Gui
from malfunction_class import Malfunction_Watcher
from data_logging_function import log_data
from dialog_window_functions import askyesno_dialog, info_dialog

def main():
    # Starts the thread that reads the sensors continuously
    sensors.thread.start()
    # Updates the GUI for the first time - after initially called, the update_gui() function will call itself
    # periodically until the program is terminated
    gui.window.after(constants.UPDATE_FREQUENCY, update_gui_and_relays)
    # Sets the initial GUI focus to temperature entry
    gui.target_temperature_textentry.focus_set()
    # Runs the cleanup function close_gui() when the window is closed
    gui.window.protocol("WM_DELETE_WINDOW", close_gui)
    # Starts the GUI event loop
    gui.window.mainloop()    


# Object initialization

# Defines the relay to GPIO connections and contains the code that sets them to high or low depending on sensor readings
relays = Relays()
# Initializes the sensors and provides an interface to access sensor readings
sensors = Sensors()
# Provides an interface to read and check user input
user_input = UserInput()
# Provides a clock and associated events
time_controller = TimeController(user_input)
# Checks for and reports malfunctions
malfunctions = Malfunction_Watcher(relays, sensors, user_input, time_controller)
# User interface
gui = Gui(relays, sensors, user_input, time_controller, malfunctions)


def update_gui_and_relays():
    """Updates the state of the relays and the GUI labels."""
    relays.update_channels(sensors, user_input)
    gui.update()
    
    # When running, updates the log file periodically
    if relays.running_ch5.is_lit:
        malfunctions.catch_malfunctions()
        sensors.check_if_target_values_reached(user_input)
        if sensors.target_values_reached and not time_controller.timer_restarted:
            time_controller.restart_timer()
        
        if time_controller.log_condition:
            log_data(user_input.target_temp,
                    sensors.current_temp_dht,
                    user_input.target_humidity,
                    sensors.current_hum_dht,
                    int(relays.ventilator_ch1.is_lit),
                    int(relays.varmer_ch2.is_lit),
                    int(relays.affugter_ch3.is_lit),
                    int(relays.damp_ch4.is_lit),
                    int(relays.error_ch6.is_lit),
                    int(sensors.target_values_reached))
        
        if time_controller.stop_condition:
            gui.cancel_process()

    # Schedule the next update
    gui.window.after(constants.UPDATE_FREQUENCY, lambda: update_gui_and_relays())


def close_gui() -> None:
    """Called when the window is closed; cleans up."""
    if relays.running_ch5.is_lit:
        info_dialog("Maskinerne er i drift", "Den igangværende kørsel skal afluttes,\ninden programmet kan lukkes.")
        return
    if askyesno_dialog("Bekræft afslutning", "Er du sikker på, at du vil lukke programmet?"):
        sensors.stop_flag.set()
        sensors.thread.join()
        GPIO.cleanup()
        gui.window.destroy()


if __name__ == "__main__":
    main()
