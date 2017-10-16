#!/usr/bin/env python

import sys
sys.path.append('../../epyapribot')
from abot import TheBot
from target import set_the_stage
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

    foo = raw_input("CHECK: Test plate (Nunc-96) in position "+str(args.plate_spot))
    foo = raw_input("CHECK: Bradford reagent DeepWell block in position "+str(args.reagent_spot))
    foo = raw_input("CHECK: At least 300ul of Bradford reagent in column "+str(args.reagent_col))
    foo = raw_input("CHECK: PCR plate DeepWell block in position "+str(args.tube_spot))
    foo = raw_input("CHECK: At least 100ul of BSA sample in column 1, row "+str(args.bsa_row))
    foo = raw_input("CHECK: At least 100ul of protein sample in column 1, row "+str(args.sample_row))
    foo = raw_input("Hit Enter to start")

    plates = {
        'test'      :   ['../templates/nunc96.apb',args.plate_spot],
        'reagent'   :   ['../templates/greiner_masterblock.apb',args.reagent_spot],
        'sample'    :   ['../templates/greiner_masterblock_pcr96.apb',args.tube_spot],
        }
    roboperator = set_the_stage(plates)

    roboperator.aspirateRCT('reagent', (1, args.reagent_col, 2), 250)
    roboperator.dispenseRCT('test', (1, args.control_col, 2), 125)
    roboperator.dispenseRCT('test', (1, args.sample_col, 2), 125)
    roboperator.emptyRCT('reagent', (1, args.reagent_col, 4))

    foo = raw_input('Now zero the plate.  Press ENTER when returned.')
    foo = raw_input('Make sure only one tip remains in front.')

    for i in range(1,9):
        roboperator.aspirateRCT('test', (i, args.control_col, 2), 2*i)
    for i in range(1,9):
        roboperator.aspirateRCT('test', (i, args.sample_col, 2), 2*i)
    roboperator.emptyRCT('reagent', (1, args.reagent_col, 6))

    roboperator.aspirateRCT('sample', (9-args.bsa_row, 1, 1), 80)
    for i in range(1,9):
        roboperator.dispenseRCT('test', (i, args.control_col, 2), 2*i)
    roboperator.emptyRCT('sample', (9-args.bsa_row, 1, 2))
    
    roboperator.aspirateRCT('sample', (9-args.sample_row, 1, 1), 80)
    for i in range(1,9):
        roboperator.dispenseRCT('test', (i, args.sample_col, 2), 2*i)
    roboperator.emptyRCT('sample', (9-args.sample_row, 1, 2))

    roboperator.home()

if __name__ == "__main__":
    main()
