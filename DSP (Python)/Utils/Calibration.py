import os
import yaml
import time
from Classes.BODYPART import BODYPART
from Classes.Human import Human
from Classes.States import CalibrationState
import Utils.ChatBot as Jarvis
import Utils.Esp32 as Esp32

CALIBRATION_FILE = "calibration.yml"





def check_and_calibrate(entity: Human):
    if not os.path.exists(CALIBRATION_FILE):
        Jarvis.say("Calibration file not found. Entering calibration mode.")
        calibrate(entity)
    else:        
        response = Jarvis.ask_and_get("Calibration file already exists yikes! Would you still like to calibrate?")
        if response == True:
            calibrate(entity)
        else:
            Jarvis.say("Alright no issue. We will just use the old data I guess.")
            load_calibration_data(entity)
            entity._state = CalibrationState.COMPLETED





def calibrate(entity: Human):
    while True:
        response = Jarvis.ask_and_get("Are you ready master?")
        if response:
            Jarvis.say("OK. Here we go!")
            break
        else:
            Jarvis.say("Oh no issue. I will wait.")
            time.sleep(5)

    Jarvis.say("Stand in default pose.")
    entity._state = CalibrationState.COUNTDOWN

    # Countdown from 3
    for i in range(3, 0, -1):
        Jarvis.say(str(i))
        time.sleep(1)

    Jarvis.say("Calibation has started, remain still.")
    entity._state = CalibrationState.POSE_DEFAULT

    start_time = time.time()
    while entity._state == CalibrationState.POSE_DEFAULT:
        entity.__update_data__(Esp32.get_random_data(), True)
        if time.time() - start_time > 10:
            entity._state = CalibrationState.COMPLETED
            entity.__updateHumanOrigin__()
        elif time.time() - start_time > 5 and time.time() - start_time < 6:
            Jarvis.say("Almost there. 5 seconds to go")

    save_calibration_data(entity)
    Jarvis.say("You can relax now. Calibration is complete.")





def save_calibration_data(entity: Human):
    calibration_data = {}
    
    for part_name in [attr for attr in dir(entity) if not attr.startswith('_')]:
        body_part: BODYPART = getattr(entity, part_name)
        calibration_data[part_name] = {
            "origin_yaw": body_part.origin_yaw,
            "origin_pitch": body_part.origin_pitch,
            "origin_roll": body_part.origin_roll
        }

    with open(CALIBRATION_FILE, 'w') as file:
        yaml.dump(calibration_data, file)
    print("Saving Data....")




def load_calibration_data(entity: Human):
    with open(CALIBRATION_FILE, 'r') as file:
        calibration_data = yaml.safe_load(file)

    for part_name, data in calibration_data.items():
        if hasattr(entity, part_name):
            body_part: BODYPART = getattr(entity, part_name)
            body_part.origin_yaw = data["origin_yaw"]
            body_part.origin_pitch = data["origin_pitch"]
            body_part.origin_roll = data["origin_roll"]