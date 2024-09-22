import os
import time
from Utils.Calibration import check_and_calibrate
from Classes.Human import Human
import Utils.Esp32 as Esp32

# Clear the console screen
os.system("cls")



if __name__ == "__main__":
    mustafa = Human()
    check_and_calibrate(mustafa)

    while True:
        mustafa.__update_data__(Esp32.get_random_data(), False)
        mustafa.__print_data__()

        
        time.sleep(0.2)  # Delay before the next iteration
        os.system("cls")  # Clear the console screen for each iteration

    

