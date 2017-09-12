#define X_STEP_CLK 3
#define Y_STEP_CLK 2
#define X_STEP_CLK 4
#define P_STEP_CLK 5

#define XYZ_DIR 12
#define P_DIR 8

#define X_LIMIT 14
#define Y_LIMIT 15
#define Z_LIMIT 16
#define P_UP_LIMIT 17
#define P_DN_LIMIT 18

#define LED 13

#define PULSE_GAP 400
#define DIR_DELAY 5

void ledblink(int duration) {
  unsigned int i;
  for (i=0; i<3; i++) {
    digitalWrite(LED,HIGH);
    delay(duration);
    digitalWrite(LED,LOW);
    delay(duration);
}

void setup() {

  pinMode(X_STEP_CLK, OUTPUT);
  pinMode(Y_STEP_CLK, OUTPUT);
  pinMode(Z_STEP_CLK, OUTPUT);
  pinMode(XYZ_DIR, OUTPUT);
  pinMode(P_DIR, OUTPUT);
  pinMode(LED, OUTPUT);
  pinMode(X_LIMIT, INPUT);
  pinMode(Y_LIMIT, INPUT);
  pinMode(Z_LIMIT, INPUT);
  pinMode(P_UP_LIMIT, INPUT);
  pinMode(P_DN_LIMIT, INPUT);

}

void loop() {
  int limState;
  limState = analogRead(X_LIMIT);
  if (limState == HIGH) {
    ledblink(500);
  }

}



