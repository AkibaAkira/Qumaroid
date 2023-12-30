import bpy

class IKDepsgraphHandler:

    __func = None
    __operator = None

    def __Handler(self, context):
        depsgraph = bpy.context.evaluated_depsgraph_get()
        if IKDepsgraphHandler.__operator is None:
            IKDepsgraphHandler.__operator = bpy.context.active_operator
        for update in depsgraph.updates:
            if not update.is_updated_transform:
                continue
            if IKDepsgraphHandler.__operator == bpy.context.active_operator:
                continue
            obj = bpy.context.active_object 
            IKDepsgraphHandler.__func(obj)
            IKDepsgraphHandler.__operator = None

    def AppendIKCursorHandler(func):

        IKDepsgraphHandler.__func = func
        IKDepsgraphHandler.__operator = None

        IKDepsgraphHandler.RemoveIKCursorHandler()
        bpy.app.handlers.depsgraph_update_post.append(IKDepsgraphHandler.__Handler)

    def RemoveIKCursorHandler():        
        for i in reversed(range(len(bpy.app.handlers.depsgraph_update_post))):
            func = bpy.app.handlers.depsgraph_update_post[i]
            if func.__name__ == IKDepsgraphHandler.__Handler.__name__:
                bpy.app.handlers.depsgraph_update_post.remove(func)