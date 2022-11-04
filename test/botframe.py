#!/bin/python3

import wx
import sys
import tools import *


if (len(sys.argv) == 2) :
    BOT1_WIN_ID = sys.argv[1]
    BOT2_WIN_ID = None
else if (len(sys.argv) == 3) : 
    BOT1_WIN_ID = sys.argv[1]
    BOT2_WIN_ID = sys.argv[2]
else 
    print("Window ID Required for BOT")
    exit(1)




#@abstract
class BotFrame(wx.Dialog):
    def __init__(self, *args, **kw):
        super(BotFrame, self).__init__(*args, **kw)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        
        self.bot1_input = Input(BOT1_WIN_ID)
        self.bot2_input = Input(BOT2_WIN_ID)

        self.widget_panel = wx.Panel(self, wx.ID_ANY)
        self.focus_panel  = wx.Panel(self, wx.ID_ANY)
        self.__add_buttons()
        self.__bind_keys()
        self.__fix_focus()

    def __fix_focus(self):
        self.focus_panel.SetFocus()

    def btnEvent(self, fn):
        def dofn(e):
            fn(e)
            self.fixFocus()
        return dofn

    #@abstract
    def addButtons(self, panel):
        raise NotImplementedError()

    #@abstract
    def bindKeys(self):
        raise NotImplementedError()
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
        self.keyboard.stopRotate()
        self.Destroy()



