import bpy, math

from .ikGroup import IKGroup

class RightLegIKGroup(IKGroup):
    
    markerName1 = "IK_Cursor_Right_Knee"
    markerName2 = "IK_Cursor_Right_Foot"
    upperLimbBoneName = "J_Bip_R_UpperLeg"
    lowerLimbBoneName = "J_Bip_R_LowerLeg"
    tipBoneName = "J_Bip_R_Foot"
    poleAngle = 90
    upperLimbRotationMode = 'ZXY'
    
    def __init__(self):
        super().__init__()
        
        # Create IK
        armature = self.GetArmature()
        
        self.ClearIK([self.upperLimbBoneName, self.lowerLimbBoneName, self.tipBoneName])
        
        self.ConnectBones(armature, [self.upperLimbBoneName, self.lowerLimbBoneName, self.tipBoneName])
        self.AddIKLimit(armature, self.lowerLimbBoneName, -180,0, 0,0, 0,0)
        
        self.CreateMarkers(armature)
        self.AlignMarkers()
                
        self.CreateIK(armature)
    
    def CreateMarkers(self, armature):
        self.marker1 = self.CreateMarker(armature, self.markerName1, "sphere")
        self.marker2 = self.CreateMarker(armature, self.markerName2, "cube")
    
    def AlignMarkers(self):
        armature = self.GetArmature()
        if armature is None:
            return
             
        if not self.CheckAllMarkers([self.markerName1,self.markerName2]):
            return
                  
        lowerLimbBone = armature.pose.bones[self.lowerLimbBoneName]
        tipBone = armature.pose.bones[self.tipBoneName]    
        
        self.marker2.location = lowerLimbBone.tail
        self.marker2.rotation_euler = (tipBone.matrix).to_euler()
        self.marker1.location = lowerLimbBone.head
        
    def CreateIK(self, armature):
        lowerLimbIK = (armature.pose.bones[self.lowerLimbBoneName].constraints.get("IK") or
                       armature.pose.bones[self.lowerLimbBoneName].constraints.new("IK"))
        lowerLimbIK.target = self.marker2
        lowerLimbIK.pole_target = self.marker1
        lowerLimbIK.pole_angle = math.radians(self.poleAngle)
        lowerLimbIK.chain_count = 2

        tipCopyRotate = (armature.pose.bones[self.tipBoneName].constraints.get("COPY_ROTATION") or 
                        armature.pose.bones[self.tipBoneName].constraints.new("COPY_ROTATION"))
        tipCopyRotate.target = self.marker2

    def ApplyIKPose(self):
        armature = self.GetArmature()
        if armature is None:
            return
        
        isArmatureHidden = armature.hide_get()
        armature.hide_set(False)
        bpy.context.view_layer.objects.active = armature
        # Must Be Done in Pose Mode
        bpy.ops.object.mode_set(mode='POSE')

        upperLimbBone = armature.pose.bones[self.upperLimbBoneName]
        upperLimbBone.rotation_mode = self.upperLimbRotationMode
        upperLimbBone.rotation_euler = self.GetBoneAngleAgainstParent(upperLimbBone)

        # Add and Apply Upper Limb IK
        upperLimbIK = (armature.pose.bones[self.upperLimbBoneName].constraints.get("IK") or
                    armature.pose.bones[self.upperLimbBoneName].constraints.new("IK"))
        upperLimbIK.target = bpy.data.objects[self.markerName1]
        upperLimbIK.chain_count = 1

        bpy.context.object.data.bones.active = armature.data.bones[self.upperLimbBoneName]
        bpy.ops.constraint.apply(constraint="IK", owner="BONE")

        # Apply Lower Limb IK
        lowerLimbBone = armature.data.bones[self.lowerLimbBoneName]
        bpy.context.object.data.bones.active = lowerLimbBone
        bpy.ops.constraint.apply(constraint="IK", owner="BONE")

        # Apply Tip IK
        tipBone = armature.data.bones[self.tipBoneName]
        bpy.context.object.data.bones.active = tipBone
        bpy.ops.constraint.apply(constraint="Copy Rotation", owner="BONE")

        # Exit Pose Mode
        bpy.ops.object.mode_set(mode='OBJECT')
        if isArmatureHidden:
            armature.hide_set(True)
            
    def DeleteMarkers(self):
        self.DeleteMarker(self.marker1.name)
        self.DeleteMarker(self.marker2.name)
    