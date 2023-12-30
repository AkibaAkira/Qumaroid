import bpy

from ..logic.ik.IKPoser import IKPoser
from ..logic.qumarion.QumaPoser import QumaPoserUtils
from ..posePanelConstants import PoseMode

class QumaResetBones(bpy.types.Operator):
    bl_label = "Reset Bones"
    bl_idname = "object.quma_reset_bones"
    bl_description = "Reset Bones"
    
    def execute(self, context):
        # Reset Bones Logic
        armature = bpy.context.scene.qumaroidArmatureObject
        if armature is not None:
            for bone in armature.pose.bones:
                bone.rotation_mode = 'XYZ'   
                bone.rotation_euler = 0,0,0
                bone.location = 0,0,0
                
        return {'FINISHED'}

class PosePanel:
    
    def DrawPanel(layout):
        scene = bpy.context.scene
        
        # Reset Bones Button
        row = layout.row()
        row.operator("object.quma_reset_bones")
        
        # Pose Mode Radio Buttons
        row = layout.row()
        row.label(text="Head")
        row.prop(scene, "qumaroidHeadPoseMode", expand=True)

        row = layout.row()
        row.label(text="Spine")
        row.prop(scene, "qumaroidSpinePoseMode", expand=True)
        
        row = layout.row()
        row.label(text="Left Arm")
        row.prop(scene, "qumaroidLeftArmPoseMode", expand=True)

        row = layout.row()
        row.label(text="Right Arm")
        row.prop(scene, "qumaroidRightArmPoseMode", expand=True)
        
        row = layout.row()
        row.label(text="Left Leg")
        row.prop(scene, "qumaroidLeftLegPoseMode", expand=True)

        row = layout.row()
        row.label(text="Right Leg")
        row.prop(scene, "qumaroidRightLegPoseMode", expand=True)
        
        row = layout.row()
        row.label(text="Hips")
        row.prop(scene, "qumaroidHipsPoseMode", expand=True)
        
        row = layout.row()
        row.prop(scene, "qumaroidIKMarkerScale")

    def StopPosing(scene):
        scene.qumaroidHeadPoseMode = PoseMode.OFF.value
        scene.qumaroidSpinePoseMode = PoseMode.OFF.value
        scene.qumaroidHipsPoseMode = PoseMode.OFF.value
        scene.qumaroidLeftArmPoseMode = PoseMode.OFF.value
        scene.qumaroidRightArmPoseMode = PoseMode.OFF.value
        scene.qumaroidLeftLegPoseMode = PoseMode.OFF.value
        scene.qumaroidRightLegPoseMode = PoseMode.OFF.value
        
        QumaPoserUtils.StopPosing()
        IKPoser.StopPosing()
 
    def __OnUpdateIKMarkerScale(self, context):
        IKPoser.ScaleAllIKMarkers()
 
    def __OnPoseModeUpdate(self, context):
        IKPoser.StartPosing()
        QumaPoserUtils.StartPosing()
        
    def register(): 
        
        bpy.utils.register_class(QumaResetBones)
        
        commonPoseModeProperties = bpy.props.EnumProperty(
                                        update=PosePanel.__OnPoseModeUpdate,
                                        items=[
                                            (PoseMode.OFF.value, 'Off', 'Off', '', 0),
                                            (PoseMode.QUMARION.value, 'Quma', 'Pose by Qumarion', '', 1),
                                            (PoseMode.IK.value, 'IK', 'Pose by IK', '', 2)
                                            ],
                                        default=PoseMode.OFF.value)
        
        bpy.types.Scene.qumaroidHeadPoseMode = commonPoseModeProperties
        bpy.types.Scene.qumaroidSpinePoseMode = commonPoseModeProperties
        bpy.types.Scene.qumaroidLeftArmPoseMode = commonPoseModeProperties
        bpy.types.Scene.qumaroidRightArmPoseMode = commonPoseModeProperties
        bpy.types.Scene.qumaroidLeftLegPoseMode = commonPoseModeProperties
        bpy.types.Scene.qumaroidRightLegPoseMode = commonPoseModeProperties
        bpy.types.Scene.qumaroidHipsPoseMode = commonPoseModeProperties
        
        bpy.types.Scene.qumaroidIKMarkerScale = bpy.props.FloatProperty(name="IK Size",
                                                                        update=PosePanel.__OnUpdateIKMarkerScale,    
                                                                        default=0.05,
                                                                        min=0,
                                                                        max=1)

    def unregister():
        
        bpy.utils.unregister_class(QumaResetBones)
        
        del bpy.types.Scene.qumaroidHeadPoseMode
        del bpy.types.Scene.qumaroidSpinePoseMode
        del bpy.types.Scene.qumaroidHipsPoseMode
        del bpy.types.Scene.qumaroidLeftArmPoseMode
        del bpy.types.Scene.qumaroidRightArmPoseMode
        del bpy.types.Scene.qumaroidLeftLegPoseMode
        del bpy.types.Scene.qumaroidRightLegPoseMode
        
        del bpy.types.Scene.qumaroidIKMarkerScale