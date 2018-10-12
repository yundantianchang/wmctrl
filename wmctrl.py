#!/usr/bin/env python3

import os
from subprocess import getoutput
from collections import namedtuple


BaseWindow = namedtuple('Window', 'id desktop pid x y w h wm_class host wm_name wm_window_role wm_state')

class Window(BaseWindow):

    @classmethod
    def list(cls):
        out = getoutput('wmctrl -l -G -p -x')
        windows = []
        for line in out.splitlines():
            parts = line.split(None, len(Window._fields)-3)
            if len(parts) == 9: # title is missing
                parts.append('')
            parts = list(map(str.strip, parts))
            parts[1:7] = list(map(int, parts[1:7]))
            parts.append(_wm_window_role(parts[0]))
            parts.append(_wm_state(parts[0]))
            windows.append(cls(*parts))
        return windows

    @classmethod
    def by_name(cls, name):
        return [win for win in cls.list() if win.wm_name == name]

    @classmethod
    def by_name_endswith(cls, name):
        return [win for win in cls.list() if win.wm_name.endswith(name)]

    @classmethod
    def by_name_startswith(cls, name):
        return [win for win in cls.list() if win.wm_name.startswith(name)]

    @classmethod
    def by_role(cls, role):
        return [win for win in cls.list() if win.wm_window_role == role]

    @classmethod
    def by_class(cls, wm_class):
        return [win for win in cls.list() if win.wm_class == wm_class]

    @classmethod
    def by_id(cls, id):
        return [win for win in cls.list() if int(win.id, 16) == id]

    @classmethod
    def get_active(cls):
        out = getoutput("xprop -root _NET_ACTIVE_WINDOW")
        parts = out.split()
        try:
            id = int(parts[-1], 16)
        except ValueError:
            return None
        lst = cls.by_id(id)
        if not lst:
            return None
        assert len(lst) == 1
        return lst[0]

    def activate(self):
        os.system('wmctrl -id -a %s' % self.id)

    def resize_and_move(self, x, y, w, h):
        mvarg = '0,%d,%d,%d,%d' % (x, y, w, h)
        os.system('wmctrl -i -r %s -e %s' % (self.id, mvarg))

    def set_geometry(self, geometry):
        dim, pos = geometry.split('+', 1)
        w, h = list(map(int, dim.split('x')))
        x, y = list(map(int, pos.split('+')))
        self.resize_and_move(x, y, w, h)

    def set_properties(self,properties):
        proparg = ",".join(properties)
        os.system('wmctrl -i -r %s -b %s' % (self.id,proparg))

    def moveto_desktop(self, desktopn):
        # begin with 0
        os.system('wmctrl -i -r %s -t %s' % (self.id, desktopn - 1))

    def hide(self):
        os.system('xdotool windowunmap %s' % (self.id,))

    def show(self):
        os.system('xdotool windowmap %s' % (self.id,))


def _wm_window_role(winid):
    out = getoutput('xprop -id %s WM_WINDOW_ROLE' % winid)
    try:
        _, value = out.split(' = ')
    except ValueError:
        # probably xprop returned an error
        return ''
    else:
        return value.strip('"')

def strip_prefix (prefix, word):
    if word.startswith(prefix):
        return word[len(prefix):]
    return word

def _wm_state (winid):
    out = getoutput('xprop -id %s _NET_WM_STATE' % winid)
    try:
        _, value = out.split(' = ')
    except ValueError:
        # probably xprop returned an error
        return []
    else:
        return [strip_prefix("_NET_WM_STATE_",s).lower()
                for s in value.split(', ')]
