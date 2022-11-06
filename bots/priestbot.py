#!/bin/python3

import wx
import sys
import json
import shlex,subprocess,os
from time import sleep
from threading import Thread
#sys.path.append(os.getcwd() + '/../lib')
#sys.path.append(os.getcwd() + '/lib')
from util import * 
from botlib import *
from botai import *
from botctrl import *


if (len(sys.argv) == 3) :
    MAIN_WIN_ID = sys.argv[1]
    PRIEST_WIN_ID = sys.argv[2]
else :
    print("Window ID Required for tank and heal")
    exit(1)



class PriestBotFrame(wx.Dialog):

    ### Initialize

    def __init__(self, *args, **kw):
        super(PriestBotFrame, self).__init__(*args, **kw)

        self.world_state = WorldState()

        self.priest_ctrl = PriestControl(Input(PRIEST_WIN_ID))
        self.priest_ai   = PriestAi(self.world_state, self.priest_ctrl)

        # Create UI
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.widget_panel = wx.Panel(self, wx.ID_ANY)
        self.focus_panel  = wx.Panel(self, wx.ID_ANY)
        self.__add_widgets()

        # Bot Worker
        self.priest_worker  = BotWorker(self.priest_ai) 
        self.priest_worker.start()
        self.world_state.on_change(self.priest_worker.wake_the_ai)
    
        # Screen Reader
        self.screen_reader = ScreenReader(MAIN_WIN_ID, self.world_state)
        self.screen_reader.poll_screen()


        
    def onClose(self, event):
        self.Destroy()


    ### Add Widgets



    def __add_widgets(self):

        def __update_world_state_labels():
            self.l_health.SetLabel("Cmbt:" + str(self.world_state.in_combat) + ", HP: " + str(self.world_state.main_health))

        b_close    = wx.Button(self.widget_panel, wx.ID_ANY, "Close")
        b_close.Bind(wx.EVT_BUTTON, lambda e : self.Close()); 

        b_read    = wx.Button(self.widget_panel, wx.ID_ANY, "Read")
        b_read.Bind(wx.EVT_BUTTON, lambda e : self.read_screen()); 
        
        self.l_health = wx.StaticText(self.widget_panel, -1, "N/A", style=wx.ALIGN_CENTRE)
        self.world_state.on_change(__update_world_state_labels) 

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(b_close)
        sizer.Add(b_read)
        sizer.Add(self.l_health)
        sizer.Add(self.add_move_btns())
        sizer.Add(self.add_buff_btns())
        sizer.Add(self.add_potion_btns())

        self.widget_panel.SetSizerAndFit(sizer)
        sizer.SetSizeHints(self)

        self.__set_focus()

    def __set_focus(self):
        self.focus_panel.SetFocus()

    def __no_focus(self, fn):
        def dofn(e):
            fn()
            self.__set_focus()
        return dofn

    def __btn_ctrl(self, action):
        return self.__no_focus(lambda : self.priest_worker.push(action))

    def add_move_btns(self):
        b_turnleft  = wx.Button(self.widget_panel, wx.ID_ANY, "R. Left")
        b_turnright = wx.Button(self.widget_panel, wx.ID_ANY, "R. Right")
        b_turnleft.Bind(wx.EVT_BUTTON, self.__btn_ctrl(self.priest_ctrl.turn_left))
        b_turnright.Bind(wx.EVT_BUTTON, self.__btn_ctrl(self.priest_ctrl.turn_right))


        b_walk       = wx.Button(self.widget_panel, wx.ID_ANY, "Walk")
        b_stop       = wx.Button(self.widget_panel, wx.ID_ANY, "Stop")
        b_follow     = wx.Button(self.widget_panel, wx.ID_ANY, "Follow")
        b_autofollow = wx.ToggleButton(self.widget_panel, wx.ID_ANY, "Lock Follow")
        b_walk.Bind(wx.EVT_BUTTON, self.__btn_ctrl(self.priest_ctrl.walk))
        b_stop.Bind(wx.EVT_BUTTON, self.__btn_ctrl(self.priest_ctrl.stop))

        def toggleAutoFollow(e):
           self.auto_follow = True if e.IsChecked() else False 
        b_autofollow.Bind(wx.EVT_TOGGLEBUTTON, self.__btn_ctrl(toggleAutoFollow)) 

        b_follow.Bind(wx.EVT_BUTTON, self.__btn_ctrl(self.priest_ctrl.follow)) 

        s = wx.StaticBoxSizer(wx.StaticBox(self.widget_panel, -1, "Move Healer"), wx.VERTICAL)

        s1 = wx.BoxSizer(wx.HORIZONTAL)
        s1.Add(b_turnleft, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s1.Add(b_turnright, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s.Add(s1, 1, wx.EXPAND)

        s1 = wx.BoxSizer(wx.HORIZONTAL)
        s1.Add(b_walk, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s1.Add(b_stop, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s.Add(s1, 1, wx.EXPAND) 

        s1 = wx.BoxSizer(wx.HORIZONTAL)
        s1.Add(b_autofollow, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s1.Add(b_follow, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s.Add(s1, 1, wx.EXPAND) 

        return s

    def add_buff_btns(self):
        b_eat       = wx.Button(self.widget_panel, wx.ID_ANY, "Eat")
        b_drink     = wx.Button(self.widget_panel, wx.ID_ANY, "Drink")
        b_buff      = wx.Button(self.widget_panel, wx.ID_ANY, "Buff")

        c_nrParty   = wx.Choice(self.widget_panel,choices = ['1', '2', '3', '4', '5'])
        c_nrParty.SetSelection(1)

        def dobuff():
            self.priest_ctrl.buff_group(c_nrParty.GetSelection() + 1)

        b_buff.Bind(wx.EVT_BUTTON, self.__btn_ctrl(dobuff)) 
        b_eat.Bind(wx.EVT_BUTTON, self.__btn_ctrl(self.priest_ctrl.eat))
        b_drink.Bind(wx.EVT_BUTTON, self.__btn_ctrl(self.priest_ctrl.drink))

        s = wx.StaticBoxSizer(wx.StaticBox(self.widget_panel, -1, "Rest"), wx.VERTICAL)

        s1 = wx.BoxSizer(wx.HORIZONTAL)
        s1.Add(c_nrParty, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s1.Add(b_buff, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s.Add(s1, 1, wx.EXPAND)

        s1 = wx.BoxSizer(wx.HORIZONTAL)
        s1.Add(b_eat, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s1.Add(b_drink, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s.Add(s1, 1, wx.EXPAND)

        return s

    def add_potion_btns(self):
        b_manapot       = wx.Button(self.widget_panel, wx.ID_ANY, "Mana")
        b_healthpot     = wx.Button(self.widget_panel, wx.ID_ANY, "Health")

        b_healthpot.Bind(wx.EVT_BUTTON, self.__btn_ctrl(self.priest_ctrl.potion_health)) 
        b_manapot.Bind(wx.EVT_BUTTON, self.__btn_ctrl(self.priest_ctrl.potion_mana)) 

        s = wx.StaticBoxSizer(wx.StaticBox(self.widget_panel, -1, "Potions"), wx.VERTICAL)

        s1 = wx.BoxSizer(wx.HORIZONTAL)
        s1.Add(b_manapot, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s1.Add(b_healthpot, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s.Add(s1, 1, wx.EXPAND)

        return s
    '''

    def autoFollow(self, fn):
        def handler(e):
            fn(e)
            if self.autoFollow and not e.IsChecked() :
                Keyboard.press("9"); 

        return handler


    def actionBtns(self, self.widget_panel):
        b_target    = wx.Button(self.widget_panel, wx.ID_ANY, "Target")
        b_burn      = wx.ToggleButton(self.widget_panel, wx.ID_ANY, "Burn")
        b_freeze    = wx.ToggleButton(self.widget_panel, wx.ID_ANY, "Freeze")
        b_wand      = wx.Button(self.widget_panel, wx.ID_ANY, "Wand")

        b_target.Bind(wx.EVT_BUTTON, self.__no_focus(lambda e : Keyboard.press("F2 f"))); 
        b_burn.Bind(wx.EVT_TOGGLEBUTTON, self.__no_focus(self.autoFollow(lambda e : self.keyboard.rotate("mage/burn") if e.IsChecked() else self.keyboard.stopRotate()))); 
        b_freeze.Bind(wx.EVT_TOGGLEBUTTON, self.__no_focus(self.autoFollow(lambda e : self.keyboard.rotate("mage/freeze") if e.IsChecked() else self.keyboard.stopRotate()))); 
        b_wand.Bind(wx.EVT_BUTTON, self.__no_focus(lambda e : Keyboard.press("F2 f 5"))); 

        s = wx.StaticBoxSizer(wx.StaticBox(self.widget_panel, -1, "Action"), wx.VERTICAL)

        s1 = wx.BoxSizer(wx.HORIZONTAL)
        s1.Add(b_target, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s.Add(s1, 1, wx.EXPAND)

        s1 = wx.BoxSizer(wx.HORIZONTAL)
        s1.Add(b_burn, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s.Add(s1, 1, wx.EXPAND)

        s1 = wx.BoxSizer(wx.HORIZONTAL)
        s1.Add(b_freeze, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s1.Add(b_wand, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s.Add(s1, 1, wx.EXPAND)

        b_info    = wx.Button(self.widget_panel, wx.ID_ANY, "Info")
        b_info.Bind(wx.EVT_BUTTON, self.__no_focus(lambda e : ScreenInfo.doPrintScreenInfo())); 
        s1 = wx.BoxSizer(wx.HORIZONTAL)
        s1.Add(b_info, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s.Add(s1, 1, wx.EXPAND)
        return s
    '''

if __name__ == '__main__':
    app = wx.App()
    frm = PriestBotFrame(None, title="Priest Bot")
    frm.Show()
    app.MainLoop()
