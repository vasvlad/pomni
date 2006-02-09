# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'activate_plugins_dlg.ui'
#
# Created: Wed May 20 22:10:56 2009
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ActivatePluginsDlg(object):
    def setupUi(self, ActivatePluginsDlg):
        ActivatePluginsDlg.setObjectName("ActivatePluginsDlg")
        ActivatePluginsDlg.resize(500,250)
        ActivatePluginsDlg.setMinimumSize(QtCore.QSize(500,250))
        self.verticalLayout_2 = QtGui.QVBoxLayout(ActivatePluginsDlg)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.plugins = QtGui.QTreeView(ActivatePluginsDlg)
        self.plugins.setObjectName("plugins")
        self.verticalLayout.addWidget(self.plugins)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ok_button = QtGui.QPushButton(ActivatePluginsDlg)
        self.ok_button.setDefault(True)
        self.ok_button.setObjectName("ok_button")
        self.horizontalLayout.addWidget(self.ok_button)
        spacerItem = QtGui.QSpacerItem(13,38,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(ActivatePluginsDlg)
        QtCore.QObject.connect(self.ok_button,QtCore.SIGNAL("clicked()"),ActivatePluginsDlg.accept)
        QtCore.QMetaObject.connectSlotsByName(ActivatePluginsDlg)

    def retranslateUi(self, ActivatePluginsDlg):
        ActivatePluginsDlg.setWindowTitle(QtGui.QApplication.translate("ActivatePluginsDlg", "Activate plugins", None, QtGui.QApplication.UnicodeUTF8))
        self.ok_button.setText(QtGui.QApplication.translate("ActivatePluginsDlg", "&OK", None, QtGui.QApplication.UnicodeUTF8))

