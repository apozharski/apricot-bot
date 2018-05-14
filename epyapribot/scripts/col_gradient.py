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
    parser.add_argument('--wash-col', type=int, help='Column of the stock block for washing the tips')
    parser.add_argument('--wash-spot', type=int, help='Location of the rinse water basin')
    parser.add_argument('-g', '--grad', action='append', help='Gradient definitions: stockCol,firstVolume,lastVolume,firstCol,lastCol,rowShift')
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
    foo = raw_input("CHECK: Target plate in position "+str(args.plate_spot))
    foo = raw_input("CHECK: Stock DeepWell block in position "+str(args.stock_spot))
    if args.wash_col is None and args.wash_spot is None and not args.manual_wash:
        foo = raw_input("CHECK: No washing option provided, assume manual wash.")
        args.manual_wash = True
    if args.wash_col is not None and args.wash_spot is not None:
        foo = raw_input("CHECK: Both block and basin washes resuested.  Assume basin wash.")
        args.wash_col = None
    if args.wash_col is not None:
        foo = raw_input("CHECK: Wash column (%d) of the stock block is filled with water" % args.wash_col)
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
        stockCol,firstVolume,lastVolume,firstCol,lastCol,rowShift = [int(x) for x in grad.split(',')]
        numCols = abs(firstCol-lastCol)+1
        dispDir = sign(lastCol-firstCol+0.1).astype(int)
        if numCols>1:
            vols = around(firstVolume + arange(numCols).astype(float)*(lastVolume-firstVolume)/(numCols-1)).astype(int)
        else:
            vols = firstVolume*ones(1).astype(int)
        if (vols>args.maxv).any():
            sys.exit('Aspirated volume limit exceeded for gradient "'+grad+'".  Check your parameters.')
        reqvols[stockCol] = reqvols.get(stockCol,0)+sum(vols)+args.xv
    for key, value in reqvols.iteritems():
        foo = raw_input("CHECK: Stock DeepWell block column %d is filled with %d ul of reagent." % (key, value+args.cush_vol))

    roboperator = set_the_stage(plates, args.dry_run, sleeptime=args.sleeptime)

    for grad in args.grad:
        stockCol,firstVolume,lastVolume,firstCol,lastCol,rowShift = [int(x) for x in grad.split(',')]
        numCols = abs(firstCol-lastCol)+1
        dispDir = sign(lastCol-firstCol+0.1).astype(int)
        if numCols>1:
            vols = around(firstVolume + arange(numCols).astype(float)*(lastVolume-firstVolume)/(numCols-1)).astype(int)
        else:
            vols = firstVolume*ones(1).astype(int)
        reqvols[stockCol] -= sum(vols)+args.xv
        actCols = sum(cumsum(vols)<args.maxv)
        aspVolume = sum(vols[cumsum(vols)<args.maxv])+args.xv
        tipstop = roboperator.good_vpos('stock', sum(vols[actCols:])+reqvols[stockCol])
        roboperator.aspirateRCT('stock', (1+rowShift, stockCol, tipstop), aspVolume, 'Aspirating %d ul to dispense columns %d to %d...' % (aspVolume, firstCol, firstCol+(actCols-1)*dispDir))
        sys.stdout.write('Done.\n')
        for iCol in range(firstCol,lastCol+dispDir,dispDir):
            iVol = (iCol-firstCol)*dispDir
            if iCol == firstCol+actCols*dispDir:
                ind = cumsum(vols[iVol:])<args.maxv
                actCols += sum(ind)
                aspVolume = sum(vols[iVol:][ind])
                tipstop = roboperator.good_vpos('stock', sum(vols[actCols:]))
                roboperator.aspirateRCT('stock', (1+rowShift, stockCol, tipstop), aspVolume, 'Aspirating %d ul to dispense columns %d to %d...' % (aspVolume, iCol, firstCol+(actCols-1)*dispDir))
            dispVolume = vols[iVol]
            roboperator.dispenseRCT('plate', (1+rowShift, iCol, 2), dispVolume, 'Dispensing %d ul into column %d...' % (dispVolume, iCol))
        roboperator.emptyRCT('stock', (1+rowShift, stockCol, 6))
        if args.manual_wash:
            foo = raw_input("Wash and/or replace the tips.  Hit ENTER when done.")
        elif args.wash_col is not None:
            roboperator.washRCT('stock', (1+rowShift,args.wash_col,2), args.maxv+args.xv)
        elif args.wash_spot is not None:
            roboperator.washRCT('wash', (1,1,1), args.maxv+args.xv)
    
    roboperator.home()

if __name__ == "__main__":
    main()



