const int delay_ms = 100; 
int pin2 = 5; //pin2 references pin D2 on the board, and so on. We only use digital pins for this
 			  //application. EDIT: Discovered that due to use of off-brand Nano, pin numbers
              //correspond directly to pin labels. This code controls pins 5-12 as a result. 
int pin3 = 6; 
int pin4 = 7; 
int pin5 = 8; 
int pin6 = 9; 
int pin7 = 10; 
int pin8 = 11; 
int pin9 = 12; 
  
void setup() { 
  pinMode(pin2, OUTPUT); 
  pinMode(pin3, OUTPUT); 
  pinMode(pin4, OUTPUT); 
  pinMode(pin5, OUTPUT); 
  pinMode(pin6, OUTPUT); 
  pinMode(pin7, OUTPUT); 
  pinMode(pin8, OUTPUT); 
  pinMode(pin9, OUTPUT); 
  
  digitalWrite(pin2, HIGH); 
  delay(delay_ms); 
  digitalWrite(pin3, HIGH); 
  delay(delay_ms); 
  digitalWrite(pin4, HIGH); 
  delay(delay_ms); 
  digitalWrite(pin5, HIGH); 
  delay(delay_ms); 
  digitalWrite(pin6, HIGH); 
  delay(delay_ms); 
  digitalWrite(pin7, HIGH); 
  delay(delay_ms); 
  digitalWrite(pin8, HIGH); 
  delay(delay_ms); 
  digitalWrite(pin9, HIGH); 
} 
  
void loop() { 
 		//because we only execute the sequential power-up on startup, we don’t need to
		//execute anything in the loop function. 
}