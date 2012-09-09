#!/usr/bin/python2
# -*- coding: utf8 -*-

import os, sys, json, urllib2, ConfigParser, time, commands
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui import MainWindow, NewPost, About, Stat
from lib import database, list_handler, list_item, common, options_dialog, information
from addons import now_playing
from identiparse import connector
import pynotify

cachepath = os.path.expanduser("~/.local/share/qtdenter/")

VERSION = "0.1-dev"

#############
# FIXME: remove that piece of shit when qt5 comes...
# Due to https://bugreports.nokia.com/browse/QTBUG-18807
#############
def get_desktop():
    desktop_environment = "generic"
    if os.environ.get("KDE_FULL_SESSION") == "true":
        desktop_environment = "kde"
    elif os.environ.get("GNOME_DESKTOP_SESSION_ID"):
        desktop_environment = "gnome"
    return desktop_environment

def iconFromTheme(*names, **kwargs):
    size = kwargs["size"] if "size" in kwargs else 32
    try:
        from PyKDE4.kdeui import KIcon
        for name in names:
            if KIcon.hasThemeIcon(name):
                return KIcon(name)
    except:
        pass
    if get_desktop() == "generic":
        try:
            from gtk import icon_theme_get_default
            iconTheme = icon_theme_get_default()
            for name in names:
                iconInfo = iconTheme.lookup_icon(name, size, 0)
                if iconInfo:
                    return QIcon(iconInfo.get_filename())
        except:
            pass
    for name in names:
        if QIcon.hasThemeIcon(name):
            return QIcon(QIcon.fromTheme(name))

        return QIcon()

#############
# FIXME end
#############

