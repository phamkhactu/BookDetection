# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow_Ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(908, 724)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(510, 60, 371, 301))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 369, 299))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(510, 400, 91, 41))
        self.label.setObjectName("label")
        self.btn_start = QtWidgets.QPushButton(self.centralwidget)
        self.btn_start.setGeometry(QtCore.QRect(40, 540, 91, 31))
        self.btn_start.setObjectName("btn_start")
        self.btn_close = QtWidgets.QPushButton(self.centralwidget)
        self.btn_close.setGeometry(QtCore.QRect(790, 610, 91, 31))
        self.btn_close.setObjectName("btn_close")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(510, 450, 111, 17))
        self.label_3.setObjectName("label_3")
        self.lable_status = QtWidgets.QLabel(self.centralwidget)
        self.lable_status.setGeometry(QtCore.QRect(670, 410, 67, 17))
        self.lable_status.setText("")
        self.lable_status.setObjectName("lable_status")
        self.label_da_doc = QtWidgets.QLabel(self.centralwidget)
        self.label_da_doc.setGeometry(QtCore.QRect(670, 450, 67, 17))
        self.label_da_doc.setText("")
        self.label_da_doc.setObjectName("label_da_doc")
        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.setGeometry(QtCore.QRect(50, 60, 381, 431))
        self.image.setText("")
        self.image.setObjectName("image")
        self.btn_stop = QtWidgets.QPushButton(self.centralwidget)
        self.btn_stop.setGeometry(QtCore.QRect(150, 540, 91, 31))
        self.btn_stop.setObjectName("btn_stop")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 908, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionStatitistics = QtWidgets.QAction(MainWindow)
        self.actionStatitistics.setObjectName("actionStatitistics")
        self.menuFile.addAction(self.actionAbout)
        self.menuFile.addAction(self.actionHelp)
        self.menuFile.addAction(self.actionStatitistics)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Trạng Thái:"))
        self.btn_start.setText(_translate("MainWindow", "Start"))
        self.btn_close.setText(_translate("MainWindow", "Close"))
        self.label_3.setText(_translate("MainWindow", "Tổng số đã đọc:"))
        self.btn_stop.setText(_translate("MainWindow", "Stop"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.actionStatitistics.setText(_translate("MainWindow", "Statitistics"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

