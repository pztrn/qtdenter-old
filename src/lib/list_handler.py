# -*- coding: utf8 -*-

import os, urllib2
from PyQt4.QtCore import QThread, QString
from PyQt4.QtGui import QTreeWidgetItem, QLabel

class List_Handler(QThread):
    """
    This is a "data parser" thread - all retrieved data goes here, parsed,
    reparsed, refining, and sending back to main thread with callback help.
    Callback will decide what to do, depending on list_type.
    
    Parameters:
    @callback - callback for sending parsed data to main thread
    """
    def __init__(self, callback, parent = None):
        QThread.__init__(self, parent)
        
        self.callback = callback
        
    def add_data(self, list_type, data):
        """
        Data parser. Opts:
        
        @list_type - list type (timeline, mentions, direct)
        @data - retrieved data
        """
        for item in data:
            item_data = {}
            item_data["avatar"] = item["user"]["profile_image_url"]
            item_data["nickname"] = item["user"]["screen_name"]
            item_data["text"] = item["statusnet_html"]
            item_data["id"] = item["id"]
            item_data["date"] = item["created_at"]
            if item["source"] == "ostatus":
                item_data["source"] = item["user"]["statusnet_profile_url"].split(":")[1][2:].split("/")[0]
            else:
                item_data["source"] = item["source"]
                
            item_data["in_favorites"] = item["favorited"]
            item_data["in_reply_to_screen_name"] = item["in_reply_to_screen_name"]
            item_data["conversation_id"] = item["statusnet_conversation_id"]
            
            item_data["retweeted"] = False
            if "retweeted_status" in item:
                item_data["retweeted"] = True
            
            self.download_avatar(item["user"]["profile_image_url"], item["user"]["screen_name"])
            
            self.callback(list_type, item_data)
        
        self.callback("end", "")
        
    def download_avatar(self, avatar, name):
        """
        Avatar downloader
        """
        extension = avatar.split(".")[-1:][0]
        avatar_path = os.path.expanduser("~/.local/share/qtdenter/avatars/") + "%s.%s" % (name, extension)
        if not os.path.exists(avatar_path):
            if "secure.gravatar.com" in avatar:
                pass
            else:
                request = urllib2.urlopen(avatar)
                data = request.read()
                f = open(avatar_path, "w")
                f.write(data)
                f.close()
        
                self.callback("home_avatar", name)
        else:
            pass
