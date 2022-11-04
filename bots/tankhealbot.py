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


if (len(sys.argv) == 3) :
    TANK_WIN_ID = sys.argv[1]
    HEAL_WIN_ID = sys.argv[2]
else :
    print("Window ID Required for tank and heal")
    exit(1)



class HealerControl():
    def __init__(self, inputdev):
        self.input = inputdev
        self.last_HoT = 0
        self.last_H = 0

    # Move

    def turn_left(self):    self.input.keyhold("a", 0.5); 
    def turn_right(self):   self.input.keyhold("d", 0.5); 
    def walk(self):         self.input.keyhold("w", 1); 
    def stop(self):         self.input.keypress("s"); 
    def follow(self):       self.input.keypress("9"); 

    # Buff

    def eat(self):          self.input.keypress("minus"); 
    def drink(self):        self.input.keypress("equal"); 
    def buff(self, nr):     
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

    def healthpot(self):   self.input.keypress("Ctrl+minus"); 
    def manapot(self):     self.input.keypress("Ctrl+equal"); 


    # Healing
    def heal_tank_over_time(self):   
        cooldown = 15000
        now = TimeUtil.get_time_ms()
        if (now - cooldown > self.last_HoT) :
            self.last_HoT = now
            self.input.keypress("F2 4"); 
            sleep(1)

    def heal_tank_small(self):       self.input.keypress("F1 5"); 

    def heal_tank_medium(self):      
        self.input.keypress("F2 5"); 
        sleep(2.55)
        '''
        cooldown = 2500
        now = TimeUtil.get_time_ms()
        if (now - cooldown > self.last_H) :
            self.last_H = now
            self.input.keypress("F2 5"); 
        '''

    def heal_tank_big(self):         self.input.keypress("F1 5"); 

    def shield_tank(self):          
        self.input.keypress("F2 Ctrl+6");
        sleep(1.5)

    def assist_tank_wand(self):     
        self.input.keypress("F2 f 0");

    def assist_tank_dot(self):     
        self.input.keypress("F2 f 2");
        sleep(1.2)


