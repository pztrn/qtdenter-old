# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created: Sat Sep  8 23:30:11 2012
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
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(715, 581)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.accountName = QtGui.QLineEdit(self.tab)
        self.accountName.setObjectName(_fromUtf8("accountName"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.accountName)
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.serverName = QtGui.QLineEdit(self.tab)
        self.serverName.setObjectName(_fromUtf8("serverName"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.serverName)
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.password = QtGui.QLineEdit(self.tab)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName(_fromUtf8("password"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.password)
        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_4)
        self.suiCheckbox = QtGui.QCheckBox(self.tab)
        self.suiCheckbox.setText(_fromUtf8(""))
        self.suiCheckbox.setObjectName(_fromUtf8("suiCheckbox"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.suiCheckbox)
        self.label_7 = QtGui.QLabel(self.tab)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_7)
        self.useSecureConnectionCheckbox = QtGui.QCheckBox(self.tab)
        self.useSecureConnectionCheckbox.setText(_fromUtf8(""))
        self.useSecureConnectionCheckbox.setObjectName(_fromUtf8("useSecureConnectionCheckbox"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.useSecureConnectionCheckbox)
        self.mllabel = QtGui.QLabel(self.tab)
        self.mllabel.setEnabled(False)
        self.mllabel.setObjectName(_fromUtf8("mllabel"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.mllabel)
        self.messageLength = QtGui.QLineEdit(self.tab)
        self.messageLength.setEnabled(False)
        self.messageLength.setObjectName(_fromUtf8("messageLength"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.messageLength)
        self.gridLayout_2.addLayout(self.formLayout, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.tab)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab1 = QtGui.QWidget()
        self.tab1.setObjectName(_fromUtf8("tab1"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tab1)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_5 = QtGui.QLabel(self.tab1)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_5)
        self.removePostsOnExitCheckbox = QtGui.QCheckBox(self.tab1)
        self.removePostsOnExitCheckbox.setText(_fromUtf8(""))
        self.removePostsOnExitCheckbox.setObjectName(_fromUtf8("removePostsOnExitCheckbox"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.removePostsOnExitCheckbox)
        self.label_9 = QtGui.QLabel(self.tab1)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_9)
        self.updateInterval = QtGui.QSpinBox(self.tab1)
        self.updateInterval.setWrapping(False)
        self.updateInterval.setFrame(True)
        self.updateInterval.setAccelerated(False)
        self.updateInterval.setPrefix(_fromUtf8(""))
        self.updateInterval.setMinimum(1)
        self.updateInterval.setMaximum(1000)
        self.updateInterval.setObjectName(_fromUtf8("updateInterval"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.updateInterval)
        self.gridLayout_3.addLayout(self.formLayout_2, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 4, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.tab1)
        self.label_8.setWordWrap(True)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_3.addWidget(self.label_8, 3, 0, 1, 1)
        self.tabWidget.addTab(self.tab1, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.cancelButton = QtGui.QPushButton(Dialog)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.okButton = QtGui.QPushButton(Dialog)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout.addWidget(self.okButton)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "mbc Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Account name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Server:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Single user installation?", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "Use secure connection?", None, QtGui.QApplication.UnicodeUTF8))
        self.mllabel.setText(QtGui.QApplication.translate("Dialog", "Message length:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PT Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<hr />\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Please, enter your credentials in this fields.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">If you use <a href=\"http://identi.ca/\"><span style=\" text-decoration: underline; color:#0000ff;\">identi.ca</span></a> service or if you know, that service you use provide authorization through secure connection - select &quot;<span style=\" font-weight:600; font-style:italic;\">Use secure connection</span>&quot;. Please note, that authorization goes through &quot;Basic auth&quot;, that means your login and password will be sent to server as plaintext.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">If you use standalone status.net installation - you can choose &quot;<span style=\" font-weight:600; font-style:italic;\">Single user installation</span>&quot; and specify maximum message length. Otherwise message length will be limited to 140 symbols.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Dialog", "Account", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Remove all posts from cache on exit?", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("Dialog", "Update interval:", None, QtGui.QApplication.UnicodeUTF8))
        self.updateInterval.setSuffix(QtGui.QApplication.translate("Dialog", " minutes", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PT Sans\'; font-size:10pt; font-weight:400; font-style:normal;\"><hr>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Select &quot;<span style=\" font-weight:600; font-style:italic;\">Remove all posts from cache on exit</span>&quot; if you want to. But it could result in slower startup.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), QtGui.QApplication.translate("Dialog", "Timelines", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("Dialog", "Save and close", None, QtGui.QApplication.UnicodeUTF8))

