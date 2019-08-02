#include <PowerFunctions.h>
#include <Wire.h>
#include <CircularBuffer.h>

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

/*
 * General Config Definitions
 */
#define ENGINE_I2C_ADDRESS 0x54
#define LegoChannel RED
#define SERIAL_BAUD 9600
#define I2C_RX_BUFFER_SIZE 50
#define I2C_TX_BUFFER_SIZE 50

/*
 * Pin Definitions
 */
#define GREEN_LED 3
#define YELLOW_LED 5
#define RED_LED 6
#define LEGO_PF_PIN 10

/*
 * LED State Machine Definitions
 */
#define OFF 0x00
#define ON  0x01
#define DC  0x10


/*
 * I2C Comms Definitions
 */
//Commands
#define GET_ENGINE_STATUS 0x22
#define SET_ENGINE_SPEED  0x23

//Response
#define UNKNOWN_COMMAND   0x33
#define NO_DATA           0xFF

/*
 * Library Instantiations
 */
PowerFunctions pf(LEGO_PF_PIN, 0);   //Setup Lego Power functions pin


/*
 * Globals
 */
short volatile currentMode = 0;
short volatile pastMode = 0;
boolean modeChange = false;
CircularBuffer<short,I2C_RX_BUFFER_SIZE> g_i2c_rx_buffer;
CircularBuffer<short,I2C_TX_BUFFER_SIZE> g_i2c_tx_buffer;

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
  set_led(ON, OFF, OFF);
  
}

/*
 * The main loop of execution for the Engine Control Unit
 */
void loop() {
  service_ir_comms();
  process_i2c_request();
}


/*
 * Set's LED State
 * 0x00 = OFF = LED off
 * 0x01 = ON = LED on
 * 0x10 = DC = Don't change the state
 */
void set_led(short g, short y, short r) {
  switch(g) {
    case 0x00:
      digitalWrite(GREEN_LED, LOW);
      break;

    case 0x01:
      digitalWrite(GREEN_LED, HIGH);
      break;
  }

  switch(y){
    case 0x00:
      digitalWrite(YELLOW_LED, LOW);
      break;

    case 0x01:
      digitalWrite(YELLOW_LED, HIGH);
      break;
  }

  switch(r) {
    case 0x00:
      digitalWrite(RED_LED, LOW);
      break;

    case 0x01:
      digitalWrite(RED_LED, HIGH);
      break;
  }
}

/*
 * Manages IR comms interface
 */
void service_ir_comms() {
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
    set_led(ON,ON,DC);
  }
}



/*
 * generate the imediate response needed as fast as possible
 */
void process_i2c_request(void) {
  short command_temp;
  if(g_i2c_rx_buffer.isEmpty() != true) {
    //clear any unsent responses
    g_i2c_tx_buffer.clear();
    //read command and pull it out of the buffer
    command_temp = g_i2c_rx_buffer.shift();
    switch(command_temp){
      case GET_ENGINE_STATUS:
        Serial.println("Command Received, GET_ENGINE_STATUS");
        g_i2c_tx_buffer.push(currentMode);
        break;
  
      case SET_ENGINE_SPEED:
        Serial.print("Command Received, SET_ENGINE_SPEED : ");
        pastMode = currentMode;
        currentMode = g_i2c_rx_buffer.shift();
        modeChange = true;
        Serial.println(currentMode, HEX);
        //Note, there should be some sanitization here, but maybe not for hacking comp?
        break;
  
      default:
        Serial.print("Received unknown command: ");
        Serial.println(command_temp);
        g_i2c_tx_buffer.push(UNKNOWN_COMMAND);
    }
    g_i2c_rx_buffer.clear(); //flush buffer after processing  
  }
}


/*
 * Event Handler for processing I2C commands sent to this device
 * NOTE: I don't like accessing the response in this inturrupt,
 * but I2C needs an imeediate response.
 */
void receiveEvent()
{  
  while(Wire.available()){
    g_i2c_rx_buffer.push((short) Wire.read());
  }
  process_i2c_request();
}

/*
 * Event Handler for processing an I2C request for data
 */
void requestEvent() {
  if(g_i2c_tx_buffer.isEmpty() != true) {
    while(g_i2c_tx_buffer.isEmpty() != true) {
      Wire.write(g_i2c_tx_buffer.shift());
    }
  }
  else {
    Wire.write(NO_DATA); // Out of data, respond with NO DATA
  }
}

/*
 * DEBUG ONLY
 * print rx receive buffer
 */
void dbg_print_rx_buffer(void) {
  int i;
  if(g_i2c_rx_buffer.isEmpty() != true) {
    for(i=0; i< g_i2c_rx_buffer.size() - 1; i++) {
      Serial.print(g_i2c_rx_buffer[i], HEX);
      Serial.print(" ");
    }
    Serial.println("Done");
  }
  else {
    Serial.println("Buffer Empty");
  }
}

/*
 * DELETE ME: 
 * Manages I2C comms interface
 */
void service_i2c_comms(void) {
  if(g_i2c_rx_buffer.isEmpty() != true) {
    modeChange = true;
    pastMode = currentMode;
    currentMode = g_i2c_rx_buffer.shift();
    Serial.println(currentMode);
    g_i2c_tx_buffer.push(currentMode);
  }
}
