# -*- coding: utf8 -*-

import os
from PyQt4.QtCore import QString, Qt, QSignalMapper
from PyQt4.QtGui import QDialog, QPushButton, QMessageBox
from ui import Context_Window as cg
from lib import list_item, list_handler, new_post

class Context(QDialog):
    """
    Context dialog. Responsoble for viewing full thread.
    
    There are a "bug" here - I have to duplicate some functions from main
    module due to architecture fail. I will fix that, soon.
    
    Parameters:
    @auth - connector instance for communication with statusnet installation
    @conversation_id - conversation id. Nuff said.
    @settings - QTDenter settings
    @self.version - QTDenter self.version
    """
    def __init__(self, auth, conversation_id, settings, version, parent = None):
        QDialog.__init__(self, parent)
        self.ui = cg.Ui_Dialog()
        self.ui.setupUi(self)
        
        self.settings = settings
        self.auth = auth
        self.version = version
        
        # Initialize signal mappers for buttons and lists for buttons pointers
        self.context_buttons_mapper = QSignalMapper(self)
        self.context_buttons_list = []
        self.destroy_buttons_mapper = QSignalMapper(self)
        self.destroy_buttons_list = []
        self.redent_buttons_mapper = QSignalMapper(self)
        self.redent_buttons_list = []
        self.like_buttons_mapper = QSignalMapper(self)
        self.like_buttons_list = []
        self.dentid_buttons_mapper = QSignalMapper(self)
        self.dentid_buttons_list = []
        
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
        self.connect_buttons()
        
    def connect_buttons(self):
        print "Connecting buttons"
        for item in self.context_buttons_list:
            self.context_buttons_mapper.setMapping(item[0], item[1])
            item[0].clicked.connect(self.context_buttons_mapper.map)
            
        for item in self.destroy_buttons_list:
            self.destroy_buttons_mapper.setMapping(item[0], item[1])
            item[0].clicked.connect(self.destroy_buttons_mapper.map)
            
        for item in self.redent_buttons_list:
            self.redent_buttons_mapper.setMapping(item[0], item[1])
            item[0].clicked.connect(self.redent_buttons_mapper.map)
            
        for item in self.like_buttons_list:
            self.like_buttons_mapper.setMapping(item[0], item[1])
            item[0].clicked.connect(self.like_buttons_mapper.map)
            
        for item in self.dentid_buttons_list:
            self.dentid_buttons_mapper.setMapping(item[0], item[1])
            item[0].clicked.connect(self.dentid_buttons_mapper.map)
            
        self.destroy_buttons_mapper.mapped.connect(self.delete_dent)
        self.redent_buttons_mapper.mapped.connect(self.redent_dent)
        self.like_buttons_mapper.mapped.connect(self.like_dent)
        self.dentid_buttons_mapper.mapped.connect(self.go_to_dent)
        
    def callback(self, list_type, data):
        """
        List callback
        """
        if list_type == "end":
            pass
        else:
            self.add_dent(data)
        
    def add_dent(self, data):
        """
        Add dent to list widget
        """
        item_data = self.list_item.process_item(data, self.settings["last_dent_id"])

        item = item_data[0]
        avatar_widget = item_data[1]
        post_widget = item_data[2]
        
        destroy_button = avatar_widget.findChild(QPushButton, "destroy_button_" + str(data["id"]))
        dentid_button = post_widget.findChild(QPushButton, "dentid_button_" + str(data["id"]))
        redent_button = post_widget.findChild(QPushButton, "redent_button_" + str(data["id"]))
        like_button = post_widget.findChild(QPushButton, "like_button_" + str(data["id"]))
        
        # Adding buttons pointers to list for later mapping
        self.destroy_buttons_list.append([destroy_button, data["id"]])
        self.dentid_buttons_list.append([dentid_button, data["id"]])
        self.redent_buttons_list.append([redent_button, data["id"]])
        self.like_buttons_list.append([like_button, data["id"]])
        
        # If current dent is not self-posted - hide "Delete" button.
        if not data["nickname"] == self.settings["user"]:
            destroy_button.hide()
        else:
            redent_button.hide()
        
        if data["retweeted"]:
            redent_button.hide()
        elif data["nickname"] != self.settings["user"] and data["retweeted"]:
            redent_button.show()
        
        self.ui.context.addTopLevelItem(item)
        self.ui.context.setItemWidget(item, 0, avatar_widget)
        self.ui.context.setItemWidget(item, 1, post_widget)

    def like_dent(self, dent_id):
        """
        Like dent button callback
        """
        # Search for item that contain pressed "Like" button, get dent id,
        # and send a request to connector for dent like.
        try:
            root = self.ui.context.invisibleRootItem()
            count = root.childCount()
            for index in range(count):
                item = root.child(index)
                if item.text(2).split(":")[0] == str(dent_id):
                    btn = self.ui.context.findChild(QPushButton, "like_button_" + str(dent_id))
                    btn.setText("...")
                    if item.text(3) == "not":
                        data = self.auth.favoritize_dent(dent_id, self.version)
                        if data["favorited"]:
                            item.setText(3, "favorited")
                            btn.setText("X")
                        else:
                            btn.setText(u"\u2665")
                        break
                    else:
                        data = self.auth.defavoritize_dent(dent_id, self.version)
                        if not data["favorited"]:
                            item.setText(3, "not")
                            btn.setText(u"\u2665")
                        else:
                            btn.setText("X")
                        break
        except:
            QMessageBox.critical(self, "QTDenter - Choose dent first!", "You have to choose dent")
        
    def redent_dent(self, dent_id):
        """
        Redent dent button callback
        """
        # Search for item that contain pressed "Redent" button, get dent id,
        # and send a request to connector for dent redenting.
        try:
            root = self.ui.context.invisibleRootItem()
            count = root.childCount()
            for index in range(count):
                item = root.child(index)
                if item.text(2).split(":")[0] == str(dent_id):
                    print "FOUND!"
                    data = self.auth.redent_dent(dent_id, self.version)
                    if data != "FAIL":
                        btn = self.ui.context.findChild(QPushButton, "redent_button_" + str(dent_id))
                        btn.hide()
                        
                    break
        except:
            QMessageBox.critical(self, "QTDenter - Choose dent first!", "You have to choose dent")
        
    def delete_dent(self, dent_id):
        """
        Delete dent button callback
        """
        # Search for item that contain pressed "Delete" button, get dent id,
        # and send a request to connector for dent deletion.
        try:
            root = self.ui.context.invisibleRootItem()
            count = root.childCount()
            for index in range(count):
                item = root.child(index)
                if item.text(2).split(":")[0] == str(dent_id):
                    data = self.auth.delete_dent(dent_id)
                    print data
                    if data == "OK":
                        index = self.ui.context.indexOfTopLevelItem(item)
                        self.ui.context.takeTopLevelItem(index)
                    break
        except:
            QMessageBox.critical(self, "QTDenter - Choose dent first!", "You have to choose dent")
            
    def reply_to_dent(self):
        """
        Reply to dent
        """
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

    def go_to_dent(self, dent_id):
        """
        Callback for ID button
        """
        try:
            root = self.ui.context.invisibleRootItem()
            count = root.childCount()
            for index in range(count):
                item = root.child(index)
                if item.text(2).split(":")[0] == str(dent_id):
                    server_address = self.settings["server"]
                    if self.settings["useSecureConnection"] == 1:
                        server_address = "https://" + server_address
                    else:
                        server_address = "http://" + server_address
        
                    QDesktopServices.openUrl(QUrl(server_address + "/notice/" + str(dent_id)))
        except:
            QMessageBox.critical(self, "QTDenter - Choose dent first!", "You have to choose dent")
        
    def send_reply(self, data):
        """
        Send reply
        """
        data = self.auth.send_reply(data, self.version)
        self.list_handler.add_data("home", [data])
            
    def new_post_callback(self, type, data):
        """
        Callback for new post dialog.
        """
        if type == "send_reply":
            self.send_reply(data)
            
            
