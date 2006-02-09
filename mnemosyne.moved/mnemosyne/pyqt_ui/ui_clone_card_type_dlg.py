# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clone_card_type_dlg.ui'
#
# Created: Wed May 20 22:10:56 2009
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_CloneCardTypeDlg(object):
    def setupUi(self, CloneCardTypeDlg):
        CloneCardTypeDlg.setObjectName("CloneCardTypeDlg")
        CloneCardTypeDlg.resize(400,100)
        CloneCardTypeDlg.setMinimumSize(QtCore.QSize(400,100))
        self.verticalLayout_2 = QtGui.QVBoxLayout(CloneCardTypeDlg)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(CloneCardTypeDlg)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label,0,0,1,1)
        self.parent_type = QtGui.QComboBox(CloneCardTypeDlg)
        self.parent_type.setObjectName("parent_type")
        self.gridLayout.addWidget(self.parent_type,0,1,1,1)
        self.label_2 = QtGui.QLabel(CloneCardTypeDlg)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2,1,0,1,1)
        self.name = QtGui.QLineEdit(CloneCardTypeDlg)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name,1,1,1,1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.OK_button = QtGui.QPushButton(CloneCardTypeDlg)
        self.OK_button.setEnabled(False)
        self.OK_button.setObjectName("OK_button")
        self.horizontalLayout_3.addWidget(self.OK_button)
        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.cancel_button = QtGui.QPushButton(CloneCardTypeDlg)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout_3.addWidget(self.cancel_button)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(CloneCardTypeDlg)
        QtCore.QObject.connect(self.OK_button,QtCore.SIGNAL("clicked()"),CloneCardTypeDlg.accept)
        QtCore.QObject.connect(self.cancel_button,QtCore.SIGNAL("clicked()"),CloneCardTypeDlg.reject)
        QtCore.QObject.connect(self.name,QtCore.SIGNAL("textChanged(QString)"),CloneCardTypeDlg.name_changed)
        QtCore.QMetaObject.connectSlotsByName(CloneCardTypeDlg)

    def retranslateUi(self, CloneCardTypeDlg):
        CloneCardTypeDlg.setWindowTitle(QtGui.QApplication.translate("CloneCardTypeDlg", "Clone card type", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("CloneCardTypeDlg", "Cloned from:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("CloneCardTypeDlg", "Clone name:", None, QtGui.QApplication.UnicodeUTF8))
        self.OK_button.setText(QtGui.QApplication.translate("CloneCardTypeDlg", "&OK", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_button.setText(QtGui.QApplication.translate("CloneCardTypeDlg", "&Cancel", None, QtGui.QApplication.UnicodeUTF8))

