#!/bin/python3

import sys,os
from time import sleep
#sys.path.append(os.getcwd() + '/../lib')
#sys.path.append(os.getcwd() + '/lib')
from util import * 


ENTER_COMBAT_LATENCY_WAIT=0.2

#@abstract
class BotAi(): 
    def __init__(self, world_state):
        self.world_state = world_state

    #@abstract
    #@returns True when the AI may have more to do, False otherwise
    def act():
        raise NotImplementedError("abstract method")


class PriestAi(BotAi):
    def __init__(self, world_state, priest_ctrl):
        super(PriestAi, self).__init__(world_state);
        self.ctrl      = priest_ctrl
        self.in_combat = False
    
    ### Public Interface

    #@returns True when the AI may have more to do, False otherwise
    def act(self): 
        return  self.__check_combat_state_change() or \
                self.__check_heal_main() or \
                self.__check_assist_main()

    ### Private Methods

    def __enter_combat(self):
        self.in_combat = True
        self.ctrl.main_shield()
        self.ctrl.main_target_dot()
        self.ctrl.main_target_wand()


    def __exit_combat(self):
        self.in_combat = False 

    def __check_combat_state_change(self):
        if self.in_combat and not self.world_state.in_combat: 
            self.__exit_combat()
            return True

        if not self.in_combat and self.world_state.in_combat:
            self.__enter_combat()
            return True

        return False

    def __check_heal_main(self):
        health = self.world_state.main_health 
        if health > 0 :
            if health < 95 : 
                self.ctrl.main_heal_over_time()
                return True

            if health < 75 : 
                self.ctrl.main_heal_medium()
                return True
        return False

    def __check_assist_main(self):
        if self.in_combat:
            self.ctrl.main_target_wand()
        return False

       
class MageAi(BotAi):
    def __init__(self, world_state, mage_ctrl):
        super(MageAi, self).__init__(world_state);
        self.ctrl      = mage_ctrl
        self.in_combat = False
    
    ### Public Interface

    #@returns True when the AI may have more to do, False otherwise
    def act(self): 
        return  self.__check_combat_state_change() or \
                self.__check_assist_main()

    ### Private Methods

    def __enter_combat(self):
        sleep(ENTER_COMBAT_LATENCY_WAIT) 
        self.in_combat = True
        self.ctrl.main_target_frostbolt()
        self.ctrl.main_target_fireblast()


    def __exit_combat(self):
        self.in_combat = False 

    def __check_combat_state_change(self):
        if self.in_combat and not self.world_state.in_combat: 
            self.__exit_combat()
            return False

        if not self.in_combat and self.world_state.in_combat:
            self.__enter_combat()
            return True

        return False


    def __check_assist_main(self):
        if self.in_combat:
            self.ctrl.main_target_fireball()
            return True
        else:
            return False


       
class WarlockAi(BotAi):
    def __init__(self, world_state, warlock_ctrl):
        super(WarlockAi, self).__init__(world_state);
        self.ctrl      = warlock_ctrl
        self.in_combat = False
    
    ### Public Interface

    #@returns True when the AI may have more to do, False otherwise
    def act(self): 
        return  self.__check_combat_state_change() or \
                self.__check_assist_main()

    ### Private Methods

    def __enter_combat(self):
        sleep(ENTER_COMBAT_LATENCY_WAIT) 
        self.in_combat = True
        self.ctrl.main_target_corruption()
        self.ctrl.main_target_curse_agony()
        self.ctrl.main_target_immolate()


    def __exit_combat(self):
        self.in_combat = False 

    def __check_combat_state_change(self):
        if self.in_combat and not self.world_state.in_combat: 
            self.__exit_combat()
            return True

        if not self.in_combat and self.world_state.in_combat:
            self.__enter_combat()
            return True

        return False


    def __check_assist_main(self):
        if self.in_combat:
            self.ctrl.main_target_drain_soul()
            #self.ctrl.main_target_shadowbolt()
        return False
