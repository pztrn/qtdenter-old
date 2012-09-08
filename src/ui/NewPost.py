# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newpost.ui'
#
# Created: Mon Jan 30 17:41:39 2012
#      by: PyQt4 UI code generator 4.9
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
        Dialog.resize(352, 195)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.postData = QtGui.QPlainTextEdit(Dialog)
        self.postData.setObjectName(_fromUtf8("postData"))
        self.verticalLayout.addWidget(self.postData)
        self.symbolCount = QtGui.QLabel(Dialog)
        self.symbolCount.setText(_fromUtf8(""))
        self.symbolCount.setObjectName(_fromUtf8("symbolCount"))
        self.verticalLayout.addWidget(self.symbolCount)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.cancelButton = QtGui.QPushButton(Dialog)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.postButton = QtGui.QPushButton(Dialog)
        self.postButton.setObjectName(_fromUtf8("postButton"))
        self.horizontalLayout.addWidget(self.postButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "mbc - New Post", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "What do you feel or think?", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.postButton.setText(QtGui.QApplication.translate("Dialog", "Post", None, QtGui.QApplication.UnicodeUTF8))
        self.postButton.setShortcut(QtGui.QApplication.translate("Dialog", "Ctrl+Return", None, QtGui.QApplication.UnicodeUTF8))

