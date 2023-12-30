import bpy, math

from .ikGroup import IKGroup

class HipsIKGroup(IKGroup):
    
    markerName0 = "IK_Cursor_Hips"
    hipsBoneName = "J_Bip_C_Hips"
    
    def __init__(self):
        super().__init__()
        
        # Create IK
        armature = self.GetArmature()
        
        self.ClearIK([self.hipsBoneName])
        
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
                      
        hipsBone = armature.pose.bones[self.hipsBoneName]
        
        self.marker0.rotation_euler = (hipsBone.matrix).to_euler()
        self.marker0.location = hipsBone.head
               
    def CreateIK(self, armature):
        hipsCopyRotate = (armature.pose.bones[self.hipsBoneName].constraints.get("COPY_ROTATION") or 
                        armature.pose.bones[self.hipsBoneName].constraints.new("COPY_ROTATION"))
        hipsCopyRotate.target = self.marker0
        
        hipsCopyLocation = (armature.pose.bones[self.hipsBoneName].constraints.get("COPY_LOCATION") or 
                        armature.pose.bones[self.hipsBoneName].constraints.new("COPY_LOCATION"))
        hipsCopyLocation.target = self.marker0
    
    def ApplyIKPose(self):
        armature = self.GetArmature()
        if armature is None:
            return
        
        isArmatureHidden = armature.hide_get()
        armature.hide_set(False)
        bpy.context.view_layer.objects.active = armature
        # Must Be Done in Pose Mode
        bpy.ops.object.mode_set(mode='POSE')

        # Apply Hips Rotation
        hipsBone = armature.data.bones[self.hipsBoneName]
        bpy.context.object.data.bones.active = hipsBone
        bpy.ops.constraint.apply(constraint="Copy Rotation", owner="BONE")
        # Apply Hips Location
        bpy.ops.constraint.apply(constraint="Copy Location", owner="BONE")

        # Exit Pose Mode
        bpy.ops.object.mode_set(mode='OBJECT')
        if isArmatureHidden:
            armature.hide_set(True) 
            
    def DeleteMarkers(self):
        self.DeleteMarker(self.marker0.name)
    