#!/usr/bin/env python3

import wmctrl

for win in wmctrl.Window.by_class('wechat.exe.Wine'):
    if win.wm_name == "" or win.wm_name == "ChatContactMenu":
        print(win)
        wmctrl.Window.hide(win)
