import json
from httprequest import HTTPRequest

class Sensors():

    def __init__(self, config):
        self.config = config
        self.httprequest = HTTPRequest(config)

    def list(self):
        response = self.httprequest.request('sensors/list', {})
        return response

    def read(self, id):
        response = self.httprequest.request('sensor/info', {"id": id})
        return response['data']

    def readall(self):
        result = {}
        sensors = self.list()

        for sensor in sensors['sensor']:
            result[sensor['name']] = {}
            sensordata = self.read(sensor['id'])
            for data in sensordata:
                result[sensor['name']][data['name']] = data['value']

        return result
