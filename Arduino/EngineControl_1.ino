#include <PowerFunctions.h>
#include <Wire.h>

/**
 *  Project: Hack The "Airplane" - dds.mil
 *  Title: Engine Control Unit
 *  
 *  Purpose: To expose people to common low level protocols that mimic aviation protocols, specifically 
 *  using I2C as a correlation to 1553.
 *    
 *    
 *  @author Dan Allen
 *  @version 1.0 7/25/19
 *    
 *  Credits:
 *    https://github.com/jurriaan/Arduino-PowerFunctions *    
 */

#define ENGINE_I2C_ADDRESS 0x54
#define LegoPF 10
#define LegoChannel RED
#define GREEN_LED 3
#define YELLOW_LED 5
#define RED_LED 6
#define SERIAL_BAUD 9600

PowerFunctions pf(LegoPF, 0);   //Setup Lego Power functions pin

short volatile currentMode = 0;
short volatile pastMode = 0;
boolean modeChange = false;

/*
 * Setup method to handle I2C Wire setup, LED Pins and Serial output
 */
void setup() {
    
  Wire.begin(ENGINE_I2C_ADDRESS);
  Wire.onReceive(receiveEvent); // register event handler for recieve
  Wire.onRequest(requestEvent); // register event handler for request

  pinMode(GREEN_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  
  Serial.begin(SERIAL_BAUD);           // start serial for output debugging
  Serial.println("Main Engine Control Unit is online, ready for tasking");
  digitalWrite(GREEN_LED, HIGH);
  
}

/*
 * The main loop of execution for the Engine Control Unit
 */
void loop() {
  if(modeChange == true){   //process new mode of operation
    Serial.print("Mode change request to: 0x");
    Serial.println(currentMode, HEX);
    modeChange = false;

    //Handle the desired mode change
    switch(currentMode){
      case 1:
        Serial.println("Slow Speed 1");
        pf.single_pwm(LegoChannel, PWM_FWD1);
        break;
      case 2:
        Serial.println("Slow Speed 2");
        pf.single_pwm(LegoChannel, PWM_FWD2);
        break;
      case 3:
        Serial.println("Medium Speed 1");
        pf.single_pwm(LegoChannel, PWM_FWD3);
        break;
      case 4:
        Serial.println("Medium Speed 2");
        pf.single_pwm(LegoChannel, PWM_FWD4);
        break;
      case 5:
        Serial.println("Fast Speed 1");
        pf.single_pwm(LegoChannel, PWM_FWD5);
        break;
      case 6:
        Serial.println("Fast Speed 2");
        pf.single_pwm(LegoChannel, PWM_FWD6);
        break;
      case 7:
        if(pastMode == 6){
          Serial.println("Ludacrious Speed");
          pf.single_pwm(LegoChannel, PWM_FWD7);
        }
        break;
      case 0x53:
        if(pastMode <= 2){
          pf.single_pwm(RED, PWM_BRK);
          digitalWrite(GREEN_LED, LOW);
          digitalWrite(RED_LED, HIGH);
        }
        break;
      default:            
        break;
    }
    delay(100);
  }

  if(currentMode != 0x53){
    digitalWrite(GREEN_LED, HIGH);
    digitalWrite(RED_LED, LOW);
  }
  
}

/*
 * Event Handler for processing I2C commands when recieved at this address
 */
void receiveEvent()
{  
  while(Wire.available()){
    short x = (short) Wire.read();           // receive byte
    modeChange = true;
    pastMode = currentMode;
    currentMode = x;
  }  
}

/*
 * Event Handler for processing an I2C request command
 */
void requestEvent() {
  Wire.write(currentMode); // respond with currentMode of operation  
}
