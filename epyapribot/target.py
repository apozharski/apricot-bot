class ApriTarget(object):

    def __init__(self, parms, *args, **kwds):
        for key, value in parms.iteritems():
            try:
                exec('self.'+key+'='+str(value))
            except NameError:
                exec('self.'+key+'="'+str(value)+'"')
