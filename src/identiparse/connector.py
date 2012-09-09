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
            
    def defavoritize_dent(self, dent_id, version):
        request = urllib2.Request(self._api_url + "/favorites/destroy/{0}.json".format(dent_id))
        base64string = base64.encodestring('%s:%s' % (self._username, self._password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header('User-agent', 'QTDenter ' + version + ' (http://www.github.com/pztrn/qtdenter)')
        print "DEFAVORITIZE REQUEST FORMED"
        
        try:
            result = urllib2.urlopen(request, "")
            result = result.read()
        
            print "DEFAVORITIZED"
            return json.loads(result)
        except:
            return "FAIL"
            
    def favoritize_dent(self, dent_id, version):
        request = urllib2.Request(self._api_url + "/favorites/create/{0}.json".format(dent_id))
        base64string = base64.encodestring('%s:%s' % (self._username, self._password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header('User-agent', 'QTDenter ' + version + ' (http://www.github.com/pztrn/qtdenter)')
        print "FAVORITIZE REQUEST FORMED"
        
        try:
            result = urllib2.urlopen(request, "")
            result = result.read()
        
            print "FAVORITIZED"
            return json.loads(result)
        except:
            return "FAIL"
            
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
        
    def redent_dent(self, dent_id, version):
        data = {"id": dent_id}
        encoded_data = urlencode(data)
        print "DATA ENCODED"
        
        request = urllib2.Request(self._api_url + "statuses/retweet/{0}.json".format(dent_id), encoded_data)
        base64string = base64.encodestring('%s:%s' % (self._username, self._password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header('User-agent', 'QTDenter ' + version + ' (http://www.github.com/pztrn/qtdenter)')
        print "REQUEST FORMED"
        
        result = urllib2.urlopen(request, encoded_data)
        result = result.read()
        
        return json.loads(result)
        
    def send_reply(self, data, version):
        data={"status": data["text"],"source": "QTDenter", "in_reply_to_status_id": data["reply_to_id"]}
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

    def get_home_timeline(self, opts):
        url = self._api_url + "statuses/home_timeline/{0}.json?".format(opts["name"])
        if opts:
            if opts["count"]:
                url = url + "count={0}&".format(opts["count"])
            if opts["from_id"]:
                url = url + "since_id={0}&".format(opts["from_id"])
                
        request = urllib2.Request(url)
        base64string = base64.encodestring('%s:%s' % (self._username, self._password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        try:
            result = urllib2.urlopen(request)
            data = json.loads(result.read())

            return data
        except urllib2.HTTPError, e:
            return e

    def get_mentions(self, opts):
        url = self._api_url + "statuses/mentions/{0}.json?".format(opts["name"])
        if opts:
            if opts["count"]:
                url = url + "count={0}&".format(opts["count"])
            if opts["from_id"]:
                url = url + "since_id={0}&".format(opts["from_id"])
        
        request = urllib2.Request(url)
        base64string = base64.encodestring('%s:%s' % (self._username, self._password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        try:
            result = urllib2.urlopen(request)
            data = json.loads(result.read())

            return data
        except urllib2.HTTPError, e:
            return e

    def get_direct_messages(self, opts):
        url = self._api_url + "direct_messages.json?".format(opts["name"])
        if opts:
            if opts["count"]:
                url = url + "count={0}&".format(opts["count"])
            if opts["from_id"]:
                url = url + "since_id={0}&".format(opts["from_id"])
        
        request = urllib2.Request(url)
        base64string = base64.encodestring('%s:%s' % (self._username, self._password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        try:
            result = urllib2.urlopen(request)
            data = json.loads(result.read())

            return data
        except urllib2.HTTPError, e:
            return e
