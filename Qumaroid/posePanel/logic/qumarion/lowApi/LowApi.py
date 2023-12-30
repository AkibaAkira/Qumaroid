from ctypes import *
import math
import os

class Vector3(Structure):
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

    HARDWARE_ASAI = 4

    # Qumarion library path
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

    def Exit()->None:
        """
        Disconnects the qumarion
        """
        LowApi.__QumaExit()

    def GetQumaHandle()->QumaHandle:
        """
        Get the main handle of the qumarion, the handle is the key for all actions on this qumarion

        Raises:
            Exception: Raise "None Qumarion Found" if no qumarion is plugged
        Returns:
            QumaHandle: The main handle of the qumarion
        """
        
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
            raise Exception("None Qumarion Found")
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
            
    def GetBoneSensorNameList(qumaHandle:QumaHandle)->[str]:
        """
        Returns a list of sensor names accroding to existing bone names 
        and the number of sensor each bones have.
        For example Waist_V had 2 sensors and it will be named as Waist_V_0 and Waist_V_1.
        The result name list will match the order EXACTLY to GetBoneSenesorsHandles
        and UpdateAndGetSensorReadings

        Args:
            qumaHandle (QumaHandle): The main handle of the qumarion

        Returns:
            [str]: The Bone Sensor Name List
        """
        
        resultBoneNameList = []
        
        rootBoneHandle = LowApi.__QumaGetRootBone(qumaHandle)
        boneHandles = LowApi.__GetChildBoneHandles(rootBoneHandle)
        
        for boneHandle in boneHandles:
            boneName = LowApi.__GetBoneName(boneHandle)
            sensorCount = LowApi.__QumaGetSensorCount(boneHandle)
            for i in range(sensorCount):
                sensorName = boneName + "_" + str(i)
                resultBoneNameList.append(sensorName)
        
        return resultBoneNameList
        
    def GetBoneSenesorsHandles(qumaHandle:QumaHandle)->[SensorHandle]:
        """
        Returns a list of sensor handles for query sensor angles

        Args:
            qumaHandle (QumaHandle): The main handle of the qumarion

        Returns:
            [SensorHandle]: The Sensor Handle List
        """
        rootBoneHandle = LowApi.__QumaGetRootBone(qumaHandle)
        boneHandles = LowApi.__GetChildBoneHandles(rootBoneHandle)

        # Convert Bone Handles to Sensors
        resultSensorHandleList = []

        for boneHandle in boneHandles:
            # Get Sensors
            numberOfSensors = LowApi.__QumaGetSensorCount(boneHandle)
            
            # Add sensor to Sensor handle array
            for sensorIndex in range(numberOfSensors):
                sensorHandle = LowApi.__QumaGetSensor(boneHandle, sensorIndex)
                resultSensorHandleList.append(sensorHandle)

        return resultSensorHandleList

    def UpdateBuffer(qumaHandle:QumaHandle)->bool:
        """
        (Must call before GetButtonState/GetBoneAngleReadings/GetAccelerometerReadings)\r\n
        Update Buffer, returns success if true

        Args:
            qumaHandle (QumaHandle): The main handle of the qumarion

        Returns:
            bool: True if the update is success and qumarion is normal
        """
        return LowApi.__QumaUpdateBuffer(qumaHandle) == 1

    def GetAccelerometerReadings(qumaHandle:QumaHandle)->list[float]:
        """
        (Must call UpdateBuffer first!!!)\r\n
        Get Qumarion root rotation from the accelerometer in Radians

        Args:
            qumaHandle (QumaHandle): The main handle of the qumarion

        Returns:
            list[float]: The X, Y, Z angles in Radians
        """
        tiltAngle = Vector3(0, 0, 0)
        LowApi.__QumaGetAccelerometer(qumaHandle.Handle, byref(tiltAngle))
        result = LowApi.__TranslateToRootRotation(tiltAngle.X, tiltAngle.Y, tiltAngle.Z)
        
        return result

    def GetButtonState(qumaHandle:QumaHandle)->int:
        """
        (Must call UpdateBuffer first!!!)\r\n
        Return 1 or 0 if the button is pressed or not

        Args:
            qumaHandle (QumaHandle): The main handle of the qumarion

        Returns:
            int: 1: Pressed / 0: Not Pressed
        """
        mainButton = c_int(0)
        buttonState = c_int(0)
        LowApi.__QumaGetButtonState(qumaHandle, mainButton, byref(buttonState))
        return buttonState.value
    
    def GetBoneAngleReadings(qumaHandle:QumaHandle, boneSensorArray:[SensorHandle])->list[float]:
        """
        (Must call UpdateBuffer first!!!)\r\n
        Get a list of bone angles from the sensors in Radians

        Args:
            qumaHandle (QumaHandle): The main handle of the qumarion
            boneSensorArray (SensorHandle]): The given list of Bone Senesors Handles from GetBoneSenesorsHandles

        Raises:
            Exception: Update Sensor Error

        Returns:
            list[float]: List of bone angles from the sensors in Radians, matching the order with GetBoneSensorNameList
        """
        try:
            # Get Bone Angles
            resultArray = LowApi.__UpdateBoneAngleArray(qumaHandle, boneSensorArray)

            return resultArray
        except:
            raise Exception("UpdateSensors Error")

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
                resultArray.append(math.radians(rawAngle.value))
            else:
                resultArray.append(0)

        return resultArray