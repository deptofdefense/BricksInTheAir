# Narratives for people to follow

Subject to change but the thought here is to put in writing different scripts/narratives that could be followed so we can
prioritize the code that needs to be written.

## Background
Common across aviation is low level data protocols such as 1553 and 429. Those protocols were designed specifically for aviation
to be robust and travel longer distances and as such they are obscure and hardware to interact with them is more expensive.
Instead, we have chosen to interact/control our Lego kits through the more ubiquitous I2C protocol that is more readily available
and with an overall lower price point for introductory purposes. At an abstract layer 1553 and I2C have many similarities, for 
instance the both have:
 - concept of bus controller (1553) / master (I2C)
 - concept of receiver/transmitter (1553) / slave (I2C)
 - concept of selective addressing
 - limited bandwidth (1553 - ~1Mbs) / I2C (~100Khz)
 
Other similarities in the overall desing strategy:
 - Lego PF support different channels for addressing (i.e. channel 1-4 each with RED/BLUE drivers), quite common to have multiple 1553 buses (i.e. 1 to many) on an aircraft.


## Ideas

### Challenge #0 - Setup - difficulty easy
- Operator install appropriate drivers to interact with Bus Pirate/FT232H or both.
- Very that they can send a command to turn on/off a motor/light not necessarily connected to a kit.
- Offer them simplified I2C commands that show direct mapping to their setup.


### Challenge #1 - Turn the Engine Off - difficulty moderate
- Read through the Aircraft Configuration Manual to determine what devices are connected and how (i.e. which 
channel (1-4) and color matching (RED/BLUE) controls which components).
- Read through the Engine ICD/Lego ICD and source code to determine what command to send that will actually
turn the engine off. 
- Solution: using either the Bus Pirate in terminal mode or scripting using FT232H send the following command 
  (XXX i.e. [0xa8 0x53])
    - Unless the person scripted their answer in a tight loop the "hack" won't persist if overridden with a properly
    configured remote controller.
    
    
### Challenge #2 - Lower the Landing Gear - difficulty moderate
Similar to #1

### Challenge #3 - Lower the Cargo Door - difficulty moderate
Similar to #1


### Challenge #4 - Persist in keeping the landing gear down - difficulty hard
This solution should require scripting to be constantly sending the desired I2C command. This will in effect override the
remote control


### Challenge #5 - Pivot - difficutly moderate/hard
Have a unit (i.e. Mission Computer) that can accept changes to the channel that it needs to talk on to interact with various other units. Essentaially have an exploit/vulnerability in the device that accepts channel assignments and blindly forwards commands along in effect allowing complete control of the entire bus.
