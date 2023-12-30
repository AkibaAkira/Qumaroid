import bpy

from .lowApi.LowApi import LowApi
from .QumaAngleTranslator import QumaAngleTranslator
from ....PopupUtils import PopupUtils
from ...posePanelConstants import PoseMode
from ....BoneName import VroidBonename

class QumaPoseLoop:
    
    def __init__(self) -> None:
        try:
            self.handle = LowApi.GetQumaHandle()
        except Exception as e:
            PopupUtils.ShowMessageBox(str(e), "Error", "ERROR")
            
        self.boneSensorHandles = LowApi.GetBoneSenesorsHandles(self.handle)
        
        # # start only ONE instance
        if bpy.app.timers.is_registered(self.__Loop):
            bpy.app.timers.unregister(self.__Loop)    
        bpy.app.timers.register(self.__Loop)
    
    def Stop(self) -> None:
        LowApi.Exit()
        self.handle = None
        self.boneSensorHandles = None
    
    def __Loop(self):
        
        if self.handle is None:
            return None
        
        try:
            LowApi.UpdateBuffer(self.handle)
            rootRotationVec = LowApi.GetAccelerometerReadings(self.handle)
            sensorAngles = LowApi.GetBoneAngleReadings(self.handle, self.boneSensorHandles)
            
            # 0. Update Hips Rotation
            if LowApi.GetButtonState(self.handle) == 1:
                hipsRotation = QumaAngleTranslator.TranslateHipsRotation(sensorAngles, rootRotationVec)
                self.__RotateBone(VroidBonename.J_Bip_C_Hips, "XYZ", hipsRotation)
                
            # 1. Update Head Rotation
            if bpy.context.scene.qumaroidHeadPoseMode == PoseMode.QUMARION.value:
                self.__RotateBone(VroidBonename.J_Bip_C_Head, "XYZ", QumaAngleTranslator.TranslateHeadRotation(sensorAngles))
                self.__RotateBone(VroidBonename.J_Bip_C_Neck, "XYZ", QumaAngleTranslator.TranslateNeckRotation(sensorAngles))
            
            # 2. Update Spine Rotation
            if bpy.context.scene.qumaroidSpinePoseMode == PoseMode.QUMARION.value:
                self.__RotateBone(VroidBonename.J_Bip_C_Chest, "XYZ", QumaAngleTranslator.TranslateChestRotation(sensorAngles))
                self.__RotateBone(VroidBonename.J_Bip_C_Spine, "XYZ", QumaAngleTranslator.TranslateSpineRotation(sensorAngles))
            
            # 3. Update Left Hand Rotation
            if bpy.context.scene.qumaroidLeftArmPoseMode == PoseMode.QUMARION.value:
                self.__RotateBone(VroidBonename.J_Bip_L_UpperArm, "YXZ", QumaAngleTranslator.TranslateLeftUpperArmRotation(sensorAngles))
                self.__RotateBone(VroidBonename.J_Bip_L_LowerArm, "XYZ", QumaAngleTranslator.TranslateLeftLowerArmRotation(sensorAngles))
                self.__RotateBone(VroidBonename.J_Bip_L_Hand, "XYZ", QumaAngleTranslator.TranslateLeftHandRotation(sensorAngles))
            
            # 3. Update Right Hand Rotation
            if bpy.context.scene.qumaroidRightArmPoseMode == PoseMode.QUMARION.value:
                self.__RotateBone(VroidBonename.J_Bip_R_UpperArm, "YXZ", QumaAngleTranslator.TranslateRightUpperArmRotation(sensorAngles))
                self.__RotateBone(VroidBonename.J_Bip_R_LowerArm, "XYZ", QumaAngleTranslator.TranslateRightLowerArmRotation(sensorAngles))
                self.__RotateBone(VroidBonename.J_Bip_R_Hand, "XYZ", QumaAngleTranslator.TranslateRightHandRotation(sensorAngles))
                
            # 4. Update Left Leg Rotation
            if bpy.context.scene.qumaroidLeftLegPoseMode == PoseMode.QUMARION.value:
                self.__RotateBone(VroidBonename.J_Bip_L_UpperLeg, "XYZ", QumaAngleTranslator.TranslateLeftUpperLegRotation(sensorAngles))
                self.__RotateBone(VroidBonename.J_Bip_L_LowerLeg, "XYZ", QumaAngleTranslator.TranslateLeftLowerLegRotation(sensorAngles))
                self.__RotateBone(VroidBonename.J_Bip_L_Foot, "XYZ", QumaAngleTranslator.TranslateLeftFootRotation(sensorAngles))
                
            # 5. Update Left Leg Rotation
            if bpy.context.scene.qumaroidRightLegPoseMode == PoseMode.QUMARION.value:
                self.__RotateBone(VroidBonename.J_Bip_R_UpperLeg, "XYZ", QumaAngleTranslator.TranslateRightUpperLegRotation(sensorAngles))
                self.__RotateBone(VroidBonename.J_Bip_R_LowerLeg, "XYZ", QumaAngleTranslator.TranslateRightLowerLegRotation(sensorAngles))
                self.__RotateBone(VroidBonename.J_Bip_R_Foot, "XYZ", QumaAngleTranslator.TranslateRightFootRotation(sensorAngles))
                
        except Exception as e:
            PopupUtils.ShowMessageBox(str(e), "Error", "ERROR")
            
        # End of Loop
        if self.__HasAnyQumaActiveToggles():
            return 0
        else:
            return None
    
    def __HasAnyQumaActiveToggles(self) -> bool:
        scene = bpy.context.scene
        
        return (scene.qumaroidHeadPoseMode == PoseMode.QUMARION.value
                or scene.qumaroidSpinePoseMode == PoseMode.QUMARION.value
                or scene.qumaroidLeftArmPoseMode == PoseMode.QUMARION.value
                or scene.qumaroidRightArmPoseMode == PoseMode.QUMARION.value
                or scene.qumaroidLeftLegPoseMode == PoseMode.QUMARION.value
                or scene.qumaroidRightLegPoseMode == PoseMode.QUMARION.value
                or scene.qumaroidHipsPoseMode == PoseMode.QUMARION.value)
    
    def __RotateBone(self, boneName, rotationMode, vec) -> None:
        bpy.context.scene.qumaroidArmatureObject.pose.bones[boneName.value].rotation_mode = rotationMode
        bpy.context.scene.qumaroidArmatureObject.pose.bones[boneName.value].rotation_euler = vec