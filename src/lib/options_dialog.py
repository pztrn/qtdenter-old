# -*- coding: utf8 -*-

import os
from PyQt4.QtCore import QString
from PyQt4.QtGui import QDialog
from ui import Settings
from lib import common

class Options_Dialog(QDialog):
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
        except:
            # No config values, passing
            pass
            
    def changing_rld_state(self):
        if self.ui.remember_last_dentid.checkState() == 2:
            self.ui.dents_quantity.setEnabled(False)
        else:
            self.ui.dents_quantity.setEnabled(True)       

    def transmitSettings(self):
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

        self.callback(settingslist)
        self.close()
