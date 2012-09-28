# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created: Fri Sep 28 05:42:22 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(582, 794)
        MainWindow.setFocusPolicy(QtCore.Qt.NoFocus)
        MainWindow.setStyleSheet(_fromUtf8(""))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.accounts_widget = QtGui.QWidget(self.centralwidget)
        self.accounts_widget.setObjectName(_fromUtf8("accounts_widget"))
        self.gridLayout = QtGui.QGridLayout(self.accounts_widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.accounts_layout = QtGui.QHBoxLayout()
        self.accounts_layout.setObjectName(_fromUtf8("accounts_layout"))
        self.timeline_btn = QtGui.QPushButton(self.accounts_widget)
        self.timeline_btn.setMinimumSize(QtCore.QSize(32, 32))
        self.timeline_btn.setMaximumSize(QtCore.QSize(32, 32))
        self.timeline_btn.setText(_fromUtf8(""))
        self.timeline_btn.setIconSize(QtCore.QSize(28, 28))
        self.timeline_btn.setCheckable(True)
        self.timeline_btn.setObjectName(_fromUtf8("timeline_btn"))
        self.accounts_layout.addWidget(self.timeline_btn)
        self.mentions_btn = QtGui.QPushButton(self.accounts_widget)
        self.mentions_btn.setMinimumSize(QtCore.QSize(32, 32))
        self.mentions_btn.setMaximumSize(QtCore.QSize(32, 32))
        self.mentions_btn.setText(_fromUtf8(""))
        self.mentions_btn.setIconSize(QtCore.QSize(28, 28))
        self.mentions_btn.setCheckable(True)
        self.mentions_btn.setObjectName(_fromUtf8("mentions_btn"))
        self.accounts_layout.addWidget(self.mentions_btn)
        self.directs_btn = QtGui.QPushButton(self.accounts_widget)
        self.directs_btn.setMinimumSize(QtCore.QSize(32, 32))
        self.directs_btn.setMaximumSize(QtCore.QSize(32, 32))
        self.directs_btn.setText(_fromUtf8(""))
        self.directs_btn.setIconSize(QtCore.QSize(28, 28))
        self.directs_btn.setCheckable(True)
        self.directs_btn.setObjectName(_fromUtf8("directs_btn"))
        self.accounts_layout.addWidget(self.directs_btn)
        self.line = QtGui.QFrame(self.accounts_widget)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.accounts_layout.addWidget(self.line)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.accounts_layout.addItem(spacerItem)
        self.no_accounts_btn = QtGui.QPushButton(self.accounts_widget)
        self.no_accounts_btn.setEnabled(False)
        self.no_accounts_btn.setObjectName(_fromUtf8("no_accounts_btn"))
        self.accounts_layout.addWidget(self.no_accounts_btn)
        self.gridLayout.addLayout(self.accounts_layout, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.accounts_widget, 0, 0, 1, 1)
        self.timeline_list = QtGui.QTreeWidget(self.centralwidget)
        self.timeline_list.setMinimumSize(QtCore.QSize(0, 0))
        self.timeline_list.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.timeline_list.setMouseTracking(False)
        self.timeline_list.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.timeline_list.setStyleSheet(_fromUtf8(""))
        self.timeline_list.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged|QtGui.QAbstractItemView.DoubleClicked)
        self.timeline_list.setAlternatingRowColors(True)
        self.timeline_list.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.timeline_list.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.timeline_list.setIconSize(QtCore.QSize(64, 64))
        self.timeline_list.setTextElideMode(QtCore.Qt.ElideRight)
        self.timeline_list.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.timeline_list.setIndentation(0)
        self.timeline_list.setUniformRowHeights(False)
        self.timeline_list.setItemsExpandable(False)
        self.timeline_list.setAnimated(True)
        self.timeline_list.setWordWrap(False)
        self.timeline_list.setObjectName(_fromUtf8("timeline_list"))
        self.timeline_list.header().setVisible(False)
        self.timeline_list.header().setDefaultSectionSize(100)
        self.gridLayout_2.addWidget(self.timeline_list, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 582, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName(_fromUtf8("menu_File"))
        self.menu_Timelines = QtGui.QMenu(self.menubar)
        self.menu_Timelines.setObjectName(_fromUtf8("menu_Timelines"))
        self.menu_Help = QtGui.QMenu(self.menubar)
        self.menu_Help.setObjectName(_fromUtf8("menu_Help"))
        self.menuAddons = QtGui.QMenu(self.menubar)
        self.menuAddons.setObjectName(_fromUtf8("menuAddons"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setMovable(False)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_Options = QtGui.QAction(MainWindow)
        self.action_Options.setObjectName(_fromUtf8("action_Options"))
        self.action_Exit = QtGui.QAction(MainWindow)
        self.action_Exit.setObjectName(_fromUtf8("action_Exit"))
        self.action_Update_all = QtGui.QAction(MainWindow)
        self.action_Update_all.setObjectName(_fromUtf8("action_Update_all"))
        self.action_About_Denter = QtGui.QAction(MainWindow)
        self.action_About_Denter.setObjectName(_fromUtf8("action_About_Denter"))
        self.actionStatistics = QtGui.QAction(MainWindow)
        self.actionStatistics.setObjectName(_fromUtf8("actionStatistics"))
        self.actionSpam_Music_data = QtGui.QAction(MainWindow)
        self.actionSpam_Music_data.setObjectName(_fromUtf8("actionSpam_Music_data"))
        self.actionAbout_me = QtGui.QAction(MainWindow)
        self.actionAbout_me.setObjectName(_fromUtf8("actionAbout_me"))
        self.actionQTDenter_Documentation = QtGui.QAction(MainWindow)
        self.actionQTDenter_Documentation.setObjectName(_fromUtf8("actionQTDenter_Documentation"))
        self.action_Mark_all_unread = QtGui.QAction(MainWindow)
        self.action_Mark_all_unread.setObjectName(_fromUtf8("action_Mark_all_unread"))
        self.menu_File.addAction(self.action_Options)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Exit)
        self.menu_Timelines.addAction(self.action_Update_all)
        self.menu_Timelines.addSeparator()
        self.menu_Timelines.addAction(self.action_Mark_all_unread)
        self.menu_Help.addAction(self.actionStatistics)
        self.menu_Help.addAction(self.actionAbout_me)
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.actionQTDenter_Documentation)
        self.menu_Help.addAction(self.action_About_Denter)
        self.menuAddons.addAction(self.actionSpam_Music_data)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Timelines.menuAction())
        self.menubar.addAction(self.menuAddons.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "QTDenter", None, QtGui.QApplication.UnicodeUTF8))
        self.timeline_btn.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p>Show timeline dents</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.mentions_btn.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p>Show mentions</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.directs_btn.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p>Show direct messages</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.no_accounts_btn.setText(QtGui.QApplication.translate("MainWindow", "No accounts", None, QtGui.QApplication.UnicodeUTF8))
        self.timeline_list.setSortingEnabled(True)
        self.timeline_list.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Avatar", None, QtGui.QApplication.UnicodeUTF8))
        self.timeline_list.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "Dent", None, QtGui.QApplication.UnicodeUTF8))
        self.timeline_list.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "dent_id", None, QtGui.QApplication.UnicodeUTF8))
        self.timeline_list.headerItem().setText(3, QtGui.QApplication.translate("MainWindow", "denter_screen_name", None, QtGui.QApplication.UnicodeUTF8))
        self.timeline_list.headerItem().setText(4, QtGui.QApplication.translate("MainWindow", "dent_text", None, QtGui.QApplication.UnicodeUTF8))
        self.timeline_list.headerItem().setText(5, QtGui.QApplication.translate("MainWindow", "account", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Timelines.setTitle(QtGui.QApplication.translate("MainWindow", "&Timelines", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Help.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAddons.setTitle(QtGui.QApplication.translate("MainWindow", "Addons", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Options.setText(QtGui.QApplication.translate("MainWindow", "&Options", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Exit.setText(QtGui.QApplication.translate("MainWindow", "E&xit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Update_all.setText(QtGui.QApplication.translate("MainWindow", "&Update all", None, QtGui.QApplication.UnicodeUTF8))
        self.action_About_Denter.setText(QtGui.QApplication.translate("MainWindow", "&About QTDenter...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStatistics.setText(QtGui.QApplication.translate("MainWindow", "&Server Information...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSpam_Music_data.setText(QtGui.QApplication.translate("MainWindow", "Spam &Music data", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout_me.setText(QtGui.QApplication.translate("MainWindow", "About &me...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQTDenter_Documentation.setText(QtGui.QApplication.translate("MainWindow", "QTDenter &Documentation", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Mark_all_unread.setText(QtGui.QApplication.translate("MainWindow", "&Mark all unread dents as read", None, QtGui.QApplication.UnicodeUTF8))

