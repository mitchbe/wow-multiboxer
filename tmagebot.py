#!/bin/python3

import wx
import sys
import shlex,subprocess
import botlib
from botlib import * 


class ClientFrame(BotFrame):
    def __init__(self, *args, **kw):
        super(ClientFrame, self).__init__(*args, **kw)
        self.autoFollow = False


    def moveBtns(self, panel):
        b_turnleft  = wx.Button(panel, wx.ID_ANY, "R. Left")
        b_turnright = wx.Button(panel, wx.ID_ANY, "R. Right")
        #b_turnleft.Bind(wx.EVT_BUTTON, lambda e : Keyboard.press("a a a a a a a a a a a")); 
        #b_turnright.Bind(wx.EVT_BUTTON, lambda e : Keyboard.press("d d d d d d d d d d d")); 
        b_turnleft.Bind(wx.EVT_BUTTON, self.btnEvent(lambda e : Keyboard.hold("a", 0.5))); 
        b_turnright.Bind(wx.EVT_BUTTON, self.btnEvent(lambda e : Keyboard.hold("d", 0.5))); 

        b_walk       = wx.Button(panel, wx.ID_ANY, "Walk")
        b_stop       = wx.Button(panel, wx.ID_ANY, "Stop")
        b_follow     = wx.Button(panel, wx.ID_ANY, "Follow")
        b_autofollow = wx.ToggleButton(panel, wx.ID_ANY, "L. Follow")
        b_walk.Bind(wx.EVT_BUTTON, self.btnEvent(lambda e : Keyboard.hold("w", 1))); 
        b_stop.Bind(wx.EVT_BUTTON, self.btnEvent(lambda e : Keyboard.press("s"))); 

        def toggleAutoFollow(e):
           self.autoFollow = True if e.IsChecked() else False 
        b_autofollow.Bind(wx.EVT_TOGGLEBUTTON, self.btnEvent(toggleAutoFollow)); 

        b_follow.Bind(wx.EVT_BUTTON, self.btnEvent(lambda e : Keyboard.press("9"))); 

        s = wx.StaticBoxSizer(wx.StaticBox(panel, -1, "Move"), wx.VERTICAL)

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

    def restBtns(self, panel):
        b_eat       = wx.Button(panel, wx.ID_ANY, "Eat")
        b_drink     = wx.Button(panel, wx.ID_ANY, "Drink")
        b_buff      = wx.Button(panel, wx.ID_ANY, "Buff")
        c_nrParty   = wx.Choice(panel,choices = ['1', '2', '3', '4', '5'])
        c_nrParty.SetSelection(1)

        def dobuff(evt):
            Keyboard.press("F2 6")

        b_buff.Bind(wx.EVT_BUTTON, self.btnEvent(dobuff)) 
        b_eat.Bind(wx.EVT_BUTTON, self.btnEvent(lambda e : Keyboard.press("minus"))) 
        b_drink.Bind(wx.EVT_BUTTON, self.btnEvent(lambda e : Keyboard.press("equal"))) 

        s = wx.StaticBoxSizer(wx.StaticBox(panel, -1, "Rest"), wx.VERTICAL)

        s1 = wx.BoxSizer(wx.HORIZONTAL)
        s1.Add(c_nrParty, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s1.Add(b_buff, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s.Add(s1, 1, wx.EXPAND)

        s1 = wx.BoxSizer(wx.HORIZONTAL)
        s1.Add(b_eat, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s1.Add(b_drink, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s.Add(s1, 1, wx.EXPAND)

        return s

    def potionBtns(self, panel):
        b_manapot       = wx.Button(panel, wx.ID_ANY, "Mana")
        b_healthpot     = wx.Button(panel, wx.ID_ANY, "Health")

        b_healthpot.Bind(wx.EVT_BUTTON, self.btnEvent(lambda e : Keyboard.press("Ctrl+minus"))); 
        b_manapot.Bind(wx.EVT_BUTTON, self.btnEvent(lambda e : Keyboard.press("Ctrl+equal"))); 

        s = wx.StaticBoxSizer(wx.StaticBox(panel, -1, "Potions"), wx.VERTICAL)

        s1 = wx.BoxSizer(wx.HORIZONTAL)
        s1.Add(b_manapot, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s1.Add(b_healthpot, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        s.Add(s1, 1, wx.EXPAND)

        return s

    def autoFollow(self, fn):
        def handler(e):
            fn(e)
            if self.autoFollow and not e.IsChecked() :
                Keyboard.press("9"); 

        return handler


    def actionBtns(self, panel):
        b_target    = wx.Button(panel, wx.ID_ANY, "Target")
        b_burn      = wx.ToggleButton(panel, wx.ID_ANY, "Burn")
        b_freeze    = wx.ToggleButton(panel, wx.ID_ANY, "Freeze")
        b_wand      = wx.Button(panel, wx.ID_ANY, "Wand")

        b_target.Bind(wx.EVT_BUTTON, self.btnEvent(lambda e : Keyboard.press("F2 f"))); 
        b_burn.Bind(wx.EVT_TOGGLEBUTTON, self.btnEvent(self.autoFollow(lambda e : self.keyboard.rotate("mage/burn") if e.IsChecked() else self.keyboard.stopRotate()))); 
        b_freeze.Bind(wx.EVT_TOGGLEBUTTON, self.btnEvent(self.autoFollow(lambda e : self.keyboard.rotate("mage/freeze") if e.IsChecked() else self.keyboard.stopRotate()))); 
        b_wand.Bind(wx.EVT_BUTTON, self.btnEvent(lambda e : Keyboard.press("F2 f 5"))); 

        s = wx.StaticBoxSizer(wx.StaticBox(panel, -1, "Action"), wx.VERTICAL)

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

        return s

    def addButtons(self, panel):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.restBtns(panel), 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        sizer.Add(self.potionBtns(panel), 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        sizer.Add(self.moveBtns(panel), 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)
        sizer.Add(self.actionBtns(panel), 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 2)

        panel.SetSizerAndFit(sizer)
        sizer.SetSizeHints(self)

if __name__ == '__main__':
    app = wx.App()
    frm = ClientFrame(None, title="Mage Bot")
    frm.Show()
    app.MainLoop()
