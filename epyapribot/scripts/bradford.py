#!/usr/bin/env python

import sys
sys.path.append('../../epyapribot')
from abot import TheBot
from target import load_template, ApriTarget, Plate
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

    robot = TheBot()
    base = ApriTarget()
    
    plates = {
        'test'      :   Plate('../templates/nunc96.apb', base),
        'reagent'   :   Plate('../templates/greiner_masterblock.apb', base),
        'sample'    :   Plate('../templates/greiner_masterblock_small_tubes.apb', base),
        }
    roboperator = Stage(plates, robot)
    roboperator.SetSpots({'test': args.plate_spot, 'reagent': args.reagent_spot, 'sample': args.tube_spot})

    roboperator.SetRCT('reagent', (1,args.reagent_col, 1))
    roboperator.goto('reagent')
    roboperator.aspirate(250)

    sys.exit(0)
    
    pcols.set_pos(args.control_col-1)
    ptips.moveup(1)
    ppiston.safe_goto(robot)
    ppiston.movedn(125, robot)
    pcols.set_pos(args.sample_col-1)
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
    pcols.set_pos(args.control_col-1)
    prows.set_pos(0)
    for i in range(8):
        ppiston.safe_goto(robot)
        ppiston.moveup(i+1, robot)
        prows.moveup()
    pcols.set_pos(args.sample_col-1)
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
    trows.set_pos(args.bsa_row-1)
    ttips.movedn()
    tpiston.safe_goto(robot)

    tpiston.moveup(50, robot)
    ppiston.set_pos(50)
    ttips.moveup()
    
    ptips.set_pos(1)
    prows.set_pos(0)
    pcols.set_pos(args.control_col-1,robot)
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
    trows.set_pos(args.sample_row-1)
    ttips.movedn()
    tpiston.safe_goto(robot)

    tpiston.moveup(50, robot)
    ttips.moveup()
    ppiston.set_pos(50)

    
    ptips.set_pos(1)
    prows.set_pos(0)
    pcols.set_pos(args.sample_col-1)
    for i in range(8):
        ppiston.safe_goto(robot)
        ppiston.movedn(i+1, robot)
        prows.moveup()

    robot.home()

if __name__ == "__main__":
    main()
