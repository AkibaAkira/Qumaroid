bl_info = {
    'name': 'Qumaroid Plugin',
    'category': '3D View',
    'author': 'Akiba Akira',
    'description': 'Qumarion Vroid Poser',
    'version': (0, 19, 0),  
    'blender': (2, 80, 0),
    'warning': '',
}

import sys,os,bpy
from bpy.app.handlers import persistent
sys.path.append(os.getcwd())

from .posePanel.ui.posePanel import PosePanel
from .poseHandPanel.PoseHandPanel import PoseHandPanel
from .facialPanel.FacialExpPanel import FacialPanel

class QumaPanel(bpy.types.Panel):
    
    bl_label = "Qumarion Pose Helper"
    bl_idname = "SCENE_PT_qumarion_panel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Item"

    def draw(self, context):
        
        layout = self.layout
        scene = context.scene
        
        row = layout.row()
        row.prop(scene, "qumaroidArmatureObject")

        if scene.qumaroidArmatureObject is not None:
            PosePanel.DrawPanel(layout)
            PoseHandPanel.DrawPanel(layout)
            FacialPanel.DrawPanel(layout)

def OnArmatureChange(self, context):
    PosePanel.StopPosing(context.scene)
    FacialPanel.OnArmatureChange(context)

@persistent
def OnQumaDepsGraphUpdatePost(scene):
    # Handles Armature Delete
    if scene.qumaroidArmatureObject is not None and scene.qumaroidArmatureObject.name not in scene.objects:
        bpy.data.objects.remove(scene.qumaroidArmatureObject)
        scene.qumaroidArmatureObject = None
        PosePanel.StopPosing(scene)

def filterVroidObjects(self, object):
        if object.pose is None:
            return False

        return True
 
def register():
    bpy.utils.register_class(QumaPanel)   
    
    # Armature Object
    bpy.types.Scene.qumaroidArmatureObject = bpy.props.PointerProperty(
        name = "Vroid Object",
        type = bpy.types.Object,
        poll = filterVroidObjects,
        update = OnArmatureChange
    )

    # Armature Object Delete Handler
    if not OnQumaDepsGraphUpdatePost in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(OnQumaDepsGraphUpdatePost)

    PosePanel.register()
    PoseHandPanel.register()
    FacialPanel.register()
      
def unregister():
    bpy.utils.unregister_class(QumaPanel)
    
    PosePanel.unregister()
    PoseHandPanel.unregister()
    FacialPanel.unregister()
    
    del bpy.types.Scene.qumaroidArmatureObject

    # Remove Armature Object Delete Handler
    if OnQumaDepsGraphUpdatePost in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(OnQumaDepsGraphUpdatePost)
