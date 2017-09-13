#define X_STEP_CLK 3
#define Y_STEP_CLK 2
#define Z_STEP_CLK 4
#define P_STEP_CLK 5

#define XYZ_DIR 12
#define P_DIR 8

#define MSEL2 6
#define MSEL3 7

#define X_LIMIT A0
#define Y_LIMIT A1
#define Z_LIMIT A2
#define P_UP_LIMIT A3
#define P_DN_LIMIT A4

#define LED 13

#define PULSE_GAP 400
#define DIR_DELAY 10

#define XYZ_FWD 1
#define XYZ_BCK 0
#define P_UP 0
#define P_DN 1

#define LIMITGAP 30

void ledblink(int duration, unsigned numb) {
  unsigned int i;
  for (i=0; i<numb; i++) {
    digitalWrite(LED,HIGH);
    delay(duration);
    digitalWrite(LED,LOW);
    delay(duration);
  }
}

void limitCheck(int limitpin, int duration, unsigned int numb) {
  int limState;
  limState = digitalRead(limitpin);
  if (limState == HIGH) {
    ledblink(duration, numb);
    delay(500);
  }
}

void set_direction(int dirpin, bool cw)
{
  if (cw)
  {
    digitalWrite(dirpin, HIGH);
    delay(DIR_DELAY);
  }
  else
  {
    digitalWrite(dirpin, LOW);
    delay(DIR_DELAY);
  }
}

void nstep_forward(unsigned int steps, int clkpin, int limitpin)
{
  unsigned int lsteps=0;
  int limState;
  set_direction(XYZ_DIR, XYZ_FWD);
  for (unsigned int i = 0; i < steps; i++)
  {
    limState = digitalRead(limitpin);
    if (limState == HIGH) { lsteps++; }
    if (lsteps<LIMITGAP) {
      digitalWrite(clkpin, HIGH);
      delayMicroseconds(PULSE_GAP);
      digitalWrite(clkpin, LOW);
      delayMicroseconds(PULSE_GAP);
    }
  }
  set_direction(XYZ_DIR, 0);
  delay(250);
}

void xstep_forward(unsigned int steps) { nstep_forward(steps, X_STEP_CLK, X_LIMIT); }
void ystep_forward(unsigned int steps) { nstep_forward(steps, Y_STEP_CLK, Y_LIMIT); }
void zstep_forward(unsigned int steps) { nstep_forward(steps, Z_STEP_CLK, Z_LIMIT); }

void nstep_back(unsigned int steps, int clkpin, int limitpin)
{
  int limState;
  set_direction(XYZ_DIR, XYZ_BCK);
  for (unsigned int i = 0; i < steps; i++)
  {
    limState = digitalRead(limitpin);
    if (limState == LOW) {
      digitalWrite(clkpin, HIGH);
      delayMicroseconds(PULSE_GAP);
      digitalWrite(clkpin, LOW);
      delayMicroseconds(PULSE_GAP);
    }
  }
  set_direction(XYZ_DIR, 0);
  delay(250);
}

void xstep_back(unsigned int steps) { nstep_back(steps, X_STEP_CLK, X_LIMIT); }
void ystep_back(unsigned int steps) { nstep_back(steps, Y_STEP_CLK, Y_LIMIT); }
void zstep_back(unsigned int steps) { nstep_back(steps, Z_STEP_CLK, Z_LIMIT); }

void gohome(int clkpin, int limitpin)
{
  int limState;
  set_direction(XYZ_DIR, XYZ_BCK);
  do {
    limState = digitalRead(limitpin);
    if (limState == LOW) {
      digitalWrite(clkpin, HIGH);
      delayMicroseconds(PULSE_GAP);
      digitalWrite(clkpin, LOW);
      delayMicroseconds(PULSE_GAP);
    }
  } while(limState == LOW);
  set_direction(XYZ_DIR, 0);
  delay(250);
}

void xhome() { gohome(X_STEP_CLK, X_LIMIT); }
void yhome() { gohome(Y_STEP_CLK, Y_LIMIT); }
void zhome() { gohome(Z_STEP_CLK, Z_LIMIT); }

void pstep(unsigned int steps, int pdir, int limitpin)
{
  int limState;
  set_direction(P_DIR, pdir);
  for (unsigned int i = 0; i < steps; i++)
  {
    limState = digitalRead(limitpin);
    if (limState == LOW) {
      digitalWrite(P_STEP_CLK, HIGH);
      delayMicroseconds(PULSE_GAP);
      digitalWrite(P_STEP_CLK, LOW);
      delayMicroseconds(PULSE_GAP);
    }
  }
  set_direction(P_DIR, 0);
  delay(250);
}

