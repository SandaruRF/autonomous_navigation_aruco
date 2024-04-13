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
