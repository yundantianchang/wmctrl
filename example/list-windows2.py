#!/usr/bin/env python3

import wmctrl

for win in wmctrl.Window.list():
    print(win)
