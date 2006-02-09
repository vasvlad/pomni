# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'convert_card_type_fields_dlg.ui'
#
# Created: Wed May 20 22:10:56 2009
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ConvertCardTypeFieldsDlg(object):
    def setupUi(self, ConvertCardTypeFieldsDlg):
        ConvertCardTypeFieldsDlg.setObjectName("ConvertCardTypeFieldsDlg")
        ConvertCardTypeFieldsDlg.resize(260,105)
        self.verticalLayout_2 = QtGui.QVBoxLayout(ConvertCardTypeFieldsDlg)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtGui.QLabel(ConvertCardTypeFieldsDlg)
        self.label_2.setMinimumSize(QtCore.QSize(250,40))
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(ConvertCardTypeFieldsDlg)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label,0,0,1,1)
        self.label_3 = QtGui.QLabel(ConvertCardTypeFieldsDlg)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3,0,1,1,1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ok_button = QtGui.QPushButton(ConvertCardTypeFieldsDlg)
        self.ok_button.setDefault(True)
        self.ok_button.setObjectName("ok_button")
        self.horizontalLayout.addWidget(self.ok_button)
        spacerItem = QtGui.QSpacerItem(208,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cancel_button = QtGui.QPushButton(ConvertCardTypeFieldsDlg)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(ConvertCardTypeFieldsDlg)
        QtCore.QObject.connect(self.ok_button,QtCore.SIGNAL("clicked()"),ConvertCardTypeFieldsDlg.accept)
        QtCore.QObject.connect(self.cancel_button,QtCore.SIGNAL("clicked()"),ConvertCardTypeFieldsDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(ConvertCardTypeFieldsDlg)

    def retranslateUi(self, ConvertCardTypeFieldsDlg):
        ConvertCardTypeFieldsDlg.setWindowTitle(QtGui.QApplication.translate("ConvertCardTypeFieldsDlg", "Convert card type fields", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ConvertCardTypeFieldsDlg", "Set the correspondence between fields in the old and the new card type:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ConvertCardTypeFieldsDlg", "Old:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ConvertCardTypeFieldsDlg", "New:", None, QtGui.QApplication.UnicodeUTF8))
        self.ok_button.setText(QtGui.QApplication.translate("ConvertCardTypeFieldsDlg", "&OK", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_button.setText(QtGui.QApplication.translate("ConvertCardTypeFieldsDlg", "&Cancel", None, QtGui.QApplication.UnicodeUTF8))

