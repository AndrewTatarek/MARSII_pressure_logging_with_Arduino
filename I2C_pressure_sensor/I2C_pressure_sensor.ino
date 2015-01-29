// Code to read a SensorTronics Pressure Sensor
// This has been tested with a pressure sensor owned by C2M Design LTD. Part number: HMIB010UZ7H5 

#include <Wire.h> //For I2C comms
#include <EEPROM.h> // to read the serial number

void setup(void) { 
  Serial.begin(115200); // Initialize the serial port.
  Wire.begin();
}

void loop(void) { 
  // I print a known byte to allow the my code on the PC to sync up with this stream
  Serial.print('\xFF');
  //Wire.print("foo");
  // I request two bytes from I2C slave address 0x78
  Wire.requestFrom(0x78, 2); 
  //Wire.print("bar");
  // I then print the two bytes I got back
  while(Wire.available())
    Serial.print((char)Wire.read());
  // The PC asks for the serial number by writing a single byte to the board
  if(Serial.available()){
    Serial.print("This is pressure sensor number:");
    // the serial number is a byte stored at address 0
    Serial.write(EEPROM.read(0));
    // remove the recieved byte from the buffer
    Serial.read();
  }
} 
/*
performance over time:
419 Hz before any optimiseation
820 Hz after I switched to a binary data format
820 Hz after I added a check for the Serial input buffer having data in. I am suprised that there is no detectable speed reduction.
820 Hz after I rearranged the execution order

relevent thread:
http://forum.arduino.cc/index.php?topic=141759.0
*/
