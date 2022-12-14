#!/bin/python3

import wx
import sys
import shlex,subprocess
from botlib import * 

class PriestFrame(BotFrame):
    def __init__(self, *args, **kw):
        super(PriestFrame, self).__init__(*args, **kw)

    def addButtons(self):
        pnl = wx.Panel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)

        b_healme   = wx.Button(pnl, wx.ID_ANY, "Heal Me")
        b_healself = wx.Button(pnl, wx.ID_ANY, "Heal Self")
        b_follow   = wx.Button(pnl, wx.ID_ANY, "Follow")
        b_stop     = wx.Button(pnl, wx.ID_ANY, "Stop")
        b_jump     = wx.Button(pnl, wx.ID_ANY, "Jump")
        b_rot1     = wx.ToggleButton(pnl, wx.ID_ANY, "Rot. 1")
        b_rot2     = wx.ToggleButton(pnl, wx.ID_ANY, "Rot. 2")

        b_healme.Bind(wx.EVT_BUTTON, lambda e : Keyboard.press("F2 6")); 
        b_healself.Bind(wx.EVT_BUTTON, lambda e : Keyboard.press("F1 6")); 
        b_follow.Bind(wx.EVT_BUTTON, lambda e : Keyboard.press("F2 slash f Return")); 
        b_stop.Bind(wx.EVT_BUTTON, lambda e : Keyboard.press("s")); 
        b_jump.Bind(wx.EVT_BUTTON, lambda e : Keyboard.press("space")); 
        b_rot1.Bind(wx.EVT_TOGGLEBUTTON, lambda e : self.keyboard.rotate("rotation1") if e.IsChecked() else self.keyboard.stopRotate()); 
        b_rot2.Bind(wx.EVT_TOGGLEBUTTON, lambda e : self.keyboard.rotate("rotation2") if e.IsChecked() else self.keyboard.stopRotate()); 

        sizer.Add(b_healme)
        sizer.Add(b_healself)
        sizer.Add(b_follow)
        sizer.Add(b_stop)
        sizer.Add(b_jump)
        sizer.Add(b_rot1)
        sizer.Add(b_rot2)

        pnl.SetSizerAndFit(sizer)
        sizer.SetSizeHints(self)

if __name__ == '__main__':
    app = wx.App()
    frm = PriestFrame(None, title="Priest Bot")
    frm.Show()
    app.MainLoop()
