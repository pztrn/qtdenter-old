#!/usr/bin/python2
# -*- coding: utf8 -*-

import os, sys, json, urllib2, ConfigParser, time, commands
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui import MainWindow, Settings, NewPost, About, Stat
from lib import database, list_handler, list_item
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

        self._hidden = 0
        self.inserted_dents_ids = []
        self._new_dents = 0
        self._changed_credentials = False
        
        # Tray icon
        self.trayIcon = QSystemTrayIcon(QIcon("ui/imgs/trayicon.png"), self)
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
        except:
            QMessageBox.critical(self, "denter - No accounts", "Setup an account in Options!")

        try:
            self.settings["messageLength"] = self.qsettings.value("messageLength").toString()
        except:
            self.settings["messageLength"] = 140

        try:
            self.restoreGeometry(self.qsettings.value("geometry").toByteArray())
            self.restoreState(self.qsettings.value("state").toByteArray())
        except:
            pass

        if not os.path.exists(os.path.expanduser("~/.config/qtdenter/data.sqlite")):
            database.createDB()

        self.ui.action_Options.triggered.connect(self.show_options_dialog)
        self.ui.action_Exit.triggered.connect(self.close_from_menu)
        self.ui.action_About_Denter.triggered.connect(self.show_about)
        self.ui.actionStatistics.triggered.connect(self.show_statistics)

        self.connect(self, SIGNAL("PostData(PyQt_PyObject)"), self.post_status)
        self.connect(self, SIGNAL("ChangeSettings(PyQt_PyObject)"), self.change_settings)
        self.connect(self, SIGNAL("ShowForm()"), self.check_for_visibility)
        self.connect(self, SIGNAL("HideForm()"), self.check_for_visibility)
        self.connect(self, SIGNAL("ShowOptions()"), self.show_options_dialog)
        self.connect(self, SIGNAL("Close()"), self.close_from_tray)

        newPostIcon = iconFromTheme("add")
        newPost = QAction(newPostIcon, "New post", self)
        newPost.setShortcut("Ctrl+N")
        newPost.triggered.connect(self.post_status_dialog)

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
        self.ui.timeline_list.setColumnHidden(2, True)
        self.ui.timeline_list.setColumnHidden(3, True)
        self.ui.timeline_list.setColumnWidth(0, 50)
        
        # Init notifications
        try:
            pynotify.init(sys.argv[0])
            print "Notifier loaded"
        except:
            print "Failed to init pynotify"
            
        self.show()
        # Initialize auther
        try:
            self.init_connector()
        
            home_timeline = self.auth.get_home_timeline()
            self.list_handler.add_data("home", home_timeline)
        except:
            print "No auth data specified"
            
        # Init timer
        self.start_timer(self.settings["updateInterval"])
        
            
    def init_connector(self):
        self.auth = connector.Requester(self.settings["user"], self.settings["password"], self.settings["server"] + "/api/", self.settings["useSecureConnection"])
        
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
        home_timeline = self.auth.get_home_timeline()
        self.list_handler.add_data("home", home_timeline)
            
    def lists_callback(self, list_type, data):
        if list_type == "home":
            self.add_to_timeline_iterator(data)
        elif list_type == "home_avatar":
            self.update_timeline_avatar(data)
        elif list_type == "end":
            curtime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            self.time_updated_action.setText("<b>Last updated on: {0}</b>".format(curtime))
            
            # Notifications
            notify = pynotify.Notification("qtdenter", "{0} new dents arrived.".format(self._new_dents), None)
            notify.set_urgency(pynotify.URGENCY_NORMAL)
            notify.set_timeout(pynotify.EXPIRES_NEVER)
            notify.add_action("clicked","Show QTDenter", self.show_window, None)
            notify.show()
            self._new_dents = 0
            
            
    def add_to_timeline_iterator(self, data):
        if data["id"] not in self.inserted_dents_ids:
            self.inserted_dents_ids.append(data["id"])
            self.add_to_timeline(data)
            self._new_dents += 1
        else:
            pass
                    
    def add_to_timeline(self, data):
        post_data = QLabel()
        avatar_data = QLabel()
        post_data.setText(QString.fromUtf8("<b>{0}</b> <span style='font-size:8pt;'>{2}</span><br/>{1}<br/><br/><span style='font-size:8pt;'>id {3}, from {4}".format(data["nickname"], data["text"], data["date"], data["id"], data["source"])))
        post_data.setWordWrap(True)
        post_data.setAlignment(Qt.AlignTop)
        post_data.setOpenExternalLinks(True)
        post_data.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.ui.timeline_list.update()
        post_data.setMinimumSize(300, 64)
        item = QTreeWidgetItem()
        
        extension = data["avatar"].split(".")[-1:][0]
        avatar = os.path.expanduser("~/.local/share/qtdenter/avatars/") + "%s.%s" % (data["nickname"], extension)
        avatar_data.setText("<img src='{0}' height=48 width=48 />".format(avatar))
        avatar_data.setMinimumSize(0, 0)
        avatar_data.setMaximumSize(48, 48)
        avatar_data.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        item.setText(2, str(data["id"]))
        item.setText(3, data["nickname"])
        
        self.ui.timeline_list.addTopLevelItem(item)
        self.ui.timeline_list.setItemWidget(item, 0, avatar_data)
        self.ui.timeline_list.setItemWidget(item, 1, post_data)
        
    def update_timeline_avatar(self, name):
        print name

    def post_status(self, data):
        data = self.auth.post_dent(data, VERSION)
        self.list_handler.add_data("home", [data])

    def post_status_dialog(self):
        newpostD = NewPostDialog(self.settings["messageLength"], None)
        newpostD.exec_()

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
        settingsD = SettingsDialog(self.settings)
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
        self.settings["isSingle"] = data[4]
        self.settings["messageLength"] = data[5]
        self.settings["deleteAllFromCacheOnExit"] = data[6]
        self.settings["updateInterval"] = data[7]
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

    def show_statistics(self):
        statD = StatisticsDialog()
        statD.exec_()

    def close_from_tray(self):
        self.close()

    def close_from_menu(self):
        self.close()

    def closeEvent(self, event):
        box = QMessageBox()
        box.setWindowTitle("mbc - Exiting")
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
            self.qsettings.setValue("isSingle", self.settings["isSingle"])
            self.qsettings.setValue("messageLength", self.settings["messageLength"])
            self.qsettings.setValue("deleteAllFromCacheOnExit", self.settings["deleteAllFromCacheOnExit"])
            self.qsettings.setValue("updateInterval", self.settings["updateInterval"])
            self.qsettings.setValue("state", self.saveState())
            self.qsettings.setValue("geometry", self.saveGeometry())
        else:
            event.ignore()

