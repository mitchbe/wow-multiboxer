#!/bin/python3

import sys,os
from time import sleep
#sys.path.append(os.getcwd() + '/../lib')
#sys.path.append(os.getcwd() + '/lib')
from util import * 


GLOBAL_COOLDOWN=1.6
BUFF_COOLDOWN=1.8

class BotControl():
    def __init__(self, inputdev):
        self.input = inputdev

    # Move

    def turn_left(self):    self.input.keyhold("a", 0.25); 
    def turn_right(self):   self.input.keyhold("d", 0.25); 
    def walk_bwd(self):     self.input.keyhold("s", 0.7); 
    def walk_fwd(self):     self.input.keyhold("w", 0.7); 
    def stop(self):         self.input.keypress("s"); 
    def follow(self):       self.input.keypress("9"); 

    # Buff

    def eat(self):          
        print("cast Eat")
        self.input.keypress("minus"); 

    def drink(self):        
        print("cast Drink")
        self.input.keypress("equal"); 

    def buff_group(self, nr):     
        self.input.keypress("F1 6"); 
        if (nr > 1) : 
            sleep(BUFF_COOLDOWN)
            self.input.keypress("F2 6"); 
        if (nr > 2) : 
            sleep(BUFF_COOLDOWN)
            self.input.keypress("F3 6"); 
        if (nr > 3) : 
            sleep(BUFF_COOLDOWN)
            self.input.keypress("F4 6"); 
        if (nr > 4) : 
            sleep(BUFF_COOLDOWN)
            self.input.keypress("F5 6"); 
        sleep(BUFF_COOLDOWN)
            
    # Potions

    def potion_health(self):   self.input.keypress("Ctrl+minus"); 
    def potion_mana(self):     self.input.keypress("Ctrl+equal"); 


class WarlockControl(BotControl):
    def __init__(self, inputdev):
        super(WarlockControl, self).__init__(inputdev)

    # Spells
    def main_target_pet(self):
        print("Warlock: cast Pet")
        self.input.keypress("F2 f Shift+t");
        sleep(0.1)

    def main_target_corruption(self):
        print("Warlock: cast Corruption")
        self.input.keypress("F2 f 2");
        sleep(GLOBAL_COOLDOWN)

    def main_target_curse_agony(self):
        print("Warlock: cast Curse of Agony")
        self.input.keypress("F2 f 3");
        sleep(GLOBAL_COOLDOWN)

    def main_target_immolate(self):
        print("Warlock: cast Immolate")
        self.input.keypress("F2 f 4");
        sleep(2.1)

    def main_target_shadowbolt(self):
        print("Warlock: cast Shadowbolt")
        self.input.keypress("F2 f 5");
        sleep(2.3)

    def main_target_drain_soul(self):
        print("Warlock: cast Drain Soul")
        self.input.keypress("F2 f 7");
        sleep(GLOBAL_COOLDOWN)

    def buff_self(self):     
        print("Warlock: buff self")
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
        print("Mage: cast Fireball")
        self.input.keypress("F2 f 2");
        sleep(2.1)

    def main_target_frostbolt(self):
        print("Mage: cast Frostbolt")
        self.input.keypress("F2 f 1");
        sleep(2)

    def main_target_arcane_missiles(self):
        print("Mage: cast Arcane Missiles")
        self.input.keypress("F2 f 4");
        sleep(3.1)

    def buff_group(self, nr):     
        print("Mage: buff group (" + str(nr) + ")")
        self.input.keypress("Ctrl+6"); 
        sleep(BUFF_COOLDOWN)
        super(MageControl, self).buff_group(nr)


class PriestControl(BotControl):
    def __init__(self, inputdev):
        super(PriestControl, self).__init__(inputdev)
        self.last_HoT = 0
        self.last_shield = 0
        self.last_H = 0
        self.last_dot = 0

    # Healing

    def self_heal_small(self):
        self.input.keypress("F1 4"); 

    def self_heal_medium(self):
        self.input.keypress("F1 5"); 

    def main_heal_over_time(self):   
        cooldown = 15000
        now = TimeUtil.get_time_ms()
        if now - self.last_HoT > cooldown :
            self.last_HoT = now
            print("Priest: cast Renew @ main")
            self.input.keypress("F2 4"); 
            sleep(GLOBAL_COOLDOWN)
            return True
        else : 
            return False

    def main_heal_small(self):       
        print("Priest: cast Small Heal @ main")
        self.input.keypress("F2 5"); 
        sleep(2.55)

    def main_heal_medium(self):      
        print("Priest: cast Medium Heal @ main")
        self.input.keypress("F2 7"); 
        sleep(3.05)
        '''
        cooldown = 2500
        now = TimeUtil.get_time_ms()
        if (now - cooldown > self.last_H) :
            self.last_H = now
            self.input.keypress("F2 5"); 
        '''

    def main_heal_big(self):     
        print("Priest: cast Big Heal @ main")
        self.input.keypress("F1 5"); 

    def main_shield(self):          
        #print("Priest: cast Shield @ main")
        #self.input.keypress("F2 Ctrl+6");
        #sleep(GLOBAL_COOLDOWN)
        cooldown = 15000
        now = TimeUtil.get_time_ms()
        if now - self.last_shield > cooldown :
            self.last_shield = now
            print("Priest: cast Shield @ main")
            self.input.keypress("F2 Ctrl+6");
            sleep(GLOBAL_COOLDOWN)
            return True
        else : 
            return False

    def main_target_wand(self):     
        print("Priest: cast Wand")
        self.input.keypress("F2 f 0");

    def main_target_dot(self, reset=False):     
        if reset:
            self.last_dot=0
        cooldown = 15000
        now = TimeUtil.get_time_ms()
        if now - self.last_dot > cooldown :
            self.last_dot = now
            print("Priest: cast Pain")
            self.input.keypress("F2 f 2");
            sleep(GLOBAL_COOLDOWN)
            return True
        else : 
            return False

    def main_target_smite(self):
        print("Priest: cast Smite")
        self.input.keypress("F2 f 3");
        sleep(2.2)


