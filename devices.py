import json
from httprequest import HTTPRequest

class Devices():

    def __init__(self, config):
        self.config = config
        self.httprequest = HTTPRequest(config)

    def list(self):
        response = self.httprequest.request('devices/list', {})
        return response

    def read(self, id):
        response = self.httprequest.request('device/info', {"id": id})
        return response

    def readall(self):
        result = []
        devices = self.list()
        for device in devices['device']:
             result.append(device)
        return result

    def turnOn(self, id):
        response = self.httprequest.request('device/turnOn', {"id": id})
        return response

    def turnOff(self, id):
        response = self.httprequest.request('device/turnOff', {"id": id})
        return response