class NewPostDialog(QDialog):
    def __init__(self, messageLength, nickname, parent = None):
        QDialog.__init__(self, parent)
        self.ui = NewPost.Ui_Dialog()
        self.ui.setupUi(self)

        self.messageLength = int(messageLength)
        if nickname:
            self.ui.postData.appendPlainText(nickname + " ")

        self._messageIsTooLong = 0

        self.ui.postData.textChanged.connect(self.countCharacters)
        self.ui.postButton.clicked.connect(self.postData)
        self.ui.cancelButton.clicked.connect(self.close)

    def countCharacters(self):
        self.textLenght = len(self.ui.postData.toPlainText())
        self.enteredSymbols = self.messageLength - self.textLenght
        if self.enteredSymbols < 0:
            self.ui.symbolCount.setText("<div style='color:red; font-weight:bold;'>" + str(self.enteredSymbols) + "/" + str(self.messageLength) + "</div>")
            self._messageIsTooLong = 1
        else:
            self.ui.symbolCount.setText(str(self.enteredSymbols) + "/" + str(self.messageLength))
            self._messageIsTooLong = 0

    def postData(self):
        if self._messageIsTooLong == 1:
            QMessageBox.critical(self, self.tr("New post - Message is too long"), self.tr("Message you entered is too long. Maximum message length is {0} symbols, you entered {1} symbols.").format(str(self.messageLength)).arg(str(self.textLenght)))
        else:
            try:
                mbc.emit(SIGNAL("PostData(PyQt_PyObject)"), str(QString.toUtf8(self.ui.postData.toPlainText())))
            except:
                print "FAILED TO SIGNAL!"

        self.close()


