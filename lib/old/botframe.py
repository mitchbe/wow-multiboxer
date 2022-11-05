#!/bin/python3

import wx
import sys
import * from tools


#@abstract
class BotFrame(wx.Dialog):
    def __init__(self, *args, **kw):
        super(BotFrame, self).__init__(*args, **kw)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        
        self.widget_panel = wx.Panel(self, wx.ID_ANY)
        self.focus_panel  = wx.Panel(self, wx.ID_ANY)

        self.add_buttons()
        self.bind_keys()
        self.set_focus()

    def set_focus(self):
        self.focusPanel.SetFocus()

    def no_focus_event(self, fn):
        def dofn(e):
            fn(e)
            self.set_focus()
        return dofn

    #@abstract
    def add_buttons(self, panel):
        pass

    #@abstract
    def bind_keys(self):
        pass
        #self.focusPanel.Bind(wx.EVT_KEY_UP, self.keyUp)
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
        #self.keyboard.stopRotate()
        self.Destroy()



