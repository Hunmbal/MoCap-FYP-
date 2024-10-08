#include <Wire.h>
#include <BluetoothSerial.h>
#include <SPIFFS.h>


#define IMU 0x68
#define PWR_MGMT_1_REG 0x6B

#define ACCEL_XOUT_H 0x3B
#define GYRO_XOUT_H 0x43
#define MAG_XOUT_H 0x0C
//#define MAG_ADDRESS 0x0C



#define SDA_PIN 21
#define SCL_PIN 22

TCA9548A mux1(0x70);
TCA9548A mux2(0x71);
TCA9548A mux3(0x72);
TCA9548A mux4(0x73);

MPU9250 imu[14];


struct imu_data {
  float accelX;     
  float accelY;
  float accelZ; 

  float gyroX;      
  float gyroY; 
  float gyroZ;

  float magX; 
  float magY; 
  float magZ;
};


imu_data imu;

void setup() {
  // put your setup code here, to run once:
  Wire.begin(SDA_PIN, SCL_PIN);
  Serial.begin(9600);

  mux1.begin();
  mux2.begin();
  mux3.begin();
  mux4.begin();
  // Wake up the MPU9250
  // Wire.beginTransmission(IMU);
  // Wire.write(PWR_MGMT_1_REG);
  // Wire.write(0);
  // Wire.endTransmission();

 
 
  // Initialize all 14 IMUs
for (int i = 0; i < 14; i++) {
    selectIMU(i);  // Select the IMU using the multiplexer
    if (imu[i].begin() != 0) {
      Serial.print("Failed to initialize IMU #");
      Serial.println(i);
      while (1);  // Stop execution if any IMU fails
    }

}

void loop() {
    for (int i = 0; i < 14; i++) {
        selectIMU(i);
  // put your main code here, to run repeatedly:
  imu.accelX = (readRegister16(IMU, ACCEL_XOUT_H)-102) / 16370.0; // Adjust scale
  imu.accelY = (readRegister16(IMU, ACCEL_XOUT_H + 2)-168) / 16390.0;
  imu.accelZ = (readRegister16(IMU, ACCEL_XOUT_H + 4)+1483) / 16290.0;

  // Read gyroscope data
  imu.gyroX = readRegister16(IMU, GYRO_XOUT_H); // Adjust scale
  imu.gyroY = readRegister16(IMU, GYRO_XOUT_H + 2);
  imu.gyroZ = readRegister16(IMU, GYRO_XOUT_H + 4);

  imu.magX = readRegister16(IMU, MAG_XOUT_H); 
  imu.magY = readRegister16(IMU, MAG_XOUT_H + 2); 
  imu.magZ = readRegister16(IMU, MAG_XOUT_H + 4); 


   Serial.printf("AX: %.2f, AY: %.2f, AZ: %.2f, GX: %.2f, GY: %.2f, GZ: %.2f, MX: %.2f, MY: %2F, MZ: %2F\n",
              imu.accelX, imu.accelY, imu.accelZ,
              imu.gyroX, imu.gyroY, imu.gyroZ,
              imu.magX,imu.magY,imu.magZ);

    }
  Serial.println("File Sent");


}

//

int16_t readRegister16(int addr, int reg) {
  Wire.beginTransmission(addr);
  Wire.write(reg);
  Wire.endTransmission(false);
  Wire.requestFrom(addr, 2, true);
  
  int16_t value = Wire.read() << 8 | Wire.read();
  return value;
}

// Function to select the correct IMU using I2C multiplexer
void selectIMU(int index) {
  if (index < 3) {
    mux1.select(index);  // Select IMU on multiplexer 1
    mux2.disableAll();   // Disable the other multiplexers 
    mux3.disableAll();
    mux4.disableAll();
  } else if (index>3 && index<6 ) {
    mux2.select(index - 3);  // Select IMU on multiplexer 2
    mux1.disableAll(); 
    mux3.disableAll();
    mux4.disableAll();      // Disable other multiplexers
  }
  else if (index>5 && index<9 ){
    mux3.select(index - 6);  // Select IMU on multiplexer 2
    mux1.disableAll(); 
    mux2.disableAll();
    mux4.disableAll();  
  
  }
  else if (index>8 && index<12) {
    mux4.select(index - 9);  // Select IMU on multiplexer 2
    mux1.disableAll(); 
    mux2.disableAll();
    mux3.disableAll();  
  }
  else {
    mux1.disableAll(); 
    mux2.disableAll();
    mux3.disableAll();
    mux4.disableAll();
  }
}
