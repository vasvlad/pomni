# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preview_cards_dlg.ui'
#
# Created: Wed May 20 22:10:56 2009
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreviewCardsDlg(object):
    def setupUi(self, PreviewCardsDlg):
        PreviewCardsDlg.setObjectName("PreviewCardsDlg")
        PreviewCardsDlg.resize(307,311)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(PreviewCardsDlg)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.fact_view_name = QtGui.QLabel(PreviewCardsDlg)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.fact_view_name.setFont(font)
        self.fact_view_name.setObjectName("fact_view_name")
        self.verticalLayout.addWidget(self.fact_view_name)
        self.question_label = QtGui.QLabel(PreviewCardsDlg)
        self.question_label.setMaximumSize(QtCore.QSize(320,16777215))
        self.question_label.setObjectName("question_label")
        self.verticalLayout.addWidget(self.question_label)
        self.question = QtWebKit.QWebView(PreviewCardsDlg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.question.sizePolicy().hasHeightForWidth())
        self.question.setSizePolicy(sizePolicy)
        self.question.setMinimumSize(QtCore.QSize(295,100))
        self.question.setUrl(QtCore.QUrl("about:blank"))
        self.question.setObjectName("question")
        self.verticalLayout.addWidget(self.question)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.answer_label = QtGui.QLabel(PreviewCardsDlg)
        self.answer_label.setObjectName("answer_label")
        self.verticalLayout_2.addWidget(self.answer_label)
        self.answer = QtWebKit.QWebView(PreviewCardsDlg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.answer.sizePolicy().hasHeightForWidth())
        self.answer.setSizePolicy(sizePolicy)
        self.answer.setMinimumSize(QtCore.QSize(295,100))
        self.answer.setUrl(QtCore.QUrl("about:blank"))
        self.answer.setObjectName("answer")
        self.verticalLayout_2.addWidget(self.answer)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.OK_button = QtGui.QPushButton(PreviewCardsDlg)
        self.OK_button.setObjectName("OK_button")
        self.horizontalLayout.addWidget(self.OK_button)
        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.previous_button = QtGui.QPushButton(PreviewCardsDlg)
        self.previous_button.setObjectName("previous_button")
        self.horizontalLayout.addWidget(self.previous_button)
        self.next_button = QtGui.QPushButton(PreviewCardsDlg)
        self.next_button.setObjectName("next_button")
        self.horizontalLayout.addWidget(self.next_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(PreviewCardsDlg)
        QtCore.QObject.connect(self.previous_button,QtCore.SIGNAL("clicked()"),PreviewCardsDlg.previous)
        QtCore.QObject.connect(self.next_button,QtCore.SIGNAL("clicked()"),PreviewCardsDlg.next)
        QtCore.QObject.connect(self.OK_button,QtCore.SIGNAL("clicked()"),PreviewCardsDlg.close)
        QtCore.QMetaObject.connectSlotsByName(PreviewCardsDlg)

    def retranslateUi(self, PreviewCardsDlg):
        PreviewCardsDlg.setWindowTitle(QtGui.QApplication.translate("PreviewCardsDlg", "Preview cards", None, QtGui.QApplication.UnicodeUTF8))
        self.fact_view_name.setText(QtGui.QApplication.translate("PreviewCardsDlg", "(fact view name)", None, QtGui.QApplication.UnicodeUTF8))
        self.question_label.setText(QtGui.QApplication.translate("PreviewCardsDlg", "Question:", None, QtGui.QApplication.UnicodeUTF8))
        self.answer_label.setText(QtGui.QApplication.translate("PreviewCardsDlg", "Answer:", None, QtGui.QApplication.UnicodeUTF8))
        self.OK_button.setText(QtGui.QApplication.translate("PreviewCardsDlg", "&OK", None, QtGui.QApplication.UnicodeUTF8))
        self.previous_button.setText(QtGui.QApplication.translate("PreviewCardsDlg", "&Previous", None, QtGui.QApplication.UnicodeUTF8))
        self.next_button.setText(QtGui.QApplication.translate("PreviewCardsDlg", "&Next", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
