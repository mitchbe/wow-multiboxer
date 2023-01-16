#!/bin/python3

import sys,os
from time import sleep
#sys.path.append(os.getcwd() + '/../lib')
#sys.path.append(os.getcwd() + '/lib')
from util import * 
from botai import *

class DruidAi(BotAi):
    def __init__(self, world_state, druid_ctrl):
        super(DruidAi, self).__init__(world_state);
        self.ctrl          = druid_ctrl
        self.in_combat     = False

        self.autoheal      = False
        self.autospell     = 0
        self.delay         = 0

    ### Public Interface

    #@returns True when the AI may have more to do, False otherwise
    def act(self): 
        return self.__check_combat_state_change() or\
               self.__check_heal_main() or\
               self.__check_assist_main()

    ### Private Methods

    def __check_combat_state_change(self):
        if self.in_combat and not self.world_state.in_combat: 
            self.__exit_combat()
            return True

        if not self.in_combat and self.world_state.in_combat:
            self.__enter_combat()
            return True

        return False

    def __enter_combat(self):
        print("Druid: enter combat")
        self.in_combat = True
        sleep(self.delay)

        #self.ctrl.main_target_dot()


    def __exit_combat(self):
        print("Druid: exit combat")
        self.in_combat = False 

    def __check_heal_main(self):
        if self.autoheal : 
            health = self.world_state.main_health 
            if health > 0 and health < 95 : 
                if self.ctrl.main_heal_over_time() : 
                    return True
                if health < 60 : self.ctrl.main_heal_medium()
                if health < 85 : self.ctrl.main_heal_small()
                return True
        return False

    def __check_assist_main(self):
        if self.in_combat:
            if self.autospell: 
                self.ctrl.main_target_wrath()
                return True 
        else: 
            return False

       
