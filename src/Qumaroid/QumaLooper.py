import bpy, math
from .LowApi import LowApi
from .BoneName import VroidBonename, QumaSensorIndex
from .PopupUtils import PopupUtils

class QumaStart(bpy.types.Operator):
    bl_label = "Start Posing"
    bl_idname = "object.quma_start_pose"
    bl_description = "Start realtime posing with Qumarion"
    
    @classmethod
    def poll(cls, context):
        return not context.scene.qumaroidIsPosing

    def execute(self, context):
        QumaLooper.Start()
        return {'FINISHED'}

class QumaStop(bpy.types.Operator):
    bl_label = "Stop Posing"
    bl_idname = "object.quma_stop_pose"
    bl_description = "Stop posing"
    
    def execute(self, context):
        QumaLooper.Stop()
        return {'FINISHED'}
    
class QumaResetBones(bpy.types.Operator):
    bl_label = "Reset Bones"
    bl_idname = "object.quma_reset_bones"
    bl_description = "Reset Bones"
    
    def execute(self, context):  
        QumaLooper.ResetBones()
        return {'FINISHED'}

class QumaSenesorProperties(bpy.types.PropertyGroup):
    angle: bpy.props.FloatProperty(default = 0)

class QumaLockVroidBoneProperties(bpy.types.PropertyGroup):
    locked: bpy.props.BoolProperty(default = False)

