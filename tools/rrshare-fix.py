#!/usr/bin/env python3

import wmctrl

for win in wmctrl.Window.by_class('rrshare.exe.Wine'):
    if win.wm_name == "人人影视":
        print(win)
        wmctrl.Window.decorate(win)
        # wmctrl.Window.undecorate(win)
