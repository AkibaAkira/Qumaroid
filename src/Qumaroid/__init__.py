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
sys.path.append(os.getcwd())

from .QumaLooper import QumaLooper
from .PoseHandPanel import PoseHandPanel
from .FacialExpPanel import FacialPanel

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
        row.enabled = not scene.qumaroidIsPosing

        if scene.qumaroidArmatureObject is not None:
            QumaLooper.DrawPanel(layout)
            PoseHandPanel.DrawPanel(layout)
            FacialPanel.DrawPanel(layout)

def OnArmatureChange(self, context):
    FacialPanel.OnArmatureChange(context)

def register():
    bpy.utils.register_class(QumaPanel)   
    
    # Armature Object
    bpy.types.Scene.qumaroidArmatureObject = bpy.props.PointerProperty(
        name = "Vroid Object",
        type = bpy.types.Object,
        poll = QumaLooper.filterVroidObjects,
        update = OnArmatureChange
    )

    QumaLooper.register()
    PoseHandPanel.register()
    FacialPanel.register()
      
def unregister():
    bpy.utils.unregister_class(QumaPanel)
    
    QumaLooper.unregister()
    PoseHandPanel.unregister()
    FacialPanel.unregister()
    
    del bpy.types.Scene.qumaroidArmatureObject