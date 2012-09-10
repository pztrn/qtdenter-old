# -*- coding: utf8 -*-

import os, dbus, subprocess
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
    def __init__(self, player, player_string):
        # Defining known player list
        
        players = ["MPD", "Clementine"]        
        players.sort()
        
        # Set global variable (accessible thru 'common' module)
        # for filling a combobox in settings
        common.set_global_parameter("players", players)
        
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
    
    def get_clementine_song(self):
        """
        Getting data from clementine
        """
        track_data = {}
        try:
            session_bus = dbus.SessionBus()
            player = session_bus.get_object('org.mpris.clementine', '/Player')
            iface = dbus.Interface(player, dbus_interface='org.freedesktop.MediaPlayer')
            metadata = iface.GetMetadata()
        
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
            command = """mpc --format "[[%artist%<><>%title%<><>%album%]]""".split(" ")
            p = subprocess.Popen(command, stdout=subprocess.PIPE)
            data = p.communicate()[0].split("\n")[0]
        
            data = data.split("<><>")
        
            # Making dict with track data
            track_data["condition"] = "OK"
            track_data["artist"] = data[0]
            track_data["trackname"] = data[1]
            track_data["album"] = data[2]
            return track_data
        except:
            track_data["condition"] = "FAIL"
            return track_data
 
