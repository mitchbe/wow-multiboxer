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
        self.ctrl          = priest_ctrl
        self.in_combat     = False
        self.conserve_mana = False
        self.shield_main   = False
        self.autoheal      = False
    
    ### Public Interface

    #@returns True when the AI may have more to do, False otherwise
    def act(self): 
        return  self.__check_combat_state_change() or \
                self.__check_heal_main() or \
                self.__check_assist_main()

    ### Private Methods

    def __enter_combat(self):
        print("Priest: enter combat")
        self.in_combat = True
        if self.shield_main : 
            self.ctrl.main_shield()
        self.ctrl.main_target_dot()
        if self.conserve_mana : 
            self.ctrl.main_target_wand();
        else : 
            self.ctrl.main_target_smite()


    def __exit_combat(self):
        print("Priest: exit combat")
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
        if self.autoheal : 
            health = self.world_state.main_health 
            if health > 0 :
                if health < 95 : self.ctrl.main_heal_over_time()
                if health < 75 : self.ctrl.main_heal_medium()
                if health < 95 : return True
            return False
        else : 
            return False

    def __check_assist_main(self):
        if self.in_combat:
            if self.conserve_mana : 
                self.ctrl.main_target_wand()
                return False
            else : 
                self.ctrl.main_target_smite()
                return True 
        else: 
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
        print("Mage: enter combat")
        #sleep(ENTER_COMBAT_LATENCY_WAIT) 
        delay(0, 1000)
        self.in_combat = True
        self.ctrl.main_target_frostbolt()
        self.ctrl.main_target_fireblast()


    def __exit_combat(self):
        print("Mage: exit combat")
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

        self.use_souldrain = False
        self.autofollow = False
    
    ### Public Interface

    #@returns True when the AI may have more to do, False otherwise
    def act(self): 
        return  self.__check_combat_state_change() or \
                self.__check_assist_main()

    ### Private Methods

    def __enter_combat(self):
        #sleep(ENTER_COMBAT_LATENCY_WAIT) 
        print("Warlock: enter combat")
        delay(0, 1000)
        self.in_combat = True
        self.ctrl.main_target_corruption()
        self.ctrl.main_target_curse_agony()
        self.ctrl.main_target_immolate()


    def __exit_combat(self):
        self.in_combat = False 
        if self.autofollow : 
            self.ctrl.follow()
        print("Warlock: exit combat")

    def __check_combat_state_change(self):
        if self.in_combat and not self.world_state.in_combat: 
            self.__exit_combat()
            return True

        if not self.in_combat and self.world_state.in_combat:
            self.__enter_combat()
            return True

        return False


    def __check_assist_main(self):
        if self.use_souldrain:
            if self.in_combat:
                self.ctrl.main_target_drain_soul()
            return False
        else : 
            if self.in_combat:
                self.ctrl.main_target_shadowbolt()
                return True
            else:
                return False

