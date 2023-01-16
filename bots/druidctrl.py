#!/bin/python3

import sys,os
from time import sleep
#sys.path.append(os.getcwd() + '/../lib')
#sys.path.append(os.getcwd() + '/lib')
from util import * 
from botctrl import *



class DruidControl(BotControl):
    def __init__(self, inputdev):
        super(DruidControl, self).__init__(inputdev)
        #self.last_HoT = 0
        #self.last_shield = 0
        #self.last_H = 0
        #self.last_dot = 0

    # Healing

    def self_heal(self):
        self.input.keypress("F1 6"); 

    def self_heal_over_time(self):
        self.input.keypress("F1 4"); 

    def main_heal_over_time(self):   
        '''
        cooldown = 15000
        now = TimeUtil.get_time_ms()
        if now - self.last_HoT > cooldown :
            self.last_HoT = now
            print("Druid: cast Renew @ main")
            self.input.keypress("F2 4"); 
            sleep(GLOBAL_COOLDOWN)
            return True
        else : 
            return False
        '''
        pass

    def main_heal_small(self):       
        print("Druid: cast Small Heal @ main")
        self.input.keypress("F2 5"); 
        sleep(1.55)

    def main_heal_medium(self):      
        print("Druid: cast Medium Heal @ main")
        self.input.keypress("F2 6"); 
        sleep(1.55)
        '''
        cooldown = 2500
        now = TimeUtil.get_time_ms()
        if (now - cooldown > self.last_H) :
            self.last_H = now
            self.input.keypress("F2 5"); 
        '''

    def main_heal_big(self):     
        print("Druid: cast Big Heal @ main")
        self.input.keypress("F2 7"); 
        sleep(1.55)

    '''
    def main_shield(self):          
        #print("Druid: cast Shield @ main")
        #self.input.keypress("F2 Ctrl+6");
        #sleep(GLOBAL_COOLDOWN)
        cooldown = 15000
        now = TimeUtil.get_time_ms()
        if now - self.last_shield > cooldown :
            self.last_shield = now
            print("Druid: cast Shield @ main")
            self.input.keypress("F2 Ctrl+6");
            sleep(GLOBAL_COOLDOWN)
            return True
        else : 
            return False
    '''
    def main_target_wrath(self, reset=False):     
        print("Druid: cast Wrath")
        self.input.keypress("F2 f 2"); 
        sleep(1.55)

    def main_target_dot(self, reset=False):     
        '''
        if reset:
            self.last_dot=0
        cooldown = 15000
        now = TimeUtil.get_time_ms()
        if now - self.last_dot > cooldown :
            self.last_dot = now
            print("Druid: cast Pain")
            self.input.keypress("F2 f 2");
            sleep(GLOBAL_COOLDOWN)
            return True
        else : 
            return False
        '''
        return False



