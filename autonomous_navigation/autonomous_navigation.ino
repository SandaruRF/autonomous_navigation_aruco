#include <Dictionary.h>
#include <AFMotor.h>

AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);

Dictionary<String, int>
directions = {
  {"East", 90},
  {"South-East", 135},
  {"South", 180},
  {"South-West", 225},
  {"West", 270},
  {"North-West", 315},
  {"North", 0},
  {"North-East", 45}
}

void Move(int cur_ang, int prev_ang);

void setup() {
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  Serial.begin(115200);
  while(!Serial){}
}

void loop() {
  if (Serial.available() > 0){
    String message = Serial.readStringUntil('\n');
    if (message == "STOP"){
      digitalWrite(13, HIGH);
    }else {
      digitalWrite(13, LOW);
    }
  }
}

void Move(int cur_ang, int prev_ang){
  diff = cur_ang - prev_ang;
  if (diff == 0){
    Run(FORWARD, STRAIGHT
  }
}
