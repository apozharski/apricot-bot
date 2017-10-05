import re
class ApriTarget(object):
    def __init__(self, parent=None, *args, **kwds):
        self.parent = parent
        self.xargs = args
        self.xkwds = kwds
        self.x = 0
        self.y = 0
        self.z = 0
        self.v = 0
    def get_xyzv(self):
        if self.parent is None:
            return self.x,self.y,self.z,self.v
        else:
            x,y,z,v = self.parent.get_xyzv()
            return x+self.x,y+self.y,z+self.z,v+self.v
    def goto(self, bot=None):
        if bot is not None:
            bot.goto(xyzv=self.get_xyzv())

class ApriTarget1D(ApriTarget):
    def __init__(self, parent=None, start=0, delta=0, nspots=1, pos = 0, *args, **kwds):
        super(ApriTarget1D, self).__init__(parent, *args, **kwds)
        self.start = start
        self.delta = delta
        self.nspots = nspots
        self.pos = max(min(pos, nspots-1), 0)
        self.set_xyzv()
    def get_value(self):
        return self.start + self.pos*self.delta
    def set_pos(self, pos, bot=None):
        self.pos = max(min(pos, self.nspots-1), 0)
        self.set_xyzv()
        self.goto(bot)
    def moveup(self, ns=1, bot=None):
        self.set_pos(self.pos+ns, bot)
    def movedn(self, ns=1, bot=None):
        self.set_pos(self.pos-ns, bot)

class ApriTargetX(ApriTarget1D):
    def __init__(self, parent=None, dx=0, nx=1, posx = 0, *args, **kwds):
        super(ApriTargetX, self).__init__(parent, dx, nx, posx, *args, **kwds)
    def set_xyzv(self):
        self.x = self.get_value()

class ApriTargetY(ApriTarget1D):
    def __init__(self, parent=None, dy=0, ny=1, posy = 0, *args, **kwds):
        super(ApriTargetY, self).__init__(parent, dy, ny, posy, *args, **kwds)
    def set_xyzv(self):
        self.y = self.get_value()

class ApriTargetZ(ApriTarget1D):
    def __init__(self, parent=None, dz=0, nz=1, posz = 0, *args, **kwds):
        super(ApriTargetZ, self).__init__(parent, dz, nz, posz, *args, **kwds)
    def set_xyzv(self):
        self.z = self.get_value()

def load_template(fname, parent=None, label=None):
    if label is None:
        label = ''
    with open(fname) as fin:
        ptrn_def = re.compile("^"+label+":([a-zA-Z0-9]*) *([a-zA-Z0-9-]*)")
        defns = dict([(x[0].lower(),x[1]) for x in [x.groups() for x in map(ptrn_def.match, fin.readlines()) if x]])
    print defns
    axtype = defns.pop('axis', None)
    if axtype == 'X':
        target = ApriTargetX
    elif axtype == 'Y':
        target = ApriTargetY
    elif axtype == 'Z':
        target = ApriTargetZ
    else:
        raise(ValueError('Unknown target axis: '+axtype))
    start = int(defns.pop('start',0))
    delta = int(defns.pop('delta',0))
    nspots = int(defns.pop('nspots',1))
    return target(parent, start, delta, nspots)

