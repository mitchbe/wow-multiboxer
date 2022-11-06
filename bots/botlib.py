#!/bin/python3

import wx, sys
import json, queue
import shlex,subprocess,os
from threading import Thread
from time import sleep
#sys.path.append(os.getcwd() + '/../lib')
#sys.path.append(os.getcwd() + '/lib')
from util import * 
import random

def delay(fn, min_sec, max_sec): 
    delay_ms = random.rantint(min_ms, max_ms)
    sleep(delay_ms / 1000)
    fn();


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