class QumaLooper:

    DEGREES_20_RAD = 0.349066 

    ZERO_POINT_ONE_DEGREE_IN_RADIANS = 0.00174
    ONE_DEGREE_IN_RADIANS = 0.0174

    PANEL_LOCK_BONE_PREFIX = "qumaroidPanelLock_"

    __qumaHandle = None
    __qumaBoneSensorHandles = None

    __vroidBoneNames = [VroidBonename.J_Bip_C_Hips.name,
                            VroidBonename.J_Bip_C_Head.name,
                            VroidBonename.J_Bip_C_Neck.name,
                            VroidBonename.J_Bip_C_Chest.name,
                            VroidBonename.J_Bip_C_Spine.name,
                            VroidBonename.J_Bip_L_Shoulder.name,
                            VroidBonename.J_Bip_L_UpperArm.name,
                            VroidBonename.J_Bip_L_LowerArm.name,
                            VroidBonename.J_Bip_L_Hand.name,
                            VroidBonename.J_Bip_R_Shoulder.name,
                            VroidBonename.J_Bip_R_UpperArm.name,
                            VroidBonename.J_Bip_R_LowerArm.name,
                            VroidBonename.J_Bip_R_Hand.name,
                            VroidBonename.J_Bip_L_UpperLeg.name,
                            VroidBonename.J_Bip_L_LowerLeg.name,
                            VroidBonename.J_Bip_L_Foot.name,
                            VroidBonename.J_Bip_R_LowerLeg.name,
                            VroidBonename.J_Bip_R_UpperLeg.name,
                            VroidBonename.J_Bip_R_Foot.name]

    #region Qumalooper -> Register Functions

    def getQumaHandle():
        return QumaLooper.__qumaHandle
    
    def getQumaBoneSensorHandles():
        return QumaLooper.__qumaBoneSensorHandles
    
    def getVroidBoneNames():
        return QumaLooper.__vroidBoneNames

    def register():
        
        bpy.utils.register_class(QumaStart)
        bpy.utils.register_class(QumaStop)
        bpy.utils.register_class(QumaResetBones)    

        bpy.types.Scene.qumaroidIsPosing = bpy.props.BoolProperty()
        bpy.types.Scene.qumaroidRefreshInterval = bpy.props.FloatProperty(name = "Refreseh interval", default = 0.02, min = 0, max = 3)
        bpy.types.Scene.qumaroidPanelShowLockBoneMenu = bpy.props.BoolProperty()

        # Quma Panel Lock Bones
        bpy.types.Scene.qumaroidPanelLockAllBones = bpy.props.BoolProperty(name = "Lock All Bones", update=QumaLooper.OnChangeQumaPanelLockAllBone, default=False)

        for boneName in QumaLooper.__vroidBoneNames:
            label = boneName.replace("J_Bip_", "")
            if boneName == VroidBonename.J_Bip_C_Hips.name:
                label = "Lock Root Rotation"

            setattr(bpy.types.Scene, QumaLooper.PANEL_LOCK_BONE_PREFIX + boneName, bpy.props.BoolProperty(name = label, update=QumaLooper.OnChangeQumaPanelLockBone, default=False))
        
        # Collection Property
        bpy.utils.register_class(QumaSenesorProperties)
        bpy.types.Scene.qumaroidQumaSensorProperties = bpy.props.CollectionProperty(type=QumaSenesorProperties)

        bpy.utils.register_class(QumaLockVroidBoneProperties)
        bpy.types.Scene.qumaroidLockBoneArr = bpy.props.CollectionProperty(type=QumaLockVroidBoneProperties)
                
    def unregister():
        
        bpy.utils.unregister_class(QumaStart)
        bpy.utils.unregister_class(QumaStop)
        bpy.utils.unregister_class(QumaResetBones)   

        bpy.utils.unregister_class(QumaSenesorProperties)
        bpy.utils.unregister_class(QumaLockVroidBoneProperties)

        del bpy.types.Scene.qumaroidIsPosing    
        del bpy.types.Scene.qumaroidRefreshInterval
        del bpy.types.Scene.qumaroidPanelShowLockBoneMenu
        del bpy.types.Scene.qumaroidLockBoneArr
        del bpy.types.Scene.qumaroidQumaSensorProperties

        del bpy.types.Scene.qumaroidPanelLockAllBones
        # Please find a way to delete all "qumaroidPanelLock_"

    def filterVroidObjects(self, object):
        if object.pose is None:
            return False

        return True
    
    def OnChangeQumaPanelLockAllBone(self, context):
        if context.scene.qumaroidPanelLockAllBones:
            for boneName in QumaLooper.__vroidBoneNames:
                if boneName == VroidBonename.J_Bip_C_Hips.name:
                    continue

                context.scene[QumaLooper.PANEL_LOCK_BONE_PREFIX + boneName] = True
        else:
            allChecked = True
            for boneName in QumaLooper.__vroidBoneNames:
                if boneName == VroidBonename.J_Bip_C_Hips.name:
                    continue

                allChecked = allChecked and context.scene[QumaLooper.PANEL_LOCK_BONE_PREFIX + boneName]
            
            if allChecked:
                for boneName in QumaLooper.__vroidBoneNames:
                    if boneName == VroidBonename.J_Bip_C_Hips.name:
                        continue

                    context.scene[QumaLooper.PANEL_LOCK_BONE_PREFIX + boneName] = False
    
    def OnChangeQumaPanelLockBone(self, context):
        allChecked = True
        for boneName in QumaLooper.__vroidBoneNames:
            if boneName == VroidBonename.J_Bip_C_Hips.name:
                    continue
            
            allChecked = allChecked and context.scene[QumaLooper.PANEL_LOCK_BONE_PREFIX + boneName]

        context.scene.qumaroidPanelLockAllBones = allChecked

    #endregion

    #region Qumalooper -> Public Functions
    
    def Start():

        QumaLooper.__PrepareQumaLoop()

        qumaHandle = LowApi.GetQumaHandle()
        if qumaHandle:
            QumaLooper.__qumaHandle = qumaHandle
            # This is the cause of the crash
            QumaLooper.__qumaBoneSensorHandles = LowApi.GetBoneSenesorsHandles(qumaHandle)

        bpy.context.scene.qumaroidIsPosing = True 

        # # start only ONE instance
        if bpy.app.timers.is_registered(QumaLooper.__QumaLoop):
            bpy.app.timers.unregister(QumaLooper.__QumaLoop)    
        bpy.app.timers.register(QumaLooper.__QumaLoop)    

    def Stop():
        bpy.context.scene.qumaroidIsPosing = False
        LowApi.Exit()
        QumaLooper.__qumaHandle = None
        QumaLooper.__qumaBoneSensorHandles = None

    def ResetBones():
        
        armature = bpy.context.scene.qumaroidArmatureObject
        if armature is None:
            return

        for bone in armature.pose.bones:
            bone.rotation_mode = 'XYZ'   
            bone.rotation_euler = 0,0,0

    #endregion

    #region QumaLooper -> Draw Panel Functions
    
    def DrawPanel(layout):
        scene = bpy.context.scene

        row = layout.row()
        row.label(text="Pose")

        if not scene.qumaroidIsPosing:
            row = layout.row()
            row.operator("object.quma_start_pose")
            row = layout.row()
            row.operator("object.quma_reset_bones")
        else:
            row = layout.row()
            row.operator("object.quma_stop_pose")
       
        row = layout.row()
        row.prop(scene, "qumaroidRefreshInterval")

        # Bone Lock
        row = layout.row()
        row.prop(scene, "qumaroidPanelLockAllBones")

        row = layout.row(align=True)
        row.alignment = 'LEFT'
        row.prop(scene, "qumaroidPanelShowLockBoneMenu", icon="TRIA_DOWN" if scene.qumaroidPanelShowLockBoneMenu else "TRIA_RIGHT", icon_only=True, emboss=False, text="Lock Bones")     

        if scene.qumaroidPanelShowLockBoneMenu:
            
            box = layout.box()
            
            for boneName in QumaLooper.__vroidBoneNames:
                if boneName == VroidBonename.J_Bip_C_Hips.name:
                    continue

                row = box.row()
                row.prop(scene, QumaLooper.PANEL_LOCK_BONE_PREFIX + boneName)

    #endregion

    #region QumaLooper -> Main Loop

    def __PrepareQumaLoop():
        
        # Initiate Bone Lock Properties
        bpy.context.scene.qumaroidLockBoneArr.clear()

        for boneName in QumaLooper.__vroidBoneNames:
            item = bpy.context.scene.qumaroidLockBoneArr.add()
            item.name = boneName
            item.locked = QumaLooper.IsQumaPanelBoneLocked(boneName)

        # Initiate Quma Sensor Properties
        bpy.context.scene.qumaroidQumaSensorProperties.clear()

        for i in range(QumaSensorIndex.length):
            item = bpy.context.scene.qumaroidQumaSensorProperties.add()
            item.name = str(i)

        for boneName in QumaLooper.__vroidBoneNames:
            bpy.context.scene.qumaroidArmatureObject.pose.bones[boneName].rotation_mode = QumaLooper.__translateRotationMode(boneName)

    def __QumaLoop():
 
        try:
            # 1. Quma update sensors
            qumaAngleArr = LowApi.UpdateAndGetSensorReadings(QumaLooper.getQumaHandle(), QumaLooper.getQumaBoneSensorHandles())
            
            # 2. Prepare trigger Bone List
            triggeredBoneNameArray = []
            isRootTriggered = False

            for qumaSensorProp in bpy.context.scene.qumaroidQumaSensorProperties:
                # Trigger for root (1 degrees)
                if int(qumaSensorProp.name) == QumaSensorIndex.Root_Rotation_X or int(qumaSensorProp.name) == QumaSensorIndex.Root_Rotation_Y or int(qumaSensorProp.name) == QumaSensorIndex.Root_Rotation_Z:
                    isRootTriggered = isRootTriggered or abs(qumaSensorProp.angle - qumaAngleArr[int(qumaSensorProp.name)]) > QumaLooper.ONE_DEGREE_IN_RADIANS

                # Trigger for other bones (0.1 degrees)
                else:
                    triggered = abs(qumaSensorProp.angle - qumaAngleArr[int(qumaSensorProp.name)]) > QumaLooper.ZERO_POINT_ONE_DEGREE_IN_RADIANS
                    if triggered:
                        boneName = QumaLooper.GetTriggeredVroidBoneName(int(qumaSensorProp.name))
                        if boneName and not boneName in triggeredBoneNameArray:
                            triggeredBoneNameArray.append(boneName)

                # store angle value globally
                qumaSensorProp.angle = qumaAngleArr[int(qumaSensorProp.name)]

            # 2.1 Update bone lock
            for boneName in QumaLooper.getVroidBoneNames():
                # Update the bone on unlock
                triggered = bpy.context.scene.qumaroidLockBoneArr[boneName].locked and not QumaLooper.IsQumaPanelBoneLocked(boneName) 
                bpy.context.scene.qumaroidLockBoneArr[boneName].locked = QumaLooper.IsQumaPanelBoneLocked(boneName)

                if triggered and not boneName in triggeredBoneNameArray:
                    triggeredBoneNameArray.append(boneName)
            
            # 3. Update Root Rotation
            if qumaAngleArr[QumaSensorIndex.Button] == 1 and bpy.context.scene.qumaroidIsPosing and isRootTriggered:
                # VVV Cause of crash (If using QumaLooper.__getQumaRot which uses bpy.context.scene.qumaroidQumaSensorProperties instead of qumaAngleArr)
                rootVec = QumaLooper.translateBoneRotation(VroidBonename.J_Bip_C_Hips.name, qumaAngleArr)
                QumaLooper.rotateBone(VroidBonename.J_Bip_C_Hips.name, rootVec)

            # 4. Update Vroid bones
            for boneName in triggeredBoneNameArray:
                if bpy.context.scene.qumaroidIsPosing:
                    vec = QumaLooper.translateBoneRotation(boneName, qumaAngleArr)
                    QumaLooper.rotateBone(boneName, vec) 
                
        except Exception as e:
            print(str(e))
            PopupUtils.ShowMessageBox(str(e), "Error", 'ERROR')

        # End of Loop

        if bpy.context.scene.qumaroidIsPosing:
            return bpy.context.scene.qumaroidRefreshInterval
        else:
            return None
        
    #endregion
    
    #region QumaLooper -> private functions

    def translateBoneRotation(vroidBoneName, qumaAngleArray):

        if vroidBoneName == VroidBonename.J_Bip_C_Hips.name:
            return qumaAngleArray[QumaSensorIndex.Root_Rotation_X] + QumaLooper.DEGREES_20_RAD + qumaAngleArray[QumaSensorIndex.Waist_H_0], qumaAngleArray[QumaSensorIndex.Root_Rotation_Y], - qumaAngleArray[QumaSensorIndex.Root_Rotation_Z] - qumaAngleArray[QumaSensorIndex.Waist_H_1]
        
        elif vroidBoneName == VroidBonename.J_Bip_C_Head.name:
            return qumaAngleArray[QumaSensorIndex.Head_0], -qumaAngleArray[QumaSensorIndex.Head_1], 0
        
        elif vroidBoneName == VroidBonename.J_Bip_C_Neck.name:
            return -qumaAngleArray[QumaSensorIndex.Neck_1], 0, qumaAngleArray[QumaSensorIndex.Neck_0]
        
        elif vroidBoneName == VroidBonename.J_Bip_C_Chest.name:
            return -qumaAngleArray[QumaSensorIndex.Waist_H_0], 0, -qumaAngleArray[QumaSensorIndex.Waist_H_1]
        
        elif vroidBoneName == VroidBonename.J_Bip_C_Spine.name:
            return 0, -qumaAngleArray[QumaSensorIndex.Waist_V_0], 0
        
        elif vroidBoneName == VroidBonename.J_Bip_L_UpperArm.name:
            x = -qumaAngleArray[QumaSensorIndex.L_Shoulder_1] * math.cos(qumaAngleArray[QumaSensorIndex.L_Shoulder_0])
            y = -qumaAngleArray[QumaSensorIndex.L_Shoulder_0] - qumaAngleArray[QumaSensorIndex.L_Shoulder_2]
            z = -qumaAngleArray[QumaSensorIndex.L_Shoulder_1] * math.sin(qumaAngleArray[QumaSensorIndex.L_Shoulder_0])

            return x,y,z
        
        elif vroidBoneName == VroidBonename.J_Bip_L_LowerArm.name:
            return 0, -qumaAngleArray[QumaSensorIndex.L_Hand_0], qumaAngleArray[QumaSensorIndex.L_Elbow_0]
        
        elif vroidBoneName == VroidBonename.J_Bip_L_Hand.name:
            return -qumaAngleArray[QumaSensorIndex.L_Hand_1], 0, 0
        
        elif vroidBoneName == VroidBonename.J_Bip_R_UpperArm.name:
            x = qumaAngleArray[QumaSensorIndex.R_Shoulder_1] * math.cos(qumaAngleArray[QumaSensorIndex.R_Shoulder_0])
            y = -qumaAngleArray[QumaSensorIndex.R_Shoulder_0] - qumaAngleArray[QumaSensorIndex.R_Shoulder_2]
            z = qumaAngleArray[QumaSensorIndex.R_Shoulder_1] * math.sin(qumaAngleArray[QumaSensorIndex.R_Shoulder_0])

            return x,y,z
        
        elif vroidBoneName == VroidBonename.J_Bip_R_LowerArm.name:
            return 0, -qumaAngleArray[QumaSensorIndex.R_Hand_0], qumaAngleArray[QumaSensorIndex.R_Elbow_0]
        
        elif vroidBoneName == VroidBonename.J_Bip_R_Hand.name:
            return qumaAngleArray[QumaSensorIndex.R_Hand_1], 0, 0
        
        elif vroidBoneName == VroidBonename.J_Bip_L_UpperLeg.name:
            x = qumaAngleArray[QumaSensorIndex.L_Thigh_0]
            y = math.sin(qumaAngleArray[QumaSensorIndex.L_Thigh_0]) * qumaAngleArray[QumaSensorIndex.L_Thigh_1]
            z = -math.cos(qumaAngleArray[QumaSensorIndex.L_Thigh_0]) * qumaAngleArray[QumaSensorIndex.L_Thigh_1]

            return x,y,z
        
        elif vroidBoneName == VroidBonename.J_Bip_L_LowerLeg.name:
            return -qumaAngleArray[QumaSensorIndex.L_Leg_0], -qumaAngleArray[QumaSensorIndex.L_Thigh_2], 0
        
        elif vroidBoneName == VroidBonename.J_Bip_L_Foot.name:
            return qumaAngleArray[QumaSensorIndex.L_Foot_1], -qumaAngleArray[QumaSensorIndex.L_Foot_0], 0
        
        elif vroidBoneName == VroidBonename.J_Bip_R_UpperLeg.name:
            x = -qumaAngleArray[QumaSensorIndex.R_Thigh_0]
            y = -math.sin(qumaAngleArray[QumaSensorIndex.R_Thigh_0]) * qumaAngleArray[QumaSensorIndex.R_Thigh_1]
            z =  -math.cos(qumaAngleArray[QumaSensorIndex.R_Thigh_0]) * qumaAngleArray[QumaSensorIndex.R_Thigh_1]

            return x,y,z
        
        elif vroidBoneName == VroidBonename.J_Bip_R_LowerLeg.name:
            return qumaAngleArray[QumaSensorIndex.R_Leg_0], -qumaAngleArray[QumaSensorIndex.R_Thigh_2], 0
        
        elif vroidBoneName == VroidBonename.J_Bip_R_Foot.name:
            return -qumaAngleArray[QumaSensorIndex.R_Foot_1], -qumaAngleArray[QumaSensorIndex.R_Foot_0], 0
        
        return 0,0,0
    
    def __translateRotationMode(vroidBoneName):
        if vroidBoneName == VroidBonename.J_Bip_L_UpperArm.name:
            return "YXZ"
        elif vroidBoneName == VroidBonename.J_Bip_R_UpperArm.name:
            return "YXZ"

        return "XYZ"
    
    def GetTriggeredVroidBoneName(qumaSensorIndex):
        if qumaSensorIndex == QumaSensorIndex.Head_0 or qumaSensorIndex == QumaSensorIndex.Head_1:
            return VroidBonename.J_Bip_C_Head.name
        
        if qumaSensorIndex == QumaSensorIndex.Neck_0 or qumaSensorIndex == QumaSensorIndex.Neck_1:
            return VroidBonename.J_Bip_C_Neck.name
            
        if qumaSensorIndex == QumaSensorIndex.Waist_H_0 or qumaSensorIndex == QumaSensorIndex.Waist_H_1:
            return VroidBonename.J_Bip_C_Chest.name
        
        if qumaSensorIndex == QumaSensorIndex.Waist_V_0:
            return VroidBonename.J_Bip_C_Spine.name
        
        if qumaSensorIndex == QumaSensorIndex.L_Shoulder_0 or qumaSensorIndex == QumaSensorIndex.L_Shoulder_1 or qumaSensorIndex == QumaSensorIndex.L_Shoulder_2:
            return VroidBonename.J_Bip_L_UpperArm.name
    
        if qumaSensorIndex == QumaSensorIndex.L_Elbow_0 or qumaSensorIndex == QumaSensorIndex.L_Hand_0:
            return VroidBonename.J_Bip_L_LowerArm.name
    
        if qumaSensorIndex == QumaSensorIndex.L_Hand_1:
            return VroidBonename.J_Bip_L_Hand.name
    
        if qumaSensorIndex == QumaSensorIndex.R_Shoulder_0 or qumaSensorIndex == QumaSensorIndex.R_Shoulder_1 or qumaSensorIndex == QumaSensorIndex.R_Shoulder_2:
            return VroidBonename.J_Bip_R_UpperArm.name
    
        if qumaSensorIndex == QumaSensorIndex.R_Elbow_0 or qumaSensorIndex == QumaSensorIndex.R_Hand_0:
            return VroidBonename.J_Bip_R_LowerArm.name
    
        if qumaSensorIndex == QumaSensorIndex.R_Hand_1:
            return VroidBonename.J_Bip_R_Hand.name
    
        if qumaSensorIndex == QumaSensorIndex.L_Thigh_0 or qumaSensorIndex == QumaSensorIndex.L_Thigh_1:
            return VroidBonename.J_Bip_L_UpperLeg.name
    
        if qumaSensorIndex == QumaSensorIndex.L_Thigh_2 or qumaSensorIndex == QumaSensorIndex.L_Leg_0:
            return VroidBonename.J_Bip_L_LowerLeg.name
    
        if qumaSensorIndex == QumaSensorIndex.L_Foot_0 or qumaSensorIndex == QumaSensorIndex.L_Foot_1:
            return VroidBonename.J_Bip_L_Foot.name
    
        if qumaSensorIndex == QumaSensorIndex.R_Thigh_0 or qumaSensorIndex == QumaSensorIndex.R_Thigh_1:
            return VroidBonename.J_Bip_R_UpperLeg.name
    
        if qumaSensorIndex == QumaSensorIndex.R_Thigh_2 or qumaSensorIndex == QumaSensorIndex.R_Leg_0:
            return VroidBonename.J_Bip_R_LowerLeg.name
    
        if qumaSensorIndex == QumaSensorIndex.R_Foot_0 or qumaSensorIndex == QumaSensorIndex.R_Foot_1:
            return VroidBonename.J_Bip_R_Foot.name
        
        return None
    
    def rotateBone(boneName, vec):

        if bpy.context.scene.qumaroidLockBoneArr[boneName].locked:
            return

        if abs(bpy.context.scene.qumaroidArmatureObject.pose.bones[boneName].rotation_euler[0] - vec[0]) > QumaLooper.ZERO_POINT_ONE_DEGREE_IN_RADIANS:
            bpy.context.scene.qumaroidArmatureObject.pose.bones[boneName].rotation_euler[0] = float(vec[0])
        if abs(bpy.context.scene.qumaroidArmatureObject.pose.bones[boneName].rotation_euler[1] - vec[1]) > QumaLooper.ZERO_POINT_ONE_DEGREE_IN_RADIANS:
            bpy.context.scene.qumaroidArmatureObject.pose.bones[boneName].rotation_euler[1] = float(vec[1])
        if abs(bpy.context.scene.qumaroidArmatureObject.pose.bones[boneName].rotation_euler[2] - vec[2]) > QumaLooper.ZERO_POINT_ONE_DEGREE_IN_RADIANS:
            bpy.context.scene.qumaroidArmatureObject.pose.bones[boneName].rotation_euler[2] = float(vec[2])

    def IsQumaPanelBoneLocked(boneName):
        if QumaLooper.PANEL_LOCK_BONE_PREFIX + boneName in bpy.context.scene:
            return bpy.context.scene[QumaLooper.PANEL_LOCK_BONE_PREFIX + boneName]
        
        return False

    #endregion