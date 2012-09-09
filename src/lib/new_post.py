# -*- coding: utf8 -*-

import os
from PyQt4.QtCore import QString, Qt
from PyQt4.QtGui import QDialog, QPushButton
from ui import NewPost

class New_Post(QDialog):
    def __init__(self, messageLength, parameters, callback, parent = None):
        QDialog.__init__(self, parent)
        self.ui = NewPost.Ui_Dialog()
        self.ui.setupUi(self)

        self.messageLength = int(messageLength)
        self.reply = False
        self.direct = False
        self.callback = callback
        
        self.params = parameters
        if self.params["type"] == "reply":
            self.ui.label.setText("Replying to {0}:<br />{1}".format(self.params["nickname"], self.params["text"]))
            self.ui.postData.appendPlainText("@{0} ".format(self.params["nickname"]))
            self.reply = True
        elif self.params["type"] == "direct":
            self.direct = True
        elif self.params["type"] == "insert":
            self.ui.postData.appendPlainText(self.params["text"])
            
        self._messageIsTooLong = 0

        self.ui.postData.textChanged.connect(self.countCharacters)
        self.ui.cancelButton.clicked.connect(self.close)
        
        if self.direct:
            self.ui.label.setText("Enter nickname of person to whom send direct message like:\n@@username")
            self.ui.postButton.clicked.connect(self.post_direct_message)
        else:
            self.ui.postButton.clicked.connect(self.postData)

    def countCharacters(self):
        self.textLenght = len(self.ui.postData.toPlainText())
        self.enteredSymbols = self.messageLength - self.textLenght
        if not self.messageLength == 0:
            if self.enteredSymbols < 0:
                self.ui.symbolCount.setText("<div style='color:red; font-weight:bold;'>" + str(self.enteredSymbols) + "/" + str(self.messageLength) + "</div>")
                self._messageIsTooLong = 1
            else:
                self.ui.symbolCount.setText(str(self.enteredSymbols) + "/" + str(self.messageLength))
                self._messageIsTooLong = 0
        else:
            self.ui.symbolCount.setText("<div style='font-weight:bold;'>No characters limit</div>")

    def postData(self):
        if self._messageIsTooLong == 1:
            QMessageBox.critical(self, self.tr("New post - Message is too long"), self.tr("Message you entered is too long. Maximum message length is {0} symbols, you entered {1} symbols.").format(str(self.messageLength), str(self.textLenght)))
        else:
            if self.reply:
                data = {}
                data["text"] = self.ui.postData.toPlainText()
                data["reply_to_id"] = self.params["reply_to_id"]
                self.callback("send_reply", data)
            else:
                self.callback("post_data", str(QString.toUtf8(self.ui.postData.toPlainText())))
                
            self.close()
                
    def post_direct_message(self):
        message = str(QString.toUtf8(self.ui.postData.toPlainText()))
        data = {}
        data["nickname"] = message.split(" ")[0][2:]
        data["message"] = message.split(" ")[1]
        
        self.callback("send_direct_message", data)

        self.close()
