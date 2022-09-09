import pybullet as p
import pybullet_data

import math
from PIL import Image
import datetime
import time

'''
import pkgutil
egl = pkgutil.get_loader('eglRenderer')
'''

class robotEngine():
    def __init__(self, isDirect=False, config=None):
        self.setEngineData(config)
        
        self.isDirect = isDirect
        imgOptions = "--width=" + str(self.robotImgWidth) + " --height=" + str(self.robotImgHeight)
        if (not self.isDirect):
            p.connect(p.GUI, options=imgOptions)    # 4:3 960:720 # 16:9 1280:720
        else:
            p.connect(p.DIRECT, options=imgOptions)    # 4:3 960:720
            
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        
                
        if config == None:
            planeId = p.loadURDF("plane.urdf")         
               
            self.RobotId = p.loadURDF("../data/roid1_urdf/roid1.urdf", 
                                    self.startLocations, 
                                    useFixedBase = False,
                                    flags = p.URDF_MAINTAIN_LINK_ORDER + p.URDF_USE_SELF_COLLISION)                  
        else:
            planeId = p.loadURDF("plane.urdf")         
            
            self.RobotId = p.loadURDF("../data/roid1_urdf/roid1.urdf", 
                                    self.startLocations, 
                                    useFixedBase = False,
                                    flags = p.URDF_MAINTAIN_LINK_ORDER + p.URDF_USE_SELF_COLLISION)                  
        p.changeDynamics(self.RobotId, -1, linearDamping=0, angularDamping=0)
        
        humanoid_fix = p.createConstraint(self.RobotId, -1, -1, -1, p.JOINT_FIXED, [0, 0, 0], [0, 0, 0],
                                            self.startLocations, [0, 0, 0, 1])
                                             
        self.updataCamera()
        
        self.projectionMatrix = p.computeProjectionMatrixFOV(
            fov = 90.0, 
            aspect = float(self.robotImgWidth) / float(self.robotImgHeight), 
            nearVal = 0.1,
            farVal = 30)

        
        if (not self.isDirect):
            width, height, self.viewMatrix, self.projectionMatrix, cameraUp, cameraForward, horizontal, vertical, yaw, pitch, dist, target = p.getDebugVisualizerCamera()
        
        width, height, rgbImg, depthImg, segImg = p.getCameraImage(
            self.robotImgWidth, 
            self.robotImgHeight, 
            viewMatrix = self.viewMatrix,
            projectionMatrix = self.projectionMatrix,
            flags = p.ER_SEGMENTATION_MASK_OBJECT_AND_LINKINDEX,
            lightDirection = self.lightDirection,
            lightDistance = self.lightDistance,
            lightAmbientCoeff = self.lightAmbientCoeff,
            lightDiffuseCoeff = self.lightDiffuseCoeff,
            lightSpecularCoeff = self.lightSpecularCoeff,            
            shadow = True)
            
        self.drawRobotColor()
        
        self.MOTOR_EN = 0
        self.MOTOR_POS = 1
        self.MOTOR_TIME = 2
        
        self.MOTOR_BASE_POS = 1500

    def getRobotId(self):
        return self.RobotId

        
    def setEngineData(self, config):
        if config == None:
            self.robotMotorCnt = 23
            self.robotImgWidth =  1280   
            self.robotImgHeight = 720   
        
            self.startLocations = [0, 0, 0]
            
            self.cameraDistance  = 1.1                  
            self.cameraYawDef    = 100.0                
            self.cameraYaw       = self.cameraYawDef
            self.cameraPitchDef  = -10.0                
            self.cameraPitch     = self.cameraPitchDef 
            self.cameraTP_xDef   = -0.7
            self.cameraTP_x    = self.cameraTP_xDef
            self.cameraTP_y    = -0.1
            self.cameraTP_z    = 0.00
            self.cameraTargetPosition = [self.cameraTP_x, self.cameraTP_y, self.cameraTP_z] 
            self.cameraRoll = 0
            self.upAxisIndex = 2 
            
            self.lightDirection = [1,1,1] #[1,1,1]   
            self.lightColor = [1.0, 1.0, 1.0]
            self.lightDistance = 7
            self.lightAmbientCoeff = 0.5             
            self.lightDiffuseCoeff = 0.5             
            self.lightSpecularCoeff = 0.5            
            
            self.cameraYawMax = self.cameraYawDef + 20
            self.cameraYawMin = self.cameraYawDef - 30
            if self.cameraYawMin < 0:
                self.cameraYawMin = 0
            self.isRotateCameraByDefaultDirLeft = True
            
            self.cameraPitchMax = self.cameraPitchDef + 10
            self.cameraPitchMin = self.cameraPitchDef - 10
            if self.cameraPitchMax > -5:
                self.cameraPitchMax = -6
            self.isRotateCameraByDefaultDirUp = True
            
            self.cameraTP_xMax = self.cameraTP_xDef + 0.2
            self.cameraTP_xMin = self.cameraTP_xDef - 0.2
            self.isZoomCameraByDefaultIn = True
        
            self.colorPalette = {"dark_gray":[0.2, 0.2, 0.2, 1.0], "light_gray":[0.8, 0.8, 0.8, 1.0], "light_blue":[0.3, 0.5, 1.0, 1.0], "orange":[1.0, 0.3, 0.1, 1.0]}
            self.colorPaletteBright = {"dark_gray":[0.5, 0.5, 0.5, 1.0], "light_gray":[1.0, 1.0, 1.0, 1.0], "light_blue":[0.6, 0.8, 1.0, 1.0], "orange":[1.0, 0.6, 0.1, 1.0]}
            self.robotColor = ["light_blue", "light_gray", "light_gray", "light_gray", "light_blue", "light_blue", "light_gray", "light_gray", "light_blue", "light_blue", "light_gray", "light_gray", "light_blue", "light_blue", "light_gray", "dark_gray", "dark_gray", "light_gray", "light_blue", "light_blue", "light_gray", "dark_gray", "dark_gray"]
            
            
        else:
            self.robotMotorCnt = config["robot"]["motorCnt"]
            self.robotImgWidth = config["3DEngine"]["image"]["width"] 
            self.robotImgHeight = config["3DEngine"]["image"]["height"]   
            
            self.startLocations = config["3DEngine"]["camera"]["basePosition"]
            
            self.cameraDistance  = config["3DEngine"]["camera"]["Distance"] 
            self.cameraYawDef    = config["3DEngine"]["camera"]["Yaw"] 
            self.cameraYaw       = self.cameraYawDef
            self.cameraPitchDef  = config["3DEngine"]["camera"]["Pitch"] 
            self.cameraPitch     = self.cameraPitchDef 
            self.cameraTP_xDef   = config["3DEngine"]["camera"]["TP_x"]
            self.cameraTP_x    = self.cameraTP_xDef
            self.cameraTP_y    = config["3DEngine"]["camera"]["TP_y"]
            self.cameraTP_z    = config["3DEngine"]["camera"]["TP_z"]
            self.cameraTargetPosition = [self.cameraTP_x, self.cameraTP_y, self.cameraTP_z] 
            self.cameraRoll = config["3DEngine"]["camera"]["Roll"]
            self.upAxisIndex = config["3DEngine"]["camera"]["upAxisIndex"] 
            self.projectionRov = config["3DEngine"]["camera"]["fov"]
            self.projectionNearVal = config["3DEngine"]["camera"]["nearVal"]
            self.projectionFarVal = config["3DEngine"]["camera"]["farVal"]
            
            self.lightDirection = config["3DEngine"]["light"]["Direction"] 
            self.lightColor = config["3DEngine"]["light"]["Color"]
            self.lightDistance = config["3DEngine"]["light"]["Distance"]
            self.lightAmbientCoeff = config["3DEngine"]["light"]["AmbientCoeff"]   
            self.lightDiffuseCoeff = config["3DEngine"]["light"]["DiffuseCoeff"]   
            self.lightSpecularCoeff = config["3DEngine"]["light"]["SpecularCoeff"] 
            
            self.cameraYawMax = self.cameraYawDef + config["3DEngine"]["camera"]["YawMaxRange"]
            self.cameraYawMin = self.cameraYawDef - config["3DEngine"]["camera"]["YawMinRange"]
            if self.cameraYawMin < 0:
                self.cameraYawMin = 0
            self.isRotateCameraByDefaultDirLeft = True
            
            self.cameraPitchMax = self.cameraPitchDef + config["3DEngine"]["camera"]["PitchMaxRange"]
            self.cameraPitchMin = self.cameraPitchDef - config["3DEngine"]["camera"]["PitchMinRange"]
            if self.cameraPitchMax > -5:
                self.cameraPitchMax = -6
            self.isRotateCameraByDefaultDirUp = True
            
            self.cameraTP_xMax = self.cameraTP_xDef + config["3DEngine"]["camera"]["TP_xMaxRange"]
            self.cameraTP_xMin = self.cameraTP_xDef - config["3DEngine"]["camera"]["TP_xMinRange"]
            self.isZoomCameraByDefaultIn = True
            
            self.colorPalette = config["colorPalette"]["normal"] 
            self.colorPaletteBright = config["colorPalette"]["bright"] 
            self.robotColor = config["robotLinkColor"]
            
    def drawRobotColor(self):
        for link in range(self.robotMotorCnt):
            p.changeVisualShape(1, link, rgbaColor = self.colorPalette[self.robotColor[link]])
        
    def drawRobotColorLink(self, obUid, LinkIndex):
        if obUid == 1:
            p.changeVisualShape(obUid, LinkIndex, rgbaColor = self.colorPalette[self.robotColor[LinkIndex]])
            
    def drawRobotColorBrightLink(self, obUid, LinkIndex):
        if obUid == 1:
            p.changeVisualShape(obUid, LinkIndex, rgbaColor = self.colorPaletteBright[self.robotColor[LinkIndex]])
            
    def saveImg(self, rgbImg):
        im = Image.fromarray(rgbImg)
        im.save('./imgs/' + str(datetime.datetime.today().strftime('%Y%m%d%H%M%S')) + ".png")
     
    def updataCamera(self):
        if (not self.isDirect):                             
            p.resetDebugVisualizerCamera(cameraDistance = self.cameraDistance,   
                                         cameraYaw = self.cameraYaw,
                                         cameraPitch = self.cameraPitch,
                                         cameraTargetPosition = self.cameraTargetPosition)
                                         
        self.viewMatrix = p.computeViewMatrixFromYawPitchRoll(
            self.cameraTargetPosition, 
            self.cameraDistance, 
            self.cameraYaw, 
            self.cameraPitch, 
            self.cameraRoll,
            self.upAxisIndex)  
        
                                         
    def rotateCameraByYaw(self, isRotateAuto = False, isRotateLeft = True, step = 2.0):        
        if isRotateAuto:
            if self.isRotateCameraByDefaultDirLeft:
                self.cameraYaw       += step    
                if self.cameraYaw > self.cameraYawMax:
                    self.cameraYaw = self.cameraYawMax
                    self.isRotateCameraByDefaultDirLeft = False
            else: 
                self.cameraYaw       -= step    
                if self.cameraYaw < self.cameraYawMin:
                    self.cameraYaw = self.cameraYawMin
                    self.isRotateCameraByDefaultDirLeft = True
        else:
            if isRotateLeft:
                self.cameraYaw       += step    
                if self.cameraYaw > self.cameraYawMax:
                    self.cameraYaw = self.cameraYawMax
            else:
                self.cameraYaw       -= step    
                if self.cameraYaw < self.cameraYawMin:
                    self.cameraYaw = self.cameraYawMin
            
        self.updataCamera()
        
        
    def rotateCameraByPitch(self, isRotateAuto = False, isRotateUp = True, step = 2.0):          
        if isRotateAuto:
            if self.isRotateCameraByDefaultDirUp:
                self.cameraPitch       += step    
                if self.cameraPitch > self.cameraPitchMax:
                    self.cameraPitch = self.cameraPitchMax
                    self.isRotateCameraByDefaultDirUp = False
            else: 
                self.cameraPitch       -= step    
                if self.cameraPitch < self.cameraPitchMin:
                    self.cameraPitch = self.cameraPitchMin
                    self.isRotateCameraByDefaultDirUp = True
        else:
            if isRotateUp:
                self.cameraPitch       += step    
                if self.cameraPitch > self.cameraPitchMax:
                    self.cameraPitch = self.cameraPitchMax
            else:
                self.cameraPitch       -= step    
                if self.cameraPitch < self.cameraPitchMin:
                    self.cameraPitch = self.cameraPitchMin
            
        self.updataCamera() 
     
    def zoomCamera(self, isZoomAuto = False, isZoomIn = True, step = 0.01):
        if isZoomAuto:
            if self.isZoomCameraByDefaultIn:
                self.cameraTP_x       -= step    
                if self.cameraTP_x < self.cameraTP_xMin:
                    self.cameraTP_x = self.cameraTP_xMin
                    self.isZoomCameraByDefaultIn = False
            else: 
                self.cameraTP_x       += step    
                if self.cameraTP_x > self.cameraTP_xMax:
                    self.cameraTP_x = self.cameraTP_xMax
                    self.isZoomCameraByDefaultIn = True
        else:
            if isZoomIn:
                self.cameraTP_x       -= step    
                if self.cameraTP_x < self.cameraTP_xMin:
                    self.cameraTP_x = self.cameraTP_xMin
            else:
                self.cameraTP_x       += step    
                if self.cameraTP_x > self.cameraTP_xMax:
                    self.cameraTP_x = self.cameraTP_xMax
         
        self.cameraTargetPosition = [self.cameraTP_x, self.cameraTP_y, self.cameraTP_z] 

        self.updataCamera()  

    def cameraDefPosition(self):
        self.cameraPitch = self.cameraPitchDef
        self.cameraYaw  = self.cameraYawDef
        self.cameraTP_x = self.cameraTP_xDef
        self.cameraTargetPosition = [self.cameraTP_x, self.cameraTP_y, self.cameraTP_z] 
        self.updataCamera() 
        
    def changeJointPosition(self, motorData, jointIdx):
      motorLen = len(jointIdx)
      self.JointPos = [0] * motorLen
      force = [240.] * motorLen

      for idx in range(motorLen):
        self.JointPos[idx] = float(motorData[idx][self.MOTOR_POS] - self.MOTOR_BASE_POS) / 50 #100
        
      self.humanoid = 1 
      
      p.setJointMotorControlArray(self.humanoid, 
                                    jointIndices = jointIdx, 
                                    controlMode = p.POSITION_CONTROL, 
                                    targetPositions = self.JointPos, 
                                    forces = force)
      for i in range(20):
        p.stepSimulation()
     
    def show(self):
      if (not self.isDirect):
        width, height, self.viewMatrix, self.projectionMatrix, cameraUp, cameraForward, horizontal, vertical, yaw, pitch, dist, target = p.getDebugVisualizerCamera()
       
      flags = p.ER_SEGMENTATION_MASK_OBJECT_AND_LINKINDEX
      
      width, height, rgbImg, depthImg, self.segImg = p.getCameraImage(
        self.robotImgWidth, 
        self.robotImgHeight, 
        viewMatrix = self.viewMatrix,
        projectionMatrix = self.projectionMatrix,
        flags = flags,
        lightDirection = self.lightDirection,
        lightColor = self.lightColor,
        lightDistance = self.lightDistance,
        lightAmbientCoeff = self.lightAmbientCoeff,
        lightDiffuseCoeff = self.lightDiffuseCoeff,
        lightSpecularCoeff = self.lightSpecularCoeff,
        shadow = True)
      
      self.mouseEvents(self.segImg)
      
      return rgbImg
      
    def getLinkByMousePos(self, mouseX, mouseY):
      pixel = self.segImg[mouseY][mouseX]
      obUid = pixel & ((1 << 24) - 1)
      linkIndex = (pixel >> 24) - 1
      return obUid, linkIndex
      
    def mouseEvents(self, segImg):
      mouseEvents = p.getMouseEvents()
      for e in mouseEvents:
        if ((e[0] == 2) and (e[3] == 0) and (e[4] & p.KEY_WAS_TRIGGERED)):
          mouseX = int(e[1])
          mouseY = int(e[2])

          pixel = segImg[mouseY][mouseX]
          obUid = pixel & ((1 << 24) - 1)
          linkIndex = (pixel >> 24) - 1
          
      
    def closeEngine(self):
        p.stepSimulation()
        
    
  
