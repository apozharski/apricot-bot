#ifndef AXIS_H_
#define AXIS_H_
#include <Arduino.h>

#define STEP_GAP 5
#define DIR_GAP 5


class Axis{
public:

  /**
   * Axis constructor should only be called once per motor axis.
   *
   * @param {**Axis} Pointer to the axis which currently holds the motion lock.
   * @param {byte} step_clk Step clock pin.
   * @param {byte} dir Direction control pin.
   * @param {byte} home Home limit switch pin
   * @param {float} step_cal Calibration of steps to meters.
   */
  Axis(Axis **lock, byte step_clk, byte dir, byte home, float step_cal);

  /**
   * Moves to the position in meters on a given axis. 
   *
   * @param {float} position Position to move the axis to in meters.
   */
  byte moveTo(float position);

  /**
   * Reset the axis to home position.
   */
  byte home();

  
private:


  byte _step_clk;
  byte _dir;
  byte _home;
  float _step_cal;
  int _curr_step;
  Axis **_lock;

  /**
   * Requests the motion lock. Requests are always honored
   */
  void _requestLock();

  /**
   * Releases the motion lock.
   */
  void _releaseLock();

  /**
   * Checks wheter this axis holds the motion lock.
   *
   * @return {bool} True if the lock is held. False otherwise.
   */ 
  bool _checkLock();

  /**
   * Takes a single step.
   */ 
  void _takeStep();

  /**
   * Sets the direction of motion.
   *
   * @param {char} dir Direction to set to. 0 : clockwise, 1 : counter-clockwise
   */
  void _setDir(char dir);

  /**
   * Takes a number of steps in the specified direction
   *
   * @param {int} steps Number of steps to take.
   * @param {char} dir Direction to take steps in. See _setDir for value meanings
   * @return {byte} Return code
   */
  byte _takeSteps(int steps, char dir);
};

#endif
