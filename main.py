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
    for read in readout:
        print read
        print "    Temp: " + str(readout[read]['temp'])
        print "    Humidity: " + str(readout[read]['humidity'])

    print "Devices"
    devices = Devices(config)
    readout = devices.readall()
    for read in readout:
	    print read['name']

if __name__ == "__main__":
    main()
