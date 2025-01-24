import RPi.GPIO as GPIO

import constants
from user_input_class import UserInput
from time_controller_class import TimeController
from relays_class import Relays
from sensors_class import Sensors
from gui_class import Gui
from malfunction_class import Malfunction_Watcher
from data_logger_class import DataLogger
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
# Logs data
logger = DataLogger()
# User interface
gui = Gui(relays, sensors, user_input, time_controller, malfunctions, logger)


def update_gui_and_relays():
    """Updates the state of the relays and the GUI labels."""
    malfunctions.catch_malfunctions()
    # If the DHT22 has malfunctioned, writes the state of the system to the log file and stops the running process
    if malfunctions.malfunctions["DHT22 sensor"]:
        if relays.running_ch5.is_lit and not logger.emergency_line_logged:
            logger.log_data(user_input, sensors, relays, malfunctions)
            logger.emergency_line_logged = True
        
        relays.reset_all_channels()
        relays.error_ch6.on()
        time_controller.reset()
        user_input.reset()

    relays.update_channels(sensors, user_input)
    gui.update()
    
    # Checks if target values have been reached (separately for the temperature and the whole system),
    # sets the relevant flags to True if yes
    if relays.running_ch5.is_lit:
        sensors.check_if_target_values_reached(user_input)
        if sensors.target_temperature_reached:
            time_controller.set_temp_reached_timestamp()
        if sensors.target_values_reached:
            time_controller.restart_timer()
        
        # Logs data periodically
        if time_controller.log_condition:
            logger.log_data(user_input, sensors, relays, malfunctions)
        
        # Stops the currently running process if the timer has reached 0
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
