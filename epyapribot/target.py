import re, sys
from abot import TheBot
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
    def safe_goto(self, bot=None, safez=None):
        if bot is not None:
            if safez is None:
                safez = self.get_safez()
            bot.goto(xyzv=self.get_xyzv(),safez=safez)
    def get_safez(self, safez=0):
        if self.parent is None:
            return safez
        else:
            if 'safez' in dir(self):
                safez = max(safez, self.safez)
            return self.parent.get_safez(safez)
    def set_safez(self, safez):
        self.safez = safez
    def set_parent(self, parent):
        self.parent = parent

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
    def __init__(self, parent=None, dz=0, nz=1, posz = 0, safez=0, vdelta=0, *args, **kwds):
        super(ApriTargetZ, self).__init__(parent, dz, nz, posz, *args, **kwds)
        self.safez = safez
        self.vdelta = vdelta
    def set_xyzv(self):
        self.z = self.get_value()
    def good_vpos(self, vrem):
        if self.vdelta:
            return 1+(10+vrem)/self.vdelta
        else:
            return 1
    def homeup(self, bot=None):
        self.set_pos(self.nspots, bot)
    def homedn(self, bot=None):
        self.set_pos(0, bot)

class ApriTargetV(ApriTarget1D):
    def __init__(self, parent=None, dv=0, nv=35000, posv = 0, *args, **kwds):
        super(ApriTargetV, self).__init__(parent, dv, nv, posv, *args, **kwds)
    def set_xyzv(self):
        self.v = self.get_value()

def load_template(fname, parent=None, label=None):
    if label is None:
        label = ''
    with open(fname) as fin:
        ptrn_def = re.compile("^"+label+":([a-zA-Z0-9]*) *([a-zA-Z0-9-]*)")
        defns = dict([(x[0].lower(),x[1]) for x in [x.groups() for x in map(ptrn_def.match, fin.readlines()) if x]])
    axtype = defns.pop('axis', None)
    if axtype == 'X':
        target = ApriTargetX
    elif axtype == 'Y':
        target = ApriTargetY
    elif axtype == 'Z':
        target = ApriTargetZ
    elif axtype == 'V':
        target = ApriTargetV
    else:
        print fname
        raise(ValueError('Unknown target axis: '+axtype))
    start = int(defns.pop('start',0))
    delta = int(defns.pop('delta',0))
    nspots = int(defns.pop('nspots',1))
    safez = int(defns.pop('safez',0))
    vdelta = int(defns.pop('vdelta',0))
    return target(parent, start, delta, nspots, safez=safez, vdelta=vdelta)

def name_template(fname):
    with open(fname) as fin:
        ptrn_def = re.compile("^name:(.*)")
        tname = (' '.join([x.groups()[0] for x in [ptrn_def.match(x) for x in fin.readlines()] if x])).strip()
    return tname if tname else 'Undefined'

class Plate:
    def __init__(self, fname, robobase, robasename, *args, **kwds):
        self.spots = load_template(robasename,robobase,'spot')
        self.rows = load_template(fname,self.spots,'rows')
        self.cols = load_template(fname,self.rows,'cols')
        self.tips = load_template(fname,self.cols,'tips')
    def SetSpot(self, nspot):
        self.spots.set_pos(nspot-1)
    def SetRow(self, nrow):
        self.rows.set_pos(nrow-1)
    def SetColumn(self, ncol):
        self.cols.set_pos(ncol-1)
    def SetTip(self, ntip):
        self.tips.set_pos(ntip-1)
    def good_vpos(self, vrem):
        return self.tips.good_vpos(vrem)
    def tipup(self, bot=None):
        self.tips.homeup(bot)
    def tipdown(self, bot=None):
        self.tips.homedn(bot)

