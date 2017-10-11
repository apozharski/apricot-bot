#!/usr/bin/env python

import sys
sys.path.append('../../epyapribot')
from abot import TheBot
from target import load_template, ApriTarget, Plate, Stage
from argparse import ArgumentParser, RawDescriptionHelpFormatter
def main():
    headerhelp = \
'''
'''
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                        description=headerhelp)

    parser.add_argument('--plate-spot', default=2, type=int, help='Location of the plate')
    parser.add_argument('--control-col', default=1, type=int, help='Column with controls')
    parser.add_argument('--sample-col', default=2, type=int, help='Column with samples')
    parser.add_argument('--reagent-spot', default=3, type=int, help='Location of the reagent block')
    parser.add_argument('--reagent-col', default=1, type=int, help='Column with the reagent')
    parser.add_argument('--bsa-row', default=1, type=int, help='Row with the BSA tube')
    parser.add_argument('--sample-row', default=5, type=int, help='Row with the sample tube')
    parser.add_argument('--tube-spot', default=4, type=int, help='Location of the sample tube holder')

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

    roboperator.SetRCT('reagent', (1, args.reagent_col, 2))
    roboperator.aspirate('reagent', 250)
    roboperator.SetRCT('test', (1, args.control_col, 3))
    roboperator.dispense('test', 125)
    roboperator.SetRCT('test', (1, args.sample_col, 3))
    roboperator.empty('test')

    foo = raw_input('Now zero the plate.  Press ENTER when returned.')
    foo = raw_input('Make sure only one tip remains in front.')

    for i in range(1,9):
        roboperator.SetRCT('test', (i, args.control_col, 1))
        roboperator.aspirate('test', 2*i)
    for i in range(1,9):
        roboperator.SetRCT('test', (i, args.sample_col, 1))
        roboperator.aspirate('test', 2*i)
    roboperator.SetRCT('reagent', (1, args.reagent_col, 6))
    roboperator.empty('reagent')

    roboperator.SetRCT('sample', (9-args.bsa_row, 1, 1))
    roboperator.aspirate('sample', 80)
    for i in range(1,9):
        roboperator.SetRCT('test', (i, args.control_col, 1))
        roboperator.dispense('test', 2*i)
    roboperator.SetRCT('sample', (9-args.bsa_row, 1, 2))
    roboperator.empty('sample')
    
    roboperator.SetRCT('sample', (9-args.sample_row, 1, 1))
    roboperator.aspirate('sample',80)
    for i in range(1,9):
        roboperator.SetRCT('test', (i, args.sample_col, 1))
        roboperator.dispense('test', 2*i)
    roboperator.SetRCT('sample', (9-args.sample_row, 1, 2))
    roboperator.empty('sample')

    robot.home()

if __name__ == "__main__":
    main()
