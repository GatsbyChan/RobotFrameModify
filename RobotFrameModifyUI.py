# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\RobotFrameModifyUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RobotFrameModifyUI(object):
    def setupUi(self, RobotFrameModifyUI):
        RobotFrameModifyUI.setObjectName("RobotFrameModifyUI")
        RobotFrameModifyUI.resize(1290, 860)
        self.centralwidget = QtWidgets.QWidget(RobotFrameModifyUI)
        self.centralwidget.setObjectName("centralwidget")
        self.VideoView = QtWidgets.QLabel(self.centralwidget)
        self.VideoView.setGeometry(QtCore.QRect(0, 49, 1280, 720))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.VideoView.sizePolicy().hasHeightForWidth())
        self.VideoView.setSizePolicy(sizePolicy)
        self.VideoView.setMinimumSize(QtCore.QSize(1280, 720))
        self.VideoView.setMaximumSize(QtCore.QSize(1280, 720))
        self.VideoView.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.VideoView.setText("")
        self.VideoView.setAlignment(QtCore.Qt.AlignCenter)
        self.VideoView.setObjectName("VideoView")
        self.MotorFrame = QtWidgets.QTableWidget(self.centralwidget)
        self.MotorFrame.setGeometry(QtCore.QRect(20, 560, 1231, 192))
        self.MotorFrame.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.MotorFrame.setObjectName("MotorFrame")
        self.MotorFrame.setColumnCount(0)
        self.MotorFrame.setRowCount(0)
        self.MotorMotion = QtWidgets.QTableWidget(self.centralwidget)
        self.MotorMotion.setGeometry(QtCore.QRect(20, 91, 291, 451))
        self.MotorMotion.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.MotorMotion.setObjectName("MotorMotion")
        self.MotorMotion.setColumnCount(0)
        self.MotorMotion.setRowCount(0)
        RobotFrameModifyUI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(RobotFrameModifyUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1290, 28))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        RobotFrameModifyUI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(RobotFrameModifyUI)
        self.statusbar.setObjectName("statusbar")
        RobotFrameModifyUI.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(RobotFrameModifyUI)
        self.toolBar.setObjectName("toolBar")
        RobotFrameModifyUI.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionFile_Open = QtWidgets.QAction(RobotFrameModifyUI)
        self.actionFile_Open.setObjectName("actionFile_Open")
        self.actionFile_Save = QtWidgets.QAction(RobotFrameModifyUI)
        self.actionFile_Save.setObjectName("actionFile_Save")
        self.actionFile_Save_as = QtWidgets.QAction(RobotFrameModifyUI)
        self.actionFile_Save_as.setObjectName("actionFile_Save_as")
        self.actionFile_Open_2 = QtWidgets.QAction(RobotFrameModifyUI)
        self.actionFile_Open_2.setObjectName("actionFile_Open_2")
        self.menuFile.addAction(self.actionFile_Open_2)
        self.menuFile.addAction(self.actionFile_Save)
        self.menuFile.addAction(self.actionFile_Save_as)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(RobotFrameModifyUI)
        QtCore.QMetaObject.connectSlotsByName(RobotFrameModifyUI)

    def retranslateUi(self, RobotFrameModifyUI):
        _translate = QtCore.QCoreApplication.translate
        RobotFrameModifyUI.setWindowTitle(_translate("RobotFrameModifyUI", "MainWindow"))
        self.menuFile.setTitle(_translate("RobotFrameModifyUI", "File"))
        self.toolBar.setWindowTitle(_translate("RobotFrameModifyUI", "toolBar"))
        self.actionFile_Open.setText(_translate("RobotFrameModifyUI", "File Open"))
        self.actionFile_Save.setText(_translate("RobotFrameModifyUI", "File Save"))
        self.actionFile_Save_as.setText(_translate("RobotFrameModifyUI", "File Save as"))
        self.actionFile_Open_2.setText(_translate("RobotFrameModifyUI", "File Open"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RobotFrameModifyUI = QtWidgets.QMainWindow()
    ui = Ui_RobotFrameModifyUI()
    ui.setupUi(RobotFrameModifyUI)
    RobotFrameModifyUI.show()
    sys.exit(app.exec_())