class SettingsDialog(QDialog):
    def __init__(self, settings, parent = None):
        QDialog.__init__(self, parent)
        self.ui = Settings.Ui_Dialog()
        self.ui.setupUi(self)

        self.settings = settings
        self.ui.accountName.setText(self.settings["user"])
        self.ui.serverName.setText(self.settings["server"])
        self.ui.password.setText(self.settings["password"])
        if self.settings["useSecureConnection"] == "1":
            self.ui.useSecureConnectionCheckbox.setCheckState(2)
        else:
            self.ui.useSecureConnectionCheckbox.setCheckState(0)
        if self.settings["isSingle"] == "1":
            self.ui.suiCheckbox.setCheckState(2)
            self.ui.mllabel.setEnabled(True)
            self.ui.messageLength.setEnabled(True)
        else:
            self.ui.suiCheckbox.setCheckState(0)
            self.ui.mllabel.setEnabled(False)
            self.ui.messageLength.setEnabled(False)
        self.ui.messageLength.setText(self.settings["messageLength"])
        if self.settings["deleteAllFromCacheOnExit"] == "1":
            self.ui.removePostsOnExitCheckbox.setCheckState(2)
        else:
            self.ui.removePostsOnExitCheckbox.setCheckState(0)
        try:
            self.ui.updateInterval.setValue(int(self.settings["updateInterval"]))
        except:
            self.ui.updateInterval.setValue(10)

        self.ui.okButton.clicked.connect(self.transmitSettings)
        self.ui.cancelButton.clicked.connect(self.close)
        
        self.ui.suiCheckbox.stateChanged.connect(self.changing_state_of_checkbox)
        
    def changing_state_of_checkbox(self):
        if self.ui.suiCheckbox.checkState() == 0:
            self.ui.messageLength.setEnabled(False)
        else:
            self.ui.messageLength.setEnabled(True)

    def transmitSettings(self):
        settingslist = []
        settingslist.append(str(self.ui.accountName.text()))
        settingslist.append(str(self.ui.password.text()))
        settingslist.append(str(self.ui.serverName.text()))
        if self.ui.useSecureConnectionCheckbox.isChecked():
            settingslist.append(str(1))
        else:
            settingslist.append(str(0))
        if self.ui.suiCheckbox.isChecked():
            settingslist.append(str(1))
        else:
            settingslist.append(str(0))
        if self.ui.messageLength.text():
            settingslist.append(str(self.ui.messageLength.text()))
        else:
            settingslist.append(str(140))
        if self.ui.removePostsOnExitCheckbox.isChecked():
            settingslist.append(str(1))
        else:
            settingslist.append(str(0))
        settingslist.append(self.ui.updateInterval.value())

        mbc.emit(SIGNAL("ChangeSettings(PyQt_PyObject)"), settingslist)
        self.close()

class StatisticsDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.ui = Stat.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.closeDialog.clicked.connect(self.close)

        self.ui.appVer.setText(VERSION)
        self.ui.dbsize.setText(self.getDatabaseSize())

    def getDatabaseSize(self):
        rawsize = os.path.getsize(os.path.expanduser("~/.config/qtdenter/data.sqlite"))
        size = rawsize / 1024

        return str(size) + " " + self.tr("Kbytes")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mbc = Denter_Form()
    mbc.show()
    sys.exit(app.exec_())
