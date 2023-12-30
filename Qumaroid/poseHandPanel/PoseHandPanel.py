import bpy
from ..BoneName import VroidBonename

class QumaSyncHands(bpy.types.Operator):
    bl_label = "Load Hand Rotations"
    bl_idname = "object.quma_sync_hands"
    bl_description = "Load hand rotations to panel"
    
    def execute(self, context):

        scene = context.scene

        if bpy.context.scene.qumaroidArmatureObject is None:
            return

        for side in PoseHandPanel.SideNames:

            scene[PoseHandPanel.EXPAND_LABEL_PREFIX + side + PoseHandPanel.OVERALL_SUFFIX] = 0
            scene[PoseHandPanel.GRIP_LABEL_PREFIX + side + PoseHandPanel.OVERALL_SUFFIX + PoseHandPanel.ROOT_SUFFIX] = 0
            scene[PoseHandPanel.GRIP_LABEL_PREFIX + side + PoseHandPanel.OVERALL_SUFFIX + PoseHandPanel.TIP_SUFFIX] = 0

            for fingerName in PoseHandPanel.FingerNames:
                
                scene[PoseHandPanel.ANGLE_UNLINK_PREFIX + side + fingerName] = True
                
                boneName1 = PoseHandPanel.VROID_BONE_PREFIX + side + fingerName + "1"
                boneName2 = PoseHandPanel.VROID_BONE_PREFIX + side + fingerName + "2"
                boneName3 = PoseHandPanel.VROID_BONE_PREFIX + side + fingerName + "3"

                if side == "R_":
                    sideFactor = -1
                else:
                    sideFactor = 1

                expandValue = sideFactor * bpy.context.scene.qumaroidArmatureObject.pose.bones[boneName1].rotation_euler[2] / PoseHandPanel.FINGER_EXPAND_FACTOR
                if fingerName == PoseHandPanel.Thumb:
                    gripRootValue = bpy.context.scene.qumaroidArmatureObject.pose.bones[boneName1].rotation_euler[1] / PoseHandPanel.THUMB_1_FACTOR
                    gripTipValue = (bpy.context.scene.qumaroidArmatureObject.pose.bones[boneName2].rotation_euler[2] / PoseHandPanel.THUMB_2_FACTOR + bpy.context.scene.qumaroidArmatureObject.pose.bones[boneName3].rotation_euler[2] / PoseHandPanel.THUMB_3_FACTOR)/2

                    gripRootValue = sideFactor * gripRootValue
                    gripTipValue = sideFactor * gripTipValue
                else:
                    gripRootValue = bpy.context.scene.qumaroidArmatureObject.pose.bones[boneName1].rotation_euler[0] / PoseHandPanel.FINGER_1_FACTOR
                    gripTipValue = (bpy.context.scene.qumaroidArmatureObject.pose.bones[boneName2].rotation_euler[0] / PoseHandPanel.FINGER_2_FACTOR + bpy.context.scene.qumaroidArmatureObject.pose.bones[boneName3].rotation_euler[0] / PoseHandPanel.FINGER_3_FACTOR)/2

                scene[PoseHandPanel.EXPAND_LABEL_PREFIX + side + fingerName] = expandValue
                scene[PoseHandPanel.GRIP_LABEL_PREFIX + side + fingerName + PoseHandPanel.ROOT_SUFFIX] = gripRootValue
                scene[PoseHandPanel.GRIP_LABEL_PREFIX + side + fingerName + PoseHandPanel.TIP_SUFFIX] = gripTipValue


        return {'FINISHED'}

