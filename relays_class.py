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
                # If the measured temperature is below target (minus the value defined in TEMPERATURE_TOLERANCE), turns
                # the heater on. Turns it off once it reaches target + TEMPERATURE_TOLERANCE.
                # For example, if target temperature is 40 and tolerance is 2, the heater will turn on if the
                # temperature is below or at 38 degrees, and turn off again once it reaches 42 degrees.
                # It will then turn on again only when the temperature falls below 38 degrees.
                if sensor_data.current_temp_dht <= user_input.target_temp - constants.TEMPERATURE_TOLERANCE:
                    self.varmer_ch2.on()
                elif sensor_data.current_temp_dht >= user_input.target_temp + constants.TEMPERATURE_TOLERANCE:
                    self.varmer_ch2.off()
                
                # Runs humidity control if the temperature is in a range defined in HUMIDITY_CONTROL_THRESHOLD.
                # For example, it target temperature is 40 and HUMIDITY_CONTROL_THRESHOLD is set to 10, humidity
                # control will only run when the temperature is in the range 30-50 degrees.
                if abs(sensor_data.current_temp_dht - user_input.target_temp) <= constants.HUMIDITY_CONTROL_THRESHOLD:
                    # Turns humidifier on if humidity is below (target - tolerance)
                    if sensor_data.current_hum_dht < user_input.target_humidity - constants.HUMIDITY_TOLERANCE:
                        self.damp_ch4.on()
                    # Turns humidifier off is humidity is at or above target
                    if sensor_data.current_hum_dht >= user_input.target_humidity:
                        self.damp_ch4.off()
                    # Turns dehumidifier on if humidity is above (target + tolerance)
                    if sensor_data.current_hum_dht > user_input.target_humidity + constants.HUMIDITY_TOLERANCE:
                        self.affugter_ch3.on()
                    # Turns dehumidifier off is humidity is at or below target
                    if sensor_data.current_hum_dht <= user_input.target_humidity:
                        self.affugter_ch3.off()
                else:
                    self.affugter_ch3.off()
                    self.damp_ch4.off()
            else:
                self.varmer_ch2.off()
                self.affugter_ch3.off()
                self.damp_ch4.off()
                self.running_ch5.off()