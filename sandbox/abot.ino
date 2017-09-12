#define X_STEP_CLK 3
#define Y_STEP_CLK 2
#define Z_STEP_CLK 4
#define P_STEP_CLK 5

#define XYZ_DIR 12
#define P_DIR 8

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

void ledblink(int duration) {
  unsigned int i;
  for (i=0; i<3; i++) {
    digitalWrite(LED,HIGH);
    delay(duration);
    digitalWrite(LED,LOW);
    delay(duration);
  }
}

void limitCheck(int limitpin, int duration) {
  int limState;
  limState = digitalRead(limitpin);
  if (limState == HIGH) {
    ledblink(duration);
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
}

void piston_dn(unsigned int steps) { pstep(steps, P_DN, P_DN_LIMIT); }
void piston_up(unsigned int steps) { pstep(steps, P_UP, P_UP_LIMIT); }


void setup() {

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
  piston_up(6000);
  
  ledblink(200);
  /*zhome();
  delay(100);
  yhome();
  delay(100);
  xhome();
  delay(100);
  ystep_forward(280);
  delay(100);
  zstep_forward(3900);
  delay(100);
  xstep_forward(666);
  set_direction(XYZ_DIR,0);
  set_direction(XYZ_DIR,1);
*/
}

void loop() {
  limitCheck(X_LIMIT, 200);
  limitCheck(Y_LIMIT, 400);
  limitCheck(Z_LIMIT, 800);
  limitCheck(P_UP_LIMIT, 100);
  limitCheck(P_DN_LIMIT, 300);
  delay(1000);

}


