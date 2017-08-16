#include "Axis.h"
#include "ErrorCodes.h"

Axis::Axis(Axis **lock, byte step_clk, byte dir, byte home, float step_cal)
{
  _lock = lock;
  _step_clk = step_clk;
  _dir = dir;
  _home = home;
  _step_cal = step_cal;
  _curr_step = -1;

  
  pinMode(_step_clk, OUTPUT);
  pinMode(_dir, OUTPUT);
  pinMode(_home, INPUT);
}


byte Axis::moveTo(float target)
{
  if(_curr_step < 0)
  {
    return MOVE_BEFORE_HOME;
  }

  
  float motion  = target - (_curr_step*_step_cal);

  char dir = motion > 0;

  int steps = (int) round((motion/_step_cal));

  _requestLock();
  return _takeSteps(steps,dir);
}


byte Axis::home()
{
  if(!_checkLock())
  {
    return LOCK_LOST;
  }
  _setDir(0);

  while(!digitalRead(_home))
  {
    if(!_checkLock())
    {
      return LOCK_LOST;
    }
    else
    {
      takeStep();
    }
  }

  _curr_steps = 0;
  
  return 0;
}
  

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
