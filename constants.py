# Time between sensor readings, in seconds
SENSOR_PROBING_INTERVAL = 2
# How often to update the GUI and relay channels, in milliseconds
UPDATE_FREQUENCY = 500
# How often to log data, in seconds
LOGGING_FREQUENCY = 120
# How many degrees the temperature has to differ from target before the heater is turned on or off
TEMPERATURE_TOLERANCE = 2
# How much the humidity has to differ from target before the (de)humidifier is turned on or off
HUMIDITY_TOLERANCE = 2
# How much the temperature can differ from target before humidifier and dehumidifier can be turned on or off
HUMIDITY_CONTROL_THRESHOLD = 10
# Lowest allowed temperature
MIN_TEMP = 0
# Highest allowed temperature
MAX_TEMP = 45
# Lowest allowed humidity
MIN_HUMIDITY = 0
# Highest allowed humidity
MAX_HUMIDITY = 100
# How long the process can be scheduled for, in minutes
MAX_TIME = 720
