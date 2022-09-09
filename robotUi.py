from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QColor, QFont, QPalette

import cv2
import numpy as np
import re
from PIL import Image
from os.path import exists

from RobotFrameModifyUI import Ui_RobotFrameModifyUI
from RobotFrameModify_MotorDialog import Ui_MotorMotion_Dialog
from robotEngine import robotEngine
from robotData import robotData

class RobotUiCtrl(QMainWindow, Ui_RobotFrameModifyUI):
    def __init__(self, parent=None):

        super(RobotUiCtrl, self).__init__(parent)
        self.setupUi(self)
      
        self.const_UI()
        self.modeFunDef()
        
        self.dataRW = robotData()

        self.robotFilename = "./roid1.config"
        self.config = self.Robot_loadData(self.robotFilename)

        
        self.UIMode = None 
        self.UIMode_change(self.FRAME_MODE)
        
        # robot
        self.robot = robotEngine(isDirect=True, config=self.config)
        self.robotId = self.robot.getRobotId()
        
    def const_UI(self):
        # for Motor struct from .config. 
        self.MOTOR_EN = 0
        self.MOTOR_POS = 1
        self.MOTOR_TIME = 2
        
        # map motor position from .config to UI
        self.MOTOR_BASE_POS = 1500

        # for UI mode 
        self.FRAME_MODE = 0
        self.OFFSET_MODE = 1
        self.CONTINUE_MODE = 2
        
    def modeFunDef(self):   
        self.mode = [                
                {   
                    "initVar" : self.FrameMode_initVar,
                    "initUI"  : self.FrameMode_initUI,
                    "init"    : self.FrameMode_init,
                    "close"   : self.FrameMode_close,
                },
                {   
                    "initVar" : self.OffsetMode_initVar,
                    "initUI"  : self.OffsetMode_initUI,
                    "init"    : self.OffsetMode_init,
                    "close"   : self.OffsetMode_close,
                },
                {   
                    "initVar" : self.ContinueMode_initVar,
                    "initUI"  : self.ContinueMode_initUI,
                    "init"    : self.ContinueMode_init,
                    "close"   : self.OffsetMode_close,
                }
            ]
        
    def converImgToQt(self, rgbImg):
        height, width, channel = rgbImg.shape
        bytesPerLine = channel * width
        
        self.imgScaleX = self.disply_width / width
        self.imgScaleY = self.display_height / height
        
        convertToQtFormat = QtGui.QImage(rgbImg, width, height, QtGui.QImage.Format_RGBA8888)
        
        qtImg = convertToQtFormat.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        
        return QPixmap.fromImage(qtImg) 

    def videoClose(self):
        self.robot.closeEngine()

    
    def closeEvent(self, event):
        self.config["motoPos"] = self.MotorFrame_MotorData
        self.config["motoFrame"] = self.MotorFrame_FrameData
        self.dataRW.write(self.robotFilename, self.config)
        
    def videoPlay(self):
        self.robot.changeJointPosition(self.MotorFrame_MotorData[self.FrameIdx], self.RobotJointId)
        rgbImg = self.robot.show()      
        qtImg = self.converImgToQt(rgbImg)
        self.VideoView.setPixmap(qtImg)
            
      
    # QT event
    def videoViewMouseRelease(self, event):
        globalPos = self.mapToGlobal(event.pos()) 
        
    def videoViewMouseMove(self, event):
        globalPos = self.mapToGlobal(event.pos()) 
 
    def videoViewMousePress(self, event):
        pass
        
    def videoViewMouseDoubleClick(self, event):
        globalPos = self.mapToGlobal(event.pos()) 
        
        # LeftButton = 1 , RightButton = 2 , MidButton = 4
        if event.button() == 1: #LeftButton
            obUid, LinkIndex = self.robot.getLinkByMousePos(int(event.pos().x() // self.imgScaleX), 
                                                            int(event.pos().y() // self.imgScaleY))
            if obUid != 0:  # background object
                self.robot.drawRobotColorBrightLink(obUid, LinkIndex)

                if self.isDialog_MotorMotion:
                    self.MotorDialog_close()
                    
                self.lastSelectLink = LinkIndex   
                self.lastSelectobUid = obUid
                self.MotorDialog_open(LinkIndex)
                self.MoterMotion_isChange = True 
            else:
                if self.isDialog_MotorMotion:
                    self.MotorDialog_close()
        
    def videoViewMouseWheel(self, event):
        delta = event.angleDelta()

        if delta.y() > 0:
            self.robot.zoomCamera(isZoomIn = True)
        elif delta.y() < 0:
            self.robot.zoomCamera(isZoomIn = False)

    def motorFrame_keyPressEvent(self, event):
        pressKey = event.key()

        if pressKey == Qt.Key_Up or \
            pressKey == Qt.Key_Down or \
            pressKey == Qt.Key_Left or \
            pressKey == Qt.Key_Right or \
            pressKey == Qt.Key_PageUp or \
            pressKey == Qt.Key_PageDown or \
            pressKey == Qt.Key_Home or \
            pressKey == Qt.Key_F12 or \
            pressKey == Qt.Key_F11:
            super(RobotUiCtrl, self).keyPressEvent(event)
        
    def motorMotion_keyPressEvent(self, event):
        pressKey = event.key()
        if pressKey == Qt.Key_Up or \
            pressKey == Qt.Key_Down or \
            pressKey == Qt.Key_Left or \
            pressKey == Qt.Key_Right or \
            pressKey == Qt.Key_PageUp or \
            pressKey == Qt.Key_PageDown or \
            pressKey == Qt.Key_Home or \
            pressKey == Qt.Key_F12 or \
            pressKey == Qt.Key_F11:
            super(RobotUiCtrl, self).keyPressEvent(event)
            
    def keyPressEvent(self, event):       
        pressKey = event.key()
        if pressKey == Qt.Key_Up:           # up pad / up
            self.robot.rotateCameraByPitch(isRotateUp=True)
        elif pressKey == Qt.Key_Down:       # down pad
            self.robot.rotateCameraByPitch(isRotateUp=False)
        elif pressKey == Qt.Key_Left:       # left pad
            self.robot.rotateCameraByYaw(isRotateLeft=True)
        elif pressKey == Qt.Key_Right:      # right pad
            self.robot.rotateCameraByYaw(isRotateLeft=False)
        elif pressKey == Qt.Key_PageUp:     # pageUp pad
            self.robot.zoomCamera(isZoomIn=True)
        elif pressKey == Qt.Key_PageDown:   # pageDn pad
            self.robot.zoomCamera(isZoomIn=False)
        elif pressKey == Qt.Key_Home:       # home pad
            self.robot.cameraDefPosition()
        elif pressKey == Qt.Key_F12:        # F12
            if self.FrameMode_isShowTable == True:
                self.MotorFrame.lower()
                self.MotorMotion.lower()     
                self.FrameMode_isShowTable = False
            else:    
                self.MotorFrame.raise_()
                self.MotorMotion.raise_()
                self.FrameMode_isShowTable = True
            
        elif pressKey == Qt.Key_F11:        # F11
               
            pass
            
    def Robot_loadData(self, filename):
        config = self.dataRW.read(filename)
        if config == None:
            return config
            
        self.RobotMotor_TotalCount = config["robot"]["motorCnt"]
        self.RobotMotorId = config["robot"]["motorId"]
        self.RobotJointId = config["robot"]["jointId"]
        
        self.MotorFrameIdx = 0
        self.MotorFrame_TotalCount = config["robot"]["frame"]
        self.MotorFrame_MotorData = config["motoPos"]
        self.MotorFrame_FrameData = config["motoFrame"]
        self.MotorFrame_MotorPosRange = config["motorConfig"]["motorRange"]

        # 1:frameNo 2:robotIcon 3:memo
        self.MotorFrame_RowCount = 3 
        self.MotorFrame_ColumnCount = self.MotorFrame_TotalCount 
        self.MotorMotion_RawCount = self.RobotMotor_TotalCount
        self.MotorMotion_ColumnCount = 3
        
        return config
                  
    def MotorDialog_open(self, motorIdx):
           
       
        self.isDialog_MotorMotion = True
        
        self.dialog = QtWidgets.QDialog()
        self.dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.dialog.ui = Ui_MotorMotion_Dialog()
        self.dialog.ui.setupUi(self.dialog)

        self.dialogMotorID = self.RobotMotorId[motorIdx]    # real ID for motor control
        self.dialogMotorIdx = motorIdx

        self.dialog.ui.MotorFrame.setText(str(self.dialogMotorID))
        MotorPosSlider_max = (self.MotorFrame_MotorPosRange[motorIdx][1] - self.MOTOR_BASE_POS) / 10 
        MotorPosSlider_min = (self.MotorFrame_MotorPosRange[motorIdx][0] - self.MOTOR_BASE_POS) / 10 
        MotorPosSlider_step = 10
        MotorPosSlider_value = self.MotorFrame_MotorData[self.FrameIdx][self.dialogMotorIdx][self.MOTOR_POS] - self.MOTOR_BASE_POS
        self.dialog.ui.MotorPosSlider.setRange(MotorPosSlider_min, MotorPosSlider_max)
        self.dialog.ui.MotorPosSlider.setSingleStep(MotorPosSlider_step)
        self.dialog.ui.MotorPosSlider.setValue(MotorPosSlider_value)
        self.dialog.ui.MotorPosEdit.setText(str(MotorPosSlider_value))

        MotorDelaySlider_max = 3000
        MotorDelaySlider_min = 0
        MotorDelaySlider_step = 100
        MotorDelaySlider_value = self.MotorFrame_MotorData[self.FrameIdx][motorIdx][self.MOTOR_TIME]
        self.dialog.ui.MotorDelaySlider.setRange(MotorDelaySlider_min, MotorDelaySlider_max)
        self.dialog.ui.MotorDelaySlider.setSingleStep(MotorDelaySlider_step)
        self.dialog.ui.MotorDelaySlider.setValue(MotorDelaySlider_value)
        self.dialog.ui.MotorDelayEdit.setText(str(MotorDelaySlider_value))

        self.dialog.ui.MotorPosSlider.valueChanged['int'].connect(self.MotorDialog_MotorPosSlider_changeValue)
        self.dialog.ui.MotorDelaySlider.valueChanged['int'].connect(self.MotorDialog_MotorDelaySlider_changeValue)
        self.dialog.ui.MotorPosEdit.textChanged.connect(self.MotorDialog_MotorPosEdit_changeValue)
        self.dialog.ui.MotorDelayEdit.textChanged.connect(self.MotorDialog_MotorDelaySlider_changeValue)
        self.dialog.ui.closeButton.pressed.connect(self.MotorDialog_close)

        self.dialog.setGeometry(400, 600, self.dialog.width(), self.dialog.height())
        self.dialog.show()
        self.dialog.exec_()
     
    def MotorDialog_close(self):
        self.isDialog_MotorMotion = None
        self.dialog.close()
        if self.lastSelectLink != None:
            self.robot.drawRobotColorLink(self.lastSelectobUid, self.lastSelectLink)
                
    def MotorDialog_MotorPosSlider_changeValue(self, motorPos):
        self.dialog.ui.MotorPosEdit.setText(str(motorPos))
        self.MotorFrame_MotorData[self.FrameIdx][self.dialogMotorIdx][self.MOTOR_POS] = motorPos + self.MOTOR_BASE_POS
        
        self.FrameMode_MotorMotion_showData(self.FrameIdx)
        
    def MotorDialog_MotorDelaySlider_changeValue(self, motorTime):
        self.dialog.ui.MotorDelayEdit.setText(str(motorTime))
        self.MotorFrame_MotorData[self.FrameIdx][self.dialogMotorIdx][self.MOTOR_TIME] = motorTime
        
        self.FrameMode_MotorMotion_showData(self.FrameIdx)    

    def MotorDialog_MotorPosEdit_changeValue(self, motorEdit):
        if motorEdit == "":
            return
        else:
            try:
                motorPos = int(motorEdit)
            except ValueError:
                # TODO dialog
                return
                
        self.MotorFrame_MotorData[self.FrameIdx][self.dialogMotorIdx][self.MOTOR_POS] = motorPos + self.MOTOR_BASE_POS
        
        self.FrameMode_MotorMotion_showData(self.FrameIdx)

    def MotorDialog_MotorDelaySlider_changeValue(self, motorEdit):
        if motorEdit == "":
            return
        else:
            try:
                motorDelay = int(motorEdit)
            except ValueError:
                # TODO dialog
                return    

        self.dialog.ui.MotorDelaySlider.setValue(motorDelay)
        self.MotorFrame_MotorData[self.FrameIdx][self.dialogMotorIdx][self.MOTOR_TIME] = motorDelay
        
        self.FrameMode_MotorMotion_showData(self.FrameIdx)
        
    def UIMode_change(self, newMode):
        if newMode != self.UIMode and self.UIMode != None:
            self.mode[self.UIMode]["close"]()

        self.UIMode = newMode
        self.mode[self.UIMode]["init"]()
        
    def FrameMode_initVar(self):
        self.FrameIdx = 0

        self.isDialog_MotorMotion = False

        self.lastSelectLink = None
        self.lastSelectobUid = None

        self.FrameMode_isShowTable = True
        
    def FrameMode_initUI(self):

        self.disply_width = 1280
        self.display_height = 720
        grey = QPixmap(self.disply_width, self.display_height)
        grey.fill(QColor('darkGray'))
        self.VideoView.setPixmap(grey)
        
        self.VideoView.mousePressEvent = self.videoViewMousePress
        self.VideoView.mouseReleaseEvent = self.videoViewMouseRelease
        self.VideoView.mouseMoveEvent = self.videoViewMouseMove
        self.VideoView.mouseDoubleClickEvent = self.videoViewMouseDoubleClick
        self.VideoView.wheelEvent = self.videoViewMouseWheel
        
        
        self.MotorFrame.setRowCount(self.MotorFrame_RowCount)
        self.MotorFrame.setColumnCount(self.MotorFrame_ColumnCount)
        self.MotorFrame.setVerticalHeaderLabels(["動作", "縮圖", "說明"])
        self.MotorFrame.setRowHeight(0, 16)
        self.MotorFrame.setRowHeight(1, 80)
        self.MotorFrame.setRowHeight(2, 16)
        self.MotorFrame.setColumnWidth(0, 80)
        self.MotorFrame.setColumnWidth(1, 80)
        self.MotorFrame.setColumnWidth(2, 80)
        self.MotorFrame.verticalHeader().setStretchLastSection(True)
        self.MotorFrame.horizontalHeader().setVisible(False)
        self.MotorFrame.cellClicked.connect(self.FrameMode_MotorFrame_on_cellClicked)
        self.MotorFrame.cellDoubleClicked.connect(self.FrameMode_MotorFrame_on_cellDoubleClicked)
        self.MotorFrame.itemChanged.connect(self.FrameMode_MotorFrame_on_itemChanged)
        self.FrameMode_MotorFrame_showData(self.FrameIdx)
        self.FrameMode_MotorFrame_showColor(self.FrameIdx)
        self.MotorFrame.keyPressEvent = self.motorFrame_keyPressEvent 
        
        self.MotorMotion.setRowCount(self.MotorMotion_RawCount)
        self.MotorMotion.setColumnCount(self.MotorMotion_ColumnCount)
        self.MotorMotion.setHorizontalHeaderLabels(["馬達", "位置", "時間"])
        self.MotorMotion.setColumnWidth(0, 60)
        self.MotorMotion.setColumnWidth(1, 60)
        self.MotorMotion.setColumnWidth(2, 60)
        
        self.MotorMotion.horizontalHeader().setStretchLastSection(True)
        self.MotorMotion.verticalHeader().setVisible(False)
        self.MotorMotion.setMouseTracking(True)
        self.MotorMotion.cellClicked.connect(self.FrameMode_MotorMotion_on_cellClicked)
        self.FrameMode_MotorMotion_showData(self.FrameIdx)
        self.MotorFrame.keyPressEvent = self.motorMotion_keyPressEvent
        self.MoterMotion_isChange = False
        
        self.timerSpeed = 33                
        self.playVideoTimer = QTimer(self)  
        self.playVideoTimer.timeout.connect(self.videoPlay)  
        self.playVideoTimer.start(self.timerSpeed)              

    def FrameMode_init(self):
        self.FrameMode_initVar()
        self.FrameMode_initUI()
        
    def FrameMode_close(self):
        pass

    def FrameMode_MotorFrame_on_cellClicked(self, row, column):         
        if self.MoterMotion_isChange:
            self.genFrameThumbnail()
            self.MoterMotion_isChange = False

            if exists('./FrameImgs/frame_' + str(self.FrameIdx) + ".png"):
                self.FrameMode_MotorFrame_showThumbnail(self.FrameIdx)
            
        self.FrameIdx = column
        self.FrameMode_MotorFrame_showColor(self.FrameIdx)
        self.FrameMode_MotorMotion_showData(self.FrameIdx)

        self.MotorFrame.resizeColumnsToContents()
            
    def FrameMode_MotorFrame_on_cellDoubleClicked(self, row, column):
        if row == 0 or row == 1:
            pass

    def FrameMode_MotorFrame_on_itemChanged(self):

        for index in self.MotorFrame.selectedIndexes():
            itemText = self.MotorFrame.item(index.row(), index.column()).text()
            if index.row() == 2: 
                if itemText != self.MotorFrame_FrameData[self.FrameIdx][1]:
                    self.MotorFrame_FrameData[self.FrameIdx][1] = itemText 
        
    def FrameMode_MotorFrame_showData(self, MotorFrame):
        for idx in range(self.MotorFrame_TotalCount):
            item = QTableWidgetItem(str(idx))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable) 
            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            self.MotorFrame.setItem(0, idx, item)   

            if exists('./FrameImgs/frame_' + str(idx) + ".png"):
                self.FrameMode_MotorFrame_showThumbnail(idx)
            else:
                item = QTableWidgetItem(self.MotorFrame_FrameData[idx][0])  
                item.setFlags(item.flags() & ~Qt.ItemIsEditable) 
                item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                self.MotorFrame.setItem(1, idx, item)   
            
            item = QTableWidgetItem(self.MotorFrame_FrameData[idx][1])  
            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            self.MotorFrame.setItem(2, idx, item)   
            
        self.MotorFrame.resizeColumnsToContents()
        
    def FrameMode_MotorFrame_showThumbnail(self, frameIdx):
        pixmap = QtGui.QPixmap('./FrameImgs/frame_' + str(frameIdx) + ".png")
        size = pixmap.size()
        label = QtWidgets.QLabel()
        label.setPixmap(pixmap)
        label.setFixedSize(size)
        
        item = QTableWidgetItem()
        item.setSizeHint(size)
        self.MotorFrame.setItem(1, frameIdx, item)
        self.MotorFrame.setCellWidget(1, frameIdx, label)
        
        
        
    def FrameMode_MotorFrame_showColor(self, targeIdx):
        normalColor = QtGui.QColor(255,255,255)
        targeColor = QtGui.QColor(250, 250, 0)
        
        for columnIdx in range(self.MotorFrame.columnCount()):
            for rowIdx in range(self.MotorFrame.rowCount()):
                if columnIdx != targeIdx:   
                    self.MotorFrame.item(rowIdx, columnIdx).setBackground(normalColor)
                else:
                    self.MotorFrame.item(rowIdx, columnIdx).setBackground(targeColor)

    def FrameMode_MotorMotion_on_cellClicked(self, row, column):
        self.FrameMode_MotorMotion_showColor(row)
                
        self.robot.drawRobotColorBrightLink(self.robotId, row)

        if self.isDialog_MotorMotion:
            self.MotorDialog_close()
            
        self.lastSelectLink = row   
        self.lastSelectobUid = self.robotId
        self.MotorDialog_open(row)
        self.MoterMotion_isChange = True   
                    
    def FrameMode_MotorMotion_showColor(self, targeIdx):
        normalColor = QtGui.QColor(255,255,255)
        targeColor = QtGui.QColor(0, 250, 250)
        for rowIdx in range(self.MotorMotion.rowCount()):
            for columnIdx in range(self.MotorMotion.columnCount()):
                if rowIdx != targeIdx:
                    self.MotorMotion.item(rowIdx, columnIdx).setBackground(normalColor)
                else:
                    self.MotorMotion.item(rowIdx, columnIdx).setBackground(targeColor)
                    
    def FrameMode_MotorMotion_showData(self, MotorFrame):
        for idx  in range(self.RobotMotor_TotalCount):
            item = QTableWidgetItem(str(self.RobotMotorId[idx]))
            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.MotorMotion.setItem(idx, 0, item)

            item = QTableWidgetItem(str(self.MotorFrame_MotorData[MotorFrame][idx][self.MOTOR_POS] - self.MOTOR_BASE_POS)) 
            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.MotorMotion.setItem(idx, 1, item)

            item = QTableWidgetItem(str(self.MotorFrame_MotorData[MotorFrame][idx][self.MOTOR_TIME]))
            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.MotorMotion.setItem(idx, 2, item)
            
    def OffsetMode_initVar(self):
        pass
    def OffsetMode_initUI(self):
        pass
    def OffsetMode_init(self):
        pass
    def OffsetMode_close(self):
        pass
        
    def ContinueMode_initVar(self):
        pass
    def ContinueMode_initUI(self):
        pass
    def ContinueMode_init(self):
        pass
    def ContinueMode_close(self):
        pass

    def genFrameThumbnail(self):
        self.robot.changeJointPosition(self.MotorFrame_MotorData[self.FrameIdx], self.RobotJointId)
        rgbImg = self.robot.show()   
        im = Image.fromarray(rgbImg)
        left = 280
        top = 0
        right = left + 720
        bottom = top + 720
        im = im.crop((left, top, right, bottom))
        im.thumbnail((80, 80), Image.ANTIALIAS)
        im.save('./FrameImgs/frame_' + str(self.FrameIdx) + ".png")

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ui = RobotUiCtrl()
    ui.show()
    sys.exit(app.exec_())        
    RobotUiCtrl.videoClose()
    
