#include <Servo.h>

Servo motor1;
Servo motor2;

void setup() {
  Serial.begin(9600);                             // start the serial port

  motor1.attach(3);
  motor2.attach(5);
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

void loop() {
  int forward_speed = 110;
  int stop_speed = 95;
  float distance = read_gp2d12_range(0);
  Serial.println(distance);                       // print the distance
  
  if (distance < 2.0){
    motor1.write(stop_speed);
    motor2.write(stop_speed);
  } else {
    motor1.write(forward_speed);
    motor2.write(forward_speed);
  }
  
  delay(100);
  
}
