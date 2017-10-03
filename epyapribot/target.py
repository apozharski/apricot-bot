class ApriTarget(object):
    def __init__(self, bot, parent=None, *args, **kwds):
        self.bot = bot
        self.parent = parent
        self.xargs = args
        self.xkwds = kwds
        self.x = 0
        self.y = 0
        self.z = 0
        self.v = 0
    def goto(self, x=None, y=None, z=None, v=None):
        if self.parent is None:
            self.bot.goto(x,y,z,v)
        else:
            parent.relgoto(x,y,z,v)
    def relgoto(self, x=None, y=None, z=None, v=None):
        if x is not None:
            self.x += x
        if y is not None:
            self.y += y
        if z is not None:
            self.z += z
        if v is not None:
            self.v += v
        self.goto(x,y,z,v)

class ApriTarg1D(ApriTarget):
    def __init__(self, 
    def goto(self, position):
        self.bot.xgoto(position*dx)
