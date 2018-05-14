#!/usr/bin/env python

import sys
sys.path.append('../../epyapribot')
from abot import TheBot
from target import set_the_stage
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from scipy import cumsum, arange, around, sign, ones
def main():
    headerhelp = \
'''
'''
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                        description=headerhelp)
    parser.add_argument('--plate-spot', default=3, type=int, help='Location of the plate')
    parser.add_argument('--stock-spot', default=2, type=int, help='Location of the stocks')
    parser.add_argument('--wash-row', type=int, help='Row of the stock block for washing the tips')
    parser.add_argument('--wash-spot', type=int, help='Location of the rinse water basin')
    parser.add_argument('-g', '--grad', action='append', help='Gradient definitions: stockRow,topVolume,bottomVolume,topRow,bottomRow,colShift')
    parser.add_argument('--xv', default=5, type=int, help='Overhead volume')
    parser.add_argument('--maxv', default=300, type=int, help='Maximum volume')
    parser.add_argument('--cush-vol', default=50, type=int, help='Cushion volume')
    parser.add_argument('--dry-run', action='store_true', help='Dry run.')
    parser.add_argument('--manual-wash', action='store_true', help='Wash tips manually (may be faster)')
    parser.add_argument('--plate-type', default='intelliplate', help='Target plate type, must match an available template')
    parser.add_argument('--stock-type', default='greiner_masterblock', help='Stock plate type, must match an available template')
    parser.add_argument('--sleeptime', default=0, type=int, help='Seconds of delay after aspiration/dispensing')
    
    args = parser.parse_args()
    
    if args.grad is None:
        sys.exit('No gradients are defined. Check your parameters.')
    if args.wash_row is None and args.wash_spot is None and not args.manual_wash:
        foo = raw_input("CHECK: No washing option provided, assume manual wash.")
        args.manual_wash = True
    foo = raw_input("CHECK: Target plate in position "+str(args.plate_spot))
    foo = raw_input("CHECK: Stock DeepWell block in position "+str(args.stock_spot))
    if args.wash_row is not None and args.wash_spot is not None:
        foo = raw_input("CHECK: Both block and basin washes resuested.  Assume basin wash.")
        args.wash_row = None
    if args.wash_row is not None:
        foo = raw_input("CHECK: Wash row (%d) of the stock block is filled with water" % args.wash_row)
    if args.wash_spot is not None:
        foo = raw_input("CHECK: Wash basin in position "+str(args.wash_spot))

    plates = {
        'robobase'  :   ['../templates/apribot.apb', 0],
        'plate'     :   ['../templates/'+args.plate_type+'.apb',args.plate_spot],
        'stock'     :   ['../templates/'+args.stock_type+'.apb',args.stock_spot],
        }
    
    if args.wash_spot is not None:
        plates['wash'] = ['../templates/wash.apb',args.wash_spot]
    reqvols = {}
    for grad in args.grad:
        stockRow,topVolume,bottomVolume,topRow,bottomRow,colShift = [int(x) for x in grad.split(',')]
        numRows = abs(topRow-bottomRow)+1
        dispDir = sign(bottomRow-topRow+0.1).astype(int)
        if numRows>1:
            vols = around(topVolume + arange(numRows).astype(float)*(bottomVolume-topVolume)/(numRows-1)).astype(int)
        else:
            vols = topVolume*ones(1).astype(int)
        if (vols>args.maxv).any():
            sys.exit('Aspirated volume limit exceeded for gradient "'+grad+'".  Check your parameters.')
        reqvols[stockRow] = reqvols.get(stockRow,0)+sum(vols)+args.xv
    for key, value in reqvols.iteritems():
        foo = raw_input("CHECK: Stock DeepWell block row %d is filled with %d ul of reagent." % (key, value+args.cush_vol))

    roboperator = set_the_stage(plates, args.dry_run, sleeptime=args.sleeptime)

    for grad in args.grad:
        stockRow,topVolume,bottomVolume,topRow,bottomRow,colShift = [int(x) for x in grad.split(',')]
        numRows = abs(topRow-bottomRow)+1
        dispDir = sign(bottomRow-topRow+0.1).astype(int)
        if numRows>1:
            vols = around(topVolume + arange(numRows).astype(float)*(bottomVolume-topVolume)/(numRows-1)).astype(int)
        else:
            vols = topVolume*ones(1).astype(int)
        reqvols[stockRow] -= sum(vols)+args.xv
        actRows = sum(cumsum(vols)<args.maxv)
        aspVolume = sum(vols[cumsum(vols)<args.maxv])+args.xv
        tipstop = roboperator.good_vpos('stock', sum(vols[actRows:]))
        roboperator.aspirateRCT('stock', (9-stockRow, 1+colShift, tipstop), aspVolume, 'Aspirating %d ul to dispense rows %d to %d...' % (aspVolume, topRow, topRow+(actRows-1)*dispDir))
        sys.stdout.write('Done.\n')
        for iRow in range(topRow,bottomRow+dispDir,dispDir):
            iVol = (iRow-topRow)*dispDir
            if iRow == topRow+actRows*dispDir:
                ind = cumsum(vols[iVol:])<args.maxv
                actRows += sum(ind)
                aspVolume = sum(vols[iVol:][ind])
                tipstop = roboperator.good_vpos('stock', sum(vols[actRows:])+reqvols[stockRow])
                roboperator.aspirateRCT('stock', (9-stockRow, 1+colShift, tipstop), aspVolume, 'Aspirating %d ul to dispense rows %d to %d...' % (aspVolume, iRow, topRow+(actRows-1)*dispDir))
            dispVolume = vols[iVol]
            roboperator.dispenseRCT('plate', (9-iRow, 1+colShift, 2), dispVolume, 'Dispensing %d ul into row %d...' % (dispVolume, iRow))
        roboperator.emptyRCT('stock', (9-stockRow, 1+colShift, 6))
        if args.manual_wash:
            foo = raw_input("Wash and/or replace the tips.  Hit ENTER when done.")
        elif args.wash_row is not None:
            roboperator.washRCT('stock', (9-args.wash_row,1+colShift,2), args.maxv+args.xv)
        elif args.wash_spot is not None:
            roboperator.washRCT('wash', (1,1,1), args.maxv+args.xv)
    
    roboperator.home()

if __name__ == "__main__":
    main()



