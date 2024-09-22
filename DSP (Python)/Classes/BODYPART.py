import numpy as np
from collections import deque
from .ImuMaths import IMU

MAX_HISTORY_SIZE = 20

class BODYPART:
    def __init__(self):
        # Initialize history deques with a maximum size
        self.accel_history = deque(maxlen=MAX_HISTORY_SIZE)
        self.gyro_history = deque(maxlen=MAX_HISTORY_SIZE)
        self.mag_history = deque(maxlen=MAX_HISTORY_SIZE)
        
        # Initialize yaw, pitch, roll
        self.yaw = 0.0
        self.pitch = 0.0
        self.roll = 0.0
        
        # Initialize origin yaw, pitch, roll
        self.origin_yaw = 0.0
        self.origin_pitch = 0.0
        self.origin_roll = 0.0
        
        # Initialize calibration values
        self.accel_calib_vals = []  # List to store arrays of calibration values
        self.gyro_calib_vals = []   # List to store arrays of calibration values
        self.mag_calib_vals = []    # List to store arrays of calibration values




    def collectCurrentData(self, ax: float, ay: float, az: float, gx: float, gy: float, gz: float, mx: float, my: float, mz: float):
        accel, gyro, mag = IMU.getCalibratedData(ax, ay, az, gx, gy, gz, mx, my, mz)
        #print(f"Updating: Accel({accel}), Gyro({gyro}), Mag({mag})")  # Debug line
        self.accel_history.append(accel)
        self.gyro_history.append(gyro)
        self.mag_history.append(mag)
        self.calculate_orientation()

    def collectOriginData(self, ax: float, ay: float, az: float, gx: float, gy: float, gz: float, mx: float, my: float, mz: float):
        accel, gyro, mag = IMU.getCalibratedData(ax, ay, az, gx, gy, gz, mx, my, mz)
        #print(f"Collecting origin data: Accel({accel}), Gyro({gyro}), Mag({mag})")  # Debug line
        self.accel_calib_vals.append(accel)
        self.gyro_calib_vals.append(gyro)
        self.mag_calib_vals.append(mag)


    def calculateOriginOrientation(self):
        #print(f"Updating origin with: Accel Calib({self.accel_calib_vals}), Mag Calib({self.mag_calib_vals})")
        self.origin_pitch=IMU.getOriginPitch(self)
        self.origin_roll=IMU.getOriginRoll(self)
        self.origin_yaw=IMU.getOriginYaw(self)
        #print(f"Origin - Pitch: {self.origin_pitch}, Roll: {self.origin_roll}, Yaw: {self.origin_yaw}")


    def calculate_orientation(self):
        self.pitch = IMU.getPitch(self) - self.origin_pitch
        self.roll = IMU.getRoll(self) - self.origin_roll
        self.yaw = IMU.getYaw(self) - self.origin_yaw