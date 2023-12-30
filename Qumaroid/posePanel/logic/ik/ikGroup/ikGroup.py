import bpy, math

from ..ikMarkerHelper.IKMarkerHelper import IKMarkerHelper
from .....PopupUtils import PopupUtils

class IKGroup:
    
    def __init__(self):
        pass
    
    def StopIK(self):
        self.ApplyIKPose()
        self.DeleteMarkers()
    
    def ConnectBones(self, armature, ikBoneNameList:[str]):        
        isArmatureHidden = armature.hide_get()
        armature.hide_set(False)
        bpy.context.view_layer.objects.active = armature        
        # Must Be Done in Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Connect bones by ikBoneNameList sequence
        for i in range(len(ikBoneNameList) - 1):
            parentBoneName = ikBoneNameList[i]
            childBoneName = ikBoneNameList[i+1]
            armature.data.edit_bones[parentBoneName].tail = armature.data.edit_bones[childBoneName].head
            armature.data.edit_bones[childBoneName].use_connect = True
        
        bpy.ops.object.mode_set(mode='OBJECT')
        if isArmatureHidden:
            armature.hide_set(True)
    
    def AddIKLimit(self, armature, boneName, min_x, max_x, min_y, max_y, min_z, max_z):
        poseBone = armature.pose.bones[boneName]
        
        if min_x == 0 and max_x == 0:
            poseBone.lock_ik_x = True
            poseBone.use_ik_limit_x = False
        else:
            poseBone.lock_ik_x = False
            poseBone.use_ik_limit_x = True
            poseBone.ik_min_x = math.radians(min_x)
            poseBone.ik_max_x = math.radians(max_x)
            
        if min_y == 0 and max_y == 0:
            poseBone.lock_ik_y = True
            poseBone.use_ik_limit_y = False
        else:
            poseBone.lock_ik_y = False
            poseBone.use_ik_limit_y = True
            poseBone.ik_min_y = math.radians(min_y)
            poseBone.ik_max_y = math.radians(max_y)
        
        if min_z == 0 and max_z == 0:
            poseBone.lock_ik_z = True
            poseBone.use_ik_limit_z = False
        else:
            poseBone.lock_ik_z = False
            poseBone.use_ik_limit_z = True
            poseBone.ik_min_z = math.radians(min_z)
            poseBone.ik_max_z = math.radians(max_z)
            
    def CreateMarker(self, armature, markerName:str, markerType:str):
        marker = IKMarkerHelper.GetMarker(markerName, markerType)
        marker.parent = armature
        return marker
    
    def DeleteMarker(self, markerName:str):
        try:
            IKMarkerHelper.DeleteMarker(markerName)
        except Exception as e:
            PopupUtils.ShowMessageBox("Cannot delete marker" + markerName, "Error", "ERROR")
    
    def GetBoneAngleAgainstParent(self, bone):
        parentRotationEuler = bone.parent.matrix.to_euler()
        selfRotationEuler = bone.matrix.to_euler()
        result = (selfRotationEuler[0] - parentRotationEuler[0]), (selfRotationEuler[1] - parentRotationEuler[1]), (selfRotationEuler[2] - parentRotationEuler[2])
        return result
    
    def ClearIK(self, boneNames:[str]):
        armature = self.GetArmature()
        if armature is None:
            return
        
        isArmatureHidden = armature.hide_get()
        armature.hide_set(False)
        bpy.context.view_layer.objects.active = armature
        # Must Be Done in Pose Mode
        bpy.ops.object.mode_set(mode='POSE')

        for boneName in boneNames:
            bone = armature.data.bones[boneName]
            bpy.context.object.data.bones.active = bone
            bpy.ops.constraint.apply(constraint="IK", owner="BONE")
            bpy.ops.constraint.apply(constraint="Copy Rotation", owner="BONE")            
            bpy.ops.constraint.apply(constraint="Copy Location", owner="BONE")

        # Exit Pose Mode
        bpy.ops.object.mode_set(mode='OBJECT')
        if isArmatureHidden:
            armature.hide_set(True)
        
    def GetArmature(self):
        return bpy.context.scene.qumaroidArmatureObject  
    
    def CreateMarkers(self, armature):
        pass
    
    def AlignMarkers(self):
        pass  
    
    def CreateIK(self, armature):
        pass
    
    def ApplyIKPose(self):
        pass
    
    def DeleteMarkers(self):
        pass
    
    def CheckAllMarkers(self, markerNames:[str])->bool:
        
        objects = bpy.context.scene.objects.keys()
        for markerName in markerNames:
            if markerName not in objects:
                return False
        
        return True