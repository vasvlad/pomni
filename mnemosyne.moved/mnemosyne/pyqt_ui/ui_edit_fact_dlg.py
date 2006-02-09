# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit_fact_dlg.ui'
#
# Created: Wed May 20 22:10:56 2009
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_EditFactDlg(object):
    def setupUi(self, EditFactDlg):
        EditFactDlg.setObjectName("EditFactDlg")
        EditFactDlg.resize(209,100)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(EditFactDlg)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setObjectName("gridlayout")
        self.label_2 = QtGui.QLabel(EditFactDlg)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,0,0,1,1)
        self.card_types = QtGui.QComboBox(EditFactDlg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.card_types.sizePolicy().hasHeightForWidth())
        self.card_types.setSizePolicy(sizePolicy)
        self.card_types.setObjectName("card_types")
        self.gridlayout.addWidget(self.card_types,0,1,1,1)
        self.label = QtGui.QLabel(EditFactDlg)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,1,0,1,1)
        self.categories = QtGui.QComboBox(EditFactDlg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.categories.sizePolicy().hasHeightForWidth())
        self.categories.setSizePolicy(sizePolicy)
        self.categories.setEditable(True)
        self.categories.setObjectName("categories")
        self.gridlayout.addWidget(self.categories,1,1,1,1)
        self.verticalLayout.addLayout(self.gridlayout)
        self.button_row = QtGui.QHBoxLayout()
        self.button_row.setObjectName("button_row")
        self.OK_button = QtGui.QPushButton(EditFactDlg)
        self.OK_button.setObjectName("OK_button")
        self.button_row.addWidget(self.OK_button)
        spacerItem = QtGui.QSpacerItem(70,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.button_row.addItem(spacerItem)
        self.preview_button = QtGui.QPushButton(EditFactDlg)
        self.preview_button.setAutoDefault(False)
        self.preview_button.setObjectName("preview_button")
        self.button_row.addWidget(self.preview_button)
        spacerItem1 = QtGui.QSpacerItem(70,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.button_row.addItem(spacerItem1)
        self.exit_button = QtGui.QPushButton(EditFactDlg)
        self.exit_button.setAutoDefault(False)
        self.exit_button.setObjectName("exit_button")
        self.button_row.addWidget(self.exit_button)
        self.verticalLayout.addLayout(self.button_row)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(EditFactDlg)
        QtCore.QObject.connect(self.exit_button,QtCore.SIGNAL("clicked()"),EditFactDlg.reject)
        QtCore.QObject.connect(self.preview_button,QtCore.SIGNAL("clicked()"),EditFactDlg.preview)
        QtCore.QObject.connect(self.OK_button,QtCore.SIGNAL("clicked()"),EditFactDlg.accept)
        QtCore.QMetaObject.connectSlotsByName(EditFactDlg)

    def retranslateUi(self, EditFactDlg):
        EditFactDlg.setWindowTitle(QtGui.QApplication.translate("EditFactDlg", "Edit card", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("EditFactDlg", "Card type:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("EditFactDlg", "Categories:", None, QtGui.QApplication.UnicodeUTF8))
        self.OK_button.setText(QtGui.QApplication.translate("EditFactDlg", "&OK", None, QtGui.QApplication.UnicodeUTF8))
        self.preview_button.setText(QtGui.QApplication.translate("EditFactDlg", "&Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.exit_button.setText(QtGui.QApplication.translate("EditFactDlg", "E&xit", None, QtGui.QApplication.UnicodeUTF8))

import mnemosyne_rc
