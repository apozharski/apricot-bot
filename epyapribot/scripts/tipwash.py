#!/usr/bin/env python

from ..abot import TheBot
from ..target import load_template, ApriTarget
from argparse import ArgumentParser, RawDescriptionHelpFormatter
def main():
    headerhelp = \
'''
'''
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                        description=headerhelp)
    parser.add_argument('--clean-spot', default=1, help='Location of the clean water basin')
    parser.add_argument('--rinse-spot', default=2, help='Location of the rinse water basin')
    args = parser.parse_args()
    args.clean_spot -= 1
    args.rinse_spot -= 1

    robot = TheBot()
    base = ApriTarget()
    fname = '../templates/wash.apb'
    washspots = load_template('../templates/apribot.apb',base,'spot')
    washrows = load_template(fname,washspots,'rows')
    washcols = load_template(fname,washrows,'cols')
    washtips = load_template(fname,washcols,'tips')
    
    washspots.set_pos(args.rinse_spot

    washtips.safe_goto(robot)

if __name__ == "__main__":
    main()



