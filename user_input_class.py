import constants


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
            self.target_temp = min(int(user_target_temp), constants.MAX_TEMP)
        except:
            print("Ugyldig temperatur input")
            self.is_correct = False
        
        try:
            self.target_humidity = max(0, min(int(user_target_humidity), constants.MAX_HUMIDITY))
        except:
            print("Ugyldig fugtighed input")
            self.is_correct = False
        
        if user_target_running_time == "":
            self.running_time = 0
        else:
            try:
                self.running_time = max(0, int(user_target_running_time))
            except:
                print("Ugyldig tid input")
                self.is_correct = False