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
        self.malfunction_on = False
        self.message = ""
        self.heater_malfunction = False
        self.humidifier_malfunction = False
        self.dehumidifier_malfunction = False
    
    def catch_heater_malfunction(self):
        if self.time_controller.seconds_elapsed >= (constants.HEATER_WARMUP_TIME * 60):
            if self.sensors.current_temp_dht < self.user_input.target_temp - constants.HUMIDITY_CONTROL_THRESHOLD:
                self.heater_malfunction = True
                
    def catch_humidifier_malfunction(self):
        if self.time_controller.temp_reached_timestamp:
            if self.time_controller.seconds_elapsed_since_temp_reached >= (constants.HUMIDIFIER_WARMUP_TIME * 60):
                if self.sensors.current_hum_dht < self.user_input.target_humidity - constants.HUMIDITY_TOLERANCE:
                    self.humidifier_malfunction = True
        
    def catch_dehumidifer_malfunction(self):
        if self.time_controller.temp_reached_timestamp:
            if self.time_controller.seconds_elapsed_since_temp_reached >= (constants.DEHUMIDIFIER_WARMUP_TIME * 60):
                if self.sensors.current_hum_dht > self.user_input.target_humidity + constants.HUMIDITY_TOLERANCE:
                    self.dehumidifier_malfunction = True
    
    def set_malfunctioned_flag(self):
        self.malfunction_on = self.heater_malfunction or self.humidifier_malfunction or self.dehumidifier_malfunction
        
    def set_malfunction_message(self):
        if self.heater_malfunction:
            self.message = "Temperaturen stiger ikke - tjek varmeren."
        if self.humidifier_malfunction:
            self.message = "Luftfugtigheden stiger ikke - tjek dampgeneratoren."
        if self.dehumidifier_malfunction:
            self.message = "Luftfugtigheden falder ikke - tjek affugteren."
    
    def activate_error_relay(self):
        if self.malfunction_on:
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
