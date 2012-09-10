# -*- coding: utf8 -*-

import os
from PyQt4.QtCore import QString
from PyQt4.QtGui import QDialog
from ui import Settings
from lib import common

class Options_Dialog(QDialog):
    """
    Options dialog class. Nuff said.
    
    Parameters:
    @settings - QTDenter settings
    @callback - callback for settings transmission to main thread
    """
    def __init__(self, settings, callback, parent = None):
        QDialog.__init__(self, parent)
        self.ui = Settings.Ui_Dialog()
        self.ui.setupUi(self)

        self.settings = settings
        self.callback = callback
        self.ui.accountName.setText(self.settings["user"])
        self.ui.serverName.setText(self.settings["server"])
        self.ui.password.setText(self.settings["password"])
        if self.settings["useSecureConnection"] == "1":
            self.ui.useSecureConnectionCheckbox.setCheckState(2)
        else:
            self.ui.useSecureConnectionCheckbox.setCheckState(0)
        if self.settings["deleteAllFromCacheOnExit"] == "1":
            self.ui.removePostsOnExitCheckbox.setCheckState(2)
        else:
            self.ui.removePostsOnExitCheckbox.setCheckState(0)
        try:
            self.ui.updateInterval.setValue(int(self.settings["updateInterval"]))
        except:
            self.ui.updateInterval.setValue(10)
            
        if self.settings["remember_last_dent_id"] == "1":
            self.ui.remember_last_dentid.setCheckState(2)
            self.ui.dents_quantity.setEnabled(False)
        else:
            self.ui.remember_last_dentid.setCheckState(0)
            self.ui.dents_quantity.setEnabled(True)
            
        self.ui.dents_quantity.setText(self.settings["fetch_on_startup"])
        
        self.ui.okButton.clicked.connect(self.transmitSettings)
        self.ui.cancelButton.clicked.connect(self.close)
        
        self.ui.remember_last_dentid.stateChanged.connect(self.changing_rld_state)
        
        # Now Playing
        for item in common.GLOBAL_PARMS["players"]:
            self.ui.players_list.addItem(item)
        
        try:
            index = common.GLOBAL_PARMS["players"].index(self.settings["player"])
            self.ui.players_list.setCurrentIndex(index)
            self.ui.player_string.appendPlainText(self.settings["player_string"])
            self.players_needs_settings = common.GLOBAL_PARMS["players_needs_settings"]
            
            if self.settings["player"] != "MPD":
                self.ui.additional_settings_wrap.hide()
            try:
                self.ui.mpdhost.setText(self.settings["mpd_host"])
                self.ui.mpdport.setText(self.settings["mpd_port"])
            except:
                pass
                
        except:
            # No config values, passing
            pass
            
        self.ui.players_list.currentIndexChanged.connect(self.player_changed)
        
    def player_changed(self):
        if self.ui.players_list.currentText() not in self.players_needs_settings:
            self.ui.additional_settings_wrap.hide()
        else:
            self.ui.additional_settings_wrap.show()
            
    def changing_rld_state(self):
        """
        Changing state of dents_quantity widget depending on
        remember_last_dent_id checkbox.
        """
        if self.ui.remember_last_dentid.checkState() == 2:
            self.ui.dents_quantity.setEnabled(False)
        else:
            self.ui.dents_quantity.setEnabled(True)       

    def transmitSettings(self):
        """
        Transmitting new settings to main thread.
        """
        settingslist = []
        settingslist.append(str(self.ui.accountName.text()))
        settingslist.append(str(self.ui.password.text()))
        settingslist.append(str(self.ui.serverName.text()))
        if self.ui.useSecureConnectionCheckbox.isChecked():
            settingslist.append(str(1))
        else:
            settingslist.append(str(0))
        if self.ui.removePostsOnExitCheckbox.isChecked():
            settingslist.append(str(1))
        else:
            settingslist.append(str(0))
        settingslist.append(self.ui.updateInterval.value())
        if self.ui.remember_last_dentid.isChecked():
            settingslist.append(str(1))
        else:
            settingslist.append(str(0))
        settingslist.append(str(self.ui.dents_quantity.text()))
        settingslist.append(str(self.ui.players_list.currentText()))
        settingslist.append(str(self.ui.player_string.toPlainText()))
        settingslist.append(str(self.ui.mpdhost.text()))
        settingslist.append(str(self.ui.mpdport.text()))

        self.callback(settingslist)
        self.close()
