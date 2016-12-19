#include <Wire.h>
/*
 * Analog read EMF inputs
 * Analog Pin -> Resistr (3.3M) -> Antenna and Ground
 * 
 * Using two inputs Left and Right
 * 
 * Acts as Slave to Raspberry Pi
 */
// Configurations
#include "Configuration.h"

unsigned long debug_last = 0;
// variable to store sensor readings
int LeftSensorValue = 0;
int RightSensorValue = 0; 
 
int leftArray[SAMPLE];
int rightArray[SAMPLE];
 
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
    if(DEBUG){
        Serial.println("Ready...");
    }
} // end setup

// callback for received data
void receiveData(int byteCount){
    while(Wire.available()) {
        command = Wire.read();
        if(DEBUG){
            Serial.print("input Data: ");
            Serial.println(command);
        }
        // valid command
        if (command == 1){
            sendData();
        }
    }
} // end call back function

// callback for sending data
void sendData(){
      Wire.write(LeftSensorValue);
      Wire.write(RightSensorValue);
      if(DEBUG){
          Serial.println("Sending sensor data");
          Serial.print("output: ");
          Serial.print(LeftSensorValue);
          Serial.print(" ");
          Serial.println(RightSensorValue);
      }
}
 
 // Main loop
void loop(){
    // loop for number of samples recording value in array
    // increment adding value to averaging variable
    for(int i = 0; i < SAMPLE; i++){
        // Left Sensor      
        leftArray[i] = analogRead(LEFT_SENSOR_PIN);
        if(leftArray[i] < 0){leftArray[i] = 0;}
        leftAveraging += leftArray[i];
        // Right Sensor
        rightArray[i] = analogRead(RIGHT_SENSOR_PIN);
        if(rightArray[i] < 0){rightArray[i] = 0;}     
        rightAveraging += rightArray[i];                     
    }   
    // Find average from values
    LeftSensorValue = leftAveraging / SAMPLE;
    RightSensorValue = rightAveraging / SAMPLE;                 
    // Set totals back to 0
    leftAveraging = 0;
    rightAveraging = 0;
    // Debug output
    if(DEBUG == 1 && millis() > DEBUG_DELAY + debug_last){
        Serial.print("Left: ");
        Serial.println(LeftSensorValue);
        Serial.print("Right: ");
        Serial.println(RightSensorValue);
        debug_last = millis();
    }
 delay(50); // slow loop down a little
 }

 


