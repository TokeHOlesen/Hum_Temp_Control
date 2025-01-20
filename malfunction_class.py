import constants


class Malfunction_Watcher:
    def __init__(self,
                 relays,
                 sensors,
                 user_input,
                 time_controller):
        self.relays = relays
        self.sensors = sensors
        self.user_input = user_input
        self.time_controller = time_controller
        self.malfunction_found = False
        self.message = ""
        self.malfunctions = {
            "Heater": False,
            "Humidifier": False,
            "Dehumidifier": False
        }
        self.malfunction_messages = {
            "Heater": "Temperaturen stiger ikke - tjek varmeren.",
            "Humidifier": "Luftfugtigheden stiger ikke - tjek dampgeneratoren.",
            "Dehumidifier": "Luftfugtigheden falder ikke - tjek affugteren."
        }
    
    def catch_heater_malfunction(self):
        if self.time_controller.seconds_elapsed >= (constants.HEATER_WARMUP_TIME * 60):
            if self.sensors.current_temp_dht < self.user_input.target_temp - constants.HUMIDITY_CONTROL_THRESHOLD:
                self.malfunctions["Heater"] = True
                
    def catch_humidifier_malfunction(self):
        if self.time_controller.temp_reached_timestamp:
            if self.time_controller.seconds_elapsed_since_temp_reached >= (constants.HUMIDIFIER_WARMUP_TIME * 60):
                if self.sensors.current_hum_dht < self.user_input.target_humidity - constants.HUMIDITY_TOLERANCE:
                    self.malfunctions["Humidifier"] = True
        
    def catch_dehumidifer_malfunction(self):
        if self.time_controller.temp_reached_timestamp:
            if self.time_controller.seconds_elapsed_since_temp_reached >= (constants.DEHUMIDIFIER_WARMUP_TIME * 60):
                if self.sensors.current_hum_dht > self.user_input.target_humidity + constants.HUMIDITY_TOLERANCE:
                    self.malfunctions["Dehumidifier"] = True
    
    def set_malfunctioned_flag(self):
        for item in self.malfunctions:
            if self.malfunctions[item]:
                self.malfunction_found = True
                break
        
    def set_malfunction_message(self):
        for item in self.malfunctions:
            if self.malfunctions[item]:
                self.message = self.malfunction_messages[item]
                break
    
    def activate_error_relay(self):
        if self.malfunction_found:
            self.relays.error_ch6.on()
        else:
            self.relays.error_ch6.off()
    
    def catch_malfunctions(self):
        self.catch_heater_malfunction()
        self.catch_humidifier_malfunction()
        self.catch_dehumidifer_malfunction()
        self.set_malfunctioned_flag()
        self.set_malfunction_message()
        self.activate_error_relay() 
