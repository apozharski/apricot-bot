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

    parser.add_argument('--plate-spot', default=1, type=int, help='Location of the plate')
    parser.add_argument('--control-col', default=1, type=int, help='Column with controls')
    parser.add_argument('--sample-col', default=2, type=int, help='Column with samples')
    parser.add_argument('--reagent-spot', default=2, type=int, help='Location of the reagent block')
    parser.add_argument('--reagent-col', default=1, type=int, help='Column with the reagent')
    parser.add_argument('--bsa-row', default=1, type=int, help='Column with the reagent')
    parser.add_argument('--sample-row', default=5, type=int, help='Column with the reagent')
    parser.add_argument('--tube-spot', default=3, type=int, help='Location of the sample tube holder')


    args = parser.parse_args()
    args.plate_spot -= 1
    args.tube_spot -= 1
    args.control_col -= 1
    args.reagent_spot -= 1
    args.sample_col -= 1
    args.reagent_col -= 1
    args.bsa_row -= 1
    args.sample_row -= 1
    

    robot = TheBot()
    base = ApriTarget()
    fname = '../templates/nunc96.apb'
    pspots = load_template('../templates/apribot.apb',base,'spot')
    prows = load_template(fname,pspots,'rows')
    pcols = load_template(fname,prows,'cols')
    ptips = load_template(fname,pcols,'tips')
    ppiston = load_template('../templates/apribot.apb',ptips,'tips')
    fname = '../templates/greiner_masterblock.apb'
    rspots = load_template('../templates/apribot.apb',base,'spot')
    rrows = load_template(fname,rspots,'rows')
    rcols = load_template(fname,rrows,'cols')
    rtips = load_template(fname,rcols,'tips')
    rpiston = load_template('../templates/apribot.apb',rtips,'tips')
    fname = '../templates/greiner_masterblock_small_tubes.apb'
    tspots = load_template('../templates/apribot.apb',base,'spot')
    trows = load_template(fname,tspots,'rows')
    tcols = load_template(fname,trows,'cols')
    ttips = load_template(fname,tcols,'tips')
    tpiston = load_template('../templates/apribot.apb',ttips,'tips')

    pspots.set_pos(args.reagent_spot)
    rspots.set_pos(args.plate_spot)
    tspots.set_pos(args.tube_spot)
    psafez = ptips.safez
    safez = min(rtips.safez, ptips.safez)
    rtips.set_safez(safez)
    ptips.set_safez(safez)
    
    rtips.moveup(1)
    rcols.set_pos(args.reagent_col)
    
    rpiston.safe_goto(robot)
    rpiston.moveup(250,robot)
    ppiston.moveup(250)
    
    pcols.set_pos(args.control_col)
    ptips.moveup(1)
    ppiston.safe_goto(robot)
    ppiston.movedn(125, robot)
    pcols.set_pos(args.sample_col)
    ptips.moveup(2)
    ppiston.safe_goto(robot)
    robot.phomedn()
    ptips.moveup(100)
    ppiston.set_pos(0, robot)
    rpiston.set_pos(0)
    
    robot.zhome()

    foo = raw_input('Now zero the plate.  Press ENTER when returned.')
    foo = raw_input('Make sure only one tip remains in front.')

    ptips.set_safez(psafez)
    ptips.set_pos(1)
    pcols.set_pos(args.control_col)
    prows.set_pos(0)
    for i in range(8):
        ppiston.safe_goto(robot)
        ppiston.moveup(i+1, robot)
        prows.moveup()
    pcols.set_pos(args.sample_col)
    prows.set_pos(0)
    for i in range(8):
        ppiston.safe_goto(robot)
        ppiston.moveup(i+1, robot)
        prows.moveup()

    robot.zhome()
    foo = raw_input('Provide wash container.')
    
    robot.phomedn()
    foo = raw_input('Replace the tip.')

    ptips.set_pos(100)
    ppiston.set_pos(0, robot)
    tpiston.set_pos(0)
    trows.set_pos(args.bsa_row)
    ttips.movedn()
    tpiston.safe_goto(robot)

    tpiston.moveup(50, robot)
    ppiston.set_pos(50)
    ttips.moveup()
    
    ptips.set_pos(1)
    prows.set_pos(0)
    pcols.set_pos(args.control_col,robot)
    for i in range(8):
        ppiston.safe_goto(robot)
        ppiston.movedn(i+1, robot)
        prows.moveup()

    robot.zhome()
    foo = raw_input('Provide wash container.')
    
    robot.phomedn()
    foo = raw_input('Replace the tip.')

    ptips.set_pos(100)
    ppiston.set_pos(0, robot)
    tpiston.set_pos(0)
    trows.set_pos(args.sample_row)
    ttips.movedn()
    tpiston.safe_goto(robot)

    tpiston.moveup(50, robot)
    ttips.moveup()
    ppiston.set_pos(50)

    
    ptips.set_pos(1)
    prows.set_pos(0)
    pcols.set_pos(args.sample_col)
    for i in range(8):
        ppiston.safe_goto(robot)
        ppiston.movedn(i+1, robot)
        prows.moveup()

    robot.home()

if __name__ == "__main__":
    main()
