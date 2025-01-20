from datetime import date, datetime
import csv
import os

def log_data(target_temp,
            current_temp,
            target_humidity,
            current_humidity,
            ventilator,
            varmer,
            affugter,
            dampgenerator,
            fejl,
            opvarmet):
    
    field_names = [
        "tidspunkt",
        "ønsket temperatur",
        "faktisk temperatur",
        "ønsket fugtighed",
        "faktisk fughtighed",
        "ventilator",
        "varmer",
        "affugter",
        "dampgenerator",
        "fejl",
        "opvarmet"
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
            "tidspunkt": timestamp,
            "ønsket temperatur": target_temp,
            "faktisk temperatur": current_temp,
            "ønsket fugtighed": target_humidity,
            "faktisk fughtighed": current_humidity,
            "ventilator": ventilator,
            "varmer": varmer,
            "affugter": affugter,
            "dampgenerator": dampgenerator,
            "fejl": fejl,
            "opvarmet": opvarmet
        })