# Copyright 2019 Amazon.com, Inc. or its affiliates.  All Rights Reserved.
# 
# You may not use this file except in compliance with the terms and conditions 
# set forth in the accompanying LICENSE.TXT file.
#
# THESE MATERIALS ARE PROVIDED ON AN "AS IS" BASIS. AMAZON SPECIFICALLY DISCLAIMS, WITH 
# RESPECT TO THESE MATERIALS, ALL WARRANTIES, EXPRESS, IMPLIED, OR STATUTORY, INCLUDING 
# THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.

import time
import logging
import json
import random
import threading
from collections import Counter

import math
#from ev3dev2.sound import Sound 

from enum import Enum
from agt import AlexaGadget

from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, MoveTank, SpeedPercent, MediumMotor

# Set the logging level to INFO to see messages from AlexaGadget
logging.basicConfig(level=logging.INFO)


class Direction(Enum):
    """
    The list of directional commands and their variations.
    These variations correspond to the skill slot values.
    """
    FORWARD = ['forward', 'forwards', 'go forward']
    BACKWARD = ['back', 'backward', 'go backward']
    LEFT = ['left', 'go left']
    RIGHT = ['right', 'go right']
    STOP = ['stop', 'brake']


class Command(Enum):
    """
    The list of preset commands and their invocation variation.
    These variations correspond to the skill slot values.
    """
    MOVE_CIRCLE = ['circle', 'spin']
    MOVE_SQUARE = ['square']
    PATROL = ['patrol', 'guard mode', 'sentry mode']
    FIRE_ONE = ['cannon', '1 shot', 'one shot']
    FIRE_ALL = ['all shot']


class MindstormsGadget(AlexaGadget):
    """
    A Mindstorms gadget that performs movement based on voice commands.
    Two types of commands are supported, directional movement and preset.
    """

    def __init__(self):
        """
        Performs Alexa Gadget initialization routines and ev3dev resource allocation.
        """
        super().__init__()

        # Gadget state
        self.patrol_mode = False

        # Ev3dev initialization
        self.leds = Leds()
        self.sound = Sound()
        #self.drive = MoveTank(OUTPUT_B, OUTPUT_C)
        #self.weapon = MediumMotor(OUTPUT_A)

        # Start threads
        threading.Thread(target=self._patrol_thread, daemon=True).start()

    def on_connected(self, device_addr):
        """
        Gadget connected to the paired Echo device.
        :param device_addr: the address of the device we connected to
        """
        self.leds.set_color("LEFT", "GREEN")
        self.leds.set_color("RIGHT", "GREEN")
        strSpeak  = "I am ready"
        self.sound.speak(strSpeak)
        print("{} connected to Echo device".format(self.friendly_name))

    def on_disconnected(self, device_addr):
        """
        Gadget disconnected from the paired Echo device.
        :param device_addr: the address of the device we disconnected from
        """
        self.leds.set_color("LEFT", "BLACK")
        self.leds.set_color("RIGHT", "BLACK")
        print("{} disconnected from Echo device".format(self.friendly_name))

    def on_custom_mindstorms_gadget_control(self, directive):
        """
        Handles the Custom.Mindstorms.Gadget control directive.
        :param directive: the custom directive with the matching namespace and name
        """
        try:
            payload = json.loads(directive.payload.decode("utf-8"))
            print("Control payload: {}".format(payload))
            control_type = payload["type"]
            if control_type == "move":

                # Expected params: [direction, duration, speed]
                self._move(payload["direction"], int(payload["duration"]), int(payload["speed"]))

            if control_type == "command":
                # Expected params: [command]
                self._activate(payload["command"],[payload['one'],payload['two']])

        except KeyError:
            print("Missing expected parameters: {}".format(directive))

    def _move(self, direction, duration: int, speed: int, is_blocking=False):
        """
        Handles move commands from the directive.
        Right and left movement can under or over turn depending on the surface type.
        :param direction: the move direction
        :param duration: the duration in seconds
        :param speed: the speed percentage as an integer
        :param is_blocking: if set, motor run until duration expired before accepting another command
        """
        strSpeak = "Move command: ({}, {}, {}, {})".format(direction, speed, duration, is_blocking)
        print(strSpeak)
        self.sound.speak(strSpeak)
        if direction in Direction.FORWARD.value:
            self.drive.on_for_seconds(SpeedPercent(speed), SpeedPercent(speed), duration, block=is_blocking)

        if direction in Direction.BACKWARD.value:
            self.drive.on_for_seconds(SpeedPercent(-speed), SpeedPercent(-speed), duration, block=is_blocking)

        if direction in (Direction.RIGHT.value + Direction.LEFT.value):
            self._turn(direction, speed)
            self.drive.on_for_seconds(SpeedPercent(speed), SpeedPercent(speed), duration, block=is_blocking)

        if direction in Direction.STOP.value:
            self.drive.off()
            self.patrol_mode = False
            
    # A function to print all prime factors of 
    # a given number n 
    def primeFactors(self,n): 
        factors = list()

        # Print the number of two's that divide n 
        while n % 2 == 0: 
            print (2), 
            factors.append(2)
            n = n / 2

        # n must be odd at this point 
        # so a skip of 2 ( i = i + 2) can be used 
        for i in range(3,int(math.sqrt(n))+1,2): 

            # while i divides n , print i ad divide n 
            while n % i== 0: 
                print (i),
                factors.append(i)
                n = n / i 
    
        # Condition if n is a prime 
        # number greater than 2 
        if n > 2: 
            print (n )
            factors.append(n)

        return factors

    def speakmath(self,primes):
      strOut = ""
      for key in primes.keys():
        if strOut != "": strOut += " and "
        print (key, primes[key])
        if primes[key] == 1:

          strAdd = str(key)
        else:
          strAdd = str(key)+" to the power of "+str(primes[key])
        strOut += strAdd

      return strOut


    def _activate(self, command, speed=50):
        """
        Handles preset commands.
        :param command: the preset command
        :param speed: the speed if applicable
        """
        strSpeak = "Activate command: ({}, {})".format(command, speed)
        print(strSpeak)
        #self.sound.speak(strSpeak)
        if command in Command.MOVE_CIRCLE.value:
            self.drive.on_for_seconds(SpeedPercent(int(speed)), SpeedPercent(5), 12)

        if command in Command.MOVE_SQUARE.value:
            for i in range(4):
                self._move("right", 2, speed, is_blocking=True)

        if command in Command.PATROL.value:
            # Set patrol mode to resume patrol thread processing
            self.patrol_mode = True

 g       if command in Command.FIRE_ONE.value:
            self.weapon.on_for_rotations(SpeedPercent(100), 3)

        if command in Command.FIRE_ALL.value:
            self.weapon.on_for_rotations(SpeedPercent(100), 10)


        if command in ['add']:
          strSpeak = "Doing math, adding " + speed[0] + " and " + speed[1] + " is " + str(int(speed[0])+int(speed[1]))
          self.sound.speak(strSpeak)
          
        if command in ['primefactors']:
          factors = self.primeFactors(int(speed[0]) )
          primes  = Counter(factors)
          strMath = self.speakmath(primes)
          
          strSpeak = "Prime factors for " + speed[0] + " are " + strMath
          self.sound.speak(strSpeak)



       