class Denter_Form(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.statusbar.hide()

        self.appVersion = "0.1-dev"
        
        common.set_qtdenter_path()

        self._hidden = 0
        self.inserted_timeline_dents_ids = []
        self.inserted_mentions_dents_ids = []
        self._new_direct_messages = 0
        self._new_mentions = 0
        self._changed_credentials = False
        
        QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))
        
        # Tray icon
        self.trayIcon = QSystemTrayIcon(QIcon(common.QTDENTER_PATH + "/ui/imgs/trayicon.png"), self)
        self.trayIcon.setVisible(True)
        self.connect(self.trayIcon, SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.check_for_visibility)
        
        # Tray menu
        menu = QMenu(parent)
        menu.addAction("Show/Hide", self.check_for_visibility)
        menu.addSeparator()
        #menu.addAction("Options", self.show_options)
        #menu.addSeparator()
        menu.addAction("Exit", self.close_from_tray)
        self.trayIcon.setContextMenu(menu)

        self.settings = {}
        if not os.path.exists(os.path.expanduser("~/.config/qtdenter")):
            os.mkdir(os.path.expanduser("~/.config/qtdenter"))
            os.system("touch ~/.config/qtdenter/qsettings.conf")
        if not os.path.exists(os.path.expanduser("~/.local/share/qtdenter/avatars")):
            os.makedirs(os.path.expanduser("~/.local/share/qtdenter/avatars"))

        if not os.path.exists(cachepath):
            os.mkdir(cachepath)

        try:
            self.qsettings = QSettings("qtdenter", "qsettings")
            self.settings["user"] = self.qsettings.value("user").toString()
            self.settings["password"] = self.qsettings.value("password").toString()
            self.settings["server"] = self.qsettings.value("server").toString()
            self.settings["useSecureConnection"] = self.qsettings.value("useSecureConnection").toString()
            self.settings["isSingle"] = self.qsettings.value("isSingle").toString()
            self.settings["deleteAllFromCacheOnExit"] = self.qsettings.value("deleteAllFromCacheOnExit").toString()
            self.settings["updateInterval"] = self.qsettings.value("updateInterval").toString()
            self.settings["last_dent_id"] = self.qsettings.value("last_dent_id").toString()
            
        except:
            QMessageBox.critical(self, "denter - No accounts", "Setup an account in Options!")

        try:
            self.restoreGeometry(self.qsettings.value("geometry").toByteArray())
            self.restoreState(self.qsettings.value("state").toByteArray())
        except:
            pass
            
        try:
            self.settings["remember_last_dent_id"] = self.qsettings.value("remember_last_dent_id").toString()
            self.settings["fetch_on_startup"] = self.qsettings.value("fetch_on_startup").toString()
        except:
            self.settings["remember_last_dent_id"] = "0"
            self.settings["fetch_on_startup"] = "20"
            
        try:
            self.settings["player"] = self.qsettings.value("player").toString()
            self.settings["player_string"] = self.qsettings.value("player_string").toString()
        except:
            self.settings["player"] = None
            self.settings["player_string"] = "!listening to: $artist - $track #$player"

        if not os.path.exists(os.path.expanduser("~/.config/qtdenter/data.sqlite")):
            database.createDB()

        self.ui.action_Options.triggered.connect(self.show_options_dialog)
        self.ui.action_Exit.triggered.connect(self.close_from_menu)
        self.ui.action_About_Denter.triggered.connect(self.show_about)
        self.ui.actionStatistics.triggered.connect(self.show_information)
        self.ui.actionSpam_Music_data.triggered.connect(self.spam_music)

        self.connect(self, SIGNAL("PostData(PyQt_PyObject)"), self.post_status)
        self.connect(self, SIGNAL("SendReply(PyQt_PyObject)"), self.send_reply)
        self.connect(self, SIGNAL("SendDirectMessage(PyQt_PyObject)"), self.send_direct_message)
        self.connect(self, SIGNAL("ShowForm()"), self.check_for_visibility)
        self.connect(self, SIGNAL("HideForm()"), self.check_for_visibility)
        self.connect(self, SIGNAL("ShowOptions()"), self.show_options_dialog)
        self.connect(self, SIGNAL("Close()"), self.close_from_tray)

        newPostIcon = iconFromTheme("add")
        newPost = QAction(newPostIcon, "New post", self)
        newPost.setShortcut("Ctrl+N")
        newPost.triggered.connect(self.post_status_dialog)
        
        new_direct_message_icon = iconFromTheme("no-new-messages")
        new_direct_message = QAction(new_direct_message_icon, "New direct message", self)
        new_direct_message.setShortcut("Ctrl+N")
        new_direct_message.triggered.connect(self.post_direct_message_dialog)

        reloadTimelinesIcon = iconFromTheme("reload")
        reloadTimelines = QAction(reloadTimelinesIcon, "Reload all timelines", self)
        reloadTimelines.setShortcut("Ctrl+R")
        reloadTimelines.triggered.connect(self.update_timelines)

        optionsIcon = iconFromTheme("document-properties")
        options = QAction(optionsIcon, "Options", self)
        options.setShortcut("Ctrl+P")
        options.triggered.connect(self.show_options_dialog)

        spacerWidget = QWidget()
        spacerWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.time_updated_action = QLabel()

        self.ui.toolBar.addAction(newPost)
        self.ui.toolBar.addAction(new_direct_message)
        self.ui.toolBar.addSeparator()
        self.ui.toolBar.addAction(reloadTimelines)
        self.ui.toolBar.addSeparator()
        self.ui.toolBar.addAction(options)
        self.ui.toolBar.addWidget(spacerWidget)
        self.ui.toolBar.addWidget(self.time_updated_action)
        
        self.ui.timeline_list.setItemDelegate(list_item.item())

        self.list_handler = list_handler.List_Handler(callback=self.lists_callback)
            
        self.ui.timeline_list.setSortingEnabled(True)
        self.ui.timeline_list.sortByColumn(2, Qt.DescendingOrder)
        for column in range(2, 5):
            self.ui.timeline_list.setColumnHidden(column, True)
        self.ui.timeline_list.setColumnWidth(0, 65)
        self.ui.timeline_list.itemActivated.connect(self.reply_to_dent)
        self.ui.timeline_list.connect(self.ui.timeline_list, SIGNAL("itemEntered(QTreeWidgetItem, int)"), self.set_current_item)
        
        self.ui.mentions_list.setSortingEnabled(True)
        self.ui.mentions_list.sortByColumn(2, Qt.DescendingOrder)
        for column in range(2, 5):
            self.ui.mentions_list.setColumnHidden(column, True)
        self.ui.mentions_list.setColumnWidth(0, 65)
        self.ui.mentions_list.itemActivated.connect(self.reply_to_dent)
        
        self.list_item = list_item.list_item()
        
        # Init notifications
        try:
            pynotify.init(sys.argv[0])
            print "Notifier loaded"
        except:
            print "Failed to init pynotify"
            
        self.show()
        # Initialize auther and get timelines for first time
        try:
            self.init_connector()
            
            if self.settings["remember_last_dent_id"] == "1":
                opts = {"count"     : None,
                        "from_id"   : self.settings["last_dent_id"], 
                        "name"      : self.settings["user"]
                        }
            else:
                opts = {"count"     : str(self.settings["fetch_on_startup"]),
                        "from_id"   : None,
                        "name"      : self.settings["user"]
                        }
                
            home_timeline = self.auth.get_home_timeline(opts)
            self.list_handler.add_data("home", home_timeline)
            mentions = self.auth.get_mentions(opts)
            self.list_handler.add_data("mentions", mentions)
            mentions = self.auth.get_direct_messages(opts)
            self.list_handler.add_data("direct_messages", mentions)
        except:
            print "No auth data specified"
            
        # Init timer
        self.start_timer(self.settings["updateInterval"])
        self.np = now_playing.Now_Playing(self.settings["player"], self.settings["player_string"])
        
        # Get max characters count from server
        try:
            server_data = self.auth.get_server_config("config")
            self.settings["messageLength"] = server_data["site"]["textlimit"]
        except:
            self.settings["messageLength"] = "140"
        
    def init_connector(self):
        self.auth = connector.Requester(self.settings["user"], self.settings["password"], self.settings["server"] + "/api/", self.settings["useSecureConnection"], self.connect_callback)
    
    def connect_callback(self, data):
        if data == "bad_credentials":
            QMessageBox.critical(self, "QTDenter - Bad credentials", "Username and password you entered\nis incorrect.")
            self.show_options_dialog()
        
    def start_timer(self, interval):
        try:
            timer_interval = int(interval) * 1000 * 60
            self.update_timer = QTimer()
            self.update_timer.timeout.connect(self.update_timelines)
            self.update_timer.start(timer_interval)
            print "Timer launched with interval of {0} minutes".format(interval)
        except:
            print "Failed to launch timer!"
            
    def update_timelines(self):
        opts = {"count"     : None,
                "from_id"   : None,
                "name"      : self.settings["user"]
                }
        home_timeline = self.auth.get_home_timeline(opts)
        self.list_handler.add_data("home", home_timeline)
        mentions = self.auth.get_mentions(opts)
        self.list_handler.add_data("mentions", mentions)
        mentions = self.auth.get_direct_messages(opts)
        self.list_handler.add_data("direct_messages", mentions)
            
    def lists_callback(self, list_type, data):
        if list_type == "home":
            self.add_to_timeline_iterator(data)
        elif list_type == "home_avatar":
            self.update_timeline_avatar(data)
        elif list_type == "mentions":
            self.add_to_mentions_iterator(data)
        elif list_type == "direct_messages":
            self.add_to_dm_iterator(data)
        elif list_type == "end":
            curtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self.time_updated_action.setText("<b>Last updated on: {0}</b>".format(curtime))
            
            # Notifications
            if self._new_direct_messages > 0:
                notify = pynotify.Notification("QTDenter", "{0} new dents arrived.".format(self._new_direct_messages), common.QTDENTER_PATH + "/ui/imgs/trayicon.png")
                notify.set_urgency(pynotify.URGENCY_NORMAL)
                notify.set_timeout(10000)
                notify.add_action("clicked","Show QTDenter", self.show_window, None)
                notify.show()
                self._new_direct_messages = 0
            
            
    def add_to_timeline_iterator(self, data):
        if data["id"] not in self.inserted_timeline_dents_ids:
            self.inserted_timeline_dents_ids.append(data["id"])
            self.add_dent_to_widget("timeline", data)
            self._new_direct_messages += 1
        else:
            pass

    def add_to_mentions_iterator(self, data):
        if data["id"] not in self.inserted_mentions_dents_ids:
            self.inserted_mentions_dents_ids.append(data["id"])
            self.add_dent_to_widget("mentions", data)
            self._new_mentions += 1
        else:
            pass
            
    def add_to_dm_iterator(self, data):
        if data["id"] not in self.inserted_mentions_dents_ids:
            self.inserted_mentions_dents_ids.append(data["id"])
            self.add_dent_to_widget("direct_messages", data)
            self._new_mentions += 1
        else:
            pass

    def add_dent_to_widget(self, list_type, data):
        item_data = self.list_item.process_item(data)
        
        item = item_data[0]
        avatar_widget = item_data[1]
        post_widget = item_data[2]
        
        destroy_button = avatar_widget.findChild(QPushButton, "destroy_button_" + str(data["id"]))
        dentid_button = post_widget.findChild(QPushButton, "dentid_button_" + str(data["id"]))
        redent_button = post_widget.findChild(QPushButton, "redent_button_" + str(data["id"]))
        like_button = post_widget.findChild(QPushButton, "like_button_" + str(data["id"]))
        destroy_button.clicked.connect(self.delete_dent)
        dentid_button.clicked.connect(self.go_to_dent)
        redent_button.clicked.connect(self.redent_dent)
        like_button.clicked.connect(self.like_dent)
        
        if not data["nickname"] == self.settings["user"]:
            destroy_button.hide()
        
        list_widget = self.ui.timeline_list
        if list_type == "mentions":
            list_widget = self.ui.mentions_list
        if list_type == "direct_messages":
            list_widget = self.ui.dm_list
        
        list_widget.addTopLevelItem(item)
        list_widget.setItemWidget(item, 0, avatar_widget)
        list_widget.setItemWidget(item, 1, post_widget)
        
    def update_timeline_avatar(self, name):
        print name
        
    def like_dent(self):
        if self.ui.tabWidget.currentIndex() == 0:
            list_widget = self.ui.timeline_list
        elif self.ui.tabWidget.currentIndex() == 1:
            list_widget = self.ui.mentions_list
        elif self.ui.tabWidget.currentIndex() == 2:
            list_widget = self.ui.dm_list
        
        try:
            item = list_widget.currentItem()
            dent_id = list_widget.currentItem().text(2).split(":")[0]
            if list_widget.currentItem().text(3) == "not":
                data = self.auth.favoritize_dent(dent_id, VERSION)
                if data != "FAIL":
                    btn = list_widget.findChild(QPushButton, "like_button_" + dent_id)
                    list_widget.currentItem().setText(3, "favorited")
                    btn.setText("X")
            else:
                data = self.auth.defavoritize_dent(dent_id, VERSION)
                if data != "FAIL":
                    btn = list_widget.findChild(QPushButton, "like_button_" + dent_id)
                    btn.findChild(QPushButton, "X")
                    list_widget.currentItem().setText(3, "not")
                    btn.setText(u"\u2665")
        except:
            QMessageBox.critical(self, "QTDenter - Choose dent first!", "You have to choose dent")
        
    def redent_dent(self):
        if self.ui.tabWidget.currentIndex() == 0:
            list_widget = self.ui.timeline_list
        elif self.ui.tabWidget.currentIndex() == 1:
            list_widget = self.ui.mentions_list
        elif self.ui.tabWidget.currentIndex() == 2:
            list_widget = self.ui.dm_list

        try:
            dent_id = list_widget.currentItem().text(2).split(":")[0]
            self.auth.redent_dent(dent_id, VERSION)
        except:
            QMessageBox.critical(self, "QTDenter - Choose dent first!", "You have to choose dent")
        
    def delete_dent(self):
        if self.ui.tabWidget.currentIndex() == 0:
            list_widget = self.ui.timeline_list
        elif self.ui.tabWidget.currentIndex() == 2:
            list_widget = self.ui.dm_list

        try:
            dent_id = list_widget.currentItem().text(2).split(":")[0]
            data = self.auth.delete_dent(dent_id)
            if data == "OK":
                index = list_widget.indexOfTopLevelItem(list_widget.currentItem())
                list_widget.takeTopLevelItem(index)
        except:
            QMessageBox.critical(self, "QTDenter - Choose dent first!", "You have to choose dent")

    def post_status(self, data):
        data = self.auth.post_dent(data, VERSION)
        self.list_handler.add_data("home", [data])
        
    def send_reply(self, data):
        data = self.auth.send_reply(data, VERSION)
        self.list_handler.add_data("home", [data])
        
    def send_direct_message(self, data):
        self.auth.send_direct_message(data, VERSION)
        
    def reply_to_dent(self):
        if self.ui.tabWidget.currentIndex() == 0:
            list_widget = self.ui.timeline_list
        elif self.ui.tabWidget.currentIndex() == 1:
            list_widget = self.ui.mentions_list
        elif self.ui.tabWidget.currentIndex() == 2:
            list_widget = self.ui.dm_list
            
        try:
            dent_id = list_widget.currentItem().text(2).split(":")[0]
            to_username = list_widget.currentItem().text(2).split(":")[1]
            dent_text = list_widget.currentItem().text(4)
            params = {}
            params["type"] = "reply"
            params["reply_to_id"] = dent_id
            params["nickname"] = to_username
            params["text"] = dent_text
            newpostD = NewPostDialog(self.settings["messageLength"], params)
            newpostD.exec_()
        except:
            QMessageBox.critical(self, "QTDenter - Choose dent first!", "You have to choose dent")
        
    def post_status_dialog(self):
        params = {
                    "type": "new_dent"
                }
        newpostD = NewPostDialog(self.settings["messageLength"], params)
        newpostD.exec_()
        
    def post_direct_message_dialog(self):
        params = {}
        params["type"] = "direct"
        newpostD = NewPostDialog(self.settings["messageLength"], params)
        newpostD.exec_()
        
    def go_to_dent(self):
        try:
            item = self.ui.timeline_list.currentItem()
            dent_id = self.ui.timeline_list.currentItem().text(2).split(":")[0]
            server_address = self.settings["server"]
            if self.settings["useSecureConnection"] == 1:
                server_address = "https://" + server_address
            else:
                server_address = "http://" + server_address
        
            QDesktopServices.openUrl(QUrl(server_address + "/notice/" + dent_id))
        except:
            QMessageBox.critical(self, "QTDenter - Choose dent first!", "You have to choose dent")
        
    def spam_music(self):
        music_data = self.np.get_music_info(self.settings["player"])
        spam_string = self.qsettings.value("player_string").toString()
        spam_string = spam_string.replace("$artist", music_data["artist"])
        spam_string = spam_string.replace("$album", music_data["album"])
        spam_string = spam_string.replace("$trackname", music_data["trackname"])
        spam_string = spam_string.replace("$player", str(self.settings["player"]).lower())
        spam_string = spam_string.replace("\"", "")
        params = {
                    "text": spam_string,
                    "direct": False,
                    "type": "insert"
                }
        newpostD = NewPostDialog(self.settings["messageLength"], params)
        newpostD.exec_()
    
    def set_current_item(self, item, column):
        print item, column

    def check_for_visibility(self):
        if self._hidden == 0:
            self.hide()
            self._hidden = 1
        else:
            self.show()
            self._hidden = 0
            
    def show_window(self):
        self.show()
        self._hidden = 0

    def show_options_dialog(self):
        settingsD = options_dialog.Options_Dialog(self.settings, self.change_settings)
        settingsD.exec_()

    def change_settings(self, data):
        if self.settings["user"] != data[0] or self.settings["server"] != data[2]:
            QMessageBox.information(self, "Username or Serve change", "In order to continue ALL cache data and currently\nshowed dents will be cleared.")
            self._changed_credentials = True
        else:
            pass
            
        self.settings["user"] = data[0]
        self.settings["password"] = data[1]
        self.settings["server"] = data[2]
        self.settings["useSecureConnection"] = data[3]
        self.settings["deleteAllFromCacheOnExit"] = data[4]
        self.settings["updateInterval"] = data[5]
        self.settings["remember_last_dent_id"] = data[6]
        self.settings["fetch_on_startup"] = data[7]
        self.settings["player"] = data[8]
        self.settings["player_string"] = data[9]
        self.init_connector()
        self.start_timer(self.settings["updateInterval"])
        
        if self._changed_credentials == True:
            self.ui.timeline_list.clear()
            self.update_timelines()
            self._changed_credentials = False
        
    def show_about(self):
        aboutW = QDialog()
        aboutW.ui = About.Ui_Dialog()
        aboutW.ui.setupUi(aboutW)
        aboutW.exec_()

    def show_information(self):
        data = self.auth.get_server_config("config")
        server_version = self.auth.get_server_config("version")
        infoD = information.Information_Dialog(data, server_version, VERSION)
        infoD.exec_()

    def close_from_tray(self):
        self.close()

    def close_from_menu(self):
        self.close()

    def closeEvent(self, event):
        box = QMessageBox()
        box.setWindowTitle("QTDenter - Exiting")
        box.setText("Are you sure you want to exit?")
        box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        box.setDefaultButton(QMessageBox.Ok)
        box.setIcon(QMessageBox.Question)
        answer = box.exec_()
        if answer == 1024:
            self.qsettings.setValue("user", self.settings["user"])
            self.qsettings.setValue("password", self.settings["password"])
            self.qsettings.setValue("server", self.settings["server"])
            self.qsettings.setValue("useSecureConnection", self.settings["useSecureConnection"])
            self.qsettings.setValue("deleteAllFromCacheOnExit", self.settings["deleteAllFromCacheOnExit"])
            self.qsettings.setValue("updateInterval", self.settings["updateInterval"])
            self.qsettings.setValue("remember_last_dent_id", self.settings["remember_last_dent_id"])
            self.qsettings.setValue("fetch_on_startup", self.settings["fetch_on_startup"])
            self.qsettings.setValue("player", self.settings["player"])
            self.qsettings.setValue("player_string", self.settings["player_string"])
            self.qsettings.setValue("state", self.saveState())
            self.qsettings.setValue("geometry", self.saveGeometry())
            if self.settings["remember_last_dent_id"] == "1":
                root = self.ui.timeline_list.invisibleRootItem()
                last_item = root.child(0)
                dent_id = last_item.text(2).split(":")[0]
                self.qsettings.setValue("last_dent_id", dent_id)
        else:
            event.ignore()

class NewPostDialog(QDialog):
    def __init__(self, messageLength, parameters, parent = None):
        QDialog.__init__(self, parent)
        self.ui = NewPost.Ui_Dialog()
        self.ui.setupUi(self)

        self.messageLength = int(messageLength)
        self.reply = False
        self.direct = False
        
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
            try:
                if self.reply:
                    data = {}
                    data["text"] = self.ui.postData.toPlainText()
                    data["reply_to_id"] = self.params["reply_to_id"]
                    mbc.emit(SIGNAL("SendReply(PyQt_PyObject)"), data)
                else:
                    mbc.emit(SIGNAL("PostData(PyQt_PyObject)"), str(QString.toUtf8(self.ui.postData.toPlainText())))
            except:
                print "FAILED TO SIGNAL!"
                
            self.close()
                
    def post_direct_message(self):
        message = str(QString.toUtf8(self.ui.postData.toPlainText()))
        data = {}
        data["nickname"] = message.split(" ")[0][2:]
        data["message"] = message.split(" ")[1]
        
        mbc.emit(SIGNAL("SendDirectMessage(PyQt_PyObject)"), data)

        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mbc = Denter_Form()
    mbc.show()
    sys.exit(app.exec_())
