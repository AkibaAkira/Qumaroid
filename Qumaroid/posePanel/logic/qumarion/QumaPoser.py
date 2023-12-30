import bpy
from .QumaPoseLoop import QumaPoseLoop
from ...posePanelConstants import PoseMode

class QumaPoserUtils:
    
    qumaPoseLoop:QumaPoseLoop = None
    
    def StartPosing() -> None:
        
        # return if no PoseMode toggle to QUMARION
        if not QumaPoserUtils.__HasAnyQumaActiveToggles():
            return
        
        if QumaPoserUtils.qumaPoseLoop is None:
            QumaPoserUtils.qumaPoseLoop = QumaPoseLoop()
            
        if not QumaPoserUtils.__HasAnyQumaActiveToggles():
            QumaPoserUtils.StopPosing()
        
    def StopPosing() -> None:
        if QumaPoserUtils.qumaPoseLoop is not None:
            QumaPoserUtils.qumaPoseLoop.Stop()
            QumaPoserUtils.qumaPoseLoop = None
            
    def __HasAnyQumaActiveToggles() -> bool:
        scene = bpy.context.scene
        
        return (scene.qumaroidHeadPoseMode == PoseMode.QUMARION.value
                or scene.qumaroidSpinePoseMode == PoseMode.QUMARION.value
                or scene.qumaroidLeftArmPoseMode == PoseMode.QUMARION.value
                or scene.qumaroidRightArmPoseMode == PoseMode.QUMARION.value
                or scene.qumaroidLeftLegPoseMode == PoseMode.QUMARION.value
                or scene.qumaroidRightLegPoseMode == PoseMode.QUMARION.value
                or scene.qumaroidHipsPoseMode == PoseMode.QUMARION.value)