class PoseHandPanel:

    ZERO_POINT_ONE_DEGREE_IN_RADIANS = 0.00174

    FINGER_EXPAND_FACTOR = 0.52360 # 30 DEGREES
    
    THUMB_1_FACTOR = 1.57079 # 90 DEGREES
    THUMB_2_FACTOR = 0.785398 # 45 DEGREES
    THUMB_3_FACTOR = 1.57079 # 90 DEGREES

    FINGER_1_FACTOR = -1.57079 # -90 DEGREES
    FINGER_2_FACTOR = -2.35619 # -135 DEGREES
    FINGER_3_FACTOR = -0.785398 # -45 DEGREES

    GRIP_LABEL_PREFIX = "qumaroidGripValue_"
    EXPAND_LABEL_PREFIX = "qumaroidExpaneValue_"
    ANGLE_UNLINK_PREFIX = "qumaroidUnlink_"

    VROID_BONE_PREFIX = "J_Bip_"

    OVERALL_SUFFIX = "Overall"
    ROOT_SUFFIX = "_Root"
    TIP_SUFFIX = "_Tip"

    SideNames = ["L_", "R_"]

    Thumb = "Thumb"
    __IndexFingerName = "Index"
    __MiddleFingerName = "Middle"
    __RingFingerName = "Ring"
    __LittleFingerName = "Little"

    FingerNames = [
        "Thumb",
        "Index",
        "Middle",
        "Ring",
        "Little"
    ]

    #region PoseHandPanel -> Register Functions

    def register():
        bpy.utils.register_class(QumaSyncHands)

        Scene = bpy.types.Scene

        Scene.qumaroidPanelShowPoseHandPanel = bpy.props.BoolProperty()
        Scene.qumaroidPanelShowLeftHandPanel = bpy.props.BoolProperty()
        Scene.qumaroidPanelShowRightHandPanel = bpy.props.BoolProperty()

        for side in PoseHandPanel.SideNames:
            
            # qumaroidExpaneValue_R_Overall
            setattr(Scene, PoseHandPanel.EXPAND_LABEL_PREFIX + side + PoseHandPanel.OVERALL_SUFFIX, 
                    bpy.props.FloatProperty(name="Expand", default=0, min=-0.3, max=1, update=PoseHandPanel.OnUpdateExpand))
            
            # qumaroidGripValue_R_Overall_Root
            setattr(Scene, PoseHandPanel.GRIP_LABEL_PREFIX + side + PoseHandPanel.OVERALL_SUFFIX + PoseHandPanel.ROOT_SUFFIX, 
                    bpy.props.FloatProperty(name="Grip", default=0, min=-0.1, max=1, update=PoseHandPanel.OnUpdateGrip))
                        
            # qumaroidGripValue_R_Overall_Tip
            setattr(Scene, PoseHandPanel.GRIP_LABEL_PREFIX + side + PoseHandPanel.OVERALL_SUFFIX + PoseHandPanel.TIP_SUFFIX, 
                    bpy.props.FloatProperty(name="Grip", default=0, min=-0.1, max=1, update=PoseHandPanel.OnUpdateGrip))

            for fingerName in PoseHandPanel.FingerNames:
                
                # qumaroidUnlink_R_Index
                setattr(Scene, PoseHandPanel.ANGLE_UNLINK_PREFIX + side + fingerName, 
                    bpy.props.BoolProperty(name="", default=False))
                
                # qumaroidExpandValue_R_Index
                setattr(Scene, PoseHandPanel.EXPAND_LABEL_PREFIX + side + fingerName, 
                    bpy.props.FloatProperty(name="Expand", default=0, min=-1, max=1, update=PoseHandPanel.OnUpdateExpand))
                
                # qumaroidGripValue_R_Index_Root
                setattr(Scene, PoseHandPanel.GRIP_LABEL_PREFIX + side + fingerName + PoseHandPanel.ROOT_SUFFIX, 
                    bpy.props.FloatProperty(name="Root Grip", default=0, min=-0.1, max=1, update=PoseHandPanel.OnUpdateGrip))
                
                # qumaroidGripValue_R_Index_Tip
                setattr(Scene, PoseHandPanel.GRIP_LABEL_PREFIX + side + fingerName + PoseHandPanel.TIP_SUFFIX, 
                    bpy.props.FloatProperty(name="Tip Grip", default=0, min=-0.1, max=1, update=PoseHandPanel.OnUpdateGrip))

    def unregister():
        bpy.utils.unregister_class(QumaSyncHands)

        del bpy.types.Scene.qumaroidPanelShowPoseHandPanel
        del bpy.types.Scene.qumaroidPanelShowLeftHandPanel
        del bpy.types.Scene.qumaroidPanelShowRightHandPanel

    #endregion

    #region PoseHandPanel -> Draw Panel

    def DrawPanel(layout):
        scene = bpy.context.scene

        row = layout.row()
        row.alignment = 'LEFT'
        row.prop(scene, "qumaroidPanelShowPoseHandPanel", icon="TRIA_DOWN" if scene.qumaroidPanelShowPoseHandPanel else "TRIA_RIGHT", icon_only=True, emboss=False, text="Pose Hands")

        if scene.qumaroidPanelShowPoseHandPanel:

            row = layout.row()
            row.operator("object.quma_sync_hands")

            row = layout.row()
            row.alignment = 'LEFT'
            row.prop(scene, "qumaroidPanelShowLeftHandPanel", icon="TRIA_DOWN" if scene.qumaroidPanelShowLeftHandPanel else "TRIA_RIGHT", icon_only=True, emboss=False, text="Left Hand")

            if scene.qumaroidPanelShowLeftHandPanel:
                PoseHandPanel.__DrawHandPanel(scene, layout, "L_")

            row = layout.row()
            row.alignment = 'LEFT'
            row.prop(scene, "qumaroidPanelShowRightHandPanel", icon="TRIA_DOWN" if scene.qumaroidPanelShowRightHandPanel else "TRIA_RIGHT", icon_only=True, emboss=False, text="Right Hand")

            if scene.qumaroidPanelShowRightHandPanel:
                PoseHandPanel.__DrawHandPanel(scene, layout, "R_")

    def __DrawHandPanel(scene, layout, side):        
        box = layout.box()

        row = box.row()
        row.label(text="Overall")

        row = box.row(align=True)
        row.prop(scene, PoseHandPanel.GRIP_LABEL_PREFIX + side + PoseHandPanel.OVERALL_SUFFIX + PoseHandPanel.TIP_SUFFIX)
        row.prop(scene, PoseHandPanel.GRIP_LABEL_PREFIX + side + PoseHandPanel.OVERALL_SUFFIX + PoseHandPanel.ROOT_SUFFIX)
        row.prop(scene, PoseHandPanel.EXPAND_LABEL_PREFIX + side + PoseHandPanel.OVERALL_SUFFIX)

        row = box.row()
        row.label(text="Unlink Fingers")

        row = box.row(align=True)
        for fingerName in PoseHandPanel.FingerNames:
            row.prop(scene, PoseHandPanel.ANGLE_UNLINK_PREFIX + side + fingerName)

        for fingerName in PoseHandPanel.FingerNames:
            row = box.row()
            row.label(text=fingerName)
            row = box.row(align=True)
            row.enabled = PoseHandPanel.__GetBoolProp(scene, PoseHandPanel.ANGLE_UNLINK_PREFIX + side + fingerName)
            row.prop(scene, PoseHandPanel.GRIP_LABEL_PREFIX + side + fingerName + PoseHandPanel.TIP_SUFFIX)
            row.prop(scene, PoseHandPanel.GRIP_LABEL_PREFIX + side + fingerName + PoseHandPanel.ROOT_SUFFIX)
            row.prop(scene, PoseHandPanel.EXPAND_LABEL_PREFIX + side + fingerName)  

    #endregion

    def __GetBoolProp(scene, propertyName)->bool:
        if propertyName in scene:
            return scene[propertyName]
        
        return False
    
    def __GetFloatProp(scene, propertyName)->float:
        if propertyName in scene:
            return scene[propertyName]
        
        return 0

    def OnUpdateExpand(self, context):
        scene = context.scene

        for side in PoseHandPanel.SideNames:
            
            expandValue = PoseHandPanel.__GetFloatProp(scene, PoseHandPanel.EXPAND_LABEL_PREFIX + side + PoseHandPanel.OVERALL_SUFFIX)

            for fingerName in PoseHandPanel.FingerNames:

                fingerBoneName1 = PoseHandPanel.VROID_BONE_PREFIX + side + fingerName + "1"

                # copy the value if not unlinked
                if not PoseHandPanel.__GetBoolProp(scene, PoseHandPanel.ANGLE_UNLINK_PREFIX + side + fingerName):
                    if fingerName == PoseHandPanel.Thumb:
                        scene[PoseHandPanel.EXPAND_LABEL_PREFIX + side + fingerName] = -expandValue
                    elif fingerName == PoseHandPanel.__IndexFingerName:
                        scene[PoseHandPanel.EXPAND_LABEL_PREFIX + side + fingerName] = -expandValue / 2
                    elif fingerName == PoseHandPanel.__MiddleFingerName:
                        scene[PoseHandPanel.EXPAND_LABEL_PREFIX + side + fingerName] = 0
                    elif fingerName == PoseHandPanel.__RingFingerName:
                        scene[PoseHandPanel.EXPAND_LABEL_PREFIX + side + fingerName] = expandValue / 2
                    elif fingerName == PoseHandPanel.__LittleFingerName:
                        scene[PoseHandPanel.EXPAND_LABEL_PREFIX + side + fingerName] = expandValue
                
                sideFactor = 1
                if side == "R_":
                    sideFactor = -1
                angle = PoseHandPanel.FINGER_EXPAND_FACTOR * PoseHandPanel.__GetFloatProp(scene, PoseHandPanel.EXPAND_LABEL_PREFIX + side + fingerName)
                PoseHandPanel.__RotateBone(fingerBoneName1, 2, sideFactor * angle)

    def OnUpdateGrip(self, context):
        
        scene = context.scene

        for side in PoseHandPanel.SideNames:
            
            grabValueRoot = PoseHandPanel.__GetFloatProp(scene, PoseHandPanel.GRIP_LABEL_PREFIX + side + PoseHandPanel.OVERALL_SUFFIX + PoseHandPanel.ROOT_SUFFIX)
            grabValueTip = PoseHandPanel.__GetFloatProp(scene, PoseHandPanel.GRIP_LABEL_PREFIX + side + PoseHandPanel.OVERALL_SUFFIX + PoseHandPanel.TIP_SUFFIX)
            
            for fingerName in PoseHandPanel.FingerNames:

                fingerBoneName1 = PoseHandPanel.VROID_BONE_PREFIX + side + fingerName + "1"
                fingerBoneName2 = PoseHandPanel.VROID_BONE_PREFIX + side + fingerName + "2"
                fingerBoneName3 = PoseHandPanel.VROID_BONE_PREFIX + side + fingerName + "3"

                # copy the value if not unlinked
                if not PoseHandPanel.__GetBoolProp(scene, PoseHandPanel.ANGLE_UNLINK_PREFIX + side + fingerName):
                    scene[PoseHandPanel.GRIP_LABEL_PREFIX + side + fingerName + PoseHandPanel.ROOT_SUFFIX] = grabValueRoot
                    scene[PoseHandPanel.GRIP_LABEL_PREFIX + side + fingerName + PoseHandPanel.TIP_SUFFIX] = grabValueTip
                
                if fingerName == PoseHandPanel.Thumb:
                    sideFactor = 1
                    if side == "R_":
                        sideFactor = -1
                    PoseHandPanel.__RotateBone(fingerBoneName1, 1, sideFactor * PoseHandPanel.THUMB_1_FACTOR * PoseHandPanel.__GetFloatProp(scene, PoseHandPanel.GRIP_LABEL_PREFIX + side + fingerName + PoseHandPanel.ROOT_SUFFIX))
                    PoseHandPanel.__RotateBone(fingerBoneName2, 2, sideFactor * PoseHandPanel.THUMB_2_FACTOR * PoseHandPanel.__GetFloatProp(scene, PoseHandPanel.GRIP_LABEL_PREFIX + side + fingerName + PoseHandPanel.TIP_SUFFIX))
                    PoseHandPanel.__RotateBone(fingerBoneName3, 2, sideFactor * PoseHandPanel.THUMB_3_FACTOR * PoseHandPanel.__GetFloatProp(scene, PoseHandPanel.GRIP_LABEL_PREFIX + side + fingerName + PoseHandPanel.TIP_SUFFIX))
                else:
                    PoseHandPanel.__RotateBone(fingerBoneName1, 0, PoseHandPanel.FINGER_1_FACTOR * PoseHandPanel.__GetFloatProp(scene, PoseHandPanel.GRIP_LABEL_PREFIX + side + fingerName + PoseHandPanel.ROOT_SUFFIX))
                    PoseHandPanel.__RotateBone(fingerBoneName2, 0, PoseHandPanel.FINGER_2_FACTOR * PoseHandPanel.__GetFloatProp(scene, PoseHandPanel.GRIP_LABEL_PREFIX + side + fingerName + PoseHandPanel.TIP_SUFFIX))
                    PoseHandPanel.__RotateBone(fingerBoneName3, 0, PoseHandPanel.FINGER_3_FACTOR * PoseHandPanel.__GetFloatProp(scene, PoseHandPanel.GRIP_LABEL_PREFIX + side + fingerName + PoseHandPanel.TIP_SUFFIX))

    def __RotateBone(boneName, axisIndex, value):

        if bpy.context.scene.qumaroidArmatureObject is None:
            return
        
        bpy.context.scene.qumaroidArmatureObject.pose.bones[boneName].rotation_mode = 'XYZ' 
        if abs(value - bpy.context.scene.qumaroidArmatureObject.pose.bones[boneName].rotation_euler[axisIndex]) > PoseHandPanel.ZERO_POINT_ONE_DEGREE_IN_RADIANS:
            bpy.context.scene.qumaroidArmatureObject.pose.bones[boneName].rotation_euler[axisIndex] = value
