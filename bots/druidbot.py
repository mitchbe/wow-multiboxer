#!/bin/python3

import wx
import sys
import json
import shlex,subprocess,os
from time import sleep
from threading import Thread
from inspect import signature
#sys.path.append(os.getcwd() + '/../lib')
#sys.path.append(os.getcwd() + '/lib')
from util import * 
from botlib import *
from botai import *
from druidai import *
from botctrl import *
from druidctrl import *


if (len(sys.argv) == 3) :
    MAIN_WIN_ID = sys.argv[1]
    PRIEST_WIN_ID = sys.argv[2]
else :
    print("Window ID Required for main and druid")
    exit(1)



class DruidBotFrame(wx.Dialog):

    ### Initialize

    def __init__(self, *args, **kw):
        super(DruidBotFrame, self).__init__(*args, **kw)

        self.world_state = WorldState()

        self.druid_ctrl = DruidControl(Input(PRIEST_WIN_ID))
        self.druid_ai   = DruidAi(self.world_state, self.druid_ctrl)

        # Create UI
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.widget_panel = wx.Panel(self, wx.ID_ANY)
        self.focus_panel  = wx.Panel(self, wx.ID_ANY)
        self.__add_widgets()

        # Bot Worker
        self.druid_worker  = BotWorker(self.druid_ai) 
        self.druid_worker.start()
        self.world_state.on_change(self.druid_worker.wake_the_ai)
    
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

        
        self.l_health = wx.StaticText(self.widget_panel, -1, "N/A", style=wx.ALIGN_CENTRE)
        self.world_state.on_change(__update_world_state_labels) 

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(b_close)
        sizer.Add(self.l_health)
        sizer.Add(self.add_move_btns())
        sizer.Add(self.add_buff_btns())
        sizer.Add(self.add_potion_btns())
        sizer.Add(self.add_druid_ai_btns())

        self.widget_panel.SetSizerAndFit(sizer)
        sizer.SetSizeHints(self)

        self.__set_focus()

    def __set_focus(self):
        self.focus_panel.SetFocus()

    def __no_focus(self, fn):
        def run(e):
            if len(signature(fn).parameters) > 0 : 
                fn(e)
            else :
                fn()
            self.__set_focus()
        return run 

    def __btn_ctrl(self, action):
        return self.__no_focus(lambda : self.druid_worker.push(action))

    def add_move_btns(self):
        b_turnleft  = wx.Button(self.widget_panel, wx.ID_ANY, "Rot L")
        b_turnright = wx.Button(self.widget_panel, wx.ID_ANY, "Rot R")
        b_turnleft.Bind(wx.EVT_BUTTON, self.__btn_ctrl(self.druid_ctrl.turn_left))
        b_turnright.Bind(wx.EVT_BUTTON, self.__btn_ctrl(self.druid_ctrl.turn_right))


        b_walkfwd    = wx.Button(self.widget_panel, wx.ID_ANY, "Fwd")
        b_walkbwd    = wx.Button(self.widget_panel, wx.ID_ANY, "Bwd")
        b_stop       = wx.Button(self.widget_panel, wx.ID_ANY, "Stop")
        b_follow     = wx.Button(self.widget_panel, wx.ID_ANY, "Follow")
        b_walkfwd.Bind(wx.EVT_BUTTON, self.__btn_ctrl(self.druid_ctrl.walk_fwd))
        b_walkbwd.Bind(wx.EVT_BUTTON, self.__btn_ctrl(self.druid_ctrl.walk_bwd))
        b_stop.Bind(wx.EVT_BUTTON, self.__btn_ctrl(self.druid_ctrl.stop))
        b_follow.Bind(wx.EVT_BUTTON, self.__btn_ctrl(self.druid_ctrl.follow)) 

        s = wx.StaticBoxSizer(wx.StaticBox(self.widget_panel, -1, "Move Healer"), wx.VERTICAL)

        s1 = wx.BoxSizer(wx.HORIZONTAL)
        s1.Add(b_turnleft, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s1.Add(b_turnright, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s.Add(s1, 1, wx.EXPAND)

        s1 = wx.BoxSizer(wx.HORIZONTAL)
        s1.Add(b_walkfwd, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s1.Add(b_walkbwd, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s.Add(s1, 1, wx.EXPAND) 

        s1 = wx.BoxSizer(wx.HORIZONTAL)
        s1.Add(b_stop, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s1.Add(b_follow, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s.Add(s1, 1, wx.EXPAND) 

        return s

    def add_buff_btns(self):
        b_eat       = wx.Button(self.widget_panel, wx.ID_ANY, "Eat")
        b_drink     = wx.Button(self.widget_panel, wx.ID_ANY, "Drink")
        b_buff      = wx.Button(self.widget_panel, wx.ID_ANY, "Buff")

        c_nrParty   = wx.Choice(self.widget_panel, choices = ['1', '2', '3', '4', '5'])
        c_nrParty.SetSelection(1)


        def dobuff():
            self.druid_ctrl.buff_group(c_nrParty.GetSelection() + 1)

        b_buff.Bind(wx.EVT_BUTTON, self.__btn_ctrl(dobuff)) 
        b_eat.Bind(wx.EVT_BUTTON, self.__btn_ctrl(self.druid_ctrl.eat))
        b_drink.Bind(wx.EVT_BUTTON, self.__btn_ctrl(self.druid_ctrl.drink))

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
        b_healself1     = wx.Button(self.widget_panel, wx.ID_ANY, "Self HoT")
        b_healself2     = wx.Button(self.widget_panel, wx.ID_ANY, "Self Heal")

        b_healthpot.Bind(wx.EVT_BUTTON, self.__btn_ctrl(self.druid_ctrl.potion_health)) 
        b_manapot.Bind(wx.EVT_BUTTON, self.__btn_ctrl(self.druid_ctrl.potion_mana)) 

        b_healself1.Bind(wx.EVT_BUTTON, self.__btn_ctrl(self.druid_ctrl.self_heal_over_time)) 
        b_healself2.Bind(wx.EVT_BUTTON, self.__btn_ctrl(self.druid_ctrl.self_heal)) 

        s = wx.StaticBoxSizer(wx.StaticBox(self.widget_panel, -1, "Potions"), wx.VERTICAL)

        s1 = wx.BoxSizer(wx.HORIZONTAL)
        s1.Add(b_manapot, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s1.Add(b_healthpot, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s0 = wx.BoxSizer(wx.HORIZONTAL) 
        s0.Add(b_healself1)
        s0.Add(b_healself2)
        
        s.Add(s1, 1, wx.EXPAND)
        s.Add(s0, 1, wx.EXPAND)

        return s

    def add_druid_ai_btns(self):
        def b_ai_delay_run(): self.druid_ai.delay = c_ai_delay.GetSelection(); 
        c_ai_delay   = wx.Choice(self.widget_panel, choices = ['0', '1', '2', '3', '4', '5'])
        c_ai_delay.SetSelection(0)
        c_ai_delay.Bind(wx.EVT_CHOICE, self.__btn_ctrl(b_ai_delay_run)) 

        def b_autoheal_run(e): self.druid_ai.autoheal = e.IsChecked(); 
        b_autoheal = wx.ToggleButton(self.widget_panel, wx.ID_ANY, "Autoheal")
        b_autoheal.Bind(wx.EVT_TOGGLEBUTTON, self.__no_focus(b_autoheal_run)); 

        def b_autospell_run(e): self.druid_ai.autospell = e.IsChecked(); 
        b_autospell    = wx.ToggleButton(self.widget_panel, wx.ID_ANY, "Autospell")
        b_autospell.Bind(wx.EVT_TOGGLEBUTTON, self.__no_focus(b_autospell_run)); 

        s = wx.StaticBoxSizer(wx.StaticBox(self.widget_panel, -1, "Druid AI"), wx.VERTICAL)

        s1 = wx.BoxSizer(wx.HORIZONTAL)
        s1.Add(b_autospell, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s1.Add(b_autoheal, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)

        s3 = wx.BoxSizer(wx.HORIZONTAL)
        s3.Add(c_ai_delay, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)

        s.Add(s1, 1, wx.EXPAND)
        s.Add(s3, 1, wx.EXPAND)
        return s

if __name__ == '__main__':
    app = wx.App()
    frm = DruidBotFrame(None, title="Druid Bot")
    frm.Show()
    app.MainLoop()
