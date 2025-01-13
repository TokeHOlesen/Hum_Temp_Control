from gpiozero import LED

import constants


class Relays:
    def __init__(self):
        # Instatiates an LED object for each relay, corresponding to the respective GPIO pin.
        # Using LED objects allows to quickly set them to high or low voltage.
        self.ventilator_ch1 = LED(5)
        self.varmer_ch2 = LED(6)
        self.affugter_ch3 = LED(13)
        self.damp_ch4 = LED(26)
        self.running_ch5 = LED(12)
        self.error_ch6 = LED(16)
        
    def reset_all_channels(self) -> None:
        self.ventilator_ch1.off()
        self.varmer_ch2.off()
        self.affugter_ch3.off()
        self.damp_ch4.off()
        self.running_ch5.off()
        self.error_ch6.off()
    
    def update_channels(self, sensor_data, user_input):
        if self.running_ch5.is_lit:
            self.ventilator_ch1.on()
            
            if self.ventilator_ch1.is_lit:
                # Only turns the heater on if the temperature is lower than target, minus acceptable tolerance
                if sensor_data.current_temp_dht <= user_input.target_temp - constants.TEMPERATURE_TOLERANCE:
                    self.varmer_ch2.on()
                else:
                    self.varmer_ch2.off()
                
                # Checks if the current temperature is within a set range of temperatures from target
                # Humidifier and dehumidifier won't be turned on otherwise
                if abs(sensor_data.current_temp_dht - user_input.target_temp) <= constants.HUMIDITY_CONTROL_THRESHOLD:
                    if sensor_data.current_hum_dht < user_input.target_humidity - constants.HUMIDITY_TOLERANCE:
                        self.affugter_ch3.off()
                        self.damp_ch4.on()
                    elif sensor_data.current_hum_dht > user_input.target_humidity + constants.HUMIDITY_TOLERANCE:
                        self.affugter_ch3.on()
                        self.damp_ch4.off()
                else:
                    self.affugter_ch3.off()
                    self.damp_ch4.off()
            else:
                self.varmer_ch2.off()
                self.affugter_ch3.off()
                self.damp_ch4.off()
                self.running_ch5.off()