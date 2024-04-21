#include <Arduino.h>
#include <AFMotor.h>

AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);

struct Direction {
  String name;
  int angle;
};

Direction directions[] = {
  {"East", 90},
  {"South-East", 135},
  {"South", 180},
  {"South-West", 225},
  {"West", 270},
  {"North-West", 315},
  {"North", 0},
  {"North-East", 45}
};

void Move(int cur_ang, int prev_ang);

void setup() {
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  Serial.begin(115200);
  while(!Serial){}
}

void loop() {
  Serial.println("Start"); // start detection
  if (Serial.available() > 0){
    String message = Serial.readStringUntil('\n');
    for (size_t i = 0; i < sizeof(directions) / sizeof(directions[0]); i++) {
      if (message.equals(directions[i].name)) {
        int angle = directions[i].angle;
        int n = angle / 45;
        for (int j = 0; j < n; j++) {
          digitalWrite(13, HIGH);
          delay(1000);
          digitalWrite(13, LOW);
          delay(1000);
        }
        break;
      }
    }
  }
//  delay(8000);
//  Serial.println("Stop");  // stop detection
  delay(2000);
}
//
//void Move(int cur_ang, int prev_ang){
//  diff = cur_ang - prev_ang;
//  if (diff == 0){
//    Run(FORWARD, STRAIGHT
//  }
//}
