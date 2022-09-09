# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\RobotFrameModify_MotorDialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MotorMotion_Dialog(object):
    def setupUi(self, MotorMotion_Dialog):
        MotorMotion_Dialog.setObjectName("MotorMotion_Dialog")
        MotorMotion_Dialog.setEnabled(True)
        MotorMotion_Dialog.resize(450, 250)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MotorMotion_Dialog.sizePolicy().hasHeightForWidth())
        MotorMotion_Dialog.setSizePolicy(sizePolicy)
        MotorMotion_Dialog.setMaximumSize(QtCore.QSize(450, 250))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        MotorMotion_Dialog.setFont(font)
        MotorMotion_Dialog.setModal(False)
        self.MotorFrameLabel = QtWidgets.QLabel(MotorMotion_Dialog)
        self.MotorFrameLabel.setGeometry(QtCore.QRect(20, 30, 80, 24))
        self.MotorFrameLabel.setObjectName("MotorFrameLabel")
        self.MotorFrame = QtWidgets.QLabel(MotorMotion_Dialog)
        self.MotorFrame.setGeometry(QtCore.QRect(120, 30, 51, 24))
        self.MotorFrame.setObjectName("MotorFrame")
        self.MotorPosLabel = QtWidgets.QLabel(MotorMotion_Dialog)
        self.MotorPosLabel.setGeometry(QtCore.QRect(20, 80, 80, 24))
        self.MotorPosLabel.setObjectName("MotorPosLabel")
        self.MotorPosEdit = QtWidgets.QLineEdit(MotorMotion_Dialog)
        self.MotorPosEdit.setGeometry(QtCore.QRect(120, 80, 80, 24))
        self.MotorPosEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.MotorPosEdit.setObjectName("MotorPosEdit")
        self.MotorPosSlider = QtWidgets.QSlider(MotorMotion_Dialog)
        self.MotorPosSlider.setGeometry(QtCore.QRect(220, 80, 190, 22))
        self.MotorPosSlider.setOrientation(QtCore.Qt.Horizontal)
        self.MotorPosSlider.setObjectName("MotorPosSlider")
        self.MotorDelayEdit = QtWidgets.QLineEdit(MotorMotion_Dialog)
        self.MotorDelayEdit.setGeometry(QtCore.QRect(120, 130, 80, 25))
        self.MotorDelayEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.MotorDelayEdit.setObjectName("MotorDelayEdit")
        self.MotorDelaySlider = QtWidgets.QSlider(MotorMotion_Dialog)
        self.MotorDelaySlider.setGeometry(QtCore.QRect(220, 130, 190, 22))
        self.MotorDelaySlider.setOrientation(QtCore.Qt.Horizontal)
        self.MotorDelaySlider.setObjectName("MotorDelaySlider")
        self.MotorDelayLabel = QtWidgets.QLabel(MotorMotion_Dialog)
        self.MotorDelayLabel.setGeometry(QtCore.QRect(20, 130, 80, 24))
        self.MotorDelayLabel.setObjectName("MotorDelayLabel")
        self.closeButton = QtWidgets.QPushButton(MotorMotion_Dialog)
        self.closeButton.setGeometry(QtCore.QRect(310, 180, 93, 28))
        self.closeButton.setObjectName("closeButton")

        self.retranslateUi(MotorMotion_Dialog)
        QtCore.QMetaObject.connectSlotsByName(MotorMotion_Dialog)

    def retranslateUi(self, MotorMotion_Dialog):
        _translate = QtCore.QCoreApplication.translate
        MotorMotion_Dialog.setWindowTitle(_translate("MotorMotion_Dialog", "馬達位置調整"))
        self.MotorFrameLabel.setText(_translate("MotorMotion_Dialog", "馬達編號"))
        self.MotorFrame.setText(_translate("MotorMotion_Dialog", "TextLabel"))
        self.MotorPosLabel.setText(_translate("MotorMotion_Dialog", "馬達位置"))
        self.MotorDelayLabel.setText(_translate("MotorMotion_Dialog", "馬達時間"))
        self.closeButton.setText(_translate("MotorMotion_Dialog", "離開"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MotorMotion_Dialog = QtWidgets.QDialog()
    ui = Ui_MotorMotion_Dialog()
    ui.setupUi(MotorMotion_Dialog)
    MotorMotion_Dialog.show()
    sys.exit(app.exec_())

