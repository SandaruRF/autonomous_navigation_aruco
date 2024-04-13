#include <AFMotor.h>

AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);

void motorRun(int direct);
void motorSetSpeed(int speedVal);

void setup() {
  motorSetSpeed(200);
  motorRun(RELEASE);
}

void loop() {
  uint8_t i; // i can get values from 0 to 255

  motorRun(FORWARD);

  for (i = 0; i < 255; i++){
    motorSetSpeed(i);
    delay(10);
  }
  for (i = 255; i > 0; i--){
    motorSetSpeed(i);
    delay(10);
  }

  motorRun(BACKWARD);

  for (i = 0; i < 255; i++){
    motorSetSpeed(i);
    delay(10);
  }
  for (i = 255; i > 0; i--){
    motorSetSpeed(i);
    delay(10);
  }

  motorRun(RELEASE);
  delay(1000);
}

void motorRun(int direct){
  motor1.run(direct);
  motor2.run(direct);
  motor3.run(direct);
  motor4.run(direct);
}

void motorSetSpeed(int speedVal){
  motor1.setSpeed(speedVal);
  motor2.setSpeed(speedVal);
  motor3.setSpeed(speedVal);
  motor4.setSpeed(speedVal);
}
