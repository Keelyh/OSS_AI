int CASE;

void setup() {                
  pinMode(13, OUTPUT);     
  Serial.begin(9600);
}


//digitalWrite(13, HIGH);
void loop() {
  if(Serial.available() > 0){
    CASE = Serial.read();
    Serial.print("Case: ");
    Serial.println(CASE);
    switch(CASE){
      case 10:
        digitalWrite(13, HIGH);
        break;
      case 5:
        digitalWrite(13, LOW);
        break;
    }
  }
}
