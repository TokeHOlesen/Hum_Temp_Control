from datetime import date, datetime
import csv
import os

class DataLogger:
    def __init__(self):
        # Set to True after an emergency log line has been written after a DHT22 malfunction
        # This is to prevent logging that data again and again when it enters the malfunction loop
        self.emergency_line_logged = False

    def log_data(self,
                user_input,
                sensors,
                relays,
                malfunctions):
        
        field_names = [
            "Tidspunkt",
            "Ønsket temperatur",
            "Faktisk temperatur",
            "Ønsket fugtighed",
            "Faktisk fugtighed",
            "Indblæsningstemp.",
            "Udblæsningstemp.",
            "Opvarmet",
            "Ventilator",
            "Varmer",
            "Affugter",
            "Dampgenerator",
            "Fejl",
            "Fejl meddelelse"
        ]
        
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        
        current_date = date.today()
        filename = f"./Logfiler/{current_date}.csv"
        day_log_exists = os.path.exists(filename)
        
        with open(filename, mode='a' if day_log_exists else 'w', newline='') as log_file:
            writer = csv.DictWriter(log_file, fieldnames=field_names, delimiter=";")
        
            if not day_log_exists:
                writer.writeheader()
            
            writer.writerow({
                "Tidspunkt": timestamp,
                "Ønsket temperatur": user_input.target_temp,
                "Faktisk temperatur": sensors.current_temp_dht,
                "Ønsket fugtighed": user_input.target_humidity,
                "Faktisk fugtighed": sensors.current_hum_dht,
                "Indblæsningstemp.": sensors.current_temp_1,
                "Udblæsningstemp.": sensors.current_temp_2,
                "Opvarmet": int(sensors.target_values_reached),
                "Ventilator": int(relays.ventilator_ch1.is_lit),
                "Varmer": int(relays.varmer_ch2.is_lit),
                "Affugter": int(relays.affugter_ch3.is_lit),
                "Dampgenerator": int(relays.damp_ch4.is_lit),
                "Fejl": int(relays.error_ch6.is_lit),
                "Fejl meddelelse": malfunctions.message
            })