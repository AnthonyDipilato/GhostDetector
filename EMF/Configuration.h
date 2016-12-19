/*    Configuration
 *   
 *    Default configurations for EMF sensor
 *  
 */

#ifndef Configuration_h
#define Configuration_h

 // Debug Settings
 #define DEBUG 1
 #define DEBUG_DELAY 1000

 // I2C Address for arduino
 #define SLAVE_ADDRESS 0x04
 // Setup pins for read
 #define LEFT_SENSOR_PIN A0
 #define RIGHT_SENSOR_PIN A1
 // Ran out of ground pins so we will use a digital pin
 #define GROUND_PIN 13
  // Number of readings to take before avergagins
 #define SAMPLE 100  


#endif


