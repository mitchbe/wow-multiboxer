#!/bin/python3

import wx
import sys
import json
import shlex,subprocess,os
from time import sleep
from threading import Thread
#import threading
sys.path.append(os.getcwd() + '/../lib')
sys.path.append(os.getcwd() + '/lib')
from tools import * 


if (len(sys.argv) == 2) :
    WIN_ID = sys.argv[1]
else :
    print("Window ID Required")
    exit(1)


class ReadScreenFrame(wx.Dialog):
    def __init__(self, *args, **kw):
        super(ReadScreenFrame, self).__init__(*args, **kw)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        #self.keyboard = Input(BOT1_WIN_ID)

        self.widget_panel = wx.Panel(self, wx.ID_ANY)
        self.focus_panel  = wx.Panel(self, wx.ID_ANY)
        self.__add_buttons()
        #self.__fix_focus()

        self.screen_thread = Thread(target=self.poll_screen, args=[])
        self.screen_thread.daemon = True
        self.screen_thread.start()
        
    def onClose(self, event):
        self.Destroy()

    def poll_screen(self):
        while (True): 
            self.process_screen()
            sleep(1.5)


    def __add_buttons(self):

        b_close    = wx.Button(self.widget_panel, wx.ID_ANY, "Close")
        b_close.Bind(wx.EVT_BUTTON, lambda e : self.Close()); 

        b_read    = wx.Button(self.widget_panel, wx.ID_ANY, "Read")
        b_read.Bind(wx.EVT_BUTTON, lambda e : self.read_screen()); 
        
        self.l_health = wx.StaticText(self.widget_panel, -1, "N/A", style=wx.ALIGN_CENTRE)

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(b_close)
        sizer.Add(b_read)
        sizer.Add(self.l_health)

        self.widget_panel.SetSizerAndFit(sizer)
        sizer.SetSizeHints(self)

    def process_screen(self):
        screen_info = self.read_screen()
        wx.CallAfter(self.process_screen_info, screen_info)

    def read_screen(self): 
        output = Runner.execute_and_wait("./readscreen.sh " + WIN_ID)
        #print("SCREEN OUTPUT: " + output)
        screen_info = json.loads(output)
        return screen_info

    def process_screen_info(self, screen_info):
        print("In combat: " + screen_info["in_combat"])
        print("Health: " + screen_info["health"])
        health = screen_info["health"]
        in_combat  = screen_info["in_combat"]
        self.l_health.SetLabel("Cmbt:" + in_combat + ", HP: " + health)

if __name__ == '__main__':
    app = wx.App()
    frm = ReadScreenFrame(None, title="Read Screen Test")
    frm.Show()
    app.MainLoop()
