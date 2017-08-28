#ifndef LAB_BOT_H_
#define LAB_BOT_H_
#include <Arduino.h>
#include "Axis.h"
#include "Plunger.h"

class LabBot{
public:
  LabBot getInstance();

  byte moveTo(float, float, float);

  byte dispense(float);

  byte aquire(float);

  byte home();

private:
  LabBot(float,float,float);
  
  Axis *_lock = NULL;

  Axis _x;
  Axis _y;
  Axis _z;
  Plunger _plunger;
};



#endif
