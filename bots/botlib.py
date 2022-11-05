#!/bin/python3

import wx, sys
import json, queue
import shlex,subprocess,os
from threading import Thread
from time import sleep
sys.path.append(os.getcwd() + '/../lib')
sys.path.append(os.getcwd() + '/lib')
from util import * 



class ScreenReader():
    def __init__(self, win_id, world_state):
        self.win_id      = win_id
        self.world_state = world_state

    ### Public Interface 

    def poll_screen(self):
        def run():
            while (True): 
                self.__process_screen()
                sleep(1)

        Thread(target=run, daemon=True, args=[]).start()

    ### Private Methods

    def __read_screen(self): 
        output = Runner.execute_and_wait("./readscreen.sh " + self.win_id)
        screen_info = json.loads(output)
        return screen_info

    def __process_screen(self):
        screen_info = self.__read_screen()
        if "nodata" in screen_info:
            print("No screen data.")
            return

        print(screen_info)

        self.world_state.in_combat   = screen_info["in_combat"]
        self.world_state.main_health = screen_info["health"]
        wx.CallAfter(self.world_state.changed)


    
       

class WorldState(): 
    def __init__(self):
        self._onchange_handlers = []

        self.main_in_combat      = False
        self.main_health         = 0
        self.main_target_health  = 0


    def on_change(self, handler):
        self._onchange_handlers.append(handler)


    def changed(self):
        for i in self._onchange_handlers :
            i()




class BotWorker():
    def __init__(self, bot_ai):
        self.bot_ai = bot_ai
        self.q      = queue.Queue()

    def push(self, action): 
        self.q.put(action)

    def wake_the_ai(self):
        self.q.put(lambda : None)

    def start(self):
        def run():
            while True:
                self.q.get(block=True)()
                self.q.task_done()
                while True:
                    try :
                        self.q.get(block=False)()
                        self.q.task_done()
                    except queue.Empty:
                        if not self.bot_ai.act(): break

        Thread(target=run, daemon=True, args=[]).start()





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
        sleep(1) # latency
        self.in_combat = True
        self.ctrl.main_target_frostbolt()
        self.ctrl.main_target_fireblast()


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
            self.ctrl.main_target_fireball()
        return False


class BotControl():
    def __init__(self, inputdev):
        self.input = inputdev

    # Move

    def turn_left(self):    self.input.keyhold("a", 0.5); 
    def turn_right(self):   self.input.keyhold("d", 0.5); 
    def walk(self):         self.input.keyhold("w", 1); 
    def stop(self):         self.input.keypress("s"); 
    def follow(self):       self.input.keypress("9"); 

    # Buff

    def eat(self):          self.input.keypress("minus"); 
    def drink(self):        self.input.keypress("equal"); 

    def buff_group(self, nr):     
        self.input.keypress("F1 6"); 
        if (nr > 1) : 
            sleep(1.5)
            self.input.keypress("F2 6"); 
        if (nr > 2) : 
            sleep(1.5)
            self.input.keypress("F3 6"); 
        if (nr > 3) : 
            sleep(1.5)
            self.input.keypress("F4 6"); 
        if (nr > 4) : 
            sleep(1.5)
            self.input.keypress("F5 6"); 

    # Potions

    def potion_health(self):   self.input.keypress("Ctrl+minus"); 
    def potion_mana(self):     self.input.keypress("Ctrl+equal"); 



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
        sleep(1.1)

    def main_target_fireball(self):
        self.input.keypress("F2 f 2");
        sleep(2.1)

    def main_target_frostbolt(self):
        self.input.keypress("F2 f 1");
        sleep(1.9)

    def main_target_arcane_missiles(self):
        self.input.keypress("F2 f 4");
        sleep(3.1)

    def buff_group(self, nr):     
        self.input.keypress("Ctrl+6"); 
        sleep(1.5)
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
            sleep(1)

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
        sleep(1.5)

    def main_target_wand(self):     
        self.input.keypress("F2 f 0");

    def main_target_dot(self):     
        self.input.keypress("F2 f 2");
        sleep(1.2)