class Stage:
    def __init__(self, plates, robot, rbname, *args, **kwds):
        self.plates = plates
        self.robot = robot
        self.piston = load_template(rbname,None,'tips')
        self.piston.goto(self.robot)
    def __attach(self, key):
        self.piston.set_parent(self.plates[key].tips)
    def SetSpots(self, spots):
        for key, value in spots.iteritems():
            if value:
                self.plates[key].SetSpot(value)
        self.spotkeys = dict([(x[1].spots.pos,x[0]) for x in self.plates.items()])
    def SetRCT(self, key, values):
        r,c,t = values
        self.plates[key].SetRow(r)
        self.plates[key].SetColumn(c)
        self.plates[key].SetTip(t)
    def goto(self, key):
        oldkey = [x for x in self.plates.keys() if self.plates[x].tips==self.piston.parent]
        if len(oldkey) == 1:
            oldkey = oldkey[0]
            if oldkey == key:
                safez = None
            else:
                f,l = sorted(set([self.plates[key].spots.pos,self.plates[oldkey].spots.pos]))
                spotrange = range(f, l+1)
                safez = min([self.plates[self.spotkeys[x]].tips.get_safez() for x in spotrange])
        else:
            safez = min([x.tips.get_safez() for x in self.plates.values()])
        self.__attach(key)
        self.piston.safe_goto(self.robot, safez)
    def gotoRCT(self, key, rct):
        self.SetRCT(key, rct)
        self.goto(key)
    def aspirate(self, key, value):
        self.goto(key)
        self.piston.moveup(value, self.robot)
    def aspirateRCT(self, key, rct, value, msg=None):
        if msg is not None:
            sys.stdout.write(msg)
        self.SetRCT(key, rct)
        self.aspirate(key, value)
        if msg is not None:
            sys.stdout.write('Done.\n')
    def dispense(self, key, value):
        self.goto(key)
        self.piston.movedn(value, self.robot)
    def dispenseRCT(self, key, rct, value, msg=None, dip=True):
        if msg is not None:
            sys.stdout.write(msg)
        self.SetRCT(key, rct)
        if value > 0:
            self.dispense(key, value)
            if dip:
                self.__tipdip(key)
        if msg is not None:
            sys.stdout.write('Done.\n')
    def empty(self, key):
        self.goto(key)
        if self.robot is not None:
            self.robot.phomedn()
        self.plates[key].tipup()
        self.piston.set_pos(0, self.robot)
    def emptyRCT(self, key, rct):
        sys.stdout.write('Empty the tips...')
        self.SetRCT(key, rct)
        self.empty(key)
        sys.stdout.write('Done.\n')
    def wash(self, key, value, ncyc=5):
        self.goto(key)
        for i in range(ncyc):
            sys.stdout.write('Wash cycle #'+str(i+1)+'\n')
            self.piston.moveup(value, self.robot)
            self.piston.movedn(value, self.robot)
        self.plates[key].tipup()
        self.goto(key)
    def washRCT(self, key, rct, value, ncyc=5):
        sys.stdout.write('Wash the tips...\n')
        self.SetRCT(key, rct)
        self.wash(key, value, ncyc)
        sys.stdout.write('Done.\n')
    def home(self):
        sys.stdout.write('Homing the robot...\n')
        if self.robot is not None:
            self.robot.home()
        sys.stdout.write('Done.\n')
    def good_vpos(self, key, vrem):
        return self.plates[key].good_vpos(vrem)
    def __tipdip(self, key):
        tipos = self.plates[key].tips.pos
        self.plates[key].tipdown()
        self.__attach(key)
        self.piston.goto(self.robot)
        self.plates[key].tips.set_pos(tipos)
        self.piston.goto(self.robot)

def set_the_stage(plates, dry_run=False):
    if not dry_run:
        robot = TheBot()
    else:
        robot = None
    rbase = ApriTarget()
    rbname = [x[0] for x in plates.values() if x[1]==0][0]
    roboperator = Stage(dict([(x[0],Plate(x[1][0],rbase,rbname)) for x in plates.iteritems() if x[1][1]]), robot, rbname)
    roboperator.SetSpots(dict([(x[0],x[1][1]) for x in plates.iteritems() if x[1][1]]))
    return roboperator
