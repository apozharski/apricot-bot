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
    parser.add_argument('--clean-spot', default=1, type=int, help='Location of the clean water basin')
    parser.add_argument('--rinse-spot', default=2, type=int, help='Location of the rinse water basin')
    parser.add_argument('--ncyc', default=5, type=int, help='Number of cycles')
    parser.add_argument('--vol', default=300, type=int, help='Volume to aspirate')
    args = parser.parse_args()
    
    foo = raw_input("CHECK: Clean waterbasin in position "+str(args.clean_spot))
    foo = raw_input("CHECK: Rinse waterbasin in position "+str(args.rinse_spot))

    plates = {
        'robobase'  :   ['../templates/apribot.apb', 0],
        'clean'      :   ['../templates/wash.apb',args.clean_spot],
        'rinse'   :   ['../templates/wash.apb',args.rinse_spot],
        }
    roboperator = set_the_stage(plates)

    for washcycle in range(args.ncyc):
        roboperator.aspirateRCT('clean', (1, 1, 1), 250)
        roboperator.emptyRCT('rinse', (1, 1, 2))
    
    roboperator.home()

if __name__ == "__main__":
    main()



