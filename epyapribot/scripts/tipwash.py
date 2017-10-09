#!/usr/bin/env python

import sys
sys.path.append('../../epyapribot')
from abot import TheBot
from target import load_template, ApriTarget
from argparse import ArgumentParser, RawDescriptionHelpFormatter
def main():
    headerhelp = \
'''
'''
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                        description=headerhelp)
    parser.add_argument('--clean-spot', default=1, help='Location of the clean water basin')
    parser.add_argument('--rinse-spot', default=2, help='Location of the rinse water basin')
    parser.add_argument('--ncyc', default=5, help='Number of cycles')
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
    piston = load_template('../templates/apribot.apb',washtips,'tips')

    for washcycle in range(args.ncyc):
        washspots.set_pos(args.clean_spot)
        piston.safe_goto(robot)
        washtips.movedn()
        piston.moveup(300, robot)
        washspots.set_pos(args.rinse_spot)
        piston.safe_goto(robot)
        robot.phomedn()
        piston.movedn(300)

if __name__ == "__main__":
    main()



