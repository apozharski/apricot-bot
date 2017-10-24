#!/usr/bin/env python

import sys
sys.path.append('../../epyapribot')
from target import set_the_stage
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from scipy import cumsum, arange, around, sign, ones, array
def main():
    headerhelp = \
'''
'''
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                        description=headerhelp)
    parser.add_argument('--plate-spot', default=3, type=int, help='Location of the plate')
    parser.add_argument('--stock-spot', default=2, type=int, help='Location of the stocks')
    parser.add_argument('--wash-col', default=12, type=int, help='Column of the stock block for washing the tips')
    parser.add_argument('-v', '--vols', action='append', help='VOlume definitions: stockCol,firstCol,lastCol,V1,V2,...')
    parser.add_argument('--xv', default=5, type=int, help='Overhead volume')
    parser.add_argument('--maxv', default=300, type=int, help='Maximum volume')
    parser.add_argument('--cush-vol', default=50, type=int, help='Cushion volume')
    parser.add_argument('--dry-run', action='store_true', help='Dry run.')
    parser.add_argument('--manual-wash', action='store_true', help='Wash tips manually (may be faster)')
    
    args = parser.parse_args()
    
    if args.vols is None:
        sys.exit('No volume sets are defined. Check your parameters.')
    foo = raw_input("CHECK: Target plate in position "+str(args.plate_spot))
    foo = raw_input("CHECK: Stock DeepWell block in position "+str(args.stock_spot))
    foo = raw_input("CHECK: Wash column (%d) of the stock block is filled with water" % args.wash_col)

    plates = {
        'plate'      :   ['../templates/nunc96.apb',args.plate_spot],
        'stock'   :   ['../templates/greiner_masterblock.apb',args.stock_spot],
        }

    reqvols = {}
    for volset in args.vols:
        stockCol,firstCol,lastCol = map(int, volset.split(',')[:3])
        numCols = abs(firstCol-lastCol)+1
        dispDir = sign(lastCol-firstCol+0.1).astype(int)
        vols = map(int, volset.split(',')[3:])
        if len(vols) == 1:
            vols = ones(numCols).astype(int)*vols[0]
        else:
            vols = array(vols)
        if (vols>args.maxv).any():
            sys.exit('Aspirated volume limit exceeded for volume set "'+volset+'".  Check your parameters.')
        reqvols[stockCol] = reqvols.get(stockCol,0)+sum(vols)+args.xv
    for key, value in reqvols.iteritems():
        foo = raw_input("CHECK: Stock DeepWell block column %d is filled with %d ul of reagent." % (key, value+args.cush_vol))

    roboperator = set_the_stage(plates, args.dry_run)

    for volset in args.vols:
        stockCol,firstCol,lastCol = map(int, volset.split(',')[:3])
        numCols = abs(firstCol-lastCol)+1
        dispDir = sign(lastCol-firstCol+0.1).astype(int)
        vols = map(int, volset.split(',')[3:])
        if len(vols) == 1:
            vols = ones(numCols).astype(int)*vols[0]
        else:
            vols = array(vols)
        reqvols[stockCol] -= sum(vols)+args.xv
        actCols = sum(cumsum(vols)<args.maxv)
        aspVolume = sum(vols[cumsum(vols)<args.maxv])+args.xv
        tipstop = roboperator.good_vpos('stock', sum(vols[actCols:])+reqvols[stockCol])
        roboperator.aspirateRCT('stock', (1, stockCol, tipstop), aspVolume, 'Aspirating %d ul to dispense columns %d to %d...' % (aspVolume, firstCol, firstCol+(actCols-1)*dispDir))
        for iCol in range(firstCol,lastCol+dispDir,dispDir):
            iVol = (iCol-firstCol)*dispDir
            if iCol == firstCol+actCols*dispDir:
                ind = cumsum(vols[iVol:])<args.maxv
                actCols += sum(ind)
                aspVolume = sum(vols[iVol:][ind])
                tipstop = roboperator.good_vpos('stock', sum(vols[actCols:]))
                roboperator.aspirateRCT('stock', (1, stockCol, tipstop), aspVolume, 'Aspirating %d ul to dispense columns %d to %d...' % (aspVolume, iCol, firstCol+(actCols-1)*dispDir))
            dispVolume = vols[iVol]
            roboperator.dispenseRCT('plate', (1, iCol, 2), dispVolume, 'Dispensing %d ul into column %d...' % (dispVolume, iCol))
        roboperator.emptyRCT('stock', (1, stockCol, 6))
        if args.manual_wash:
            foo = raw_input("Wash and/or replace the tips.  Hit ENTER when done.")
        else:
            roboperator.washRCT('stock', (1,args.wash_col,2), args.maxv+args.xv)
    
    roboperator.home()

if __name__ == "__main__":
    main()



