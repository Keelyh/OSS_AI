#include <Servo.h>

/* Sensor Pins */
#define F_SEN 0    // forward
#define R_SEN 1    // right
#define L_SEN 2    // left

/* Motor Speeds */
#define FRWD 110
#define STOP 90
#define BKWD 70

int CASE;
float f_sen;
float r_sen;
float l_sen;

Servo motor1;
Servo motor2;

void setup() {
  Serial.begin(9600);                             // start the serial port

  motor1.attach(3);  //green wire goes to port 3
  motor2.attach(5);  //grey wire goes to port 5
}

float read_gp2d12_range(byte pin) {
	int tmp;

	tmp = analogRead(pin);
	if (tmp < 3)
		return -1; // invalid value
        
        float voltage = tmp*0.0048828125;
        
        float fifth = voltage*voltage*voltage*voltage*voltage;
        float fourth = voltage*voltage*voltage*voltage;
        float third = voltage*voltage*voltage;
        float square = voltage*voltage;
        float keely_calc = -0.2887*fifth + 3.3107*fourth - 14.925*third + 33.221*square - 38.116*voltage + 21.376;
        
        return keely_calc;
} 
void robot_stop(){
  motor1.write(STOP);
  motor2.write(STOP);
}
void forward(){
  motor1.write(FRWD);
  motor2.write(FRWD);
}  

void right_turn(){
  motor1.write(FRWD);
  motor2.write(BKWD);
  delay(1200);
  robot_stop();
}

void left_turn(){
  motor1.write(BKWD);
  motor2.write(FRWD);
  delay(1400);
  robot_stop();
}


void one_eighty(){
  motor1.write(FRWD);
  motor2.write(BKWD);
  delay(2400);
  robot_stop();
}

void loop() {
  if(Serial.available() > 0){
    CASE = Serial.read();
    switch(CASE){
      case 0:
        forward();
        break;
      case 1:
        right_turn();
        break;
      case 2:
        left_turn();
        break;
      case 3:
        one_eighty();
        break;
      case 4:
        robot_stop();
        break;
    }
  }
  else{
    f_sen = read_gp2d12_range(F_SEN);
    r_sen = read_gp2d12_range(R_SEN);
    l_sen = read_gp2d12_range(L_SEN);
    Serial.println(100 + f_sen);
    Serial.println(200 + r_sen);
    Serial.println(300 + l_sen);
  }
}
