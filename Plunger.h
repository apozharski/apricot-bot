#include"Arduino.h"

#ifndef PLUNGER_H__
#define PLUNGER_H__

class Plunger
{
public:

  Plunger();
  
  byte dispense(float);

  byte aquire(float);

  
private:
  
  /**
   *
   */ 
  byte _step_clk;
  
  /**
   *
   */
  byte _dir;

  /**
   *
   */
  byte _home;

  /**
   *
   */
  float _step_cal;

  /**
   *
   */
  int _curr_step;
  
};



#endif
