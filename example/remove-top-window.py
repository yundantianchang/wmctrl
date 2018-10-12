#!/usr/bin/env python3

import wmctrl
for win in wmctrl.Window.by_class('thunder.exe.Wine'):
    if win.x == 0 and win.y == 0 and win.wm_name == "":
        wmctrl.Window.resize_and_move(win, 0, 0, 1, 1)
        wmctrl.Window.set_properties(win, ("remove", "above"))
