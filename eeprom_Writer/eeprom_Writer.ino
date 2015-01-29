#include <EEPROM.h>

void setup()
{
  // the first argument is the address (int), the second argument is the value to write (byte)
  EEPROM.write(0, 4);

  // turn the LED on when we're done
  digitalWrite(13, HIGH);
}

void loop()
{
}
