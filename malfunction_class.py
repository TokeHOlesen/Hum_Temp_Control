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
            "DHT22 sensor": False,
            "DHT22 quarantine": False,
            "DS18B20 sensor": False,
            "Heater warmup": False,
            "Humidifier warmup": False,
            "Dehumidifier warmup": False,
            "Temp too low": False,
            "Temp too high": False,
            "Humidity too low": False,
            "Humidity too high": False
        }
        self.malfunction_messages = {
            "DHT22 sensor": "DHT22 er offline, maskinen er stoppet.",
            "DHT22 quarantine": "DTH22 er offline, forsøger at genetablere forbindelsen.",
            "DS18B20 sensor": "DS18B20 temperatursensor fejl, tjek forbindelsen.",
            "Heater warmup": "Temperaturen stiger ikke - tjek varmeren.",
            "Humidifier warmup": "Luftfugtigheden stiger ikke - tjek dampgeneratoren.",
            "Dehumidifier warmup": "Luftfugtigheden falder ikke - tjek affugteren.",
            "Temp too low": "Temperaturen er for lav - tjek varmeren.",
            "Temp too high": "Temperaturen er for høj - tjek varmeren.",
            "Humidity too low": "Luftfugtigheden er for lav - tjek dampgeneratoren.",
            "Humidity too high": "Luftfugtigheden er for høj - tjek affugteren."
        }
        self.malfunction_catchers = {
            "DHT22 sensor": self.catch_dht22_malfunction,
            "DHT22 quarantine": self.catch_dht22_quarantine,
            "DS18B20 sensor": self.catch_ds18b20_malfunction,
            "Heater warmup": self.catch_heater_warmup_malfunction,
            "Humidifier warmup": self.catch_humidifier_warmup_malfunction,
            "Dehumidifier warmup": self.catch_dehumidifier_warmup_malfunction,
            "Temp too low": self.catch_temperature_too_low_malfunction,
            "Temp too high": self.catch_temperature_too_high_malfunction,
            "Humidity too low": self.catch_humidity_too_low_malfunction,
            "Humidity too high":self.catch_humidity_too_high_malfunction
        }
    
    # If the DHT22 sensor has been in quarantine for a set amount of time, sets the malfunction flag and stops the machine.
    def catch_dht22_malfunction(self):
        if self.malfunctions["DHT22 quarantine"]:
            if self.time_controller.seconds_in_quarantine * 60 > constants.QUARANTINE_LENGTH:
                self.malfunctions["DHT22 sensor"] = True
        
    # If a connection with the DHT22 sensor cannot be established, puts the sensor in quarantine mode and starts
    # the quarantine timer. Removes the flag if the connection has been reestablished.
    def catch_dht22_quarantine(self):
        if self.sensors.dht22_error:
            if not self.malfunctions["DHT22 quarantine"]:
                self.malfunctions["DHT22 quarantine"] = True
                self.time_controller.start_dht22_quarantine()
        else:
            self.malfunctions["DHT22 quarantine"] = False

    # Raises a malfunction if a connection with the DS18B20 sensors cannot be established.
    def catch_ds18b20_malfunction(self):
        self.malfunctions["DS18B20 sensor"] = self.sensors.ds18b20_error
    
    # If the target temperature has not been reached after the time specified in HEATER_WARMUP_TIME
    # raises possible malfunction
    def catch_heater_warmup_malfunction(self):
        if self.relays.running_ch5.is_lit and self.time_controller.seconds_elapsed >= (constants.HEATER_WARMUP_TIME * 60) and not self.sensors.target_temperature_reached:
            if self.sensors.current_temp_dht < self.user_input.target_temp - constants.HUMIDITY_CONTROL_THRESHOLD:
                self.malfunctions["Heater warmup"] = True
            else:
                self.malfunctions["Heater warmup"] = False
    
    # If the target temperature has been reached but the humidity has not gone up and and is still below target after
    # the time specified in HUMIDIFIER_WARMUP_TIME (counting from the moment target temperature has been reached),
    # raises possible malfunction
    def catch_humidifier_warmup_malfunction(self):
        if self.relays.running_ch5.is_lit and self.sensors.target_temperature_reached and not self.sensors.target_values_reached:
            if self.time_controller.seconds_elapsed_since_temp_reached >= (constants.HUMIDIFIER_WARMUP_TIME * 60):
                if self.sensors.current_hum_dht < self.user_input.target_humidity - constants.HUMIDITY_TOLERANCE:
                    self.malfunctions["Humidifier warmup"] = True
                else:
                    self.malfunctions["Humidifier warmup"] = False

    # If the target temperature has been reached but the humidity has not gone down and and is still above target after
    # the time specified in DEHUMIDIFIER_WARMUP_TIME (counting from the moment target temperature has been reached),
    # raises possible malfunction
    def catch_dehumidifier_warmup_malfunction(self):
        if self.relays.running_ch5.is_lit and self.sensors.target_temperature_reached and not self.sensors.target_values_reached:
            if self.time_controller.seconds_elapsed_since_temp_reached >= (constants.DEHUMIDIFIER_WARMUP_TIME * 60):
                if self.sensors.current_hum_dht > self.user_input.target_humidity + constants.HUMIDITY_TOLERANCE:
                    self.malfunctions["Dehumidifier warmup"] = True
                else:
                    self.malfunctions["Dehumidifier warmup"] = False
    
    # After warmup, if the temperature falls too low, raises a malnfunction
    def catch_temperature_too_low_malfunction(self):
        if self.relays.running_ch5.is_lit and self.sensors.target_values_reached:
            if self.sensors.current_temp_dht + constants.TEMPERATURE_ERROR_THRESHOLD <= self.user_input.target_temp:
                self.malfunctions["Temp too low"] = True
            else:
                self.malfunctions["Temp too low"] = False
    
    # After warmup, if the temperature rises too high, raises a malnfunction
    def catch_temperature_too_high_malfunction(self):
        if self.relays.running_ch5.is_lit and self.sensors.target_values_reached:
            if self.sensors.current_temp_dht - constants.TEMPERATURE_ERROR_THRESHOLD >= self.user_input.target_temp:
                self.malfunctions["Temp too high"] = True
            else:
                self.malfunctions["Temp too high"] = False
    
    # After warmup, if the humidity falls too low, raises a malnfunction                
    def catch_humidity_too_low_malfunction(self):
        if self.relays.running_ch5.is_lit and self.sensors.target_values_reached:
            if self.sensors.current_hum_dht + constants.HUMIDITY_ERROR_THRESHOLD <= self.user_input.target_humidity:
                self.malfunctions["Humidity too low"] = True
            else:
                self.malfunctions["Humidity too low"] = False
    
    # After warmup, if the humidity rises too high, raises a malnfunction
    def catch_humidity_too_high_malfunction(self):
        if self.relays.running_ch5.is_lit and self.sensors.target_values_reached:
            if self.sensors.current_hum_dht - constants.HUMIDITY_ERROR_THRESHOLD >= self.user_input.target_humidity:
                self.malfunctions["Humidity too high"] = True
            else:
                self.malfunctions["Humidity too high"] = False
    
    def set_malfunctioned_flag(self):
        self.malfunction_found = False
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
        for item in self.malfunction_catchers:
            self.malfunction_catchers[item]()
        self.set_malfunctioned_flag()
        self.set_malfunction_message()
        self.activate_error_relay()
    
    def reset(self):
        for item in self.malfunctions:
            self.malfunctions[item] = False
        self.malfunction_found = False
        self.message = ""
