#!/usr/bin/env python

import sys
sys.path.append('../../epyapribot')
from abot import TheBot
from target import set_the_stage
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from scipy import cumsum, arange, around
def main():
    headerhelp = \
'''
'''
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                        description=headerhelp)
    parser.add_argument('--plate-spot', default=2, type=int, help='Location of the plate')
    parser.add_argument('--stock-spot', default=1, type=int, help='Location of the stocks')
    parser.add_argument('-g', '--grad', action='append', help='Gradient definitions: stockRow,topVolume,bottomVolume,topRow,bottomRow')
    parser.add_argument('--xv', default=5, type=int, help='Overhead volume')
    parser.add_argument('--maxv', default=300, type=int, help='Maximum volume')
    
    args = parser.parse_args()
    
    foo = raw_input("CHECK: Target plate in position "+str(args.plate_spot))
    foo = raw_input("CHECK: Stock DeepWell block in position "+str(args.stock_spot))

    plates = {
        'plate'      :   ['../templates/nunc96.apb',args.plate_spot],
        'stock'   :   ['../templates/greiner_masterblock.apb',args.stock_spot],
        }
    roboperator = set_the_stage(plates)

    for grad in args.grad:
        stockRow,topVolume,bottomVolume,topRow,bottomRow = map(int, grad.split(','))
        numRows = abs(topRow-bottomRow)+1
        vols = around(topVolume + arange(numRows).astype(float)*(bottomVolume-topVolume)/(numRows-1)).astype(int)
        actRows = sum(cumsum(vols)<args.maxv)
        if actRows == numRows:
            vol1 = sum(vols)+args.xv
        else:
            vol1 = sum(vols[cumsum(vols)<args.maxv])+args.xv
        roboperator.aspirateRCT('stock', (stockRow, 1, 2), vol1)
        for i in range(1,numRows
    
    roboperator.home()

if __name__ == "__main__":
    main()



