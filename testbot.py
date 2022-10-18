#!/bin/python3

import wx
import sys
import shlex,subprocess
import botlib
from botlib import * 


class ClientFrame(BotFrame):
    def __init__(self, *args, **kw):
        super(ClientFrame, self).__init__(*args, **kw)


if __name__ == '__main__':
    app = wx.App()
    frm = ClientFrame(None, title="Mage Bot")
    frm.Show()
    app.MainLoop()
