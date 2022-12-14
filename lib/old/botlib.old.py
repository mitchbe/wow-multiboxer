#!/bin/python3

import wx
import sys
import shlex,subprocess
import threading,time

if (len(sys.argv) != 2) :
    #print("Window ID Required for CONTROL and BOT")
    print("Window ID Required for BOT")
    exit(1)

#CONTROL_WIN_ID = sys.argv[1]
BOT_WIN_ID = sys.argv[1]
CMD_TEMPLATE = "xdotool key --clearmodifiers --window " + BOT_WIN_ID + " --delay 28 "

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
           print(cmd)
        except Exception as ex: 
            print("Error executing: '" + cmd + "'");
            print(repr(ex))

    @staticmethod
    def hold(key, time):
        cmd1 = "xdotool keydown --clearmodifiers --window " + BOT_WIN_ID + " --delay 28 " + key 
        cmd2 = "sleep " + str(time) 
        cmd3 = "xdotool keyup --clearmodifiers --window " + BOT_WIN_ID + " --delay 28 " + key 
        try:
           Runner.executeAndWait(cmd1); 
           print(cmd1)
           Runner.executeAndWait(cmd2); 
           Runner.executeAndWait(cmd3); 
           print(cmd3)
        except Exception as ex: 
            print("Error executing: '" + cmd + "'");
            print(repr(ex))

    @staticmethod
    def release(key):
        #cmd = "xdotool keyup --clearmodifiers --window " + CONTROL_WIN_ID + " --delay 28 " + key 
        try:
            pass
           #Runner.executeAndWait(cmd); 
        except Exception as ex: 
            print("Error executing: '" + cmd + "'");
            print(repr(ex))

    def rotate(self, rotation):
        cmd = "./rotations/" + rotation + ".sh " + BOT_WIN_ID
        self.runner.executeBackground(cmd)

    def stopRotate(self):
        self.runner.stopBackground()
    
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





class BotFrame(wx.Dialog):
    def __init__(self, *args, **kw):
        super(BotFrame, self).__init__(*args, **kw)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.keyboard = Keyboard()
        panel = wx.Panel(self, wx.ID_ANY)
        self.keypanel = wx.Panel(self, wx.ID_ANY)
        self.addButtons(panel)
        self.bindKeys()
        self.fixFocus()

    def fixFocus(self):
        self.keypanel.SetFocus()

    def btnEvent(self, fn):
        def dofn(e):
            fn(e)
            self.fixFocus()
        return dofn

    def addButtons(self, panel):
        pass

    def bindKeys(self):
        pass
        #self.keypanel.Bind(wx.EVT_KEY_UP, self.keyUp)
        #panel.Bind(wx.EVT_KEY_DOWN, self.keyDown)
        #panel.Bind(wx.EVT_CHAR_HOOK, self.charHook)
        #self.Bind(wx.EVT_CHAR, self.keyDown)

    def keyDown(self, evt):
        pass

    '''
    def keyUp(self, event):
        keycode = event.GetUnicodeKey()
        if keycode != wx.WXK_NONE:
            print("Key released " + chr(keycode))
            Keyboard.release(chr(keycode))
        else:
            pass
            #if keycode == wx.WXK_SHIFT:
            #    Keyboard.press('Shift_L Shift_R')
            # It's a special key, deal with all the known ones:
            #keycode = event.GetKeyCode()
            #if keycode in [wx.WXK_LEFT, wx.WXK_RIGHT]:
            #    pass
            #elif keycode == wx.WXK_F1:
            #    pass
    '''

    def onClose(self, event):
        self.keyboard.stopRotate()
        self.Destroy()



