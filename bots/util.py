#!/bin/python3

import wx
import sys
import shlex,subprocess
import threading,time
import datetime
import random
from time import sleep

def delayfn(fn, min_ms, max_ms): 
    delay(min_ms, max_ms);
    print("running fn")
    fn();

def delay(min_ms, max_ms): 
    delay_ms = random.randint(min_ms, max_ms)
    print("delaying: " + (delay_ms/1000))
    sleep(delay_ms / 1000)

class Runner():
    @staticmethod
    def execute_and_wait(cmd):
        print("Executing: '" + cmd + "'")
        process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            raise Exception(error)
        else:
            return output.decode("utf-8")


class Input():
    def __init__(self, win_id):
        self.win_id = win_id

    def keypress(self, keys):
        try:
            self.__xdo("xdotool key --clearmodifiers --window " + self.win_id + " --delay 28 " + keys)
        except Exception as ex: 
            print(ex)
            pass

    def keyhold(self, key, period_ms):
        try:
            self.__xdo("xdotool keydown --clearmodifiers --window " + self.win_id + " --delay 28 " + key)
            self.__xdo("sleep " + str(period_ms))
            self.__xdo("xdotool keyup --clearmodifiers --window " + self.win_id + " --delay 28 " + key)
        except Exception as ex: 
            print(ex)
            pass

    def keyrelease(self, key):
        try:
            self.__xdo("xdotool keyup --clearmodifiers --window " + self.win_id + " --delay 28 " + key)
        except Exception as ex: 
            print(ex)
            pass
    
    def __xdo(self, cmd):
        print(cmd)
        try: 
            Runner.execute_and_wait(cmd); 
        except Exception as ex: 
            print("Error executing: '" + cmd + "'");
            print(repr(ex))
            raise ex



class TimeUtil: 
    @staticmethod
    def get_time_ms():
        return round(datetime.datetime.utcnow().timestamp() * 1000)





'''



class ScreenInfo():
    def __init__(self):
        pass

    def printScreenInfo():
        result=Runner.executeAndWait("./readscreen.sh");
        print(result)

    def doPrintScreenInfo():
        def print_loop():
            for i in range(1,60):
                ScreenInfo.printScreenInfo()
                time.sleep(1)

        x = threading.Thread(target=print_loop)
        x.start()
        x.join()

class Paths():
    @staticmethod
    def path(path_from_program_root):
        return "./" + path_from_program_root

class Rotation():
    def __init__(self, name, win_id) :
        self.name    = name
        self.script  = Paths.path("rotations/" + name + ".sh " + win_id)
        self.process = None

    def start(self, rotation):
        try: 
            self.process = subprocess.Popen(shlex.split(self.script))
        except SubProcessError as error:
            print("Failed to execute rotation:'" + str(self) + "'")
            print(repr(ex))

    def stop(self):
        if self.is_active(): 
            self.process.kill()
            self.process.wait()
            self.process = None

    def is_active(self):
        return self.process is not None

    def __str__(self):
        return f'Rotation({self.name},{self.script},{self.process})'
'''
