/*
 * servo_game_test
 * Version: 3
 * Author: Parker King
 * Purpose:
 *   Test code to prototype the concept of using a gamepad (Nintendo Switch
 * Pro controller in this case) to control servos.
 *
 * New:
 *   - Added functionality for 5 servos instead of 1
 *     - Rove function behaves differently for each servo
 *     - Perform macro maps all servos to the same positions
 *   - Added wave macro (mimics people doing the wave in a stadium)
 */

//~~~~~~~~~~~~~~~~~ Imports ~~~~~~~~~~~~~~~~~
import processing.serial.*;

import net.java.games.input.*;
import org.gamecontrolplus.*;
import org.gamecontrolplus.gui.*;

import cc.arduino.*;
import org.firmata.*;

//~~~~~~~~~~~~~~~~~ Constants and Variable Declaration ~~~~~~~~~~~~~~~~~
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`~~~~~~~~~~~~
//~~~~~~~~~~~~~~~~~ Declare Control Variables ~~~~~~~~~~~~~~~~~
ControlDevice device;
ControlIO control;
ControlSlider leftV;
ControlSlider leftH;
ControlSlider rightV;
ControlSlider rightH;
ControlButton leftBump;
ControlButton leftTrigger;
ControlButton rightTrigger;
ControlButton aButton;
ControlButton bButton;
ControlButton xButton;
ControlHat dPad;

Arduino arduino;

//~~~~~~~~~~~~~~~~~ Declare Servo Pins ~~~~~~~~~~~~~~~~~
final int SERVO1_PIN = 3;
final int SERVO2_PIN = 5;
final int SERVO3_PIN = 6;
final int SERVO4_PIN = 9;
final int SERVO5_PIN = 10;
final int SERVO6_PIN = 11;

//~~~~~~~~~~~~~~~~~ Declare Constants ~~~~~~~~~~~~~~~~~
final int MAX_POS = 135;
final int MIN_POS = 45;
final int MID_POS = (MIN_POS + MAX_POS) / 2;
final int MID_RANGE = MAX_POS - MID_POS;
final int SENS_STEP = 1;
final int MAX_SENS = 20;
final int MIN_SENS = 1;
final int WAVE_MILLIS = 100;

//~~~~~~~~~~~~~~~~~ Initialize Variables ~~~~~~~~~~~~~~~~~
ControlMode controlMode;
ControlMode prevManualMode;
PerformMode performMode;
WaveMode waveMode;
int performChangeMillis;
int waveDelay;
int prevManualPos1;
int prevManualPos2;
int prevManualPos3;
int prevManualPos4;
int prevManualPos5;
int prevManualPos6;
int pos1;
int pos2;
int pos3;
int pos4;
int pos5;
int pos6;
int stickStepSens = 5;
boolean prevStateLBump;
boolean prevStateA;
boolean prevStateB;
boolean prevStateX;
boolean prevStateDPadH;
boolean prevStateDPadV;

boolean lBrowLUp;
boolean lBrowRUp;
boolean rBrowRUp;
boolean rBrowLUp;
boolean jawUp;

//~~~~~~~~~~~~~~~~~ Setup Function ~~~~~~~~~~~~~~~~~
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
void setup() {
  size(360, 200);
  
  control = ControlIO.getInstance(this);
  device = control.getMatchedDevice("test_default");
  
   if (device == null) {
    println("Ha! Loser!");
    System.exit(-1);
  }
  
  leftV = device.getSlider("joyLeftVert");
  leftH = device.getSlider(3);
  rightV = device.getSlider("joyRightVert");
  rightH = device.getSlider("joyRightHor");
  leftBump = device.getButton("lBumper");
  leftTrigger = device.getButton("lTrigger");
  rightTrigger = device.getButton("rTrigger");
  aButton = device.getButton("aButton");
  bButton = device.getButton("bButton");
  xButton = device.getButton("xButton");
  dPad = device.getHat("dPad");
  
  println(Arduino.list());
  arduino = new Arduino(this, Arduino.list()[0], 57600);
  arduino.pinMode(SERVO1_PIN, Arduino.SERVO);
  arduino.pinMode(SERVO2_PIN, Arduino.SERVO);
  arduino.pinMode(SERVO3_PIN, Arduino.SERVO);
  arduino.pinMode(SERVO4_PIN, Arduino.SERVO);
  arduino.pinMode(SERVO5_PIN, Arduino.SERVO);
  arduino.pinMode(SERVO6_PIN, Arduino.SERVO);
  
  pos1 = MID_POS;
  pos2 = MID_POS;
  pos3 = MID_POS;
  pos4 = MID_POS;
  pos5 = MID_POS;
  pos6 = MID_POS;
  
  controlMode = ControlMode.EXACT_POS;
  performMode = PerformMode.START;
  prevStateLBump = leftBump.pressed();
  
  printSettings();
}

//~~~~~~~~~~~~~~~~~ Get User Feedback ~~~~~~~~~~~~~~~~~
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
public void getUserInput(){
  boolean currStateLBump = leftBump.pressed();
  if (!prevStateLBump) {
    if (currStateLBump) {
      if (!isMacro(controlMode)) {
        print("Bumper Pressed: Switching from " + controlMode.toString() + " to ");
        controlMode = ControlMode.nextState(controlMode);
        println(controlMode.toString());
      }
    }
  }
  prevStateLBump = currStateLBump;
  
  if (rightTrigger.pressed()) {
    if (!isMacro(controlMode)) {
      pos5 += stickStepSens;
      pos6 += -stickStepSens;
    }
  }
  if (leftTrigger.pressed()) {
    if (!isMacro(controlMode)) {
      pos5 -= stickStepSens;
      pos6 -= -stickStepSens;
    }
  }
  
  boolean currStateA = aButton.pressed();
  if (!prevStateA) {
    if (currStateA) {
      switch (controlMode) {
        case ROVE_MACRO_UP:
        case ROVE_MACRO_DOWN:
          controlMode = prevManualMode;
          returnPrevManPos();
          println("A Button Pressed: Switching back to " + controlMode.toString());
          break;
        default:
          if (!isMacro(controlMode)) {
            prevManualMode = controlMode;
            recordPrevManPos();
            pos1 = MID_POS + (MID_RANGE / 2);
            lBrowLUp = true;
            pos2 = MID_POS + (MID_RANGE / 2);
            lBrowRUp = false;
            pos3 = MID_POS;
            rBrowLUp = false;
            pos4 = MIN_POS;
            rBrowRUp = true;
            pos5 = MID_POS - (MID_RANGE / 2);
            pos6 = MID_POS + (MID_RANGE / 2);
            jawUp = true;
          }
          controlMode = ControlMode.ROVE_MACRO_UP;
          println("A Button Pressed: Switching to macro " + controlMode.toString());
          //pos1 = MIN_POS;
          //pos2 = MIN_POS;
          //pos3 = MAX_POS;
          //pos4 = MAX_POS;
          //pos5 = MID_POS + (MAX_POS - MIN_POS) / 4;
          //pos6 = MID_POS - (MAX_POS - MIN_POS) / 4;
      }
    }
  }
  prevStateA = currStateA;
  
  boolean currStateB = bButton.pressed();
  if (!prevStateB) {
    if (currStateB) {
      switch (controlMode) {
        case PERFORM_MACRO:
          controlMode = prevManualMode;
          returnPrevManPos();
          println("B Button Pressed: Switching back to " + controlMode.toString());
          break;
        default:
          if (!isMacro(controlMode)) {
            prevManualMode = controlMode;
            recordPrevManPos();
          }
          controlMode = ControlMode.PERFORM_MACRO;
          performMode = PerformMode.begin();
          println("B Button Pressed: Switching to macro " + controlMode.toString());
      }
    }
  }
  prevStateB = currStateB;
  
  boolean currStateX = xButton.pressed();
  if (!prevStateX) {
    if (currStateX) {
      switch (controlMode) {
        case WAVE_MACRO:
          controlMode = prevManualMode;
          returnPrevManPos();
          println("X Button Pressed: Switching back to " + controlMode.toString());
          break;
        default:
          if (!isMacro(controlMode)) {
            prevManualMode = controlMode;
            recordPrevManPos();
          }
          setAllPos(MAX_POS);
          pos1 = MIN_POS;
          pos4 = MIN_POS;
          controlMode = ControlMode.WAVE_MACRO;
          waveMode = WaveMode.begin();
          waveDelay = millis() + 5 * WAVE_MILLIS;
          println("X Button Pressed: Switching to macro " + controlMode.toString());
      }
    }
  }
  prevStateX = currStateX;
  
  switch (controlMode) {
    case PERFORM_MACRO:
      checkDPadH();
      break;
    default:
      checkDPadH();
      checkDPadV();
  }
  
 // assign our float value 
 //access the deviceroller.
 checkMacroInterrup();
 switch (controlMode) {
   case EXACT_POS:
     pos1 = (int)mapServoMinToMax(leftV);
     pos2 = (int)mapServoMinToMax(leftH);
     pos3 = MAX_POS + MIN_POS - (int)mapServoMinToMax(rightV);
     pos4 = (int)mapServoMinToMax(rightH);
     break;
   case STEP_POS:
     pos1 += (int)mapServoCenteredRange(leftV);
     pos2 += (int)mapServoCenteredRange(leftH);
     pos3 += -(int)mapServoCenteredRange(rightV);
     pos4 += (int)mapServoCenteredRange(rightH);
     break;
   case ROVE_MACRO_UP:
     if (lBrowLUp) pos1 += stickStepSens;
     else pos1 -= stickStepSens;
     if (pos1 >= MAX_POS || pos1 <= MIN_POS) lBrowLUp = !lBrowLUp;
     
     if (lBrowRUp) pos2 += stickStepSens;
     else pos2 -= stickStepSens;
     if (pos2 >= MAX_POS || pos2 <= MIN_POS) lBrowRUp = !lBrowRUp;
     
     if (rBrowRUp) pos3 += stickStepSens;
     else pos3 -= stickStepSens;
     if (pos3 >= MAX_POS || pos3 <= MIN_POS) rBrowRUp = !rBrowRUp;
     
     if (rBrowLUp) pos4 += stickStepSens;
     else pos4 -= stickStepSens;
     if (pos4 >= MAX_POS || pos4 <= MIN_POS) rBrowLUp = !rBrowLUp;
     
     if (jawUp) {
       pos5 += stickStepSens;
       pos6 -= stickStepSens;
     }
     else {
       pos5 -= stickStepSens;
       pos6 += stickStepSens;
     }
     if (pos5 >= MAX_POS || pos5 <= MIN_POS) jawUp = !jawUp;
     //if (pos1 < MAX_POS) {
     //  pos1 += stickStepSens;
     //  pos2 -= stickStepSens;
     //  pos3 -= stickStepSens;
     //  pos4 += stickStepSens;
     //}
     //else {
     //  pos5 = MID_POS - (MAX_POS - MIN_POS);
     //  pos6 = MID_POS + (MAX_POS - MIN_POS);
     //  controlMode = ControlMode.nextState(controlMode);
     //}
     break;
   //case ROVE_MACRO_DOWN:
   //  if (pos1 > MIN_POS) {
   //    pos1 -= stickStepSens;
   //    pos2 += stickStepSens;
   //    pos3 += stickStepSens;
   //    pos4 -= stickStepSens;
   //  }
   //  else {
   //    pos5 = MID_POS + (MAX_POS - MIN_POS);
   //    pos6 = MID_POS - (MAX_POS - MIN_POS);
   //    controlMode = ControlMode.nextState(controlMode);
   //  }
   //  break;
   case PERFORM_MACRO:
     runPerformMacro();
     break;
   case WAVE_MACRO:
     runWaveMacro();
     break;
 }
 
}

//~~~~~~~~~~~~~~~~~ Program Loop ~~~~~~~~~~~~~~~~~
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
void draw(){
 getUserInput();
 background(map(pos1, MIN_POS, MAX_POS, 0, 255),
           map(pos3, MIN_POS, MAX_POS, 0, 255),
           map(pos5, MIN_POS, MAX_POS, 0, 255));
 
 if (controlMode == ControlMode.PERFORM_MACRO) println("Before Check -- Position 5: " + pos5 + "\tPosition 6: " + pos6);
 pos1 = boundCheckInt(pos1, MAX_POS, MIN_POS);
 pos2 = boundCheckInt(pos2, MAX_POS, MIN_POS);
 pos3 = boundCheckInt(pos3, MAX_POS, MIN_POS);
 pos4 = boundCheckInt(pos4, MAX_POS, MIN_POS);
 pos5 = boundCheckInt(pos5, MAX_POS, MIN_POS);
 pos6 = boundCheckInt(pos6, MAX_POS, MIN_POS);
 if (controlMode == ControlMode.PERFORM_MACRO) println("Before Write -- Position 5: " + pos5 + "\tPosition 6: " + pos6);
 arduino.servoWrite(SERVO1_PIN, pos1);
 arduino.servoWrite(SERVO2_PIN, pos2);
 arduino.servoWrite(SERVO3_PIN, pos3);
 arduino.servoWrite(SERVO4_PIN, pos4);
 arduino.servoWrite(SERVO5_PIN, pos5);
 arduino.servoWrite(SERVO6_PIN, pos6);
 if (controlMode == ControlMode.PERFORM_MACRO) println("After Write  -- Position 5: " + pos5 + "\tPosition 6: " + pos6);
 if (controlMode == ControlMode.PERFORM_MACRO) println();
}

//~~~~~~~~~~~~~~~~~ Helper Functions ~~~~~~~~~~~~~~~~~
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//~~~~~~~~~~~~~~~~~ DPad Checks ~~~~~~~~~~~~~~~~~
void checkDPadH() {
  boolean currStateDPadH = dPad.left() || dPad.right();
  if (!prevStateDPadH) {
    if (currStateDPadH) {
      if (dPad.left()) {
        stickStepSens = boundCheckInt(stickStepSens - SENS_STEP, MAX_SENS, MIN_SENS);
        println("Stick Sensitivity: " + stickStepSens);
      }
      if (dPad.right()) {
        stickStepSens = boundCheckInt(stickStepSens + SENS_STEP, MAX_SENS, MIN_SENS);
        println("Stick Sensitivity: " + stickStepSens);
      }
    }
  }
  prevStateDPadH = currStateDPadH;
}

void checkDPadV() {
  boolean currStateDPadV = dPad.up() || dPad.down();
  if (!prevStateDPadV) {
    if (currStateDPadV) {
      int step = (MAX_POS - MIN_POS) / stickStepSens;
      if (dPad.up()) pos1 += step;
      if (dPad.down()) pos1 -= step;
    }
  }
  prevStateDPadV = currStateDPadV;
}

//~~~~~~~~~~~~~~~~~ isMacro Function ~~~~~~~~~~~~~~~~~
boolean isMacro(ControlMode currMode) {
  switch (currMode) {
    case ROVE_MACRO_UP:
    case ROVE_MACRO_DOWN:
    case PERFORM_MACRO:
    case WAVE_MACRO:
      return true;
    case EXACT_POS:
    case STEP_POS:
    default:
      return false;
  }
}

//~~~~~~~~~~~~~~~~~ Check Macro Interrupts ~~~~~~~~~~~~~~~~~
void checkMacroInterrup() {
  if (!isMacro(controlMode)) return;
  
  float tolerance = .25;
  if (controlMode != ControlMode.PERFORM_MACRO &&
      joysticksAboveTolerance(tolerance)) {
    println("Joystick Interrupt: Switching from " + controlMode.toString() +
            " to " + controlMode.STEP_POS.toString());
    controlMode = ControlMode.STEP_POS;
  }
}

boolean joysticksAboveTolerance(float tolerance) {
  float leftCheckV = leftV.getValue();
  float leftCheckH = leftH.getValue();
  float rightCheckV = rightV.getValue();
  float rightCheckH = rightH.getValue();
  
  
  return leftCheckV > tolerance || leftCheckV < -tolerance ||
         leftCheckH > tolerance || leftCheckH < -tolerance ||
         rightCheckV > tolerance || rightCheckV < -tolerance ||
         rightCheckH > tolerance || rightCheckH < -tolerance;
}

//~~~~~~~~~~~~~~~~~ Performance Macro State Switcher ~~~~~~~~~~~~~~~~~
void runPerformMacro() {
  final int OFFSET = 5;
  switch (performMode) {
  case START:
    performMode = PerformMode.nextState(performMode);
    println("START Set All");
    setAllPos(MIN_POS + OFFSET);
    pos1 = MID_POS + (MID_POS - pos1);
    pos2 = MID_POS + (MID_POS - pos2);
    performChangeMillis = millis() + performMode.getDuration();
    break;
  case ANGRY_1:
    if (millis() >= performChangeMillis) {
      performMode = PerformMode.nextState(performMode);
      println("ANGRY_1 Set All");
      setAllPos(MID_POS);
      performChangeMillis = millis() + performMode.getDuration();
    }
    break;
  case MID:
    if (millis() >= performChangeMillis) {
      performMode = PerformMode.nextState(performMode);
      println("MAX_POS Set All");
      setAllPos(MAX_POS - OFFSET);
      pos1 = MID_POS + (MID_POS - pos1);
      pos2 = MID_POS + (MID_POS - pos2);
      performChangeMillis = millis() + performMode.getDuration();
    }
    break;
  case SAD_1:
    if (millis() >= performChangeMillis) {
      performMode = PerformMode.nextState(performMode);
      println("SAD_1 Set All");
      setAllPos(MIN_POS + OFFSET);
      pos1 = MID_POS + (MID_POS - pos1);
      pos2 = MID_POS + (MID_POS - pos2);
      performChangeMillis = millis() + performMode.getDuration();
    }
    break;
  case WAIT_1:
    if (millis() >= performChangeMillis) {
      performMode = PerformMode.nextState(performMode);
    }
    break;
  case MAD_TO_SAD:
    if (pos3 >= MAX_POS - OFFSET) {
      performMode = PerformMode.nextState(performMode);
      performChangeMillis = millis() + performMode.getDuration();
    }
    else {
      incrementAllPos(stickStepSens);
      pos1 += -(2 * stickStepSens);
      pos2 += -(2 * stickStepSens);
    }
    break;
  case WAIT_2:
    if (millis() >= performChangeMillis) {
      performMode = PerformMode.nextState(performMode);
    }
    break;
  case SAD_TO_MAD:
    if (pos3 <= MIN_POS + OFFSET) {
      performMode = PerformMode.nextState(performMode);
      performChangeMillis = millis() + performMode.getDuration();
    }
    else {
      incrementAllPos(-stickStepSens);
        pos1 += 2 * stickStepSens;
        pos2 += 2 * stickStepSens;
    }
    break;
  case WAIT_3:
    if (millis() >= performChangeMillis) {
      performMode = PerformMode.nextState(performMode);
      setAllPos(MAX_POS - OFFSET);
      pos1 = MID_POS + (MID_POS - pos1);
      pos2 = MID_POS + (MID_POS - pos2);
      performChangeMillis = millis() + performMode.getDuration();
    }
    break;
  case SAD_2:
    if (millis() >= performChangeMillis) {
      performMode = PerformMode.nextState(performMode);
      setAllPos(MIN_POS + OFFSET);
      pos1 = MID_POS + (MID_POS - pos1);
      pos2 = MID_POS + (MID_POS - pos2);
      performChangeMillis = millis() + performMode.getDuration();
    }
    break;
  case ANGRY_2:
    if (millis() >= performChangeMillis) {
      performMode = PerformMode.nextState(performMode);
      performChangeMillis = millis() + performMode.getDuration();
    }
    break;
  case END:
    if (millis() >= performChangeMillis) {
      performMode = PerformMode.nextState(performMode);
      controlMode = prevManualMode;
      returnPrevManPos();
      println("Macro Finished: Switching back to " + controlMode.toString());
    }
    break;
  }
}

//~~~~~~~~~~~~~~~~~ Wave Macro State Switcher ~~~~~~~~~~~~~~~~~
void runWaveMacro() {
  switch (waveMode) {
  case START:
    if (millis() >= waveDelay) waveMode = WaveMode.nextState(waveMode);
    break;
  case UP_1:
    if (pos1 >= MAX_POS) waveMode = WaveMode.nextState(waveMode);
    else pos1 += stickStepSens;
    break;
  case UP_2:
    if (pos2 <= MIN_POS) waveMode = WaveMode.nextState(waveMode);
    else pos2 -= stickStepSens;
    break;
  case UP_3:
    if (pos4 >= MAX_POS) waveMode = WaveMode.nextState(waveMode);
    else pos4 += stickStepSens;
    break;
  case UP_4:
    if (pos3 <= MIN_POS) waveMode = WaveMode.nextState(waveMode);
    else pos3 -= stickStepSens;
    break;
  case UP_5:
    if (pos5 <= MIN_POS) waveMode = WaveMode.nextState(waveMode);
    else pos5 -= stickStepSens; pos6 -= -stickStepSens;
    break;
  case UP_6:
    waveMode = WaveMode.nextState(waveMode);
    waveDelay = millis() + WAVE_MILLIS * stickStepSens / 4;
    break;
  case DOWN_6:
    waveMode = WaveMode.nextState(waveMode);
    break;
  case DOWN_5:
    if (pos5 >= MAX_POS) waveMode = WaveMode.nextState(waveMode);
    else pos5 += stickStepSens; pos6 += -stickStepSens;
    break;
  case DOWN_4:
    if (pos3 >= MAX_POS) waveMode = WaveMode.nextState(waveMode);
    else pos3 += stickStepSens;
    break;
  case DOWN_3:
    if (pos4 <= MIN_POS) waveMode = WaveMode.nextState(waveMode);
    else pos4 -= stickStepSens;
    break;
  case DOWN_2:
    if (pos2 >= MAX_POS) waveMode = WaveMode.nextState(waveMode);
    else pos2 += stickStepSens;
    break;
  case DOWN_1:
    if (pos1 <= MIN_POS) {
      waveMode = WaveMode.nextState(waveMode);
      waveDelay = millis() + WAVE_MILLIS * stickStepSens / 4;
    }
    else pos1 -= stickStepSens;
    break;
  case END:
    if (millis() >= waveDelay) {
      waveMode = WaveMode.nextState(waveMode);
      controlMode = prevManualMode;
      returnPrevManPos();
      println("Macro Finished: Switching back to " + controlMode.toString());
    }
    break;
  }
}

//~~~~~~~~~~~~~~~~~ Map Function For Servo Position ~~~~~~~~~~~~~~~~~
float mapServoMinToMax(ControlSlider input) {
  return map(input.getValue(), -1, 1, MAX_POS, MIN_POS);
}

float mapServoCenteredRange(ControlSlider input) {
  return map(input.getValue(), -1, 1, stickStepSens, -stickStepSens);
}

//~~~~~~~~~~~~~~~~~ Functions for all Positions ~~~~~~~~~~~~~~~~~
void setAllPos(int pos) {
  pos1 = pos;
  pos2 = pos;
  pos3 = pos;
  pos4 = pos;
  pos5 = pos;
  pos6 = MAX_POS + MIN_POS - pos;
  println("After Set -- Position 5: " + pos5 + "\tPosition 6: " + pos6);
}

void incrementAllPos(int step) {
  pos1 += step;
  pos2 += step;
  pos3 += step;
  pos4 += step;
  pos5 += step;
  pos6 += -step;
}

void recordPrevManPos() {
  prevManualPos1 = pos1;
  prevManualPos2 = pos2;
  prevManualPos3 = pos3;
  prevManualPos4 = pos4;
  prevManualPos5 = pos5;
  prevManualPos6 = pos6;
}

void returnPrevManPos() {
  pos1 = prevManualPos1;
  pos2 = prevManualPos2;
  pos3 = prevManualPos3;
  pos4 = prevManualPos4;
  pos5 = prevManualPos5;
  pos6 = prevManualPos6;
}

//~~~~~~~~~~~~~~~~~ Bound Checker Functions ~~~~~~~~~~~~~~~~~
int boundCheckInt(int check, int max, int min) {
 if (check > max) check = max;
 if (check < min) check = min;
 return check;
}

float boundCheckFloat(float check, float max, float min) {
 if (check > max) check = max;
 if (check < min) check = min;
 return check;
}

//~~~~~~~~~~~~~~~~~ Display Initial Settings ~~~~~~~~~~~~~~~~~
void printSettings() {
  println("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~");
  println("Program Settings\n");
  println("Max Servo Position: " + MAX_POS);
  println("Middle Servo Position: " + MID_POS);
  println("Min Servo Position: " + MIN_POS);
  println("Control Mode: " + controlMode.toString());
  println("Sensitivity Step Increments: " + SENS_STEP);
  println("Max Sensitivity: " + MAX_SENS);
  println("Min Sensitivity: " + MIN_SENS);
  println("Stick Sensitivity: " + stickStepSens);
  println("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n");
}
