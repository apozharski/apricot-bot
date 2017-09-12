#include "Arduino.h"
#include "Axis.h"
#include "LabBot.h"

LabBot LabBot::getInstance()
{
  static LabBot instance();

  return instance;
}

byte LabBot::moveTo(float x_pos, float y_pos, float z_pos)
{
  _x.moveTo(x_pos);
  _y.moveTo(y_pos);
  _z.moveTo(z_pos);
}

byte LabBot::dispense(float vol)
{
  return _plunger.dispense(vol);
}

byte LabBot::aquire(float vol)
{
  return _plunger.aquire(vol);
}

byte LabBot::home()
{
  _x.home();
  _y.home();
  _z.home();
}

//LabBot::LabBot(float x_cal, float y_cal, float z_cal) : _x(&lock,0,1,2,x_cal) : _y(&lock,3,4,5,y_cal) : _z(&lock,6,7,8,z_cal)
//{}

