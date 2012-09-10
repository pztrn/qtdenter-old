# -*- coding: utf8 -*-

import os
from PyQt4.QtCore import QString
from PyQt4.QtGui import QDialog
from ui import Stat

class Information_Dialog(QDialog):
    """
    Information dialog. Shows server information, like statusnet version and
    dent lenght limit.
    
    Parameters:
    @server_data - statusnet config
    @server_version - statusnet version
    @version - QTDenter version
    """
    def __init__(self, server_data, server_version, version, parent = None):
        QDialog.__init__(self, parent)
        self.ui = Stat.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.closeDialog.clicked.connect(self.close)

        self.ui.appVer.setText(version)

        self.ui.server_name.setText(server_data["site"]["name"])
        self.ui.server_address.setText(server_data["site"]["server"])
        self.ui.sn_version.setText(server_version)
        self.ui.dent_size.setText(server_data["site"]["textlimit"] + " characters")
        if server_data["attachments"]["uploads"]:
            upload_status = "Enabled"
            file_size = str(server_data["attachments"]["file_quota"] / 1024) + " KBytes"
            self.ui.max_file_size.setText(str(file_size))
        else:
            upload_status = "Disabled"
            self.ui.max_file_size.setText("Unknown")
        self.ui.uploads_status.setText(upload_status)
        
        server_type = ""
        
        if server_data["site"]["closed"] == "1":
            server_type += "Registrations closed"
        if server_data["site"]["inviteonly"] == "1":
            server_type += ", Inviation only"
        if server_data["site"]["private"] == "1":
            server_type += ", No anonymous reading"
            
        self.ui.server_type.setText(server_type)
