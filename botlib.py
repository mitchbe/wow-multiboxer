#!/bin/python3

import wx
import sys
import shlex,subprocess

if (len(sys.argv) != 2) :
    print("Window ID Required")

WIN_ID = sys.argv[1]
CMD_TEMPLATE = "xdotool key --window " + WIN_ID + " --delay 28 "

class Runner():
    @staticmethod
    def executeAndWait(cmd):
        print("Executing: '" + cmd + "'")
        process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            raise Exception(error)
        else:
            return output
        return

    def __init__(self):
        self.process = None


    def executeBackground(self, cmd):
        self.stopBackground()
        print("Bg Executing: '" + cmd + "'")
        try: 
            self.process = subprocess.Popen(shlex.split(cmd))
        except SubProcessError as error:
            print("Error subprocess bg executing: '" + cmd + "'")
            print(repr(ex))

    def stopBackground(self):
        if self.process is not None: 
            print("Stop bg process")
            self.process.kill()
            self.process.wait()
            self.process = None

class Keyboard():
   
    def __init__(self) :
        self.runner = Runner();
    
    @staticmethod
    def press(keys):
        cmd = CMD_TEMPLATE + keys;
        try:
           Runner.executeAndWait(cmd); 
        except Exception as ex: 
            print("Error executing: '" + cmd + "'");
            print(repr(ex))

    def rotate(self, rotation):
        cmd = "./" + rotation + ".sh " + WIN_ID
        self.runner.executeBackground(cmd)

    def stopRotate(self):
        self.runner.stopBackground()
        

class BotFrame(wx.Dialog):
    def __init__(self, *args, **kw):
        super(BotFrame, self).__init__(*args, **kw)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.keyboard = Keyboard()
        self.addButtons()

    def addButtons(self):
        pass

    def onClose(self, event):
        self.keyboard.stopRotate()
        self.Destroy()

