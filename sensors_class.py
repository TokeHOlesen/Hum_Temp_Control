from threading import Event, Thread
from time import sleep
import board
import adafruit_dht
import os

import constants


class Sensors:
    def __init__(self) -> None:
        self.current_temp_dht = None
        self.current_hum_dht = None
        self.current_temp_1 = None
        self.current_temp_2 = None
        # Initializes a thread that will run in the background and continuously update sensor readings
        self.thread = Thread(target=self.read_sensors_in_thread)
        # Sensor readings will continue being taken for as long as this flag is not set
        self.stop_flag = Event()
        self.target_temperature_reached = False
        self.target_values_reached = False
        self.sensor_error = False
        self.error_message = ""
        self.initialize()

    def initialize(self) -> None:
        # Initializes the DHT22 humidity and temperature sensor
        self.dht22_sensor = adafruit_dht.DHT22(board.D18)
        # Initializes the DS18B20 temperature probes
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        self.base_dir = '/sys/bus/w1/devices/'
        self.temp_sensor_1_file = self.base_dir + '28-0000006a045f/w1_slave'
        self.temp_sensor_2_file = self.base_dir + '28-00000085eccb/w1_slave'
        
    def read_temp_from_probe(self, probe_number: int):
        """
        Reads data from the given device file; accepts an argument that is the path to a DS18B20 probe device file.
        Returns a float with 1 decimal place if data is found, else None.
        """
        probes = {
            1: self.temp_sensor_1_file,
            2: self.temp_sensor_2_file
        }
        
        sensor_device_file = probes[probe_number]
        
        with open(sensor_device_file, 'r') as file:
            temp_data_lines = file.readlines()
        temp_data_start_pos = temp_data_lines[1].find('t=')
        if temp_data_start_pos != -1:
            temp_string = temp_data_lines[1][temp_data_start_pos + 2:]
            return round(float(temp_string) / 1000.0, 1)
        return None

    def read_sensors_in_thread(self) -> None:
        """
        Runs in a background thread. Reads sensor data and stores it in the sensor_data object.
        Runs until self.stop_flag is set.
        """
        while not self.stop_flag.is_set():
            try:
                # Read from DHT22
                self.current_temp_dht = self.dht22_sensor.temperature
                self.current_hum_dht = self.dht22_sensor.humidity
                # Read from DS18B20 probes
                self.current_temp_1 = self.read_temp_from_probe(1)
                self.current_temp_2 = self.read_temp_from_probe(2)
                self.sensor_error = False
                self.sensor_message = ""
            except IndexError as e:
                # An index error will be raised when one or both of the temp probes can't be accessed.
                # Since they are not used for anything right now, it only outputs a message to terminal.
                print("DS18B20 error: " + str(e))
            except Exception as e:
                # Since the DHT22 frequently raises read errors, which almost always are inconsequential, only reacts
                # to the "Sensor not found" error
                if str(e) == "DHT sensor not found, check wiring":
                    self.sensor_error = True
                    self.error_message = "DHT22 blev ikke fundet, tjek forbindelsen."
                else:
                    print("Sensor error: " + str(e))

            # Time between each reading (in seconds)
            sleep(constants.SENSOR_PROBING_INTERVAL)

    def check_if_target_values_reached(self, user_input):
        if abs(self.current_temp_dht - user_input.target_temp) <= constants.HUMIDITY_CONTROL_THRESHOLD:
            self.target_temperature_reached = True
        if self.target_temperature_reached:
            if abs(self.current_hum_dht - user_input.target_humidity) <= constants.HUMIDITY_TOLERANCE:
                self.target_values_reached = True
    
    def reset(self):
        self.target_temperature_reached = False
        self.target_values_reached = False
        self.sensor_error = False
        self.error_message = ""
