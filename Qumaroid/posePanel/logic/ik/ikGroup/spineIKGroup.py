import bpy, math

from .ikGroup import IKGroup

class SpineIKGroup(IKGroup):
    
    markerName0 = "IK_Cursor_Spine"
    markerName1 = "IK_Cursor_Chest"
    upperChestBoneName = "J_Bip_C_UpperChest"
    chestBoneName = "J_Bip_C_Chest"
    spineBoneName = "J_Bip_C_Spine"
    poleAngle = 90
    
    def __init__(self):
        super().__init__()
        
        # Create IK
        armature = self.GetArmature()
        
        self.ClearIK([self.spineBoneName, self.chestBoneName, self.upperChestBoneName])
        
        self.ConnectBones(armature, [self.spineBoneName, self.chestBoneName, self.upperChestBoneName])
        
        self.CreateMarkers(armature)
        self.AlignMarkers()
                
        self.CreateIK(armature)
        
    def CreateMarkers(self, armature):
        self.marker0 = self.CreateMarker(armature, self.markerName0, "sphere")
        self.marker1 = self.CreateMarker(armature, self.markerName1, "cube")
    
    def AlignMarkers(self):
        armature = self.GetArmature()
        if armature is None:
            return
        
        if not self.CheckAllMarkers([self.markerName0,self.markerName1]):
            return
                  
        upperChestBone = armature.pose.bones[self.upperChestBoneName]
        chestBone = armature.pose.bones[self.chestBoneName]
        spineBone = armature.pose.bones[self.spineBoneName]
        
        self.marker0.location = spineBone.tail
        
        self.marker1.rotation_euler = (upperChestBone.matrix).to_euler()
        self.marker1.location = chestBone.tail
        
    def CreateIK(self, armature):
        spineIK = (armature.pose.bones[self.spineBoneName].constraints.get("IK") or
                    armature.pose.bones[self.spineBoneName].constraints.new("IK"))
        spineIK.target = self.marker0
        spineIK.chain_count = 1
        
        chestIK = (armature.pose.bones[self.chestBoneName].constraints.get("IK") or
                    armature.pose.bones[self.chestBoneName].constraints.new("IK"))
        chestIK.target = self.marker1
        chestIK.chain_count = 1
        
        upperChestCopyRotate = (armature.pose.bones[self.upperChestBoneName].constraints.get("COPY_ROTATION") or 
                                armature.pose.bones[self.upperChestBoneName].constraints.new("COPY_ROTATION"))
        upperChestCopyRotate.target = self.marker1
    
    def ApplyIKPose(self):
        armature = self.GetArmature()
        if armature is None:
            return
        
        isArmatureHidden = armature.hide_get()
        armature.hide_set(False)
        bpy.context.view_layer.objects.active = armature
        # Must Be Done in Pose Mode
        bpy.ops.object.mode_set(mode='POSE')
        
        spineBone = armature.data.bones[self.spineBoneName]
        bpy.context.object.data.bones.active = spineBone
        bpy.ops.constraint.apply(constraint="IK", owner="BONE")

        chestBone = armature.data.bones[self.chestBoneName]
        bpy.context.object.data.bones.active = chestBone
        bpy.ops.constraint.apply(constraint="IK", owner="BONE")

        # Apply Tip IK
        upperChestBone = armature.data.bones[self.upperChestBoneName]
        bpy.context.object.data.bones.active = upperChestBone
        bpy.ops.constraint.apply(constraint="Copy Rotation", owner="BONE")

        
        # Exit Pose Mode
        bpy.ops.object.mode_set(mode='OBJECT')
        if isArmatureHidden:
            armature.hide_set(True) 
            
    def DeleteMarkers(self):
        self.DeleteMarker(self.marker0.name)
        self.DeleteMarker(self.marker1.name)