import bpy

from ...posePanelConstants import PoseMode
from .depsgraphHandler.ikDepsgraphHandler import IKDepsgraphHandler
from .ikMarkerHelper.IKMarkerHelper import IKMarkerHelper
from .ikGroup.ikGroup import IKGroup
from .ikGroup.headIKGroup import HeadIKGroup
from .ikGroup.spineIKGroup import SpineIKGroup
from .ikGroup.hipsIKGroup import HipsIKGroup
from .ikGroup.leftArmIKGroup import LeftArmIKGroup
from .ikGroup.rightArmIKGroup import RightArmIKGroup
from .ikGroup.leftLegIKGroup import LeftLegIKGroup
from .ikGroup.rightLegIKGroup import RightLegIKGroup

class IKPoser:
    
    headIKGroup:IKGroup = None
    spineIKGroup:IKGroup = None
    hipsIKGroup:IKGroup = None
    leftArmIKGroup:IKGroup = None
    rightArmIKGroup:IKGroup = None
    leftLegIKGroup:IKGroup = None
    rightLegIKGroup:IKGroup = None
        
    def StartPosing() -> None:
        
        # Head        
        if bpy.context.scene.qumaroidHeadPoseMode == PoseMode.IK.value:
            if IKPoser.headIKGroup is None:
                IKPoser.headIKGroup = HeadIKGroup()
        else:
            if IKPoser.headIKGroup is not None:
                IKPoser.headIKGroup.StopIK()
                IKPoser.headIKGroup = None
                
        # Spine
        if bpy.context.scene.qumaroidSpinePoseMode == PoseMode.IK.value:
            if IKPoser.spineIKGroup is None:
                IKPoser.spineIKGroup = SpineIKGroup()
        else:
            if IKPoser.spineIKGroup is not None:
                IKPoser.spineIKGroup.StopIK()
                IKPoser.spineIKGroup = None
        
        # Hips
        if bpy.context.scene.qumaroidHipsPoseMode == PoseMode.IK.value:
            if IKPoser.hipsIKGroup is None:
                IKPoser.hipsIKGroup = HipsIKGroup()
        else:
            if IKPoser.hipsIKGroup is not None:
                IKPoser.hipsIKGroup.StopIK()
                IKPoser.hipsIKGroup = None
                
        # Left Arm
        if bpy.context.scene.qumaroidLeftArmPoseMode == PoseMode.IK.value:
            if IKPoser.leftArmIKGroup is None:
                IKPoser.leftArmIKGroup = LeftArmIKGroup()
        else:
            if IKPoser.leftArmIKGroup is not None:
                IKPoser.leftArmIKGroup.StopIK()
                IKPoser.leftArmIKGroup = None
            
        # Right Arm
        if bpy.context.scene.qumaroidRightArmPoseMode == PoseMode.IK.value:
            if IKPoser.rightArmIKGroup is None:
                IKPoser.rightArmIKGroup = RightArmIKGroup()
        else:
            if IKPoser.rightArmIKGroup is not None:
                IKPoser.rightArmIKGroup.StopIK()
                IKPoser.rightArmIKGroup = None
             
        # Left Leg
        if bpy.context.scene.qumaroidLeftLegPoseMode == PoseMode.IK.value:            
            if IKPoser.leftLegIKGroup is None:
                IKPoser.leftLegIKGroup = LeftLegIKGroup()
        else:
            if IKPoser.leftLegIKGroup is not None:
                IKPoser.leftLegIKGroup.StopIK()
                IKPoser.leftLegIKGroup = None
            
        # Right Leg
        if bpy.context.scene.qumaroidRightLegPoseMode == PoseMode.IK.value:
            if IKPoser.rightLegIKGroup is None:
                IKPoser.rightLegIKGroup = RightLegIKGroup()
        else:
            if IKPoser.rightLegIKGroup is not None:
                IKPoser.rightLegIKGroup.StopIK()
                IKPoser.rightLegIKGroup = None
            
        # Update Marker Scale
        IKPoser.ScaleAllIKMarkers()        
        
        # Add depsgraphHandler
        IKDepsgraphHandler.AppendIKCursorHandler(IKPoser.SnapAllIKMarkers)
            
    def StopPosing() -> None:
        if IKPoser.headIKGroup is not None:
            IKPoser.headIKGroup.StopIK()
            IKPoser.headIKGroup = None
        
        if IKPoser.spineIKGroup is not None:
            IKPoser.spineIKGroup.StopIK()
            IKPoser.spineIKGroup = None
        
        if IKPoser.hipsIKGroup is not None:
            IKPoser.hipsIKGroup.StopIK()
            IKPoser.hipsIKGroup = None
        
        if IKPoser.leftArmIKGroup is not None:
            IKPoser.leftArmIKGroup.StopIK()
            IKPoser.leftArmIKGroup = None
            
        if IKPoser.rightArmIKGroup is not None:
            IKPoser.rightArmIKGroup.StopIK()
            IKPoser.rightArmIKGroup = None
            
        if IKPoser.leftLegIKGroup is not None:
            IKPoser.leftLegIKGroup.StopIK()
            IKPoser.leftLegIKGroup = None
            
        if IKPoser.rightLegIKGroup is not None:
            IKPoser.rightLegIKGroup.StopIK()
            IKPoser.rightLegIKGroup = None
    
    def ScaleAllIKMarkers() -> None:
        scale = bpy.context.scene.qumaroidIKMarkerScale
        collection = bpy.data.collections.get(IKMarkerHelper.COLLECT_NAME)
        if collection is not None:
            for object in collection.objects:
                object.scale = scale, scale, scale
                
    def SnapAllIKMarkers(obj):
        if IKPoser.headIKGroup is not None:
            IKPoser.headIKGroup.AlignMarkers()
            
        if IKPoser.spineIKGroup is not None:
            IKPoser.spineIKGroup.AlignMarkers()            
        
        if IKPoser.hipsIKGroup is not None:
            IKPoser.hipsIKGroup.AlignMarkers()            
        
        if IKPoser.leftArmIKGroup is not None:
            IKPoser.leftArmIKGroup.AlignMarkers()            
        
        if IKPoser.rightArmIKGroup is not None:
            IKPoser.rightArmIKGroup.AlignMarkers()            
        
        if IKPoser.leftLegIKGroup is not None:
            IKPoser.leftLegIKGroup.AlignMarkers()            
        
        if IKPoser.rightLegIKGroup is not None:
            IKPoser.rightLegIKGroup.AlignMarkers()