class TankHealFrame(wx.Dialog):

    ### Initialize

    def __init__(self, *args, **kw):
        super(TankHealFrame, self).__init__(*args, **kw)
        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.tank_input = Input(TANK_WIN_ID)
        self.heal_input = Input(HEAL_WIN_ID)
        self.heal_ctrl = HealerControl(self.heal_input)

        self.widget_panel = wx.Panel(self, wx.ID_ANY)
        self.focus_panel  = wx.Panel(self, wx.ID_ANY)

        self.__add_widgets()

        self.auto_follow = False

        self.poll_screen()

        self.in_combat = False

        
    def onClose(self, event):
        self.Destroy()


    ### Screen Reading


    def poll_screen(self):
        def run():
            while (True): 
                self.process_screen()
                sleep(1)

        self.screen_thread = Thread(target=run, args=[])
        self.screen_thread.daemon = True
        self.screen_thread.start()


    def process_screen(self):
        screen_info = self.read_screen()
        wx.CallAfter(self.process_screen_info, screen_info)

    def read_screen(self): 
        output = Runner.execute_and_wait("./readscreen.sh " + TANK_WIN_ID)
        #print("SCREEN OUTPUT: " + output)
        screen_info = json.loads(output)
        return screen_info

    def process_screen_info(self, screen_info):
        if "nodata" in screen_info:
            print("No screen data.")
            return

        print(screen_info)
        self.l_health.SetLabel("Cmbt:" + str(screen_info["in_combat"]) + ", HP: " + screen_info["health"])
    
        in_combat  = screen_info["in_combat"]
        if self.in_combat and not in_combat: 
            self.exit_combat()

        if not self.in_combat and in_combat:
            self.enter_combat()

        cast = False

        health = float(screen_info["health"])
        if health > 0 :
            if health < 95 : 
                self.heal_ctrl.heal_tank_over_time()
                cast = True

            if health < 75 : 
                self.heal_ctrl.heal_tank_medium()
                cast = True

        #if cast == True and self.in_combat:
        #    self.heal_ctrl.assist_tank_wand()

        if self.in_combat:
            self.heal_ctrl.assist_tank_wand()
       
    
    def enter_combat(self):
        print("Enter Combat...")
        self.in_combat = True
        self.heal_ctrl.shield_tank()
        self.heal_ctrl.assist_tank_dot()
        self.heal_ctrl.assist_tank_wand()

    def exit_combat(self):
        print("...Exit Combat!")
        self.in_combat = False 




    ### Add Widgets


    def __add_widgets(self):

        b_close    = wx.Button(self.widget_panel, wx.ID_ANY, "Close")
        b_close.Bind(wx.EVT_BUTTON, lambda e : self.Close()); 

        b_read    = wx.Button(self.widget_panel, wx.ID_ANY, "Read")
        b_read.Bind(wx.EVT_BUTTON, lambda e : self.read_screen()); 
        
        self.l_health = wx.StaticText(self.widget_panel, -1, "N/A", style=wx.ALIGN_CENTRE)

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

    def add_move_btns(self):
        b_turnleft  = wx.Button(self.widget_panel, wx.ID_ANY, "R. Left")
        b_turnright = wx.Button(self.widget_panel, wx.ID_ANY, "R. Right")
        b_turnleft.Bind(wx.EVT_BUTTON, self.__no_focus(self.heal_ctrl.turn_left))
        b_turnright.Bind(wx.EVT_BUTTON, self.__no_focus(self.heal_ctrl.turn_right))

        b_walk       = wx.Button(self.widget_panel, wx.ID_ANY, "Walk")
        b_stop       = wx.Button(self.widget_panel, wx.ID_ANY, "Stop")
        b_follow     = wx.Button(self.widget_panel, wx.ID_ANY, "Follow")
        b_autofollow = wx.ToggleButton(self.widget_panel, wx.ID_ANY, "Lock Follow")
        b_walk.Bind(wx.EVT_BUTTON, self.__no_focus(self.heal_ctrl.walk))
        b_stop.Bind(wx.EVT_BUTTON, self.__no_focus(self.heal_ctrl.stop))

        def toggleAutoFollow(e):
           self.auto_follow = True if e.IsChecked() else False 
        b_autofollow.Bind(wx.EVT_TOGGLEBUTTON, self.__no_focus(toggleAutoFollow)) 

        b_follow.Bind(wx.EVT_BUTTON, self.__no_focus(self.heal_ctrl.follow)) 

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
            self.heal_ctrl.buff(c_nrParty.GetSelection() + 1)

        b_buff.Bind(wx.EVT_BUTTON, self.__no_focus(dobuff)) 
        b_eat.Bind(wx.EVT_BUTTON, self.__no_focus(self.heal_ctrl.eat))
        b_drink.Bind(wx.EVT_BUTTON, self.__no_focus(self.heal_ctrl.drink))

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

        b_healthpot.Bind(wx.EVT_BUTTON, self.__no_focus(self.heal_ctrl.healthpot)) 
        b_manapot.Bind(wx.EVT_BUTTON, self.__no_focus(self.heal_ctrl.manapot)) 

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


    def addButtons(self, self.widget_panel):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.restBtns(self.widget_panel), 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        sizer.Add(self.potionBtns(self.widget_panel), 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        sizer.Add(self.moveBtns(self.widget_panel), 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        sizer.Add(self.actionBtns(self.widget_panel), 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)

        self.widget_panel.SetSizerAndFit(sizer)
        sizer.SetSizeHints(self)
    '''

if __name__ == '__main__':
    app = wx.App()
    frm = TankHealFrame(None, title="Tank/Heal Botter")
    frm.Show()
    app.MainLoop()
