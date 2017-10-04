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

class ApriTarget1D(ApriTarget):
    def __init__(self, parent=None, delta=0, nspots=1, pos = 0, *args, **kwds):
        super(ApriTarget1D, self).__init__(parent, *args, **kwds)
        self.delta = delta
        self.nspots = nspots
        self.pos = max(min(pos, nspots-1), 0)
        self.set_xyzv()
    def set_xyzv(self):
        self.x = self.pos*self.delta
    def set_pos(self, pos):
        self.pos = max(min(pos, self.nspots-1), 0)
        self.set_xyzv()
    def moveup(self):
        self.set_pos(self.pos+1)
    def movedn(self):
        self.set_pos(self.pos-1)

class ApriTargetX(ApriTarget1D):
    def __init__(self, parent=None, dx=0, nx=1, posx = 0, *args, **kwds):
        super(ApriTargetX, self).__init__(parent, dx, nx, posx, *args, **kwds)
    def set_xyzv(self):
        self.x = self.pos*self.delta

class ApriTargetY(ApriTarget1D):
    def __init__(self, parent=None, dy=0, ny=1, posy = 0, *args, **kwds):
        super(ApriTargetY, self).__init__(parent, dy, ny, posy, *args, **kwds)
    def set_xyzv(self):
        self.y = self.pos*self.delta

class ApriTargetZ(ApriTarget1D):
    def __init__(self, parent=None, dz=0, nz=1, posz = 0, *args, **kwds):
        super(ApriTargetZ, self).__init__(parent, dz, nz, posz, *args, **kwds)
    def set_xyzv(self):
        self.z = self.pos*self.delta
