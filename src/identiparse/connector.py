# -*- coding: utf8 -*-

import os, sys, urllib2, base64, json
from urllib import urlencode

class Requester():
    """
    Requester - an uberclass. The most important part ever written.
    
    Requiesting data from specified server.
    
    All data retrieved in JSON format for easy parsing.
    
    Parameters:
    @username - username
    @password - password
    @realm - statusnet script address
    @secure_state - "Use secure connection?" checkbox status
    @callback - callback for exceptions
    """
    def __init__(self, username, password, realm, secure_state, callback):
        """
        INIT ME COMPLETELY! :)
        """
        # Checking secure state. Secure state = checkstatus of
        # "Use secure connection?" checkbox in settings
        if secure_state == "1":
            API_URL = "https://" + realm
        else:
            API_URL = "http://" + realm
        
        # Redefining variables for class-wide usage
        self._username = str(username)
        self._password = str(password)
        self._api_url = str(API_URL)
        self.callback = callback

        # Pass nomer uno - checking credentials validity
        request = urllib2.Request(self._api_url + "account/verify_credentials.json")
        base64string = base64.encodestring('%s:%s' % (self._username, self._password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        try:
            result = urllib2.urlopen(request)
            # Everything ok. YAY! ^_^
            print "Credentials OK"
        except urllib2.HTTPError, e:
            # Crap. You've mistyped something!
            self.callback("bad_credentials")
            
    def defavoritize_dent(self, dent_id, version):
        """
        Defavoritize dent request former and sender
        Opts:
        
        @dent_id - dent id to defavoritize
        @version - app version
        """
        request = urllib2.Request(self._api_url + "/favorites/destroy/{0}.json".format(dent_id))
        base64string = base64.encodestring('%s:%s' % (self._username, self._password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header('User-agent', 'QTDenter (http://www.github.com/pztrn/qtdenter)')
        print "DEFAVORITIZE REQUEST FORMED"
        
        try:
            result = urllib2.urlopen(request, "")
            result = result.read()
        
            print "DEFAVORITIZED"
            return json.loads(result)
        except:
            self.callback("failed_to_defavoritize")
            
    def favoritize_dent(self, dent_id, version):
        """
        Favoritize dent request former and sender
        Opts:
        
        @dent_id - dent id to favoritize
        @version - app version
        """
        request = urllib2.Request(self._api_url + "/favorites/create/{0}.json".format(dent_id))
        base64string = base64.encodestring('%s:%s' % (self._username, self._password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header('User-agent', 'QTDenter (http://www.github.com/pztrn/qtdenter)')
        print "FAVORITIZE REQUEST FORMED"
        
        #try:
        result = urllib2.urlopen(request, "")
        result = result.read()
        
        print "FAVORITIZED"
        return json.loads(result)
        #except:
        #    self.callback("bad_credentials")
            
    def post_dent(self, text, version):
        """
        Post dent request former and sender
        Opts:
        
        @text - dent text to post
        @version - app version
        """
        data = {"status": text, "source": "QTDenter"}
        encoded_data = urlencode(data)
        print "DATA ENCODED"
        
        request = urllib2.Request(self._api_url + "statuses/update.json", encoded_data)
        base64string = base64.encodestring('%s:%s' % (self._username, self._password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header('User-agent', 'QTDenter (http://www.github.com/pztrn/qtdenter)')
        print "REQUEST FORMED"
        
        try:
            result = urllib2.urlopen(request, encoded_data)
            result = result.read()
        
            return json.loads(result)
        except:
            self.callback("bad_credentials")
        
    def delete_dent(self, dent_id):
        """
        Delete dent request former and sender
        Opts:
        
        @dent_id - dent id to delete
        """
        data = {"id": dent_id}
        encoded_data = urlencode(data)
        print "DATA ENCODED"
        
        request = urllib2.Request(self._api_url + "statuses/destroy.json".format(dent_id), encoded_data)
        base64string = base64.encodestring('%s:%s' % (self._username, self._password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        print "REQUEST FORMED"
        
        try:
            result = urllib2.urlopen(request)
            result = result.read()
        
            return "OK"
        except:
            self.callback("bad_credentials")
        
    def redent_dent(self, dent_id, version):
        """
        Redent dent request former and sender
        Opts:
        
        @dent_id - dent id to redent
        @version - app version
        """
        data = {"id": dent_id}
        encoded_data = urlencode(data)
        print "DATA ENCODED"
        
        request = urllib2.Request(self._api_url + "statuses/retweet/{0}.json".format(dent_id), encoded_data)
        base64string = base64.encodestring('%s:%s' % (self._username, self._password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header('User-agent', 'QTDenter (http://www.github.com/pztrn/qtdenter)')
        print "REDENT REQUEST FORMED"
        
        try:
            result = urllib2.urlopen(request, encoded_data)
            result = result.read()
        
            return json.loads(result)
        except:
            return "FAIL"
        
    def send_direct_message(self, data, version):
        """
        Send direct message request former and sender
        Opts:
        
        @data - post data (message, nickname)
        @version - app version
        """
        data={"text": data["message"], "screen_name": data["nickname"], "source": "QTDenter"}
        encoded_data = urlencode(data)
        print "DATA ENCODED"
        
        request = urllib2.Request(self._api_url + "direct_messages/new.json", encoded_data)
        base64string = base64.encodestring('%s:%s' % (self._username, self._password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header('User-agent', 'QTDenter (http://www.github.com/pztrn/qtdenter)')
        print "REQUEST FORMED"
        
        try:
            result = urllib2.urlopen(request, encoded_data)
            result = result.read()
        
            return json.loads(result)
        except:
            self.callback("bad_credentials")
        
    def send_reply(self, data, version):
        """
        Send reply request former and sender
        Opts:
        
        @data - reply data (text, id of dent to which we send reply)
        @version - app version
        """
        data={"status": data["text"],"source": "QTDenter", "in_reply_to_status_id": data["reply_to_id"]}
        encoded_data = urlencode(data)
        print "DATA ENCODED"
        
        request = urllib2.Request(self._api_url + "statuses/update.json", encoded_data)
        base64string = base64.encodestring('%s:%s' % (self._username, self._password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header('User-agent', 'QTDenter (http://www.github.com/pztrn/qtdenter)')
        print "REQUEST FORMED"
        
        try:
            result = urllib2.urlopen(request, encoded_data)
            result = result.read()
        
            return json.loads(result)
        except:
            self.callback("bad_credentials")

    def get_home_timeline(self, opts):
        """
        Get home timeline request former and sender
        Opts:
        
        @opts - some neccessary options (username, count)
        """
        url = self._api_url + "statuses/home_timeline/{0}.json?".format(opts["name"])
        if opts:
            if opts["count"]:
                url = url + "count={0}&".format(opts["count"])
                
        request = urllib2.Request(url)
        base64string = base64.encodestring('%s:%s' % (self._username, self._password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        try:
            result = urllib2.urlopen(request)
            data = json.loads(result.read())
            
            return data
        except urllib2.HTTPError, e:
            self.callback("bad_credentials")

    def get_mentions(self, opts):
        """
        Get mentions request former and sender
        Opts:
        
        @opts - some neccessary options (username, count)
        """
        url = self._api_url + "statuses/mentions/{0}.json?".format(opts["name"])
        if opts:
            if opts["count"]:
                url = url + "count={0}&".format(opts["count"])
        
        request = urllib2.Request(url)
        base64string = base64.encodestring('%s:%s' % (self._username, self._password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        try:
            result = urllib2.urlopen(request)
            data = json.loads(result.read())

            return data
        except urllib2.HTTPError, e:
            self.callback("bad_credentials")

    def get_direct_messages(self, opts):
        """
        Get direct messages request former and sender
        Opts:
        
        @opts - some neccessary options (username, count)
        """
        url = self._api_url + "direct_messages.json?".format(opts["name"])
        if opts:
            if opts["count"]:
                url = url + "count={0}&".format(opts["count"])
        
        request = urllib2.Request(url)
        base64string = base64.encodestring('%s:%s' % (self._username, self._password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        try:
            result = urllib2.urlopen(request)
            data = json.loads(result.read())

            return data
        except urllib2.HTTPError, e:
            self.callback("bad_credentials")
            
    def get_conversation(self, conversation_id):
        """
        Get conversation request former and sender
        Opts:
        
        @conversation_id - conversation id to retrieve
        
        Posts count forced to 1000, to get full conversation. I do not believe
        there is any conversations on statusnetz, that comments count exceeds 1000 :)
        """
        url = self._api_url + "/statusnet/conversation/{0}.json?count=1000".format(conversation_id)
        
        request = urllib2.Request(url)
        base64string = base64.encodestring('%s:%s' % (self._username, self._password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        try:
            result = urllib2.urlopen(request)
            data = json.loads(result.read())

            return data
        except urllib2.HTTPError, e:
            self.callback("bad_credentials")

    def get_server_config(self, type):
        """
        Get sever config request former and sender
        Opts:
        
        @type - type of config to retrieve. There are 2 types:
          * config - full config
          * version - statusnet script version
        """
        if type == "config":
            url = self._api_url + "statusnet/config.json"
        elif type == "version":
            url = self._api_url + "statusnet/version.json"
        
        request = urllib2.Request(url)
        base64string = base64.encodestring('%s:%s' % (self._username, self._password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        try:
            result = urllib2.urlopen(request)
            data = json.loads(result.read())

            return data
        except urllib2.HTTPError, e:
            self.callback("bad_credentials")
