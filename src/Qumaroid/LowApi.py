from ctypes import *
from .BoneName import QumaSensorIndex
from .PopupUtils import PopupUtils
import math
import os

class Vector3(Structure):
    _fields_ = [('X', c_float), ('Y', c_float), ('Z', c_float)]


class Vector16(Structure):
    _fields_ = [('X', c_float), ('Y', c_float), ('Z', c_float)]


class QumaId(Structure):
    _fields_ = [('QumaType', c_int), ('Id', c_int)]


class QumaHandle(Structure):
    _fields_ = [('Handle', POINTER(c_int))]


class BoneHandle(Structure):
    _fields_ = [('Handle', POINTER(c_int))]


class SensorHandle(Structure):
    _fields_ = [('Handle', POINTER(c_int))]


class LowApi:

    ANGLE_CORRECTION = 5
    HARDWARE_ASAI = 4

    __qumaDllPath = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "QmPdkDll.dll")

    #region C Functions

    __QumaInitialize = getattr(CDLL(__qumaDllPath), "?QmLowInitialize@@YAHXZ")
    __QumaEnumlateQumaIDs = getattr(
        CDLL(__qumaDllPath), "?QmLowEnumlateQumaIDs@@YAHPEAUt_QmLowQumaID@@PEAH@Z")
    __QumaGetHandle = getattr(
        CDLL(__qumaDllPath), "?QmLowGetQumaHandle@@YAHUt_QmLowQumaID@@PEAPEAX@Z")
    __QumaActivate = getattr(
        CDLL(__qumaDllPath), "?QmLowActivateQuma@@YAHPEAXPEAUt_QmLowActivateInfo@@@Z")
    __QumaUpdateBuffer = getattr(
        CDLL(__qumaDllPath), "?QmLowUpdateBuffer@@YAHPEAX@Z")
    __QumaExit = getattr(CDLL(__qumaDllPath), "?QmLowExit@@YAHXZ")

    __QumaGetRootBone = getattr(
        CDLL(__qumaDllPath), "?QmLowGetRootBone@@YAPEAXPEAX@Z")
    __QumaGetChildBone = getattr(
        CDLL(__qumaDllPath), "?QmLowGetChildBone@@YAPEAXPEAXH@Z")
    __QumaGetChildCount = getattr(
        CDLL(__qumaDllPath), "?QmLowGetChildCount@@YAHPEAX@Z")
    __QumaGetBoneName = getattr(
        CDLL(__qumaDllPath), "?QmLowGetBoneName@@YAXPEAXPEA_W@Z")

    __QumaGetSensorCount = getattr(
        CDLL(__qumaDllPath), "?QmLowGetSensorCount@@YAHPEAX@Z")
    __QumaGetSensor = getattr(
        CDLL(__qumaDllPath), "?QmLowGetSensor@@YAPEAXPEAXH@Z")
    __QumaGetSensorState = getattr(
        CDLL(__qumaDllPath), "?QmLowGetSensorState@@YA?AW4QMLOW_SENSOR_STATE@@PEAX0@Z")
    __QumaGetSensorAngle = getattr(
        CDLL(__qumaDllPath), "?QmLowComputeSensorAngle@@YAHPEAX0PEAM@Z")
    __QumaGetAccelerometer = getattr(
        CDLL(__qumaDllPath), "?QmLowGetAccelerometer@@YAHPEAXPEAM@Z")
    __QumaGetAccMatrix = getattr(
        CDLL(__qumaDllPath), "?QmLowGetAccelerometerPoseMatrix@@YAHPEAXPEAM@Z")

    __QumaGetButtonState = getattr(CDLL(
        __qumaDllPath), "?QmLowGetButtonState@@YAHPEAXW4QMLOW_BUTTON_TYPE@@PEAW4QMLOW_BUTTON_STATE@@@Z")

    #endregion

    def Exit():
        LowApi.__QumaExit()
        print("Quma Exit.")

    def GetQumaHandle()->QumaHandle:

        LowApi.__QumaGetRootBone.restype = POINTER(c_int)
        LowApi.__QumaGetChildBone.restype = POINTER(c_int)
        LowApi.__QumaGetSensor.restype = POINTER(c_int)

        if LowApi.__QumaGetAccelerometer.argtypes is None:
            LowApi.__QumaGetAccelerometer.argtypes = [c_void_p, c_void_p]

        # Init
        LowApi.__QumaInitialize()

        # Get Quma Handle
        # Enumlate Quma IDs
        outIdCount = c_int(0)
        qumaIdArray = (QumaId * 256)()
        LowApi.__QumaEnumlateQumaIDs(byref(qumaIdArray), byref(outIdCount))

        qumaId = None
        for i in range(outIdCount.value):
            if (qumaIdArray[i].QumaType == LowApi.HARDWARE_ASAI):
                qumaId = qumaIdArray[i]
                break

        if (qumaId is None):
            print("None Qumarion Found")
            PopupUtils.ShowMessageBox("None Qumarion Found", "Error", 'ERROR')
            return None
        else:
            qumaHandle = QumaHandle()
            LowApi.__QumaGetHandle(qumaId, byref(qumaHandle))
            if qumaHandle.Handle:
                # Activate Quma
                zero = c_int(0)
                LowApi.__QumaActivate(qumaHandle, zero)

                return qumaHandle
            else:
                return None

    def GetBoneSenesorsHandles(qumaHandle):
        rootBoneHandle = LowApi.__QumaGetRootBone(qumaHandle)
        boneHandles = LowApi.__GetChildBoneHandles(rootBoneHandle)

        # Use hard coded sensor names to avoid calling __GetBoneName and causing crashes
        sensorNames = ["Waist_V_0",
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
                        "R_Hand_1"]

        # Convert Bone Handles to Sensors
        boneSensorArray = {}
        count = 0

        for boneHandle in boneHandles:
            # Get Sensors
            numberOfSensors = LowApi.__QumaGetSensorCount(boneHandle)
            
            # Add sensor to Sensor handle array
            for sensorIndex in range(numberOfSensors):
                sensorHandle = LowApi.__QumaGetSensor(boneHandle, sensorIndex)
                enumName = sensorNames[count]
                count = count + 1
                boneSensorArray[QumaSensorIndex.GetIndex(enumName)] = sensorHandle

        return boneSensorArray

    # Warning! Resource intensive and causes crash!
    def __GetBoneName(boneHandle):
        boneName = c_wchar_p("")
        LowApi.__QumaGetBoneName(boneHandle, boneName)
        return boneName.value
    
    def __GetChildBoneHandles(boneHandle):
        result = []

        childboneCount = LowApi.__QumaGetChildCount(boneHandle)
        for i in range(childboneCount):
            childBoneHandle = LowApi.__QumaGetChildBone(boneHandle, i)
            result.append(childBoneHandle)
            childBones = LowApi.__GetChildBoneHandles(childBoneHandle)
            for childBone in childBones:
                result.append(childBone)

        return result

    def UpdateAndGetSensorReadings(qumaHandle, boneSensorArray)->list[float]:

        if qumaHandle and boneSensorArray:
            try:
                if LowApi.__QumaUpdateBuffer(qumaHandle) == 1: # if update buffer AND SUCCESS
                    # Get Bone Angles
                    resultArray = LowApi.__UpdateBoneAngleArray(qumaHandle, boneSensorArray)

                    # # Get Accelerometer Data
                    tiltAngle = Vector3(0, 0, 0)
                    LowApi.__QumaGetAccelerometer(qumaHandle.Handle, byref(tiltAngle))
                    
                    resultArray = resultArray + LowApi.__TranslateToRootRotation(tiltAngle.X, tiltAngle.Y, tiltAngle.Z)

                    # Get Button
                    mainButton = c_int(0)
                    buttonState = c_int(0)
                    LowApi.__QumaGetButtonState(qumaHandle, mainButton, byref(buttonState))
                    resultArray.append(buttonState.value)

                    return resultArray
            except:
                print("UpdateSensors Error")

        # return empty Array
        emptyArray = []
        for i in range(QumaSensorIndex.length):
            emptyArray.append(0)

        return emptyArray

    def __TranslateToRootRotation(x, y, z):
        if y < 0:
            xAngle = math.pi + math.atan2(z, y)
            zAngle = math.atan2(x, y) - math.pi
            yAngle = 0
        else:
            xAngle = math.atan2(z, y)
            zAngle = math.atan2(x, y) - math.pi
            yAngle = math.pi
        return [xAngle, yAngle, zAngle]

    def __UpdateBoneAngleArray(qumaHandle, boneSensorArray)->list[float]:
        resultArray = []

        for i in range(len(boneSensorArray)):
            rawAngle = c_float(0)
            if LowApi.__QumaGetSensorAngle(qumaHandle, boneSensorArray[i], byref(rawAngle)) == 1: # if update sensor AND SUCCESS
                resultArray.append(round(math.radians(rawAngle.value), LowApi.ANGLE_CORRECTION))
            else:
                resultArray.append(0)

        return resultArray