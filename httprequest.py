import time
import json
import httplib
from urllib import urlencode
from oauth.oauth import OAuthConsumer, OAuthRequest, OAuthSignatureMethod_HMAC_SHA1, OAuthToken

class HTTPRequest():
    def __init__(self, config):
        self.config = config

    # Does the HTTP request to telldus. Copied from http://developer.telldus.com/browser/examples/python/live/tdtool/tdtool.py
    def request(self, method, params):
        consumer = OAuthConsumer(self.config['tellstick']['public_key'], self.config['tellstick']['private_key'])
        token = OAuthToken(self.config['tellstick']['token'], self.config['tellstick']['token_secret'])

        oauth_request = OAuthRequest.from_consumer_and_token(consumer, token=token, http_method='GET', http_url="http://api.telldus.com/json/" + method, parameters=params)
        oauth_request.sign_request(OAuthSignatureMethod_HMAC_SHA1(), consumer, token)
        headers = oauth_request.to_header()
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        conn = httplib.HTTPConnection("api.telldus.com:80")
        conn.request('GET', "/json/" + method + "?" + urlencode(params, True).replace('+', '%20'), headers=headers)

        response = conn.getresponse()
        return json.load(response)

