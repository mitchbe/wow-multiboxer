# wow-multiboxer
World of Warcraft Multiboxing Bot

A very simple tool to assist in multiboxing World of Warcraft. This tool provides a control dialog with buttons to direct keystrokes to the multibox client. 

In order for the World of Warcraft client to receive to keystrokes it must be in focus, which is no good for multiboxing. The WoW client can be tricked to think it's always in focus on wine/Linux by removing the implementation of focus_out in dlls/winex11.drv/event.c and recompiling wine (32-bit). ie: 

static void focus_out( Display *display , HWND hwnd ) { return; }  

Best to keep the modified wine to its own user account just for this purpose or it will probably mess up your .wine folder. 
