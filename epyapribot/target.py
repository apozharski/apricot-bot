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
