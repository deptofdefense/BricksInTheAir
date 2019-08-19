# [DDS](https://www.dds.mil) Bricks in the Air

Hack the Plane with [Legos](https://www.lego.com/en-us) and [Arduinos](https://www.arduino.cc/)!

This challenge was developed for Defcon27 in the Aviation Village. The concept is to create an environment that requires similar approaches to hacking actual aviation buses without using any of the real hardware, protocols, or commands. Challengers can freely play and develop skills without worrying about legalities or sensitivities of real systems. This also makes it much cheaper and easier for people to replicate. 

## Lego Kits
Pictures of the kits are contained below but chekc out the [LegoKits](https://github.com/deptofdefense/hackThePlane/tree/master/LegoKIts) page for more info on each kit.

[LEGO Jet 42066](https://www.amazon.com/LEGO-Technic-Race-42066-Building/dp/B072MHYCYZ/ref=asc_df_B072MHYCYZ/?tag=hyprod-20&linkCode=df0&hvadid=312131879690&hvpos=1o3&hvnetw=g&hvrand=1663373337932599929&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9058761&hvtargid=pla-567522045562&psc=1)
<img src="https://images.brickset.com/sets/images/42066-1.jpg?201611300919" width="300">

---

[LEGO Plane 42025](https://www.amazon.com/Lego-42025-Technic-Cargo-Plane/dp/B00F3B48YA/ref=asc_df_B00F3B48YA/?tag=hyprod-20&linkCode=df0&hvadid=312131879690&hvpos=1o2&hvnetw=g&hvrand=1663373337932599929&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9058761&hvtargid=pla-440286468189&psc=1 )
<img src="https://images.brickset.com/sets/images/42025-1.jpg?201311210338" width="300">

---

[LEGO Helicopter 42052](https://www.amazon.com/LEGO-Technic-Helicopter-Advanced-Building/dp/B01E78WKEO/ref=asc_df_B01E78WKEO/?tag=hyprod-20&linkCode=df0&hvadid=312143210575&hvpos=1o2&hvnetw=g&hvrand=8773246636342787586&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9058761&hvtargid=pla-572282343772&psc=1 )
<img src="https://images.brickset.com/sets/images/42052-1.jpg?201601050913" width="300">

---

[LEGO Power Functions IR Receiver (8884)](https://www.amazon.com/LEGO-Functions-Power-IR-8884/dp/B00440E2GK/ref=sr_1_1?keywords=lego+power+functions+IR&qid=1565984821&s=toys-and-games&sr=1-1 )
<img src="https://images.brickset.com/sets/images/8884-1.jpg?200712260710" width="300">

---

[LEGO Power Functions IR Remote (8879)](https://www.amazon.com/LEGO-Functions-Control-Discontinued-manufacturer/dp/B003FOA2VK/ref=sr_1_4?keywords=lego+power+functions+IR+remote&qid=1565985000&s=toys-and-games&sr=1-4 )
<img src="https://images.brickset.com/sets/large/8879-1.jpg?200903300421" width="300">


We added the LEGO Power Functions IR Receivers to control the motors in the models. These receivers have 4 IR manually selectable channels and two (Red and Blue) data ports that can be used at the same time. The IR receiver also provides PWM to motors and lights connected to it. I recommend picking up the kit which includes the battery pack, motor, LED’s and a hand full of extras. The LEGO Power Functions IR Remote was also a huge help in testing and setup. 

## PCB
The PCB was designed in KiCad, a cross platform, open source, electronics design suite. 
[KiCad](http://www.kicad-pcb.org/ )

The board is basically three ATMEGA chips running the Arduino stack, each with their own IR, Serial, and programming ports. They are all connected to the same I2C bus. The original intent was to have three different systems, say engine, landing gear, and other accessories, being controlled by different chips. The challenge as it was run has the same code on all three and only worked with the original single motor in each model. We ran out of time to expand it. 

It is worth noting that an Arduino Uno with an IR LED and resistor connected to it will work as well. 

## I2C
We used the Bus Pirate to interface with the Arduino over I2C.

[Bus Pirate](http://dangerousprototypes.com/docs/Bus_Pirate)

Why? 
Well on several actual avionics buses, the system is set up on a bus much like I2C where you have a master and several slaves. Once you have physical access, you are a trusted device that does not need authentication. I2C fits a lot of these characteristics using widely available cheap hardware. This allows us to provide an environments that stays true to the nature of the challenge while avoiding legal issues. The skills learned here is also applicable to other I2C buses which are popular in consumer embedded electronics. 

## Documentation
The FlySafe Developers guide is also included which describes the details needed to get started with the control protocol the challenge was using. This guide is intended to be handed out to people tackling the challenge. 

## Smoker (fog machine)
What about the smoker?! 
Well, the smoker was a last minute add-in that was hacked together using an air pump, and esig, an 18650 Lithium Ion cell and some creative circuitry. It basically used the Red port on the LEGO IR receiver to turn a FET on for 10 seconds, which activated the cartridge and pump.

Our Electrical Engineer was on site to keep on eye on everything during the competition but the design is not ready for prime time. Additional safety features to prevent overheating and the system from getting stuck into the ON state should be added. 

If you want to take a stab at making your own setup (at your own risk) here are a couple of links to get you started.

[Pump](https://www.amazon.com/DIMINUS-Replacement-Accessories-Aquarium-Circulate/dp/B06ZXW7Z1P)

[eCig Ceramic Cartridge](https://www.amazon.com/Ceramic-Wickless-Cartridge-AC-1003-Acessaries/dp/B07SMRZZMY/ref=sr_1_1?keywords=5+pack+1ml+ceramic+ac1003&qid=1566240299&s=hi&sr=8-1)


Thank you to all that participated in the challenge and I hope you all have fun with this challenge!

