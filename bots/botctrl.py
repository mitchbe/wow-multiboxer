#!/bin/python3

import sys,os
from time import sleep
#sys.path.append(os.getcwd() + '/../lib')
#sys.path.append(os.getcwd() + '/lib')
from util import * 


GLOBAL_COOLDOWN=1.6

class BotControl():
    def __init__(self, inputdev):
        self.input = inputdev

    # Move

    def turn_left(self):    self.input.keyhold("a", 0.5); 
    def turn_right(self):   self.input.keyhold("d", 0.5); 
    def walk_back(self):    self.input.keyhold("s", 0.7); 
    def walk_fwd(self):     self.input.keyhold("w", 0.7); 
    def stop(self):         self.input.keypress("s"); 
    def follow(self):       self.input.keypress("9"); 

    # Buff

    def eat(self):          self.input.keypress("minus"); 
    def drink(self):        self.input.keypress("equal"); 

    def buff_group(self, nr):     
        self.input.keypress("F1 6"); 
        if (nr > 1) : 
            sleep(GLOBAL_COOLDOWN)
            self.input.keypress("F2 6"); 
        if (nr > 2) : 
            sleep(GLOBAL_COOLDOWN)
            self.input.keypress("F3 6"); 
        if (nr > 3) : 
            sleep(GLOBAL_COOLDOWN)
            self.input.keypress("F4 6"); 
        if (nr > 4) : 
            sleep(GLOBAL_COOLDOWN)
            self.input.keypress("F5 6"); 
        sleep(GLOBAL_COOLDOWN)
            
    # Potions

    def potion_health(self):   self.input.keypress("Ctrl+minus"); 
    def potion_mana(self):     self.input.keypress("Ctrl+equal"); 


class WarlockControl(BotControl):
    def __init__(self, inputdev):
        super(WarlockControl, self).__init__(inputdev)

    # Spells
    def main_target_corruption(self):
        self.input.keypress("F2 f 2");
        sleep(GLOBAL_COOLDOWN)

    def main_target_curse_agony(self):
        self.input.keypress("F2 f 3");
        sleep(GLOBAL_COOLDOWN)

    def main_target_immolate(self):
        self.input.keypress("F2 f 4");
        sleep(2.1)

    def main_target_shadowbolt(self):
        self.input.keypress("F2 f 5");
        sleep(2.3)

    def main_target_drain_soul(self):
        self.input.keypress("F2 f 7");
        sleep(GLOBAL_COOLDOWN)

    def buff_self(self):     
        self.input.keypress("F1 6"); 
        sleep(GLOBAL_COOLDOWN)

    def buff_group(self, nr):     
        raise NotImplementedError("bad call")


class MageControl(BotControl):
    def __init__(self, inputdev):
        super(MageControl, self).__init__(inputdev)
        #self.last_fireblast = 0

    # Spells
    def main_target_fireblast(self):
        #cooldown_ms = 8100
        #now = TimeUtil.get_time_ms()
        #if (now - cooldown_ms > self.last_fireblast) :
        #    self.last_fireblast = now
        self.input.keypress("F2 f 3");
        sleep(1)

    def main_target_fireball(self):
        self.input.keypress("F2 f 2");
        sleep(2.1)

    def main_target_frostbolt(self):
        self.input.keypress("F2 f 1");
        sleep(2)

    def main_target_arcane_missiles(self):
        self.input.keypress("F2 f 4");
        sleep(3.1)

    def buff_group(self, nr):     
        self.input.keypress("Ctrl+6"); 
        sleep(GLOBAL_COOLDOWN)
        super(MageControl, self).buff_group(nr)


class PriestControl(BotControl):
    def __init__(self, inputdev):
        super(PriestControl, self).__init__(inputdev)
        self.last_HoT = 0
        self.last_H = 0

    # Healing

    def main_heal_over_time(self):   
        cooldown = 15000
        now = TimeUtil.get_time_ms()
        if (now - cooldown > self.last_HoT) :
            self.last_HoT = now
            self.input.keypress("F2 4"); 
            sleep(GLOBAL_COOLDOWN)

    def main_heal_small(self):       self.input.keypress("F1 5"); 

    def main_heal_medium(self):      
        self.input.keypress("F2 5"); 
        sleep(2.55)
        '''
        cooldown = 2500
        now = TimeUtil.get_time_ms()
        if (now - cooldown > self.last_H) :
            self.last_H = now
            self.input.keypress("F2 5"); 
        '''

    def main_heal_big(self):         self.input.keypress("F1 5"); 

    def main_shield(self):          
        self.input.keypress("F2 Ctrl+6");
        sleep(GLOBAL_COOLDOWN)

    def main_target_wand(self):     
        self.input.keypress("F2 f 0");

    def main_target_dot(self):     
        self.input.keypress("F2 f 2");
        sleep(GLOBAL_COOLDOWN)

