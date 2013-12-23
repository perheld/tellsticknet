import json
import time
import httplib
import datetime
from urllib import urlencode
import gdata.spreadsheet.service
from oauth.oauth import OAuthConsumer, OAuthRequest, OAuthSignatureMethod_HMAC_SHA1, OAuthToken


# Does the HTTP request to telldus. Copied from http://developer.telldus.com/browser/examples/python/live/tdtool/tdtool.py
def httprequest(config, method, params):
    consumer = OAuthConsumer(config['public_key'], config['private_key'])
    token = OAuthToken(config['token'], config['token_secret'])

    oauth_request = OAuthRequest.from_consumer_and_token(consumer, token=token, http_method='GET', http_url="http://api.telldus.com/json/" + method, parameters=params)
    oauth_request.sign_request(OAuthSignatureMethod_HMAC_SHA1(), consumer, token)
    headers = oauth_request.to_header()
    headers['Content-Type'] = 'application/x-www-form-urlencoded'

    conn = httplib.HTTPConnection("api.telldus.com:80")
    conn.request('GET', "/json/" + method + "?" + urlencode(params, True).replace('+', '%20'), headers=headers)

    response = conn.getresponse()
    return json.load(response)


# Gets a list of sensors connected to the system
def listsensors(config):
    response = httprequest(config, 'sensors/list', {})
    return response


# Reads out data from one sensor given its id
def readsensor(config, sensorid):
    response = httprequest(config, 'sensor/info', {"id": sensorid})
    return response['data']


# Reads all sensors connected to the system and returns their values as a dict
def readallsensors(config):
    sensorresult = {}
    sensors = listsensors(config)

    for sensor in sensors['sensor']:
        sensorresult[sensor['name']] = {}
        sensordata = readsensor(config, sensor['id'])
        for data in sensordata:
            sensorresult[sensor['name']][data['name']] = data['value']

    return sensorresult


def push_to_google(config, values):
    spreadsheet_key = config['spreadsheet']
    # All spreadsheets have worksheets. I think worksheet #1 by default always
    # has a value of 'od6'
    worksheet_id = 'od6'

    spr_client = gdata.spreadsheet.service.SpreadsheetsService()
    spr_client.email = config['email']
    spr_client.password = config['password']
    spr_client.source = 'Per Held Tellstick temperature exporter'
    spr_client.ProgrammaticLogin()

    # Prepare the dictionary to write
    dict = {}
    dict['timestamp'] = str(datetime.datetime.now())
    dict['temperature'] = str(values['temp']).replace(".", ",")
    dict['humidity'] = str(values['humidity'])

    entry = spr_client.InsertRow(dict, spreadsheet_key, worksheet_id)
    if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
        print dict
    else:
        print "Insert row failed."


def main():
    json_data = open('config.json')
    config = json.load(json_data)
    tellstickconfig = config['tellstick']
    gmailconfig = config['google']

    readout = readallsensors(tellstickconfig)

    # push each sensor read out
    for sensor in readout:
        push_to_google(gmailconfig, readout[sensor])

if __name__ == "__main__":
    main()
