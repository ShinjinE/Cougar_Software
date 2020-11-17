/**
 * RC Signal to Arduino with interrupts to control 2D Face Test
 * Author: Parker King
 * Date: Oct 29, 2020
 * 
 * Connect RC receiver signals (PWM) to Arduino.
 * Connect servos to Arduino.
 * 
 * This code is the prototype for controlling the servos
 * in the 2D face mock up via an Arduino receiving an
 * RC signal using interrupts to process the RC signals.
 */

#include <Servo.h>

// Servo Objects
Servo leftBrowL;
Servo leftBrowR;
Servo rightBrowR;
Servo rightBrowL;
Servo jawR;
Servo jawL;

// Channel numbers
const int NUM_CHANNELS = 5;
const int CHAN_LBL = 1;
const int CHAN_LBR = 2;
const int CHAN_RBR = 3;
const int CHAN_RBL = 4;
const int CHAN_JAW = 5;

// Controller pins
const int IN_L_EYE_L = 2;
const int IN_L_EYE_R = 4;
const int IN_R_EYE_R = 7;
const int IN_R_EYE_L = 8;
const int IN_JAW = 12;

// Servo driver pins
const int OUT_L_EYE_L = 3;
const int OUT_L_EYE_R = 5;
const int OUT_R_EYE_R = 6;
const int OUT_R_EYE_L = 9;
const int OUT_JAW_L = 10;
const int OUT_JAW_R = 11;

// Servo Parameters
const int MAX_POS = 135;
const int MIN_POS = 45;
const int MID_POS = (MAX_POS + MIN_POS) / 2;
const int FULL_RANGE = MIN_POS - MAX_POS;
const int MID_RANGE = MAX_POS - MID_POS;
const int SENS_STEP = 1;
const int MAX_SENS = 20;
const int MIN_SENS = 1;
const int WAVE_MILLIS = 100;

// Servo Positions
int posLBL = 90;
int posLBR = 90;
int posRBR = 90;
int posRBL = 90;
int posJawL = 0;
int posJawR = 0;

void setup()  {
  setup_pwmRead();
  Serial.begin(9600);

  // Configure pins
  pinMode(IN_L_EYE_L, INPUT);
  pinMode(IN_L_EYE_R, INPUT);
  pinMode(IN_R_EYE_R, INPUT);
  pinMode(IN_R_EYE_L, INPUT);
  pinMode(IN_JAW, INPUT);
  leftBrowL.attach(OUT_L_EYE_L);
  leftBrowR.attach(OUT_L_EYE_R);
  rightBrowR.attach(OUT_R_EYE_R);
  rightBrowL.attach(OUT_R_EYE_L);
  jawR.attach(OUT_JAW_L);
  jawL.attach(OUT_JAW_R);
}

void loop() {
  read_inputs();
  write_positions();
  
  if (Serial) {
    print_decoded_pwm();
  }
}

void read_inputs() {
  posLBL = read_signal(CHAN_LBL,MIN_POS,MAX_POS);
  posLBR = read_signal(CHAN_LBR,MAX_POS,MIN_POS); // Position Inverted
  posRBR = read_signal(CHAN_RBR,MAX_POS,MIN_POS); // Position Inverted
  posRBL = read_signal(CHAN_RBL,MAX_POS,MIN_POS); // Position Inverted
  posJawL = read_signal(CHAN_JAW,MIN_POS,MAX_POS);
  posJawR = map(posJawL,MIN_POS,MAX_POS,MAX_POS,MIN_POS);
}

int read_signal(int channel, int minPos, int maxPos) {
  const int MAX_SIGNAL = 100;
  const int MIN_SIGNAL = -MAX_SIGNAL;
  const float CONVERT_INT = (float)abs(MAX_SIGNAL);
  
  float pwmSignal = RC_decode(channel) * CONVERT_INT;
  pwmSignal = constrain(pwmSignal, MIN_SIGNAL, MAX_SIGNAL);
  return map(pwmSignal, MIN_SIGNAL, MAX_SIGNAL, minPos, maxPos);
}

void write_positions() {
  leftBrowL.write(posLBL);
  leftBrowR.write(posLBR);
  rightBrowR.write(posRBR);
  rightBrowL.write(posRBL);
  jawL.write(posJawL);
  jawR.write(posJawR);
}

void print_decoded_pwm () {
  Serial.print(posLBL); Serial.print("\t");
  Serial.print(posLBR); Serial.print("\t");
  Serial.print(posRBR); Serial.print("\t");
  Serial.print(posRBL); Serial.print("\t");
  Serial.print(posJawL); Serial.print("\t");
  Serial.print(posJawR); Serial.print("\t");
  Serial.println("");
}
