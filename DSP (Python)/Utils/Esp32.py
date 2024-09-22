import random
import serial

ser: serial.Serial

def register_esp():
    #Configure the serial port (replace with your port and baudrate)
    ser = serial.Serial('COM3', 9600, timeout=1)

def read_esp32():
    data_buffer = []
    body_parts = [
        "head", "chest", "left_shoulder", "left_elbow", "left_wrist",
        "right_shoulder", "right_elbow", "right_wrist", "left_hip",
        "left_knee", "left_ankle", "right_hip", "right_knee", "right_ankle"
    ]
    parsed_data = {}

    while True:
        line = ser.readline().decode('utf-8').strip()
        if "sent" in line.lower():
            if len(data_buffer) == 14:
                # Parse the buffer into a dictionary
                for i, part_name in enumerate(body_parts):
                    values = tuple(map(float, data_buffer[i].split(',')))
                    parsed_data[part_name] = values
                return parsed_data
            else:
                data_buffer = []
        else:
            data_buffer.append(line)
            print(f"data -> {line}")




def get_random_data():
    # Simulate Bluetooth data for 14 body parts with values rounded to 2 decimal places
    return {
        "head": tuple(round(random.random(), 2) for _ in range(9)),
        "chest": tuple(round(random.random(), 2) for _ in range(9)),
        "left_shoulder": tuple(round(random.random(), 2) for _ in range(9)),
        "left_elbow": tuple(round(random.random(), 2) for _ in range(9)),
        "left_wrist": tuple(round(random.random(), 2) for _ in range(9)),
        "right_shoulder": tuple(round(random.random(), 2) for _ in range(9)),
        "right_elbow": tuple(round(random.random(), 2) for _ in range(9)),
        "right_wrist": tuple(round(random.random(), 2) for _ in range(9)),
        "left_hip": tuple(round(random.random(), 2) for _ in range(9)),
        "left_knee": tuple(round(random.random(), 2) for _ in range(9)),
        "left_ankle": tuple(round(random.random(), 2) for _ in range(9)),
        "right_hip": tuple(round(random.random(), 2) for _ in range(9)),
        "right_knee": tuple(round(random.random(), 2) for _ in range(9)),
        "right_ankle": tuple(round(random.random(), 2) for _ in range(9)),
    }