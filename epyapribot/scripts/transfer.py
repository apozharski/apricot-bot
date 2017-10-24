#!/usr/bin/env python

import sys
sys.path.append('../../epyapribot')
from target import set_the_stage
from argparse import ArgumentParser, RawDescriptionHelpFormatter
def main():
    headerhelp = \
'''
'''
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                        description=headerhelp)
    parser.add_argument('--plate-spot', default=3, type=int, help='Location of the plate')
    parser.add_argument('--stock-spot', default=2, type=int, help='Location of the stocks')
    parser.add_argument('--wash-spot', default=1, type=int, help='Location of the rinse water basin')
    parser.add_argument('-v', '--volume', type=int, help='Volume to be transferred.')
    parser.add_argument('--stock-volume', type=int, default=0, help='Volume currently in the stock block')
    parser.add_argument('--maxv', default=300, type=int, help='Maximum volume')
    parser.add_argument('--xv', default=5, type=int, help='Overhead volume')
    parser.add_argument('--dry-run', action='store_true', help='Dry run.')
    parser.add_argument('--plate-type', default='intelliplate', help='Target plate type, must match an available template')
    parser.add_argument('--stock-type', default='greiner_masterblock', help='Stock plate type, must match an available template')
    parser.add_argument('--manual-wash', action='store_true', help='Wash tips manually (may be faster)')
    parser.add_argument('--tipstop', type=int, help="Manual tip stop point")
    args = parser.parse_args()
    
    if args.volume is None:
        sys.exit('Volume to transfer unknown. Check your parameters.')
    foo = raw_input("CHECK: Target plate in position "+str(args.plate_spot))
    foo = raw_input("CHECK: Stock DeepWell block in position "+str(args.stock_spot))
    foo = raw_input("CHECK: Wash basin in position "+str(args.wash_spot))

    plates = {
        'plate'     :   ['../templates/'+args.plate_type+'.apb',args.plate_spot],
        'stock'     :   ['../templates/'+args.stock_type+'.apb',args.stock_spot],
        'wash'      :   ['../templates/wash.apb',args.wash_spot],
        }
    roboperator = set_the_stage(plates, args.dry_run)

    if args.tipstop is None:
        tipstop = roboperator.good_vpos('stock', args.stock_volume)
    else:
        tipstop = args.tipstop
    roboperator.aspirateRCT('stock', (1, 1, tipstop), args.volume+args.xv, 'Aspirating %d ul ...' % (args.volume+args.xv))
    roboperator.dispenseRCT('plate', (1, 1, 2), args.volume, 'Dispensing %d ul ...' % (args.volume))
    roboperator.emptyRCT('stock', (1, 1, tipstop))
    if args.manual_wash:
        foo = raw_input("Wash and/or replace the tips.  Hit ENTER when done.")
    else:
        roboperator.washRCT('wash', (1,1,1), args.maxv+args.xv)

    
    roboperator.home()

if __name__ == "__main__":
    main()



