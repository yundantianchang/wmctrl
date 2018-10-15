#!/usr/bin/env python3

import wmctrl

for win in wmctrl.Window.by_class('thunder.exe.Wine'):
    if win.x == 0 and win.y == 0 and win.wm_name == "":
        print(win)
        wmctrl.Window.hide(win)
