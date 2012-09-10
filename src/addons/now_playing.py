# -*- coding: utf8 -*-

import os, dbus, subprocess, socket
from lib import common

class Now_Playing():
    """
    Let's spam all over !listening! :)
    
    This class parsing current track metadata from specified player. After that it
    sending to main thread, where spam_music() replacing pseudowords with medatada
    and creates new post dialog.
    
    Parameters:
    @player - current player
    @player_string - player string
    """
    def __init__(self, settings):
        self.settings = settings

        # Defining known player list
        players = ["MPD", "Clementine", "Exaile", "DeaDBeeF"]
        needs_settings = ["MPD"]
        players.sort()
        
        # Set global variable (accessible thru 'common' module)
        # for filling a combobox in settings
        common.set_global_parameter("players", players)
        common.set_global_parameter("players_needs_settings", needs_settings)
        
        print "'Now Playing' initialization ok"
        
    def get_music_info(self, player):
        """
        Primary function. Here is deciding what player to use, depending on
        "player" parameter.
        """
        if player == "MPD":
            return self.get_mpd_song()
        elif player == "Clementine":
            return self.get_clementine_song()
        elif player == "Exaile":
            return self.get_exaile_song()
        elif player == "DeaDBeeF":
            return self.get_deadbeef_song()
    
    def get_clementine_song(self):
        """
        Getting data from clementine
        """
        track_data = {}
        try:
            try:
                session_bus = dbus.SessionBus()
                player = session_bus.get_object('org.mpris.clementine', '/Player')
                iface = dbus.Interface(player, dbus_interface='org.freedesktop.MediaPlayer')
                metadata = iface.GetMetadata()
            except:
                return "not-running"
        
            # Making dict with track data
            track_data["condition"] = "OK"
            track_data["artist"] = metadata["artist"][2:]
            track_data["trackname"] = metadata["title"]
            track_data["album"] = metadata["album"]
            return track_data
        except:
            track_data["condition"] = "FAIL"
            return track_data
            

    def get_mpd_song(self):
        """
        Getting data from mpd
        """            
        track_data = {}
        try:
            print "Getting music info from MPD, running on '{0}:{1}'...".format(self.settings["mpd_host"], self.settings["mpd_port"])
            #command = """mpc --format "[[%artist%<><>%title%<><>%album%]]""".split(" ")
            #p = subprocess.Popen(command, stdout=subprocess.PIPE)
            #data = p.communicate()[0].split("\n")[0]
            
            def get_info():
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((str(self.settings["mpd_host"]), int(self.settings["mpd_port"])))
                s.send("currentsong\n")
            
                data = s.recv(1000)
                s.send("close\n")
                s.close()
                return data
            
            data = get_info()
            while True:
                if "Id" not in data:
                    data = get_info()
                else:
                    break
            
            data = data.split("\n")
        
            # Making dict with track data
            track_data["condition"] = "OK"
            for item in data:
                index = data.index(item)
                if "Artist" in item:
                    track_data["artist"] = data[index][8:]
                elif "Title" in item:
                    track_data["trackname"] = data[index][7:]
                elif "Album" in item:
                    track_data["album"] = data[index][7:]
            return track_data
        except:
            track_data["condition"] = "FAIL"
            return track_data
 
    def get_exaile_song(self):
        """
        Getting data from exaile
        """
        track_data = {}
        
        try:
            session_bus = dbus.SessionBus()
            player = session_bus.get_object("org.exaile.Exaile","/org/exaile/Exaile")
            iface = dbus.Interface(player, "org.exaile.Exaile")
        except:
            return "not-running"
        
        if iface.IsPlaying:
            # Making dict with track data
            track_data["condition"] = "OK"
            track_data["artist"] = iface.GetTrackAttr("artist")
            track_data["trackname"] = iface.GetTrackAttr("title")
            track_data["album"] = iface.GetTrackAttr("album")
            return track_data

    def get_deadbeef_song(self):
        """
        Getting data from DeaDBeeF
        """
        track_data = {}
        
        try:        
            command = "deadbeef --nowplaying %a\<\>\<\>%t\<\>\<\>%b".split(" ")
            p = subprocess.Popen(command, stdout=subprocess.PIPE)
            data = p.communicate()[0]
            data = data.split("\<\>\<\>")
            if "nothing" in data:
                return "not-running"
        except:
            return "not-running"
        
        track_data["condition"] = "OK"
        track_data["artist"] = data[0]
        track_data["trackname"] = data[1]
        track_data["album"] = data[2]
        return track_data
            
        
