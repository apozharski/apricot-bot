#!/usr/bin/env python

import sys
sys.path.append('../../epyapribot')
from abot import TheBot
from target import set_the_stage
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from scipy import cumsum, arange, around, sign
def main():
    headerhelp = \
'''
'''
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                        description=headerhelp)
    parser.add_argument('--plate-spot', default=2, type=int, help='Location of the plate')
    parser.add_argument('--stock-spot', default=1, type=int, help='Location of the stocks')
    parser.add_argument('--wash-row', default=8, type=int, help='Row of the stock block for washing the tips')
    parser.add_argument('-g', '--grad', action='append', help='Gradient definitions: stockRow,topVolume,bottomVolume,topRow,bottomRow')
    parser.add_argument('--xv', default=5, type=int, help='Overhead volume')
    parser.add_argument('--maxv', default=300, type=int, help='Maximum volume')
    parser.add_argument('--dry-run', action='store_true', help='Dry run.')
    
    args = parser.parse_args()
    
    if args.grad is None:
        sys.exit('No gradients are defined. Check your parameters.')
    foo = raw_input("CHECK: Target plate in position "+str(args.plate_spot))
    foo = raw_input("CHECK: Stock DeepWell block in position "+str(args.stock_spot))
    foo = raw_input("CHECK: Wash row (%d) of the stock block is filled with water" % args.wash_row)

    plates = {
        'plate'      :   ['../templates/nunc96.apb',args.plate_spot],
        'stock'   :   ['../templates/greiner_masterblock.apb',args.stock_spot],
        }
    roboperator = set_the_stage(plates, args.dry_run)

    for grad in args.grad:
        stockRow,topVolume,bottomVolume,topRow,bottomRow = map(int, grad.split(','))
        numRows = abs(topRow-bottomRow)+1
        dispDir = sign(bottomRow-topRow+0.1).astype(int)
        vols = around(topVolume + arange(numRows).astype(float)*(bottomVolume-topVolume)/(numRows-1)).astype(int)
        if (vols>args.maxv).any():
            sys.exit('Aspirated volume limit exceeded for gradient "'+grad+'".  Check your parameters.')
        actRows = sum(cumsum(vols)<args.maxv)
        aspVolume = sum(vols[cumsum(vols)<args.maxv])+args.xv
        roboperator.aspirateRCT('stock', (stockRow, 1, 2), aspVolume, 'Aspirating %d ul to dispense rows %d to %d...' % (aspVolume, topRow, topRow+(actRows-1)*dispDir))
        sys.stdout.write('Done.\n')
        for iRow in range(topRow,bottomRow+dispDir,dispDir):
            iVol = (iRow-topRow)*dispDir
            if iRow == topRow+actRows*dispDir:
                ind = cumsum(vols[iVol:])<args.maxv
                actRows += sum(ind)
                aspVolume = sum(vols[iVol:][ind])
                roboperator.aspirateRCT('stock', (stockRow, 1, 2), aspVolume, 'Aspirating %d ul to dispense rows %d to %d...' % (aspVolume, iRow, topRow+(actRows-1)*dispDir))
            dispVolume = vols[iVol]
            roboperator.dispenseRCT('plate', (iRow, 1, 1), dispVolume, 'Dispensing %d ul into row %d...' % (dispVolume, iRow))
        roboperator.emptyRCT('stock', (stockRow, 1, 8))
        roboperator.washRCT('stock', (args.wash_row,1,4), args.maxv+args.xv)
    
    roboperator.home()

if __name__ == "__main__":
    main()



