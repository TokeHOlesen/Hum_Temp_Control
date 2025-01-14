import constants

from dialog_window_functions import info_dialog
from error_definitions import ValueOutsideRangeError, ValueMissingError

class UserInput:
    def __init__(self) -> None:
        self.reset()
    
    def reset(self) -> None:
        self.is_correct = False
        self.target_temp = None
        self.target_humidity = None
        self.running_time = None
    
    def read(self,
             user_target_temp,
             user_target_humidity,
             user_target_running_time) -> None:
        # Sets the .is_correct flag to True. If any of the inputs are incorrect, it will be set to False
        self.is_correct = True
        
        try:
            if user_target_temp == "":
                raise ValueMissingError
            self.target_temp = int(user_target_temp)
            if self.target_temp not in range(constants.MIN_TEMP, constants.MAX_TEMP + 1):
                raise ValueOutsideRangeError
        except ValueMissingError:
            info_dialog("Ugyldigt input", f"Du skal indtaste den ønskede temperatur\n({constants.MIN_TEMP} - {constants.MAX_TEMP}°C).")
            self.is_correct = False
        except ValueOutsideRangeError:
            info_dialog("Ugyldigt input", f"Den ønskede temperatur skal være\nmellem {constants.MIN_TEMP} og {constants.MAX_TEMP}°C.")
            self.is_correct = False
        except ValueError:
            info_dialog("Ugyldigt input", f"Den ønskede temperatur skal være et heltal\n(ingen bogstaver, mellerum eller decimaler).")
            self.is_correct = False
        
        try:
            if user_target_humidity == "":
                raise ValueMissingError
            self.target_humidity = int(user_target_humidity)
            if self.target_humidity not in range(constants.MIN_HUMIDITY, constants.MAX_HUMIDITY + 1):
                raise ValueOutsideRangeError
        except ValueMissingError:
            info_dialog("Ugyldigt input", f"Du skal indtaste den ønskede\nluftfugtighed ({constants.MIN_HUMIDITY} - {constants.MAX_HUMIDITY}%).")
            self.is_correct = False
        except ValueOutsideRangeError:
            info_dialog("Ugyldigt input", f"Den ønskede luftfugtighed skal være\nmellem {constants.MIN_HUMIDITY} og {constants.MAX_HUMIDITY}%.")
            self.is_correct = False
        except ValueError:
            info_dialog("Ugyldigt input", f"Den ønskede luftfugtighed skal være et heltal\n(ingen bogstaver, mellerum eller decimaler).")
            self.is_correct = False
        
        if user_target_running_time == "":
            self.running_time = 0
        else:
            try:
                self.running_time = int(user_target_running_time)
                if self.running_time not in range(0, constants.MAX_TIME + 1):
                    raise ValueOutsideRangeError
            except ValueOutsideRangeError:
                info_dialog("Ugyldigt input", f"Den ønskede køretid skal være\nmellem 1 og {constants.MAX_TIME} minutter (0 for ubestemt).")
                self.is_correct = False
            except ValueError:
                info_dialog("Ugyldigt input", f"Den ønskede køretid skal være et heltal\n(ingen bogstaver, mellerum eller decimaler).")
                self.is_correct = False