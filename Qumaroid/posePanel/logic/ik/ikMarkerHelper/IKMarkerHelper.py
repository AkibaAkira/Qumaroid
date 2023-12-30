import bpy

class IKMarkerHelper:

    COLLECT_NAME = "IK_MARKERS"

    def GetMarker(markerName:str, markerType:str) -> bpy.ops.object:
        
        # Return if marker already created
        if bpy.data.objects.get(markerName) != None:
            return bpy.data.objects.get(markerName)
        
        # create marker
        if markerType == "cube":
            bpy.ops.mesh.primitive_cube_add(size=1)
        else:
            bpy.ops.mesh.primitive_uv_sphere_add(segments=16,
                                                            ring_count = 8,
                                                            radius=0.5)
        marker = bpy.context.object
        marker.name = markerName
        
        # 2. Put marker to collection   
        # Unlink the object
        for coll in marker.users_collection:
            coll.objects.unlink(marker)
        # Link to IK_MARKERS collection
        IKMarkerHelper.__GetCollection().objects.link(marker)
        
        # 3. Return marker
        return marker

    def DeleteMarker(markerName:str):
        if markerName is None or markerName not in bpy.data.objects:
            return
        
        obj = bpy.data.objects.get(markerName)
        obj.hide_set(False)
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)    
        bpy.ops.object.delete()
        
    def __GetCollection() -> bpy.types.bpy_prop_collection:
        if bpy.data.collections.get(IKMarkerHelper.COLLECT_NAME) == None:
            collection = bpy.data.collections.new(IKMarkerHelper.COLLECT_NAME) 
            bpy.context.scene.collection.children.link(collection)
        else:
            collection = bpy.data.collections.get(IKMarkerHelper.COLLECT_NAME)
            
        return collection