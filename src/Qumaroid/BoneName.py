from enum import Enum

class QumaSensorIndex():
    
    def GetIndex(name) -> int:
        return QumaSensorIndex.__nameArray.index(name)

    Waist_V_0       = 0
    Waist_V_1       = 1
    L_Thigh_0     	= 2
    L_Thigh_1    	= 3
    L_Thigh_2     	= 4
    L_Leg_0         = 5
    L_Foot_0        = 6
    L_Foot_1        = 7
    R_Thigh_0       = 8
    R_Thigh_1       = 9
    R_Thigh_2       = 10
    R_Leg_0         = 11
    R_Foot_0        = 12
    R_Foot_1        = 13
    Waist_H_0       = 14
    Waist_H_1       = 15
    Neck_0          = 16
    Neck_1          = 17
    Head_0          = 18
    Head_1          = 19
    L_Shoulder_0    = 20
    L_Shoulder_1    = 21
    L_Shoulder_2    = 22
    L_Elbow_0       = 23
    L_Hand_0        = 24
    L_Hand_1        = 25
    R_Shoulder_0    = 26
    R_Shoulder_1    = 27
    R_Shoulder_2    = 28
    R_Elbow_0       = 29
    R_Hand_0        = 30
    R_Hand_1        = 31

    #Extras
    Root_Rotation_X = 32
    Root_Rotation_Y = 33
    Root_Rotation_Z = 34
    Button = 35

    # Not an id
    length = 36

    __nameArray = ["Waist_V_0",
            "Waist_V_1",
            "L_Thigh_0",
            "L_Thigh_1",
            "L_Thigh_2",
            "L_Leg_0",
            "L_Foot_0",
            "L_Foot_1",
            "R_Thigh_0",
            "R_Thigh_1",
            "R_Thigh_2",
            "R_Leg_0",
            "R_Foot_0",
            "R_Foot_1",
            "Waist_H_0",
            "Waist_H_1",
            "Neck_0",
            "Neck_1",
            "Head_0",
            "Head_1",
            "L_Shoulder_0",
            "L_Shoulder_1",
            "L_Shoulder_2",
            "L_Elbow_0",
            "L_Hand_0",
            "L_Hand_1",
            "R_Shoulder_0",
            "R_Shoulder_1",
            "R_Shoulder_2",
            "R_Elbow_0",
            "R_Hand_0",
            "R_Hand_1",
            #Extras
            "Root_Rotation_X",
            "Root_Rotation_Y",
            "Root_Rotation_Z",
            "Button"]

class VroidBonename(Enum):
    J_Bip_C_Hips = "J_Bip_C_Hips"
    J_Bip_C_Neck = "J_Bip_C_Neck"
    J_Bip_C_Head = "J_Bip_C_Head"
    J_Bip_C_Chest = "J_Bip_C_Chest"
    J_Bip_C_Spine = "J_Bip_C_Spine"
    J_Bip_L_Shoulder = "J_Bip_L_Shoulder"
    J_Bip_L_UpperArm = "J_Bip_L_UpperArm"
    J_Bip_L_LowerArm = "J_Bip_L_LowerArm"
    J_Bip_L_Hand = "J_Bip_L_Hand"
    J_Bip_R_Shoulder = "J_Bip_R_Shoulder"
    J_Bip_R_UpperArm = "J_Bip_R_UpperArm"
    J_Bip_R_LowerArm = "J_Bip_R_LowerArm"
    J_Bip_R_Hand = "J_Bip_R_Hand"    
    J_Bip_L_UpperLeg = "J_Bip_L_UpperLeg"
    J_Bip_L_LowerLeg = "J_Bip_L_LowerLeg"
    J_Bip_L_Foot = "J_Bip_L_Foot"
    J_Bip_R_LowerLeg = "J_Bip_R_LowerLeg"
    J_Bip_R_UpperLeg = "J_Bip_R_UpperLeg"
    J_Bip_R_Foot = "J_Bip_R_Foot"

    # Eyes
    J_Adj_L_FaceEye = "J_Adj_L_FaceEye"
    J_Adj_R_FaceEye = "J_Adj_R_FaceEye"

    # Hands
    J_Bip_L_Thumb1 = "J_Bip_L_Thumb1"
    J_Bip_L_Thumb2 = "J_Bip_L_Thumb2"
    J_Bip_L_Thumb3 = "J_Bip_L_Thumb3"
    J_Bip_L_Index1 = "J_Bip_L_Index1"
    J_Bip_L_Index2 = "J_Bip_L_Index2"
    J_Bip_L_Index3 = "J_Bip_L_Index3"
    J_Bip_L_Middle1 = "J_Bip_L_Middle1"
    J_Bip_L_Middle2 = "J_Bip_L_Middle2"
    J_Bip_L_Middle3 = "J_Bip_L_Middle3"
    J_Bip_L_Ring1 = "J_Bip_L_Ring1"
    J_Bip_L_Ring2 = "J_Bip_L_Ring2"
    J_Bip_L_Ring3 = "J_Bip_L_Ring3"
    J_Bip_L_Little1 = "J_Bip_L_Little1"
    J_Bip_L_Little2 = "J_Bip_L_Little2"
    J_Bip_L_Little3 = "J_Bip_L_Little3"

    J_Bip_R_Thumb1 = "J_Bip_R_Thumb1"
    J_Bip_R_Thumb2 = "J_Bip_R_Thumb2"
    J_Bip_R_Thumb3 = "J_Bip_R_Thumb3"
    J_Bip_R_Index1 = "J_Bip_R_Index1"
    J_Bip_R_Index2 = "J_Bip_R_Index2"
    J_Bip_R_Index3 = "J_Bip_R_Index3"
    J_Bip_R_Middle1 = "J_Bip_R_Middle1"
    J_Bip_R_Middle2 = "J_Bip_R_Middle2"
    J_Bip_R_Middle3 = "J_Bip_R_Middle3"
    J_Bip_R_Ring1 = "J_Bip_R_Ring1"
    J_Bip_R_Ring2 = "J_Bip_R_Ring2"
    J_Bip_R_Ring3 = "J_Bip_R_Ring3"
    J_Bip_R_Little1 = "J_Bip_R_Little1"
    J_Bip_R_Little2 = "J_Bip_R_Little2"
    J_Bip_R_Little3 = "J_Bip_R_Little3"