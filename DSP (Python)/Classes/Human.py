from .States import CalibrationState
from .BODYPART import BODYPART

class Human:
    def __init__(self) -> None:
        self._state = CalibrationState.FAILED
        # Center parts
        self.head = BODYPART()
        self.chest = BODYPART()
        # Upper left
        self.left_shoulder = BODYPART()
        self.left_elbow = BODYPART()
        self.left_wrist = BODYPART()
        # Upper right
        self.right_shoulder = BODYPART()
        self.right_elbow = BODYPART()
        self.right_wrist = BODYPART()
        # Lower left
        self.left_hip = BODYPART()
        self.left_knee = BODYPART()
        self.left_ankle = BODYPART()
        # Lower right
        self.right_hip = BODYPART()
        self.right_knee = BODYPART()
        self.right_ankle = BODYPART()

    def __update_data__(self, data, isCalibrating: bool):
        #print("Updating data...")
        #print(f"Data received: {data}")  # Add this line to see the data format
        for name, values in data.items():
            if hasattr(self, name):
                ax, ay, az, gx, gy, gz, mx, my, mz = values
                body_part: BODYPART = getattr(self, name)
                if isCalibrating:
                    body_part.collectOriginData(ax, ay, az, gx, gy, gz, mx, my, mz)
                else:                    
                    body_part.collectCurrentData(ax, ay, az, gx, gy, gz, mx, my, mz)



    def __updateHumanOrigin__(self):
        for part_name in [attr for attr in dir(self) if not attr.startswith('_')]:
            body_part: BODYPART = getattr(self, part_name)
            body_part.calculateOriginOrientation()

    def __print_data__(self):
        for part_name in [attr for attr in dir(self) if not attr.startswith('_')]:
            body_part: BODYPART = getattr(self, part_name)
            print(f"{part_name:<15} -> Yaw: {body_part.yaw:<6} Pitch: {body_part.pitch:<6} Roll: {body_part.roll:<6}")
