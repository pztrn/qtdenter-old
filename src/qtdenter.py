#!/usr/bin/python2
# -*- coding: utf8 -*-

import os, sys, json, urllib2, ConfigParser, time, commands
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui import MainWindow, NewPost, About, Stat
from lib import list_handler, list_item, common, options_dialog, information, context, new_post
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
        
        # Setting QTDenter path
        common.set_qtdenter_path()
        
        # Some variables
        self._hidden = 0
        self.inserted_timeline_dents_ids = []
        self.inserted_mentions_dents_ids = []
        self._new_direct_messages = 0
        self._new_mentions = 0
        self._changed_credentials = False
        self.filters = {}
        # Set default filters
        self._filters_state = ["timeline", "mentions"]
        
        # Set QTextCodec explicitly. Some disadvantages for rarely used
        # languages, but no problems for others.
        QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))
        
        # Tray icon
        self.icon = {}
        if not os.path.exists(common.QTDENTER_PATH + "/imgs/qtdenter.png"):
            self.icon["qicon"] = QIcon("/usr/share/pixmaps/qtdenter.png")
            self.icon["path"] = "/usr/share/pixmaps/qtdenter.png"
        else:
            self.icon["qicon"] = QIcon(common.QTDENTER_PATH + "/imgs/qtdenter.png")
            self.icon["path"] = common.QTDENTER_PATH + "/ui/imgs/qtdenter.png"
            
        self.trayIcon = QSystemTrayIcon(self.icon["qicon"], self)
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

        # Reading settings and fill settings dict
        self.settings = {}
        if not os.path.exists(os.path.expanduser("~/.config/qtdenter")):
            os.mkdir(os.path.expanduser("~/.config/qtdenter"))
            os.system("touch ~/.config/qtdenter/qsettings.conf")
        if not os.path.exists(os.path.expanduser("~/.local/share/qtdenter/avatars/temp")):
            os.makedirs(os.path.expanduser("~/.local/share/qtdenter/avatars/temp"))

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
            self.settings["mpd_port"] = self.qsettings.value("mpd_port").toString()
            self.settings["mpd_host"] = self.qsettings.value("mpd_host").toString()
        except:
            self.settings["player"] = None
            self.settings["player_string"] = "!listening to: $artist - $track #$player"
            self.settings["mpd_port"] = "6600"
            self.settings["mpd_host"] = "localhost"
            
        try:
            self._filters_state = self.qsettings.value("filters_state").toString()
            self._filters_state = self._filters_state.split(":")
        except:
            print "Failed to restore filters state"

        # Connecting menu actions
        self.ui.action_Options.triggered.connect(self.show_options_dialog)
        self.ui.action_Exit.triggered.connect(self.close_from_menu)
        self.ui.action_About_Denter.triggered.connect(self.show_about)
        self.ui.actionStatistics.triggered.connect(self.show_information)
        self.ui.actionSpam_Music_data.triggered.connect(self.spam_music)
        self.ui.action_Update_all.triggered.connect(self.update_timelines)
        self.ui.action_Mark_all_unread.triggered.connect(self.mark_all_as_read)

        # Connecting some signals
        self.connect(self, SIGNAL("ShowForm()"), self.check_for_visibility)
        self.connect(self, SIGNAL("HideForm()"), self.check_for_visibility)
        self.connect(self, SIGNAL("ShowOptions()"), self.show_options_dialog)
        self.connect(self, SIGNAL("Close()"), self.close_from_tray)

        # New post toolbar icon
        newPostIcon = iconFromTheme("add")
        newPost = QAction(newPostIcon, "New post", self)
        newPost.setShortcut("Ctrl+N")
        newPost.triggered.connect(self.post_status_dialog)
        
        # New direct message toolbar icon
        new_direct_message_icon = iconFromTheme("no-new-messages")
        new_direct_message = QAction(new_direct_message_icon, "New direct message", self)
        new_direct_message.setShortcut("Ctrl+D")
        new_direct_message.triggered.connect(self.post_direct_message_dialog)

        # Timelines reload toolbar icon
        reloadTimelinesIcon = iconFromTheme("reload")
        reloadTimelines = QAction(reloadTimelinesIcon, "Reload all timelines", self)
        reloadTimelines.setShortcut("Ctrl+R")
        reloadTimelines.triggered.connect(self.update_timelines)
        
        # Mark all read icon
        mark_all_read_icon = iconFromTheme("dialog-ok")
        mark_all_read = QAction(mark_all_read_icon, "Mark all unread dents as read", self)
        mark_all_read.setShortcut("Ctrl+X")
        mark_all_read.triggered.connect(self.mark_all_as_read)

        # Options toolbar icon
        optionsIcon = iconFromTheme("document-properties")
        options = QAction(optionsIcon, "Options", self)
        options.setShortcut("Ctrl+P")
        options.triggered.connect(self.show_options_dialog)

        # Spacer widget, making last updated time label in toolbar to align
        # strictly right
        spacerWidget = QWidget()
        spacerWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Last updated label
        self.time_updated_action = QLabel()

        # Adding everything to toolbar
        self.ui.toolBar.addAction(newPost)
        self.ui.toolBar.addAction(new_direct_message)
        self.ui.toolBar.addSeparator()
        self.ui.toolBar.addAction(reloadTimelines)
        self.ui.toolBar.addAction(mark_all_read)
        self.ui.toolBar.addSeparator()
        self.ui.toolBar.addAction(options)
        self.ui.toolBar.addWidget(spacerWidget)
        self.ui.toolBar.addWidget(self.time_updated_action)
        
        # Setting icons
        self.ui.timeline_btn.setIcon(QIcon(common.QTDENTER_PATH + "/imgs/timeline.png"))
        self.ui.mentions_btn.setIcon(QIcon(common.QTDENTER_PATH + "/imgs/mentions.png"))
        self.ui.directs_btn.setIcon(QIcon(common.QTDENTER_PATH + "/imgs/directs.png"))
        
        # Adding accounts
        self.ui.no_accounts_btn.hide()
        
        self.btn = QPushButton()
        self.btn.setIcon(QIcon(common.QTDENTER_PATH + "/imgs/identica.png"))
        self.btn.setText(self.settings["server"])
        
        self.ui.accounts_layout.addWidget(self.btn)
        
        if "timeline" in self._filters_state:
            self.ui.timeline_btn.setChecked(True)
        if "mentions" in self._filters_state:
            self.ui.mentions_btn.setChecked(True)
        if "directs" in self._filters_state:
            self.ui.directs_btn.setChecked(True)
        
        self.ui.timeline_btn.clicked.connect(self.change_filters)
        self.ui.mentions_btn.clicked.connect(self.change_filters)
        self.ui.directs_btn.clicked.connect(self.change_filters)

        # Defining list_handler instance
        self.list_handler = list_handler.List_Handler(callback=self.lists_callback)
        
        # Set some options to timeline list
        self.ui.timeline_list.setSortingEnabled(True)
        self.ui.timeline_list.sortByColumn(2, Qt.DescendingOrder)
        for column in range(2, 6):
            self.ui.timeline_list.setColumnHidden(column, True)
        self.ui.timeline_list.setColumnWidth(0, 65)
        self.ui.timeline_list.itemActivated.connect(self.reply_to_dent)
        self.ui.timeline_list.itemSelectionChanged.connect(self.change_item_read_state)
        
        # Defining list_item instance, that generates items for lists
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
        except:
            print "No auth data specified"
        
        try:
            self.initialize_button_mappers()
        
            opts = {"count"     : str(self.settings["fetch_on_startup"]),
                    "name"      : self.settings["user"]
                    }
            
            if self.settings["remember_last_dent_id"] == "1":
                # Getting last dent ID from server
                temp = self.auth.get_home_timeline(opts)
                # Calculation count of dents we will download on startup
                count = temp[0]["id"] - int(self.settings["last_dent_id"])
                    
                if count == 0:
                    count = 20
                else:
                    pass
            
                opts = {"count"     : str(count),
                        "name"      : self.settings["user"]
                        }
        except:
            print "Can't specify options!"
        
        try:
            home_timeline = self.auth.get_home_timeline(opts)
            self.list_handler.add_data("home", home_timeline, self.settings["server"])
        except:
            print "Can't get home timeline. WTF?"
        
        try:
            mentions = self.auth.get_direct_messages(opts)
            self.list_handler.add_data("direct_messages", mentions, self.settings["server"])
            if self.settings["remember_last_dent_id"] == "1":
                root = self.ui.timeline_list.invisibleRootItem()
                last_item = root.child(0)
                dent_id = last_item.text(2).split(":")[0]
                self.qsettings.setValue("last_dent_id", dent_id)
            self.qsettings.sync()
        except:
            print "Can't get direct messages. WTF?"
            
        try:
            # Connect buttons
            self.connect_buttons()
        except:
            print "Failed to connect buttons!"
        
            
        # Init timer
        self.start_timer(self.settings["updateInterval"])
        
        # Init "Now Playing"
        self.np = now_playing.Now_Playing(self.settings)
        
        # Get max characters count from server
        try:
            server_data = self.auth.get_server_config("config")
            self.settings["messageLength"] = server_data["site"]["textlimit"]
        except:
            self.settings["messageLength"] = "140"
        
    def init_connector(self):
        """
        Initialize connection instance
        """
        self.auth = connector.Requester(self.settings["user"], self.settings["password"], self.settings["server"] + "/api/", self.settings["useSecureConnection"], self.connect_callback)
    
    def connect_callback(self, data):
        """
        Callback for connection instance
        """
        if data == "bad_credentials":
            QMessageBox.critical(self, "QTDenter - Bad credentials", "Username and password you entered\nis incorrect.")
            self.show_options_dialog()
        
    def start_timer(self, interval):
        """
        Timer starting/redefining
        """
        try:
            timer_interval = int(interval) * 1000 * 60
            self.update_timer = QTimer()
            self.update_timer.timeout.connect(self.update_timelines)
            self.update_timer.start(timer_interval)
            print "Timer launched with interval of {0} minutes".format(interval)
        except:
            print "Failed to launch timer!"
            
    def update_timelines(self):
        """
        Update timelines
        """
        self.initialize_button_mappers()
        opts = {"count"     : None,
                "name"      : self.settings["user"]
                }
        home_timeline = self.auth.get_home_timeline(opts)
        self.list_handler.add_data("home", home_timeline, self.settings["server"])
        mentions = self.auth.get_direct_messages(opts)
        self.list_handler.add_data("direct_messages", mentions, self.settings["server"])
        if self.settings["remember_last_dent_id"] == "1":
            root = self.ui.timeline_list.invisibleRootItem()
            last_item = root.child(0)
            dent_id = last_item.text(2).split(":")[0]
            self.qsettings.setValue("last_dent_id", dent_id)
        self.qsettings.sync()
        
        # Connect buttons
        self.connect_buttons()
        
    def initialize_button_mappers(self):
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
            
        self.context_buttons_mapper.mapped.connect(self.show_context)
        self.destroy_buttons_mapper.mapped.connect(self.delete_dent)
        self.redent_buttons_mapper.mapped.connect(self.redent_dent)
        self.like_buttons_mapper.mapped.connect(self.like_dent)
        self.dentid_buttons_mapper.mapped.connect(self.go_to_dent)
            
    def lists_callback(self, dent_type, data, account):
        """
        Lists callback. Depending on "dent_type" parameter, sending "data"
        to specified function, responsible for own list.
        """
        if dent_type == "home_avatar":
            self.update_timeline_avatar(data)
        elif dent_type == "end":
            curtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self.time_updated_action.setText("<b>Last updated on: {0}</b>".format(curtime))
            
            # Notifications
            if self._new_direct_messages > 0:
                notify = pynotify.Notification("QTDenter", "{0} new dents arrived.".format(self._new_direct_messages), self.icon["path"])
                notify.set_urgency(pynotify.URGENCY_NORMAL)
                notify.set_timeout(10000)
                notify.add_action("clicked","Show QTDenter", self.show_window, None)
                notify.show()
                self._new_direct_messages = 0
        else:
            self.add_to_timeline_iterator(data, account, dent_type)
            
            
    def add_to_timeline_iterator(self, data, account, dent_type):
        """
        This function called multiple times, until "data" flows in.
        """
        if data["id"] not in self.inserted_timeline_dents_ids:
            self.inserted_timeline_dents_ids.append(data["id"])
            self.add_dent_to_widget(dent_type, data, account)
            self._new_direct_messages += 1
        else:
            pass

    def add_dent_to_widget(self, dent_type, data, account):
        """
        Add dents to widget. Widget specified in "dent_type" option
        """
        item_data = self.list_item.process_item(data, self.settings["last_dent_id"], self.settings["user"], account, dent_type)
        
        item = item_data[0]
        avatar_widget = item_data[1]
        post_widget = item_data[2]

        # Searching buttons
        destroy_button = avatar_widget.findChild(QPushButton, "destroy_button_" + str(data["id"]))
        dentid_button = post_widget.findChild(QPushButton, "dentid_button_" + str(data["id"]))
        redent_button = post_widget.findChild(QPushButton, "redent_button_" + str(data["id"]))
        like_button = post_widget.findChild(QPushButton, "like_button_" + str(data["id"]))
        context_button = post_widget.findChild(QPushButton, "context_button_" + str(data["conversation_id"]))
        
        # Adding buttons pointers to list for later mapping
        self.destroy_buttons_list.append([destroy_button, data["id"]])
        self.dentid_buttons_list.append([dentid_button, data["id"]])
        self.redent_buttons_list.append([redent_button, data["id"]])
        self.like_buttons_list.append([like_button, data["id"]])
        if data["in_reply_to_screen_name"]:
            self.context_buttons_list.append([context_button, data["conversation_id"]])
            context_button.show()
        
        # If current dent is not self-posted - hide "Delete" button.
        if not data["nickname"] == self.settings["user"]:
            destroy_button.hide()
        else:
            redent_button.hide()
        
        if data["retweeted"]:
            redent_button.hide()
        elif data["nickname"] != self.settings["user"] and data["retweeted"]:
            redent_button.show()
            
        read_state = item.text(2).split(":")[3]
        dent_type = item.text(5).split(":")[1]
        
        if dent_type == "home":
            item.setBackground(0, QColor(255, 255, 200, 0))
            item.setBackground(1, QColor(255, 255, 200, 0))            
        if dent_type == "mentions":
            item.setBackground(0, QColor(150, 150, 255, 100))
            item.setBackground(1, QColor(150, 150, 255, 100))
        if dent_type == "directs":
            item.setBackground(0, QColor(255, 150, 150, 100))
            item.setBackground(1, QColor(255, 150, 150, 100))
        
        if read_state == "not":
            item.setBackground(0, QColor(200, 255, 200, 255))
            item.setBackground(1, QColor(200, 255, 200, 255))
        
        self.ui.timeline_list.addTopLevelItem(item)
        self.ui.timeline_list.setItemWidget(item, 0, avatar_widget)
        self.ui.timeline_list.setItemWidget(item, 1, post_widget)
        
    def update_timeline_avatar(self, name):
        """
        Updating avatars if no avatars present. Temporary, this function prints only
        avatar holder screen name, in future it will update avatars in lists.
        """
        print name
        
    def like_dent(self, dent_id):
        """
        Like dent button callback
        """
        # Search for item that contain pressed "Like" button, get dent id,
        # and send a request to connector for dent like.
        try:
            root = self.ui.timeline_list.invisibleRootItem()
            count = root.childCount()
            for index in range(count):
                item = root.child(index)
                if item.text(2).split(":")[0] == str(dent_id):
                    btn = self.ui.timeline_list.findChild(QPushButton, "like_button_" + str(dent_id))
                    btn.setText("...")
                    if item.text(3) == "not":
                        data = self.auth.favoritize_dent(dent_id, VERSION)
                        if data["favorited"]:
                            item.setText(3, "favorited")
                            btn.setText("X")
                        else:
                            btn.setText(u"\u2665")
                        break
                    else:
                        data = self.auth.defavoritize_dent(dent_id, VERSION)
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
            root = self.ui.timeline_list.invisibleRootItem()
            count = root.childCount()
            for index in range(count):
                item = root.child(index)
                if item.text(2).split(":")[0] == str(dent_id):
                    print "FOUND!"
                    data = self.auth.redent_dent(dent_id, VERSION)
                    if data != "FAIL":
                        btn = self.ui.timeline_list.findChild(QPushButton, "redent_button_" + str(dent_id))
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
            root = self.ui.timeline_list.invisibleRootItem()
            count = root.childCount()
            for index in range(count):
                item = root.child(index)
                if item.text(2).split(":")[0] == str(dent_id):
                    data = self.auth.delete_dent(dent_id)
                    print data
                    if data == "OK":
                        index = self.ui.timeline_list.indexOfTopLevelItem(item)
                        self.ui.timeline_list.takeTopLevelItem(index)
                    break
        except:
            QMessageBox.critical(self, "QTDenter - Choose dent first!", "You have to choose dent")

    def post_status(self, data):
        """
        Post status requester
        """
        data = self.auth.post_dent(data, VERSION)
        self.update_timelines()
        
    def send_reply(self, data):
        """
        Send reply callback
        """
        data = self.auth.send_reply(data, VERSION)
        self.update_timelines()
        
    def send_direct_message(self, data):
        self.auth.send_direct_message(data, VERSION)
        self.update_timelines()
        
    def reply_to_dent(self):
        """
        Reply to dent (item double-click) callback
        """
        # Search for item that contain pressed "Reply" button, get dent id,
        # and show post dent dialog.            
        try:
            dent_id = self.ui.timeline_list.currentItem().text(2).split(":")[0]
            to_username = self.ui.timeline_list.currentItem().text(2).split(":")[1]
            dent_text = self.ui.timeline_list.currentItem().text(4)
            params = {}
            params["type"] = "reply"
            params["reply_to_id"] = dent_id
            params["nickname"] = to_username
            params["text"] = dent_text
            newpostD = new_post.New_Post(self.settings["messageLength"], params, self.new_post_callback)
            newpostD.exec_()
        except:
            QMessageBox.critical(self, "QTDenter - Choose dent first!", "You have to choose dent")
        
    def post_status_dialog(self):
        """
        Post new dent dialog
        """
        params = {
                    "type": "new_dent"
                }
        newpostD = new_post.New_Post(self.settings["messageLength"], params, self.new_post_callback)
        newpostD.exec_()
        
    def post_direct_message_dialog(self):
        """
        Send direct message dialog
        """
        params = {}
        params["type"] = "direct"
        newpostD = new_post.New_Post(self.settings["messageLength"], params, self.new_post_callback)
        newpostD.exec_()
        
    def new_post_callback(self, type, data):
        """
        Callback for new post dialog
        """
        if type == "post_data":
            self.post_status(data)
        elif type == "send_reply":
            self.send_reply(data)
        elif type == "send_direct_message":
            self.send_direct_message(data)
        
    def go_to_dent(self, dent_id):
        """
        Callback for ID button
        """
        root = self.ui.timeline_list.invisibleRootItem()
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
            
    def show_context(self, conversation_id):
        """
        Callback for "Context" button
        """
        contextD = context.Context(self.auth, conversation_id, self.settings, VERSION)
        contextD.exec_()
        
    def change_item_read_state(self):
        """
        Change item state from 'not_read' to 'read'
        """
        item = self.ui.timeline_list.currentItem()
            
        read_state = item.text(2).split(":")[3]
        dent_type = item.text(5).split(":")[1]
        if read_state == "not":
            item_text_joined = QString()
            
            if dent_type == "home":
                item.setBackground(0, QColor(255, 255, 200, 0))
                item.setBackground(1, QColor(255, 255, 200, 0))            
            if dent_type == "mentions":
                item.setBackground(0, QColor(150, 150, 255, 100))
                item.setBackground(1, QColor(150, 150, 255, 100))
            if dent_type == "directs":
                item.setBackground(0, QColor(255, 150, 150, 100))
                item.setBackground(1, QColor(255, 150, 150, 100))
            
            item_text = item.text(2).split(":")
            item_text[3] = "read"
            item_text_joined = item_text.join(":")
            item.setText(2, item_text_joined)
            
    def mark_all_as_read(self):
        """
        Mark all unread dents as read
        """
        root = self.ui.timeline_list.invisibleRootItem()
        count = root.childCount()
        for index in range(count):
            item = root.child(index)
            try:
                read_state = item.text(2).split(":")[3]
                dent_type = item.text(5).split(":")[1]
                if read_state == "not":
                    item_text_joined = QString()
                    if dent_type == "home":
                        item.setBackground(0, QColor(255, 255, 200, 100))
                        item.setBackground(1, QColor(255, 255, 200, 100))            
                    if dent_type == "mentions":
                        item.setBackground(0, QColor(150, 150, 255, 100))
                        item.setBackground(1, QColor(150, 150, 255, 100))
                    if dent_type == "directs":
                        item.setBackground(0, QColor(255, 150, 150, 100))
                        item.setBackground(1, QColor(255, 150, 150, 100))
            
                    item_text = item.text(2).split(":")
                    item_text[3] = "read"
                    item_text_joined = item_text.join(":")
                    item.setText(2, item_text_joined)
            except:
                print "Failed to change state of item id", item.text(2).split(":")[0]
                
    def change_filters(self):
        """
        Change filters state and resort dents list
        """
        if self.ui.timeline_btn.isChecked():
            self.filters["home"] = True
        else:
            self.filters["home"] = False
        
        if self.ui.mentions_btn.isChecked():
            self.filters["mentions"] = True
        else:
            self.filters["mentions"] = False
            
        if self.ui.directs_btn.isChecked():
            self.filters["directs"] = True
        else:
            self.filters["directs"] = False
            
        self._filters_state = []
        if self.ui.timeline_btn.isChecked():
            self._filters_state.append("timeline")
        if self.ui.mentions_btn.isChecked():
            self._filters_state.append("mentions")
        if self.ui.directs_btn.isChecked():
            self._filters_state.append("directs")
            
        print self._filters_state       

        self.resort_dents_list()
        
    def resort_dents_list(self):
        """
        Re-sort dents list after filters state change
        """
        sort_string = ""
        
        if self.filters["home"]:
            sort_string += ":home:"
        if self.filters["mentions"]:
            sort_string += ":mentions:"
        if self.filters["directs"]:
            sort_string += ":directs:"
        
        filters_list = sort_string.split(":")
        root = self.ui.timeline_list.invisibleRootItem()
        count = root.childCount()
        for index in range(count):
            item = root.child(index)
            item_type = item.text(5).split(":")[1]
            if item_type not in filters_list:
                item.setHidden(True)
            else:
                item.setHidden(False)
            
            

    def spam_music(self):
        """
        Music spam :) Get current track info, forming dict with data and
        send it to new post dialog.
        """
        music_data = self.np.get_music_info(self.settings["player"])
        if music_data == "failed-connect":
            QMessageBox.critical(self, "QTDenter - FAIL!", "Failed to connect to server!")
        elif music_data == "not-running":
            QMessageBox.critical(self, "QTDenter - FAIL!", "{0} not running!".format(self.settings["player"]))
        elif music_data == "failed-getsong" or music_data["condition"] == "FAIL":
            QMessageBox.critical(self, "QTDenter - FAIL!", "Failed to get track data!")
        else:
            spam_string = self.qsettings.value("player_string").toString()
            if "artist" in music_data:
                spam_string = spam_string.replace("$artist", music_data["artist"])
            else:
                spam_string = spam_string.replace("$artist", "No artist")
            if "album" in music_data:
                spam_string = spam_string.replace("$album", music_data["album"])
            else:
                spam_string = spam_string.replace("$album", "No album")
            if "trackname" in music_data:
                spam_string = spam_string.replace("$trackname", music_data["trackname"])
            else:
                spam_string = spam_string.replace("$trackname", "No title")
            spam_string = spam_string.replace("$player", str(self.settings["player"]).lower())
            spam_string = spam_string.replace("\"", "")
            params = {
                        "text": spam_string,
                        "direct": False,
                        "type": "insert"
                    }
            newpostD = new_post.New_Post(self.settings["messageLength"], params, self.new_post_callback)
            newpostD.exec_()

    def check_for_visibility(self):
        """
        Checking for window visibility.
        """
        if self._hidden == 0:
            self.hide()
            self._hidden = 1
        else:
            self.show()
            self._hidden = 0
            
    def show_window(self):
        """
        Show window on notification click
        """
        self.show()
        self._hidden = 0

    def show_options_dialog(self):
        """
        Show options dialog
        """
        settingsD = options_dialog.Options_Dialog(self.settings, self.change_settings)
        settingsD.exec_()

    def change_settings(self, data):
        """
        Callback for options dialog for settings change, timer restart
        and redefining connector instance.
        """
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
        self.settings["mpd_host"] = data[10]
        self.settings["mpd_port"] = data[11]
        self.init_connector()
        self.start_timer(self.settings["updateInterval"])
        
        if self._changed_credentials == True:
            self.ui.timeline_list.clear()
            self.update_timelines()
            self._changed_credentials = False
        
    def show_about(self):
        """
        Show about dialog
        """
        aboutW = QDialog()
        aboutW.ui = About.Ui_Dialog()
        aboutW.ui.setupUi(aboutW)
        aboutW.exec_()

    def show_information(self):
        """
        Show server information
        """
        data = self.auth.get_server_config("config")
        server_version = self.auth.get_server_config("version")
        infoD = information.Information_Dialog(data, server_version, VERSION)
        infoD.exec_()

    def close_from_tray(self):
        self.close()

    def close_from_menu(self):
        self.close()

    def closeEvent(self, event):
        """
        CloseEvent override, for settings saving
        """
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
            self.qsettings.setValue("mpd_host", self.settings["mpd_host"])
            self.qsettings.setValue("mpd_port", self.settings["mpd_port"])
            self.qsettings.setValue("state", self.saveState())
            self.qsettings.setValue("geometry", self.saveGeometry())
            self.qsettings.setValue("filters_state", self._filters_state.join(":"))
            if self.settings["remember_last_dent_id"] == "1":
                root = self.ui.timeline_list.invisibleRootItem()
                last_item = root.child(0)
                dent_id = last_item.text(2).split(":")[0]
                self.qsettings.setValue("last_dent_id", dent_id)
            
            # Filters buttons checkstates
            
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mbc = Denter_Form()
    mbc.show()
    sys.exit(app.exec_())
