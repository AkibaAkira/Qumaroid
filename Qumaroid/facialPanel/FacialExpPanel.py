import bpy
from ..BoneName import VroidBonename

class ResetFacialPanelOperator(bpy.types.Operator):
    bl_label = "Reset All"
    bl_idname = "object.quma_reset_facial"
    bl_description = "Reset all facial expressions"
    
    def execute(self, context):
        FacialPanel.ResetFacialExpressions(context)
        return {'FINISHED'}

class FacialPanel:

    SHAPE_KEY_NAME_PREFIX = "qumaroidShapeKey_"

    EYE_ROTATION_MAX = 0.61087 #35 deg

    _shapeKeyNames = [
        "Basis",
        "Fcl_ALL_Neutral",
        "Fcl_ALL_Angry",
        "Fcl_ALL_Fun",
        "Fcl_ALL_Joy",
        "Fcl_ALL_Sorrow",
        "Fcl_ALL_Surprised", #6
        "Fcl_BRW_Angry",
        "Fcl_BRW_Fun",
        "Fcl_BRW_Joy",
        "Fcl_BRW_Sorrow",
        "Fcl_BRW_Surprised", #11
        "Fcl_EYE_Natural",
        "Fcl_EYE_Angry",
        "Fcl_EYE_Close",
        "Fcl_EYE_Close_R",
        "Fcl_EYE_Close_L",
        "Fcl_EYE_Fun",
        "Fcl_EYE_Joy",
        "Fcl_EYE_Joy_R",
        "Fcl_EYE_Joy_L",
        "Fcl_EYE_Sorrow",
        "Fcl_EYE_Surprised",
        "Fcl_EYE_Spread",
        "Fcl_EYE_Iris_Hide",
        "Fcl_EYE_Highlight_Hide", #25
        "Fcl_MTH_Close",
        "Fcl_MTH_Up",
        "Fcl_MTH_Down",
        "Fcl_MTH_Angry",
        "Fcl_MTH_Small",
        "Fcl_MTH_Large",
        "Fcl_MTH_Neutral",
        "Fcl_MTH_Fun",
        "Fcl_MTH_Joy",
        "Fcl_MTH_Sorrow",
        "Fcl_MTH_Surprised",
        "Fcl_MTH_SkinFung",
        "Fcl_MTH_SkinFung_R",
        "Fcl_MTH_SkinFung_L", #39
        "Fcl_MTH_A",
        "Fcl_MTH_I",
        "Fcl_MTH_U",
        "Fcl_MTH_E",
        "Fcl_MTH_O", #44
        "Fcl_HA_Hide",
        "Fcl_HA_Fung1",
        "Fcl_HA_Fung1_Low",
        "Fcl_HA_Fung1_Up",
        "Fcl_HA_Fung2",
        "Fcl_HA_Fung2_Low",
        "Fcl_HA_Fung2_Up",
        "Fcl_HA_Fung3",
        "Fcl_HA_Fung3_Up",
        "Fcl_HA_Fung3_Low",
        "Fcl_HA_Short",
        "Fcl_HA_Short_Up",
        "Fcl_HA_Short_Low" #57
    ]

    def DrawPanel(layout):
        scene = bpy.context.scene

        # Eye Panel
        row = layout.row()
        row.alignment = 'LEFT'
        row.prop(scene, "qumaroidShowEyePanel", icon="TRIA_DOWN" if scene.qumaroidShowEyePanel else "TRIA_RIGHT", icon_only=True, emboss=False, text="Eyes")

        if scene.qumaroidShowEyePanel:
            box = layout.box()
            row = box.row()
            row.prop(scene, "qumaroidEyeRotationL_Y")
            row = box.row()
            row.prop(scene, "qumaroidEyeRotationL_X")
            row = box.row()
            row.enabled = not scene.qumaroidSyncEyes
            row.prop(scene, "qumaroidEyeRotationR_Y")
            row = box.row()
            row.enabled = not scene.qumaroidSyncEyes
            row.prop(scene, "qumaroidEyeRotationR_X")
            row = box.row()
            row.prop(scene, "qumaroidSyncEyes")

        # Facial Expression Panel
        row = layout.row()
        row.alignment = 'LEFT'
        row.prop(scene, "qumaroidPanelShowFacialPanel", icon="TRIA_DOWN" if scene.qumaroidPanelShowFacialPanel else "TRIA_RIGHT", icon_only=True, emboss=False, text="Facial Expressions")

        if scene.qumaroidPanelShowFacialPanel:
            
            row = layout.row()
            row.operator("object.quma_reset_facial")

            box = layout.box()

            # Expressions
            row = box.row()
            row.alignment = 'LEFT'
            row.prop(scene, "qumaroidPanelShowGeneralExpressionPanel", icon="TRIA_DOWN" if scene.qumaroidPanelShowGeneralExpressionPanel else "TRIA_RIGHT", icon_only=True, emboss=False, text="Expressions")
            
            if scene.qumaroidPanelShowGeneralExpressionPanel:
                for i in range(0, 7):
                    row = box.row()
                    row.prop(scene, FacialPanel.SHAPE_KEY_NAME_PREFIX + FacialPanel._shapeKeyNames[i])

            # Eyebrows
            row = box.row()
            row.alignment = 'LEFT'
            row.prop(scene, "qumaroidPanelShowEyebrowsPanel", icon="TRIA_DOWN" if scene.qumaroidPanelShowEyebrowsPanel else "TRIA_RIGHT", icon_only=True, emboss=False, text="Eyebrows")
            
            if scene.qumaroidPanelShowEyebrowsPanel:
                for i in range(7, 12):
                    if FacialPanel._shapeKeyNames[i] == "":
                        continue
                    row = box.row()
                    row.prop(scene, FacialPanel.SHAPE_KEY_NAME_PREFIX + FacialPanel._shapeKeyNames[i])

            # Eyes
            row = box.row()
            row.alignment = 'LEFT'
            row.prop(scene, "qumaroidPanelShowEyesPanel", icon="TRIA_DOWN" if scene.qumaroidPanelShowEyesPanel else "TRIA_RIGHT", icon_only=True, emboss=False, text="Eyes")
            
            if scene.qumaroidPanelShowEyesPanel:
                for i in range(12, 26):
                    if FacialPanel._shapeKeyNames[i] == "":
                        continue
                    row = box.row()
                    row.prop(scene, FacialPanel.SHAPE_KEY_NAME_PREFIX + FacialPanel._shapeKeyNames[i])

            # Mouth
            row = box.row()
            row.alignment = 'LEFT'
            row.prop(scene, "qumaroidPanelShowMouthPanel", icon="TRIA_DOWN" if scene.qumaroidPanelShowMouthPanel else "TRIA_RIGHT", icon_only=True, emboss=False, text="Mouth")
            
            if scene.qumaroidPanelShowMouthPanel:
                for i in range(26, 40):
                    if FacialPanel._shapeKeyNames[i] == "":
                        continue
                    row = box.row()
                    row.prop(scene, FacialPanel.SHAPE_KEY_NAME_PREFIX + FacialPanel._shapeKeyNames[i])

            # AIUEO
            row = box.row()
            row.alignment = 'LEFT'
            row.prop(scene, "qumaroidPanelShowMouthAIUEOPanel", icon="TRIA_DOWN" if scene.qumaroidPanelShowMouthAIUEOPanel else "TRIA_RIGHT", icon_only=True, emboss=False, text="AEIOU")
            
            if scene.qumaroidPanelShowMouthAIUEOPanel:
                for i in range(40, 45):
                    if FacialPanel._shapeKeyNames[i] == "":
                        continue
                    row = box.row()
                    row.prop(scene, FacialPanel.SHAPE_KEY_NAME_PREFIX + FacialPanel._shapeKeyNames[i])

            # Teeth
            row = box.row()
            row.alignment = 'LEFT'
            row.prop(scene, "qumaroidPanelShowTeethPanel", icon="TRIA_DOWN" if scene.qumaroidPanelShowTeethPanel else "TRIA_RIGHT", icon_only=True, emboss=False, text="Teeth")
            
            if scene.qumaroidPanelShowTeethPanel:
                for i in range(45, 58):
                    if FacialPanel._shapeKeyNames[i] == "":
                        continue
                    row = box.row()
                    row.prop(scene, FacialPanel.SHAPE_KEY_NAME_PREFIX + FacialPanel._shapeKeyNames[i])
                    
    def ResetFacialExpressions(context):
        for i in range(len(FacialPanel._shapeKeyNames)):
            keyName = FacialPanel.SHAPE_KEY_NAME_PREFIX + FacialPanel._shapeKeyNames[i]
            context.scene[keyName] = 0

        FacialPanel.__ReadWriteAllShapeKeys(context, True)

    def OnArmatureChange(context):
        FacialPanel.__ReadWriteAllShapeKeys(context)
        FacialPanel.__ReadWriteEyes(context)

    def OnUpdateShapeKey(self, context):
        FacialPanel.__ReadWriteAllShapeKeys(context, True)

    def OnUpdateSyncEyes(self, context):
        context.scene.qumaroidEyeRotationR_X = context.scene.qumaroidEyeRotationL_X
        context.scene.qumaroidEyeRotationR_Y = context.scene.qumaroidEyeRotationL_Y

    def OnUpdateEye(self, context):
        FacialPanel.__ReadWriteEyes(context, True)

    def register():

        bpy.utils.register_class(ResetFacialPanelOperator)

        Scene = bpy.types.Scene

        Scene.qumaroidPanelShowFacialPanel = bpy.props.BoolProperty()
        
        #Show/Hide Panels
        Scene.qumaroidPanelShowGeneralExpressionPanel = bpy.props.BoolProperty()
        Scene.qumaroidPanelShowEyebrowsPanel = bpy.props.BoolProperty()
        Scene.qumaroidPanelShowEyesPanel = bpy.props.BoolProperty()
        Scene.qumaroidPanelShowMouthPanel = bpy.props.BoolProperty()
        Scene.qumaroidPanelShowMouthAIUEOPanel = bpy.props.BoolProperty()
        Scene.qumaroidPanelShowTeethPanel = bpy.props.BoolProperty()

        #Eye Bone
        Scene.qumaroidShowEyePanel = bpy.props.BoolProperty()
        Scene.qumaroidSyncEyes = bpy.props.BoolProperty(update=FacialPanel.OnUpdateSyncEyes)
        Scene.qumaroidEyeRotationL_Y = bpy.props.FloatProperty(min=-FacialPanel.EYE_ROTATION_MAX, max=FacialPanel.EYE_ROTATION_MAX, update=FacialPanel.OnUpdateEye, name="Left Eye Horizotal")
        Scene.qumaroidEyeRotationL_X = bpy.props.FloatProperty(min=-FacialPanel.EYE_ROTATION_MAX, max=FacialPanel.EYE_ROTATION_MAX, update=FacialPanel.OnUpdateEye, name="Left Eye Vertical")
        Scene.qumaroidEyeRotationR_Y = bpy.props.FloatProperty(min=-FacialPanel.EYE_ROTATION_MAX, max=FacialPanel.EYE_ROTATION_MAX, update=FacialPanel.OnUpdateEye, name="Right Eye Horizotal")
        Scene.qumaroidEyeRotationR_X = bpy.props.FloatProperty(min=-FacialPanel.EYE_ROTATION_MAX, max=FacialPanel.EYE_ROTATION_MAX, update=FacialPanel.OnUpdateEye, name="Right Eye Vertical")

        for i in range(len(FacialPanel._shapeKeyNames)):
            keyName = FacialPanel.SHAPE_KEY_NAME_PREFIX + FacialPanel._shapeKeyNames[i]
            displayedName = FacialPanel._shapeKeyNames[i]
            setattr(Scene, keyName, bpy.props.FloatProperty(min=0, max=1, name=displayedName, update=FacialPanel.OnUpdateShapeKey))

    def unregister():

        bpy.utils.unregister_class(ResetFacialPanelOperator)

        del bpy.types.Scene.qumaroidPanelShowFacialPanel

        del bpy.types.Scene.qumaroidShowEyePanel
        del bpy.types.Scene.qumaroidPanelShowGeneralExpressionPanel
        del bpy.types.Scene.qumaroidPanelShowEyebrowsPanel
        del bpy.types.Scene.qumaroidPanelShowEyesPanel
        del bpy.types.Scene.qumaroidPanelShowMouthPanel
        del bpy.types.Scene.qumaroidPanelShowMouthAIUEOPanel
        del bpy.types.Scene.qumaroidPanelShowTeethPanel

        del bpy.types.Scene.qumaroidSyncEyes
        del bpy.types.Scene.qumaroidEyeRotationL_Y
        del bpy.types.Scene.qumaroidEyeRotationL_X
        del bpy.types.Scene.qumaroidEyeRotationR_Y
        del bpy.types.Scene.qumaroidEyeRotationR_X 

    #region Private Functions

    def __ReadWriteAllShapeKeys(context, isWrite=False):
        armature = context.scene.qumaroidArmatureObject

        if armature:
            faceObject = FacialPanel.__LoadFaceObject(armature)
            if faceObject:
                for i in range(len(FacialPanel._shapeKeyNames)):
                    shapeKeyName = FacialPanel._shapeKeyNames[i]
                    propName = FacialPanel.SHAPE_KEY_NAME_PREFIX + FacialPanel._shapeKeyNames[i]
                    if isWrite:
                        value = 0
                        if propName in context.scene:
                            value = context.scene[propName]
                        faceObject.data.shape_keys.key_blocks[shapeKeyName].value = value
                    else:
                        context.scene[propName] = faceObject.data.shape_keys.key_blocks[shapeKeyName].value
    
    def __ReadWriteEyes(context, isWrite=False):
        armature = context.scene.qumaroidArmatureObject
        scene = context.scene

        if armature:
            armature.pose.bones[VroidBonename.J_Adj_L_FaceEye.name].rotation_mode = "XYZ"
            armature.pose.bones[VroidBonename.J_Adj_R_FaceEye.name].rotation_mode = "XYZ"
            
            if isWrite:
                armature.pose.bones[VroidBonename.J_Adj_L_FaceEye.name].rotation_euler = scene.qumaroidEyeRotationL_X, scene.qumaroidEyeRotationL_Y, 0
                if scene.qumaroidSyncEyes:
                    armature.pose.bones[VroidBonename.J_Adj_R_FaceEye.name].rotation_euler = scene.qumaroidEyeRotationL_X, scene.qumaroidEyeRotationL_Y, 0
                else:
                    armature.pose.bones[VroidBonename.J_Adj_R_FaceEye.name].rotation_euler = scene.qumaroidEyeRotationR_X, scene.qumaroidEyeRotationR_Y, 0
            else:
                rot_LX = armature.pose.bones[VroidBonename.J_Adj_L_FaceEye.name].rotation_euler[0]
                rot_LY = armature.pose.bones[VroidBonename.J_Adj_L_FaceEye.name].rotation_euler[1]
                rot_RX = armature.pose.bones[VroidBonename.J_Adj_R_FaceEye.name].rotation_euler[0]
                rot_RY = armature.pose.bones[VroidBonename.J_Adj_R_FaceEye.name].rotation_euler[1]
                
                scene.qumaroidEyeRotationL_X = rot_LX
                scene.qumaroidEyeRotationL_Y = rot_LY
                scene.qumaroidEyeRotationR_X = rot_RX
                scene.qumaroidEyeRotationR_Y = rot_RY

                isXSame = round(rot_LX, 5) == round(rot_RX, 5)
                isYSame = round(rot_LY, 5) == round(rot_RY, 5)
                scene.qumaroidSyncEyes = isXSame and isYSame

    def __LoadFaceObject(armature): 
        children = [] 
        for ob in bpy.data.objects: 
            if ob.parent == armature: 
                children.append(ob)

        for child in children:
            if hasattr(child.data, "shape_keys"):
                if hasattr(child.data.shape_keys, "key_blocks"):
                    checkValid = True

                    for i in range(len(FacialPanel._shapeKeyNames)):
                        if not FacialPanel._shapeKeyNames[i] in child.data.shape_keys.key_blocks:
                            checkValid = False
                            break

                    if checkValid:
                        return child
    
    #endregion Private Functions