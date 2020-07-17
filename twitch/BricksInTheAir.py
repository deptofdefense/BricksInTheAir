# Code for managing the game part of cpx simpleSat
# Created for defcon28 aerospace village

import threading    # needed for threading
import time         # needed for sleep
import struct       # needed for serial
import random       # used for selection of sound effects

import serial   # needed for serial
import pygame   # used for playing audio sound effects
import os
import math     # used for math.inf for non hex provided numbers
import binascii


class BricksInTheAir:
    ''' Used to manage progressing through the cpx simple sat game '''

    def __init__(self, CFG):

        self.cfg = CFG

        i2c_device = self.cfg["hardware"]["i2c"]
        i2c_value = self.cfg["hardware"]["value"]
        i2c_frequency = self.cfg["hardware"]["frequency"]

        # board modue needs this variable set
        os.environ[i2c_device] = str(i2c_value)

        # with ^^ the os env set we can now import busio
        import board
        import busio

        self.fcc_address = self.cfg["hardware"]["fcc_address"]
        self.engine_address = self.cfg["hardware"]["engine_address"]
        self.gear_address = self.cfg["hardware"]["gear_address"]

        self.i2c = busio.I2C(board.SCL, board.SDA, frequency=i2c_frequency)

        # Verify that everything is communicating as expected
        avail = self.i2c.scan()
        print("fcc_address present: {}".format("True" if self.fcc_address in avail else "False"))
        print("engine_address present: {}".format("True" if self.engine_address in avail else "False"))
        print("gear_address present: {}".format("True" if self.gear_address in avail else "False"))

        # configure the audio sound effect outputs
        pygame.mixer.init(channels=2)
        pygame.init()
        self.background_channel = pygame.mixer.Channel(0)
        self.effect_channel = pygame.mixer.Channel(1)

        try:
            bg_audio_loop = pygame.mixer.Sound(self.cfg["audio"]["background"])
            self.background_channel.play(bg_audio_loop, loops=-1)
        except FileNotFoundError as err:
            print("background audio: file not found")

    def checkCmd(self, user, cmd):
        """
        Checks the user command and passes to the appropriate function
        """

        # run prologoue for this specific step
        self.run_prolouge(user)


        passed_step = user.checkAnswer(cmd)
        if passed_step == True:
            # limitations to VR and time to build, some answers just need to be faked
            # allow the config file to guide the gameplay.
            response = ""
            if user.getFakeI2CResponse() != None:
                 response = user.getFakeI2CResponse()
            else:
                # do the stuff to indicate complete
                response = "0x" + self.process_cmd(user, cmd)[2:-1]

            user.incrementCurrentStepIndex()

            return "\n\nI2C Response: " + response + "\n\nCongratulations, you've completed this step.\n"\
                            "\n\nNext Question: " + user.getQuestion()

        else:
            # nothing to do here?
            # response = self.process_cmd(user, cmd)
            return "Incorrect cmd sent for the current question."


    def process_cmd(self, user, cmd):
        # Need to send i2c, change scene, provide sound effect
        x = cmd.split()
        addr = str_to_hex(x[0])
        payload = []
        for i in range(1, len(x)):
            payload.append(str_to_hex(x[i]))

        print(hex(addr))
        for x in payload:
            print(hex(x))

        response = None
        response = self.write_read_i2c(addr, payload, 1)
        print(binascii.hexlify(response))


        # handle the possible sound effect
        sound_effect_str = user.getAudio()
        if(sound_effect_str):
            try:
                effect = pygame.mixer.Sound(sound_effect_str)
                self.background_channel.set_volume(.4)
                # restore the background audio AFTER the effect has completed
                threading.Thread(target=self.restore_background_volume, args=(effect.get_length(),), daemon=True).start()

                self.effect_channel.play(effect)
            except FileNotFoundError as err:
                print("sound effect: file not found")

        # handle the possible scene change

        return str(binascii.hexlify(response))

    def restore_background_volume(self, delay):
        # Simple function to restore the background volume AFTER a delay
        time.sleep(delay)
        self.background_channel.set_volume(1)


    def write_read_i2c(self, address, command, buf_size=1):

        self.i2c.writeto(address, command)
        buf = None
        #print("wrote to address: 0x{:x}, value: {}".format(address, command))
        if buf_size > 0:
            buf = bytearray(buf_size)
            self.i2c.readfrom_into(address, buf)

        return buf

    def reset(self, user):

        #print("Calling brick reset")
        #time.sleep(.1)
        self.write_read_i2c(self.fcc_address, [0xFE])
        time.sleep(.1)


    def run_prolouge(self, user):
        prologue = user.get_prologue()
        #print(prologue)
        if prologue != None:
            for i2c_command in prologue:
                tmp_command = i2c_command.split()
                tmp = []
                for x in tmp_command:
                    tmp.append(str_to_hex(x))
                self.write_read_i2c(tmp[0], tmp[1:])



def str_to_hex(hex_str):
    try:
        return int(hex_str, 16)
    except ValueError:
        return math.inf
