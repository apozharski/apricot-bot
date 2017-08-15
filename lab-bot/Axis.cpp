#include "Axis.h"
#include "ErrorCodes.h"

Axis::Axis(Axis **lock, byte step_clk, byte dir, byte home, float step_cal)
{
  _lock = lock;
  _step_clk = step_clk;
  _dir = dir;
  _home = home;
  _step_cal = step_cal;

  pinMode(_step_clk, OUTPUT);
  pinMode(_dir, OUTPUT);
  pinMode(_home, INPUT);
}


byte Axis::moveTo(float)
{
  //TODO: finish this implementation
  return 0;
}


byte Axis::home();
  

void Axis::_requestLock()
{
  *_lock = this;
}

void Axis::_releaseLock()
{
  *_lock = NULL;
}

bool Axis::_checkLock()
{
  return *_lock == this ? true : false;
}

void Axis::_takeStep()
{
  digitalWrite(STEP_CL, HIGH);
  delayMicroseconds(STEP_GAP);
  digitalWrite(STEP_CLK, LOW);
  delayMicroseconds(STEP_GAP);
}

void Axis::_setDir(char dir)
{
  if(dir)
  {
    digitalWrite(_dir, HIGH);
  }
  else
  {
    digitalWrite(_dir, LOW);
  }
}

byte Axis::_takeSteps(int steps, char dir)
{
   if(!_checkLock())
   {
     return LOCK_LOST;
   }
  _setDir(dir);

  for(int i = 0; i < steps; i++)
  {
    if(digitalRead(_home))
    {
      return HOME_OVERRUN;
    }
    else if(!_checkLock())
    {
      return LOCK_LOST;
    }
    else
    {
      takeStep();
    }
  }

  return 0;
}
