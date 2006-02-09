# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cloned_card_types_list_dlg.ui'
#
# Created: Wed May 20 22:10:56 2009
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ClonedCardTypesListDlg(object):
    def setupUi(self, ClonedCardTypesListDlg):
        ClonedCardTypesListDlg.setObjectName("ClonedCardTypesListDlg")
        ClonedCardTypesListDlg.resize(300,240)
        ClonedCardTypesListDlg.setMinimumSize(QtCore.QSize(300,240))
        self.verticalLayout_2 = QtGui.QVBoxLayout(ClonedCardTypesListDlg)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtGui.QLabel(ClonedCardTypesListDlg)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.cloned_card_types = QtGui.QListWidget(ClonedCardTypesListDlg)
        self.cloned_card_types.setObjectName("cloned_card_types")
        self.verticalLayout.addWidget(self.cloned_card_types)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_button = QtGui.QPushButton(ClonedCardTypesListDlg)
        self.add_button.setObjectName("add_button")
        self.horizontalLayout.addWidget(self.add_button)
        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.help_button = QtGui.QPushButton(ClonedCardTypesListDlg)
        self.help_button.setObjectName("help_button")
        self.horizontalLayout.addWidget(self.help_button)
        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.exit_button = QtGui.QPushButton(ClonedCardTypesListDlg)
        self.exit_button.setObjectName("exit_button")
        self.horizontalLayout.addWidget(self.exit_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(ClonedCardTypesListDlg)
        QtCore.QObject.connect(self.exit_button,QtCore.SIGNAL("clicked()"),ClonedCardTypesListDlg.accept)
        QtCore.QObject.connect(self.help_button,QtCore.SIGNAL("clicked()"),ClonedCardTypesListDlg.help)
        QtCore.QObject.connect(self.add_button,QtCore.SIGNAL("clicked()"),ClonedCardTypesListDlg.clone_card_type)
        QtCore.QMetaObject.connectSlotsByName(ClonedCardTypesListDlg)

    def retranslateUi(self, ClonedCardTypesListDlg):
        ClonedCardTypesListDlg.setWindowTitle(QtGui.QApplication.translate("ClonedCardTypesListDlg", "Cloned card types", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ClonedCardTypesListDlg", "Cloned card types in use in this deck:", None, QtGui.QApplication.UnicodeUTF8))
        self.add_button.setText(QtGui.QApplication.translate("ClonedCardTypesListDlg", "&Add clone", None, QtGui.QApplication.UnicodeUTF8))
        self.help_button.setText(QtGui.QApplication.translate("ClonedCardTypesListDlg", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.exit_button.setText(QtGui.QApplication.translate("ClonedCardTypesListDlg", "E&xit", None, QtGui.QApplication.UnicodeUTF8))

