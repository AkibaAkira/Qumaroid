import math
from ....BoneName import QumaSensorIndex

class QumaAngleTranslator:
    
    DEGREES_20_RAD = 0.349066
    
    def TranslateHipsRotation(sensorAngles:[float], rootRotationVector:[float]) -> [float]:
        
        return [rootRotationVector[0] + 
                        QumaAngleTranslator.DEGREES_20_RAD + 
                        sensorAngles[QumaSensorIndex.Waist_H_0],                         
                rootRotationVector[1],                
                -rootRotationVector[2] - sensorAngles[QumaSensorIndex.Waist_H_1]]
        
    def TranslateHeadRotation(sensorAngles:[float]) -> [float]:
        
        return sensorAngles[QumaSensorIndex.Head_0], -sensorAngles[QumaSensorIndex.Head_1], 0
                
    def TranslateNeckRotation(sensorAngles:[float]) -> [float]:
        
        return -sensorAngles[QumaSensorIndex.Neck_1], 0, sensorAngles[QumaSensorIndex.Neck_0]
                
    def TranslateChestRotation(sensorAngles:[float]) -> [float]:
        
        return -sensorAngles[QumaSensorIndex.Waist_H_0], 0, -sensorAngles[QumaSensorIndex.Waist_H_1]
         
    def TranslateSpineRotation(sensorAngles:[float]) -> [float]:
        
        return 0, -sensorAngles[QumaSensorIndex.Waist_V_0], 0
        
    def TranslateLeftUpperArmRotation(sensorAngles:[float]) -> [float]:
        
        return [-sensorAngles[QumaSensorIndex.L_Shoulder_1] * math.cos(sensorAngles[QumaSensorIndex.L_Shoulder_0]),
                -sensorAngles[QumaSensorIndex.L_Shoulder_0] - sensorAngles[QumaSensorIndex.L_Shoulder_2],
                -sensorAngles[QumaSensorIndex.L_Shoulder_1] * math.sin(sensorAngles[QumaSensorIndex.L_Shoulder_0])]

    def TranslateLeftLowerArmRotation(sensorAngles:[float]) -> [float]:
        
        return 0, -sensorAngles[QumaSensorIndex.L_Hand_0], sensorAngles[QumaSensorIndex.L_Elbow_0]
                
    def TranslateLeftHandRotation(sensorAngles:[float]) -> [float]:
        
        return -sensorAngles[QumaSensorIndex.L_Hand_1], 0, 0
        
    def TranslateRightUpperArmRotation(sensorAngles:[float]) -> [float]:
        
        return [sensorAngles[QumaSensorIndex.R_Shoulder_1] * math.cos(sensorAngles[QumaSensorIndex.R_Shoulder_0]),
                -sensorAngles[QumaSensorIndex.R_Shoulder_0] - sensorAngles[QumaSensorIndex.R_Shoulder_2],
                sensorAngles[QumaSensorIndex.R_Shoulder_1] * math.sin(sensorAngles[QumaSensorIndex.R_Shoulder_0])]

    def TranslateRightLowerArmRotation(sensorAngles:[float]) -> [float]:
        
        return 0, -sensorAngles[QumaSensorIndex.R_Hand_0], sensorAngles[QumaSensorIndex.R_Elbow_0]
        
    def TranslateRightHandRotation(sensorAngles:[float]) -> [float]:
        
        return sensorAngles[QumaSensorIndex.R_Hand_1], 0, 0
        
    def TranslateLeftUpperLegRotation(sensorAngles:[float]) -> [float]:
        
        return [sensorAngles[QumaSensorIndex.L_Thigh_0],
                math.sin(sensorAngles[QumaSensorIndex.L_Thigh_0]) * sensorAngles[QumaSensorIndex.L_Thigh_1],
                -math.cos(sensorAngles[QumaSensorIndex.L_Thigh_0]) * sensorAngles[QumaSensorIndex.L_Thigh_1]]
    
    def TranslateLeftLowerLegRotation(sensorAngles:[float]) -> [float]:
        
        return -sensorAngles[QumaSensorIndex.L_Leg_0], -sensorAngles[QumaSensorIndex.L_Thigh_2], 0
            
    def TranslateLeftFootRotation(sensorAngles:[float]) -> [float]:
        
        return sensorAngles[QumaSensorIndex.L_Foot_1], -sensorAngles[QumaSensorIndex.L_Foot_0], 0
        
    def TranslateRightUpperLegRotation(sensorAngles:[float]) -> [float]:
        
        return [-sensorAngles[QumaSensorIndex.R_Thigh_0],
                math.sin(sensorAngles[QumaSensorIndex.R_Thigh_0]) * sensorAngles[QumaSensorIndex.R_Thigh_1],
                -math.cos(sensorAngles[QumaSensorIndex.R_Thigh_0]) * sensorAngles[QumaSensorIndex.R_Thigh_1]]
    
    def TranslateRightLowerLegRotation(sensorAngles:[float]) -> [float]:
        
        return sensorAngles[QumaSensorIndex.R_Leg_0], -sensorAngles[QumaSensorIndex.R_Thigh_2], 0
            
    def TranslateRightFootRotation(sensorAngles:[float]) -> [float]:
        
        return -sensorAngles[QumaSensorIndex.R_Foot_1], -sensorAngles[QumaSensorIndex.R_Foot_0], 0