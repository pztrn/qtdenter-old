# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created: Fri Sep 21 16:54:07 2012
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
        MainWindow.resize(582, 790)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.North)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout_4 = QtGui.QGridLayout(self.tab)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.timeline_list = QtGui.QTreeWidget(self.tab)
        self.timeline_list.setMinimumSize(QtCore.QSize(0, 0))
        self.timeline_list.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.timeline_list.setMouseTracking(True)
        self.timeline_list.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged|QtGui.QAbstractItemView.DoubleClicked)
        self.timeline_list.setAlternatingRowColors(True)
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
        self.gridLayout_4.addWidget(self.timeline_list, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.gridLayout = QtGui.QGridLayout(self.tab_2)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.mentions_list = QtGui.QTreeWidget(self.tab_2)
        self.mentions_list.setMinimumSize(QtCore.QSize(0, 0))
        self.mentions_list.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.mentions_list.setMouseTracking(True)
        self.mentions_list.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged|QtGui.QAbstractItemView.DoubleClicked)
        self.mentions_list.setAlternatingRowColors(True)
        self.mentions_list.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.mentions_list.setIconSize(QtCore.QSize(64, 64))
        self.mentions_list.setTextElideMode(QtCore.Qt.ElideRight)
        self.mentions_list.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.mentions_list.setIndentation(0)
        self.mentions_list.setUniformRowHeights(False)
        self.mentions_list.setItemsExpandable(False)
        self.mentions_list.setAnimated(True)
        self.mentions_list.setWordWrap(False)
        self.mentions_list.setObjectName(_fromUtf8("mentions_list"))
        self.mentions_list.header().setVisible(False)
        self.mentions_list.header().setDefaultSectionSize(100)
        self.gridLayout.addWidget(self.mentions_list, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tab_3)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.dm_list = QtGui.QTreeWidget(self.tab_3)
        self.dm_list.setMinimumSize(QtCore.QSize(0, 0))
        self.dm_list.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.dm_list.setMouseTracking(True)
        self.dm_list.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged|QtGui.QAbstractItemView.DoubleClicked)
        self.dm_list.setAlternatingRowColors(True)
        self.dm_list.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.dm_list.setIconSize(QtCore.QSize(64, 64))
        self.dm_list.setTextElideMode(QtCore.Qt.ElideRight)
        self.dm_list.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.dm_list.setIndentation(0)
        self.dm_list.setUniformRowHeights(False)
        self.dm_list.setItemsExpandable(False)
        self.dm_list.setAnimated(True)
        self.dm_list.setWordWrap(False)
        self.dm_list.setObjectName(_fromUtf8("dm_list"))
        self.dm_list.header().setVisible(False)
        self.dm_list.header().setDefaultSectionSize(100)
        self.gridLayout_3.addWidget(self.dm_list, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 582, 24))
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
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "QTDenter", None, QtGui.QApplication.UnicodeUTF8))
        self.timeline_list.setSortingEnabled(True)
        self.timeline_list.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Avatar", None, QtGui.QApplication.UnicodeUTF8))
        self.timeline_list.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "Dent", None, QtGui.QApplication.UnicodeUTF8))
        self.timeline_list.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "dent_id", None, QtGui.QApplication.UnicodeUTF8))
        self.timeline_list.headerItem().setText(3, QtGui.QApplication.translate("MainWindow", "denter_screen_name", None, QtGui.QApplication.UnicodeUTF8))
        self.timeline_list.headerItem().setText(4, QtGui.QApplication.translate("MainWindow", "dent_text", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Timeline", None, QtGui.QApplication.UnicodeUTF8))
        self.mentions_list.setSortingEnabled(True)
        self.mentions_list.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Avatar", None, QtGui.QApplication.UnicodeUTF8))
        self.mentions_list.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "Dent", None, QtGui.QApplication.UnicodeUTF8))
        self.mentions_list.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "dent_id", None, QtGui.QApplication.UnicodeUTF8))
        self.mentions_list.headerItem().setText(3, QtGui.QApplication.translate("MainWindow", "denter_screen_name", None, QtGui.QApplication.UnicodeUTF8))
        self.mentions_list.headerItem().setText(4, QtGui.QApplication.translate("MainWindow", "dent_text", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "Mentions", None, QtGui.QApplication.UnicodeUTF8))
        self.dm_list.setSortingEnabled(True)
        self.dm_list.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Avatar", None, QtGui.QApplication.UnicodeUTF8))
        self.dm_list.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "Dent", None, QtGui.QApplication.UnicodeUTF8))
        self.dm_list.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "dent_id", None, QtGui.QApplication.UnicodeUTF8))
        self.dm_list.headerItem().setText(3, QtGui.QApplication.translate("MainWindow", "denter_screen_name", None, QtGui.QApplication.UnicodeUTF8))
        self.dm_list.headerItem().setText(4, QtGui.QApplication.translate("MainWindow", "dent_text", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("MainWindow", "Direct messages", None, QtGui.QApplication.UnicodeUTF8))
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

