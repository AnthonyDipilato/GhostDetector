#include <Wire.h>
/*
 * Analog read EMF inputs
 * Analog Pin -> Resistr (3.3M) -> Antenna and Ground
 * 
 * Using two inputs Left and Right
 * 
 * Acts as Slave to Raspberry Pi
 */

 // I2C Address for arduino
 #define SLAVE_ADDRESS 0x04
 // Setup pins for read
 #define LEFT_SENSOR_PIN A0
 #define RIGHT_SENSOR_PIN A1
 // Out of ground pins so we will use a digital pin
 #define GROUND_PIN 13
 // variable to store sensor readings
 int LeftSensorValue = 0;
 int RightSensorValue = 0; 
 // Averaging variables
 #define sample 100        
 int leftArray[sample];
 int rightArray[sample];
 unsigned long leftAveraging;  
 unsigned long rightAveraging;  
 int command = 0; // I2C input command
 String output;
void setup(){
  //initialize serial communication
  Serial.begin(9600);
  // pin modes
  pinMode(RIGHT_SENSOR_PIN, INPUT);
  pinMode(LEFT_SENSOR_PIN, INPUT);
  // Ground
  pinMode(GROUND_PIN,OUTPUT);
  digitalWrite(GROUND_PIN,LOW);
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);
  
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  Serial.println("Ready...");
 } // end setup

 // callback for received data
void receiveData(int byteCount){

  while(Wire.available()) {
    command = Wire.read();
    Serial.print("input Data: ");
    Serial.println(command);
    if (command == 1){
      Serial.println("valid command");
      sendData();
    }
  }
} // end call back function

// callback for sending data
void sendData(){
  Serial.println("Sending sensor data");
  Wire.write(LeftSensorValue);
  Wire.write(RightSensorValue);
  Serial.print("output: ");
  Serial.print(LeftSensorValue);
  Serial.print(" ");
  Serial.println(RightSensorValue);
}
 
 // Main loop
 void loop(){
    // loop for number of samples recording value in array
    // increment adding value to averagin variable
    for(int i = 0; i < sample; i++){
      // Left          
      leftArray[i] = analogRead(LEFT_SENSOR_PIN);       
      leftAveraging += leftArray[i];
      // Right
      rightArray[i] = analogRead(RIGHT_SENSOR_PIN);       
      rightAveraging += rightArray[i];                       
    }                                                               

    // Find average from values
    LeftSensorValue = leftAveraging / sample;
    RightSensorValue = rightAveraging / sample;                   
    // Constrain values to 100
    LeftSensorValue = constrain(LeftSensorValue, 0, 100);    
    RightSensorValue = constrain(RightSensorValue, 0, 100);    
    // Set totals back to 0
    leftAveraging = 0;
    rightAveraging = 0;

  delay(50);
 }

 

