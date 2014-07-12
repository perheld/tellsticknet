import json
import time
from sensors import Sensors
from devices import Devices

def main():
    json_data = open('config.json')
    config = json.load(json_data)

    print "Sensors"
    sensors = Sensors(config)
    readout = sensors.readall()
    print readout

    print "Devices"
    devices = Devices(config)
    readout = devices.readall()
    print readout

if __name__ == "__main__":
    main()
