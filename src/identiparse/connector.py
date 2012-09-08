# -*- coding: utf8 -*-

import os, sys, urllib2, base64, json
from urllib import urlencode

class Requester():
    def __init__(self, username, password, realm, secure_state):
        if secure_state == "1":
            API_URL = "https://" + realm
        else:
            API_URL = "http://" + realm
        
        self._username = str(username)
        self._password = str(password)
        self._api_url = str(API_URL)

        request = urllib2.Request(self._api_url + "account/verify_credentials.json")
        base64string = base64.encodestring('%s:%s' % (self._username, self._password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        try:
            result = urllib2.urlopen(request)
            print "Credentials OK"
        except urllib2.HTTPError, e:
            return e
            
    def post_dent(self, text, version):
        data = {"status": text, "source": "QTDenter"}
        encoded_data = urlencode(data)
        print "DATA ENCODED"
        
        request = urllib2.Request(self._api_url + "statuses/update.json", encoded_data)
        base64string = base64.encodestring('%s:%s' % (self._username, self._password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header('User-agent', 'QTDenter ' + version + ' (http://www.github.com/pztrn/qtdenter)')
        print "REQUEST FORMED"
        
        result = urllib2.urlopen(request, encoded_data)
        result = result.read()
        
        return json.loads(result)

    def get_home_timeline(self):
        print "START"
        request = urllib2.Request(self._api_url + "statuses/home_timeline.json")
        base64string = base64.encodestring('%s:%s' % (self._username, self._password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        try:
            result = urllib2.urlopen(request)
            data = json.loads(result.read())
            print "DATA RECEIVED"

            return data
        except urllib2.HTTPError, e:
            return e
