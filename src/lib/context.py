# -*- coding: utf8 -*-

import os
from PyQt4.QtCore import QString, Qt
from PyQt4.QtGui import QDialog, QPushButton, QMessageBox
from ui import Context as cg
from lib import list_item, list_handler, new_post

class Context(QDialog):
    def __init__(self, auth, conversation_id, settings, version, parent = None):
        QDialog.__init__(self, parent)
        self.ui = cg.Ui_Dialog()
        self.ui.setupUi(self)
        
        self.settings = settings
        self.auth = auth
        self.VERSION = version
        
        self.ui.context.setSortingEnabled(True)
        self.ui.context.sortByColumn(2, Qt.DescendingOrder)
        for column in range(2, 5):
            self.ui.context.setColumnHidden(column, True)
        self.ui.context.setColumnWidth(0, 65)
        self.ui.context.itemActivated.connect(self.reply_to_dent)

        conversation = self.auth.get_conversation(conversation_id)
        
        self.list_handler = list_handler.List_Handler(self.callback)
        
        self.list_item = list_item.list_item()
        self.list_handler.add_data("conversation", conversation)
        
    def callback(self, list_type, data):
        if list_type == "end":
            pass
        else:
            self.add_dent(data)
        
    def add_dent(self, data):
        item_data = self.list_item.process_item(data)

        item = item_data[0]
        avatar_widget = item_data[1]
        post_widget = item_data[2]
        
        destroy_button = avatar_widget.findChild(QPushButton, "destroy_button_" + str(data["id"]))
        dentid_button = post_widget.findChild(QPushButton, "dentid_button_" + str(data["id"]))
        redent_button = post_widget.findChild(QPushButton, "redent_button_" + str(data["id"]))
        like_button = post_widget.findChild(QPushButton, "like_button_" + str(data["id"]))
        context_button = post_widget.findChild(QPushButton, "context_button_" + str(data["conversation_id"]))
        destroy_button.clicked.connect(self.delete_dent)
        dentid_button.clicked.connect(self.go_to_dent)
        redent_button.clicked.connect(self.redent_dent)
        like_button.clicked.connect(self.like_dent)
        if data["in_reply_to_screen_name"]:
            context_button.hide()
        
        if not data["nickname"] == self.settings["user"]:
            destroy_button.hide()
        
        self.ui.context.addTopLevelItem(item)
        self.ui.context.setItemWidget(item, 0, avatar_widget)
        self.ui.context.setItemWidget(item, 1, post_widget)

    def like_dent(self):
        try:
            item = self.ui.context.currentItem()
            dent_id = self.ui.context.currentItem().text(2).split(":")[0]
            if self.ui.context.currentItem().text(3) == "not":
                data = self.auth.favoritize_dent(dent_id, self.VERSION)
                if data != "FAIL":
                    btn = self.ui.context.findChild(QPushButton, "like_button_" + dent_id)
                    self.ui.context.currentItem().setText(3, "favorited")
                    btn.setText("X")
            else:
                data = self.auth.defavoritize_dent(dent_id, self.VERSION)
                if data != "FAIL":
                    btn = self.ui.context.findChild(QPushButton, "like_button_" + dent_id)
                    btn.findChild(QPushButton, "X")
                    self.ui.context.currentItem().setText(3, "not")
                    btn.setText(u"\u2665")
        except:
            QMessageBox.critical(self, "QTDenter - Choose dent first!", "You have to choose dent")
        
    def redent_dent(self):
        try:
            dent_id = self.ui.context.currentItem().text(2).split(":")[0]
            self.auth.redent_dent(dent_id, self.VERSION)
        except:
            QMessageBox.critical(self, "QTDenter - Choose dent first!", "You have to choose dent")
        
    def delete_dent(self):
        try:
            dent_id = self.ui.context.currentItem().text(2).split(":")[0]
            data = self.auth.delete_dent(dent_id)
            if data == "OK":
                index = self.ui.context.indexOfTopLevelItem(self.ui.context.currentItem())
                self.ui.context.takeTopLevelItem(index)
        except:
            QMessageBox.critical(self, "QTDenter - Choose dent first!", "You have to choose dent")
            
    def reply_to_dent(self):
        try:
            dent_id = self.ui.context.currentItem().text(2).split(":")[0]
            to_username = self.ui.context.currentItem().text(2).split(":")[1]
            dent_text = self.ui.context.currentItem().text(4)
            params = {}
            params["type"] = "reply"
            params["reply_to_id"] = dent_id
            params["nickname"] = to_username
            params["text"] = dent_text
            newpostD = new_post.New_Post(self.settings["messageLength"], params, self.new_post_callback)
            newpostD.exec_()
        except:
            QMessageBox.critical(self, "QTDenter - Choose dent first!", "You have to choose dent")

    def go_to_dent(self):
        try:
            item = self.ui.context.currentItem()
            dent_id = self.ui.context.currentItem().text(2).split(":")[0]
            server_address = self.settings["server"]
            if self.settings["useSecureConnection"] == 1:
                server_address = "https://" + server_address
            else:
                server_address = "http://" + server_address
        
            QDesktopServices.openUrl(QUrl(server_address + "/notice/" + dent_id))
        except:
            QMessageBox.critical(self, "QTDenter - Choose dent first!", "You have to choose dent")
            
    def post_status(self, data):
        data = self.auth.post_dent(data, self.VERSION)
        self.list_handler.add_data("home", [data])
        
    def send_reply(self, data):
        data = self.auth.send_reply(data, self.VERSION)
        self.list_handler.add_data("home", [data])
            
    def new_post_callback(self, type, data):
        if type == "send_reply":
            self.send_reply(data)
            
            