# This code is contributed by Harshit Agrawal 



    def _turn(self, direction, speed):
        """
        Turns based on the specified direction and speed.
        Calibrated for hard smooth surface.
        :param direction: the turn direction
        :param speed: the turn speed
        """
        if direction in Direction.LEFT.value:
            self.drive.on_for_seconds(SpeedPercent(0), SpeedPercent(speed), 2)

        if direction in Direction.RIGHT.value:
            self.drive.on_for_seconds(SpeedPercent(speed), SpeedPercent(0), 2)

    def _patrol_thread(self):
        """
        Performs random movement when patrol mode is activated.
        """
        while True:
            while self.patrol_mode:
                print("Patrol mode activated randomly picks a path")
                direction = random.choice(list(Direction))
                duration = random.randint(1, 5)
                speed = random.randint(1, 4) * 25

                while direction == Direction.STOP:
                    direction = random.choice(list(Direction))

                # direction: all except stop, duration: 1-5s, speed: 25, 50, 75, 100
                self._move(direction.value[0], duration, speed)
                time.sleep(duration)
            time.sleep(1)


if __name__ == '__main__':

    # Startup sequence
    gadget = MindstormsGadget()
    gadget.sound.play_song((('C4', 'e'), ('D4', 'e'), ('E5', 'q')))
    gadget.leds.set_color("LEFT", "GREEN")
    gadget.leds.set_color("RIGHT", "GREEN")

    # Gadget main entry point
    gadget.main()

    # Shutdown sequence
    gadget.sound.play_song((('E5', 'e'), ('C4', 'e')))
    gadget.leds.set_color("LEFT", "BLACK")
    gadget.leds.set_color("RIGHT", "BLACK")
