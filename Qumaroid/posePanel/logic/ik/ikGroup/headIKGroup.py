import bpy, math

from .ikGroup import IKGroup

class HeadIKGroup(IKGroup):
    
    markerName0 = "IK_Cursor_Neck"
    headBoneName = "J_Bip_C_Head"
    neckBoneName = "J_Bip_C_Neck"
    
    def __init__(self):
        super().__init__()
        
        # Create IK
        armature = self.GetArmature()
        
        self.ConnectBones(armature, [self.neckBoneName, self.headBoneName])
        
        self.ClearIK([self.neckBoneName, self.headBoneName])
        
        self.CreateMarkers(armature)
        self.AlignMarkers()
                
        self.CreateIK(armature)
        
    def CreateMarkers(self, armature):
        self.marker0 = self.CreateMarker(armature, self.markerName0, "cube")
    
    def AlignMarkers(self):
        armature = self.GetArmature()
        if armature is None:
            return
        
        if not self.CheckAllMarkers([self.markerName0]):
            return
                
        neckBone = armature.pose.bones[self.neckBoneName]
        headBone = armature.pose.bones[self.headBoneName]
        
        self.marker0.rotation_euler = (headBone.matrix).to_euler()
        self.marker0.location = neckBone.tail
        
    def CreateIK(self, armature):
        neckIK = (armature.pose.bones[self.neckBoneName].constraints.get("IK") or
                       armature.pose.bones[self.neckBoneName].constraints.new("IK"))
        neckIK.target = self.marker0
        neckIK.chain_count = 1

        headCopyRotate = (armature.pose.bones[self.headBoneName].constraints.get("COPY_ROTATION") or 
                        armature.pose.bones[self.headBoneName].constraints.new("COPY_ROTATION"))
        headCopyRotate.target = self.marker0
        
    def ApplyIKPose(self):
        armature = self.GetArmature()
        if armature is None:
            return
        
        isArmatureHidden = armature.hide_get()
        armature.hide_set(False)
        bpy.context.view_layer.objects.active = armature
        # Must Be Done in Pose Mode
        bpy.ops.object.mode_set(mode='POSE')

        neckBone = armature.data.bones[self.neckBoneName]
        bpy.context.object.data.bones.active = neckBone
        bpy.ops.constraint.apply(constraint="IK", owner="BONE")

        # Apply Tip IK
        headBone = armature.data.bones[self.headBoneName]
        bpy.context.object.data.bones.active = headBone
        bpy.ops.constraint.apply(constraint="Copy Rotation", owner="BONE")

        # Exit Pose Mode
        bpy.ops.object.mode_set(mode='OBJECT')
        if isArmatureHidden:
            armature.hide_set(True) 
            
    def DeleteMarkers(self):
        self.DeleteMarker(self.marker0.name)
    