#!/usr/bin/env

"""
Installation requirements:

```
sudo apt-get install libbluetooth-dev
python3 -m pip install pybluex
```

"""

from bluetooth import *
import time
import argparse
import sys

class LegoSpike:
    """
    Class to handle the Bluetooth rfcomm connection bits to Lego Spike hub

    This intent is search for locally available bluetooth Lego Hubs
    and if found return a list of viable addresses.

    Upon knowing the desired address to connect to, the constructor can
    then be called and will then attempt the following:
        1. establish a bluetooth connection
        2. send initial commands (CTRL+C & CTRL+B) to stop the program currently
        running on the hub and put the device into normal REPL mode.
        3. Send the requisite "import hub" command
        4. Wait for subsequent calls as issued by any other method.
    """

    def __init__(self, addr):
        """
        Basic constructor.

        Parameters:
        addr (str): the hexadecimal format of the hub address
        """

        self.buf_size = 1024
        self.addr = addr

        try:
            self.conn = BluetoothSocket(RFCOMM)
            self.conn.connect((self.addr, 1))
            #self.conn.recv(self.buf_size)
            # Send the a sequence of CTRL+comds to enter normal REPL mode
            self.conn.send("\x03\x02".encode())

            time.sleep(1)
            self.conn.send("\x02".encode())
            self.conn.send("\r\n\r\n".encode())
            #self.conn.recv(self.buf_size)
            self.run_spike_command("import hub")
        except Exception as err:
            print(repr(err))
            sys.exit(1)

    def search_for_hub():
        """
        Search for nearby Lego Hubs and return a list of hubs found.
        """
        nearby_devices = discover_devices(lookup_names=True)

        lego_hub_addr = []
        for found_addr, name in nearby_devices:
            if "lego" in name.lower():
                lego_hub_addr.append(found_addr)
        return lego_hub_addr

    def run_spike_command(self, cmd):
        """
        Allow to send raw commands straight to the interactive shell on the hub.
        """
        self.conn.send(cmd + "\r\n")
        return self.conn.recv(self.buf_size)


    def close_connection(self):
        """Close the Lego Spike BLE connection"""
        self.conn.close()


    def run_at_speed(self, motor, speed):
        """Directly call the Lego motor.run_at_speed()

        Parameters:
        motor (chr): the motor port (i.e. A, B, C, D, E, F)
        speed (int): a valid speed, -100 to 100 or 127
        """
        # Run the motor port at a speed
        self.run_spike_command("hub.port." + str(motor) +
                               ".motor.run_at_speed("+str(speed)+")")

    def break_dance(self, duration):
        """
        Silly method to make the Lego break Dance kit dance.

        Parameters:
        duration (int): the duration the dance should occur for.
        """
        for i in range(11):
            self.run_at_speed("F", i*10)
            self.run_at_speed("D", -1*i*10)
            time.sleep(.3)

        time.sleep(duration)

        for i in range(10, -1, -1):
            self.run_at_speed("F", i*10)
            self.run_at_speed("D", -1*i*10)
            time.sleep(.3)

def main():
    parser = argparse.ArgumentParser(description="Interact with a Lego Spike Hub. "\
                                     "Without an known address provided the module "\
                                     "will search for nearby Lego Spike Hubs.")
    parser.add_argument('--addr', help='the address of a known Lego Hub.')
    args = parser.parse_args()

    if args.addr is not None:
        spike = LegoSpike(args.addr)
        spike.break_dance(5)
        spike.close_connection()

    else:
        avail_addr = LegoSpike.search_for_hub()
        print(avail_addr)


if __name__ == "__main__":
    main()
