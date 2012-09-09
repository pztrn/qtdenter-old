# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'context.ui'
#
# Created: Sun Sep  9 16:31:35 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(561, 718)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.context = QtGui.QTreeWidget(Dialog)
        self.context.setMinimumSize(QtCore.QSize(0, 0))
        self.context.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.context.setMouseTracking(True)
        self.context.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged|QtGui.QAbstractItemView.DoubleClicked)
        self.context.setAlternatingRowColors(True)
        self.context.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.context.setIconSize(QtCore.QSize(64, 64))
        self.context.setTextElideMode(QtCore.Qt.ElideRight)
        self.context.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.context.setIndentation(0)
        self.context.setUniformRowHeights(False)
        self.context.setItemsExpandable(False)
        self.context.setAnimated(True)
        self.context.setWordWrap(False)
        self.context.setObjectName(_fromUtf8("context"))
        self.context.header().setVisible(False)
        self.context.header().setDefaultSectionSize(100)
        self.gridLayout.addWidget(self.context, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Context", None, QtGui.QApplication.UnicodeUTF8))
        self.context.setSortingEnabled(True)
        self.context.headerItem().setText(0, QtGui.QApplication.translate("Dialog", "Avatar", None, QtGui.QApplication.UnicodeUTF8))
        self.context.headerItem().setText(1, QtGui.QApplication.translate("Dialog", "Dent", None, QtGui.QApplication.UnicodeUTF8))
        self.context.headerItem().setText(2, QtGui.QApplication.translate("Dialog", "dent_id", None, QtGui.QApplication.UnicodeUTF8))
        self.context.headerItem().setText(3, QtGui.QApplication.translate("Dialog", "denter_screen_name", None, QtGui.QApplication.UnicodeUTF8))
        self.context.headerItem().setText(4, QtGui.QApplication.translate("Dialog", "dent_text", None, QtGui.QApplication.UnicodeUTF8))

