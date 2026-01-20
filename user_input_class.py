import constants

from dialog_window_functions import info_dialog
from error_definitions import ValueOutsideRangeError, MinuteValueOutsideRangeError, HourValueOutsideRangeError, ValueMissingError

class UserInput:
    def __init__(self) -> None:
        self.reset()
    
    def reset(self) -> None:
        self.is_correct = False
        self.target_temp = None
        self.target_humidity = None
        self.running_time = None
        self.startup_delay = None
    
    def read(self,
             user_target_temp,
             user_target_humidity,
             user_target_running_time_h,
             user_target_running_time_m,
             user_startup_delay) -> None:
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
        
        if user_target_running_time_h == "" and user_target_running_time_m == "":
            self.running_time = 0
        else:
            try:
                time_h = 0 if user_target_running_time_h == "" else int(user_target_running_time_h) * 60
                time_m = 0 if user_target_running_time_m == "" else int(user_target_running_time_m)
                
                if time_m not in range(60):
                    raise MinuteValueOutsideRangeError
                
                if time_h < 0:
                    raise ValueError
                
                self.running_time = time_h + time_m
                if self.running_time not in range(0, constants.MAX_TIME * 60 + 1):
                    raise ValueOutsideRangeError
                
            except ValueOutsideRangeError:
                info_dialog("Ugyldigt input", f"Den ønskede køretid må ikke\noverstige {constants.MAX_TIME} timer (tast 0 for ubestemt).")
                self.is_correct = False
            except MinuteValueOutsideRangeError:
                info_dialog("Ugyldigt input", f"Værdien i minutfeltet skal være\nmellem 0 og 59.")
                self.is_correct = False
            except ValueError:
                info_dialog("Ugyldigt input", f"Den ønskede køretid skal bestå af to heltal\n(ingen bogstaver, mellerum eller decimaler).")
                self.is_correct = False
        
        if user_startup_delay == "":
            self.startup_delay = 0
        else:
            try:
                self.startup_delay = int(user_startup_delay)
                if not user_startup_delay in range(0, constants.MAX_DELAY):
                    raise HourValueOutsideRangeError
            
            except ValueError:
                info_dialog("Ugyldigt input", f"Opstart må højst udsættes med {constants.MAX_DELAY} timer.")
                self.is_correct = False
            except HourValueOutsideRangeError:
                info_dialog("Ugyldigt input", f"I feltet 'Udsat opstart' må der kun skrives heltal\n(ingen bogstaver, mellerum eller decimaler).")
                self.is_correct = False