void piston_dn(unsigned int steps) { pstep(steps, P_DN, P_DN_LIMIT); }
void piston_up(unsigned int steps) { pstep(steps, P_UP, P_UP_LIMIT); }

void phome(int pdir, int limitpin) {
  int limState;
  set_direction(P_DIR, pdir);
  do {
    limState = digitalRead(limitpin);
    if (limState == LOW) {
      digitalWrite(P_STEP_CLK, HIGH);
      delayMicroseconds(PULSE_GAP);
      digitalWrite(P_STEP_CLK, LOW);
      delayMicroseconds(PULSE_GAP);
    }
  } while (limState == LOW);
  set_direction(P_DIR, 0);
  delay(250);
}

void phome_dn() { phome(P_DN, P_DN_LIMIT); }
void phome_up() { phome(P_UP, P_UP_LIMIT); }

void setup() {

  unsigned int column;
  
  pinMode(X_STEP_CLK, OUTPUT);
  pinMode(Y_STEP_CLK, OUTPUT);
  pinMode(Z_STEP_CLK, OUTPUT);
  pinMode(P_STEP_CLK, OUTPUT);
  pinMode(XYZ_DIR, OUTPUT);
  pinMode(P_DIR, OUTPUT);
  pinMode(LED, OUTPUT);
  pinMode(X_LIMIT, INPUT);
  pinMode(Y_LIMIT, INPUT);
  pinMode(Z_LIMIT, INPUT);
  pinMode(P_UP_LIMIT, INPUT);
  pinMode(P_DN_LIMIT, INPUT);
  pinMode(MSEL2, OUTPUT);
  pinMode(MSEL3, OUTPUT);

/*  piston_up(1000);
  delay(5000);
  zstep_back(1500);
  delay(5000);
  zstep_forward(1500);
  delay(500);
  piston_dn(1000);
  
  
  zhome();
  delay(500);
  yhome();
  delay(500);
  xhome();
  delay(500);
  ystep_forward(4700);
  xstep_forward(666);
  phome_dn();
  piston_up(1500);
  zstep_forward(4700);
  piston_up(12000);
  for (column=0; column<11; column++) {
    zstep_back(1000);
    ystep_back(281);
    zstep_forward(1000);
    piston_dn(1000);
  }
  zstep_back(1000);
  ystep_forward(3091);
  zstep_forward(1000);
  phome_dn();
  zhome();
*/

  Serial.begin(9600);

}

#include "sercomm.h"

void loop() {
/*  limitCheck(X_LIMIT, 200, 1);
  limitCheck(Y_LIMIT, 200, 2);
  limitCheck(Z_LIMIT, 200, 3);
  limitCheck(P_UP_LIMIT, 200, 4);
  limitCheck(P_DN_LIMIT, 200, 5);
*/
  char sComm[] = { ' ',' ',' ',' ' };
  char sVal[] = { ' ',' ',' ',' ',' ',' ',' ',' ' };
  unsigned int iComm;
  
  if (Serial.available()) {
    Serial.readBytes(sComm, 4);
    Serial.readBytes(sVal, 8);

    iComm = atoi(sComm);
    switch(iComm) {
      case COMM_XHOME:
        xhome();
        break;
      case COMM_YHOME:
        yhome();
        break;
      case COMM_ZHOME:
        zhome();
        break;
      case COMM_XFWD:
        xstep_forward(atoi(sVal));
        break;
      case COMM_YFWD:
        ystep_forward(atoi(sVal));
        break;
      case COMM_ZFWD:
        zstep_forward(atoi(sVal));
        break;
      case COMM_XBACK:
        xstep_back(atoi(sVal));
        break;
      case COMM_YBACK:
        ystep_back(atoi(sVal));
        break;
      case COMM_ZBACK:
        zstep_back(atoi(sVal));
        break;
      case COMM_PHOMEDN:
        phome_dn();
        break;
      case COMM_PHOMEUP:
        phome_up();
        break;
      case COMM_PISTONUP:
        piston_up(atoi(sVal));
        break;
      case COMM_PISTONDN:
        piston_dn(atoi(sVal));
        break;
      case COMM_LEDBLINK:
        ledblink(100, atoi(sVal));
        break;
      default:
        break;

    }
        Serial.println(1);
  }
  delay(500);

}



