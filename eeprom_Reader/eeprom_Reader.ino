#include <EEPROM.h>

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  // print the value at address 0 as a human readable number
  Serial.print(EEPROM.read(0));
  // print the value at address 0 as a raw byte
  Serial.write(EEPROM.read(0));
  delay(500);
}
