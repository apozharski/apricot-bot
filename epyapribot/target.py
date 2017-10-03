class ApriTarget(object):
    def __init__(self, bot, *args, **kwds):
        self.abot = abot
        self.nx = kwds.pop('nx', None)
        self.ny = kwds.pop('ny', None)
        self.dx = kwds.pop('dx', None)
        self.dy = kwds.pop('dy', None)
        self.name = kwds.pop('name',None)
        self.xkwds = kwds
    def goto(self, *args, **kwds):
        if self.name is None:
            self.bot.home()

class ApriTarg1D(ApriTarget):
    def goto(self, position):
        self.bot.xgoto(position*dx)
