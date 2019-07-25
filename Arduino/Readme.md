# Arduino Files

Basic functional board setup:
  - 3 ATmega328/Arduinos interconnected through I2C.
  - Each Arduino has 
    - 3 LEDs for discrete signals
      - Green LED - Digital Pin 3 (PD3)
      - Yellow LED - Digital Pin 5 (PD5)
      - Red LED - Digital Pin 6 (PD6)
    - 1 IR LED for interaction/driving the Lego Power function IR. - Digital Pin 10 (PB2)
    - Serial RX on Digital Pin 0 (PD0)
    - Serial TX on Digital Pin 1 (PD1)
    - I2C connectivity via standard SDA(PC4)/SCL(PC5) Pins
  
  
  
