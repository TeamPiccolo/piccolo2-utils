from piccolo2.utils import PiccoloSpectralLines, CalibrateConfig
from piccolo2.common import PiccoloSpectraList
import argparse
import sys, os.path
from matplotlib import pyplot
import numpy

def gaussian(a,b,c,x):
    return a*numpy.exp(-(x-b)**2/(2*c**2))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('spectra',nargs='*',help='the spectra files to load')
    parser.add_argument('-c','--config',help="read config file")
    parser.add_argument('-l','--spectral-lines',help="csv file containing spectral lines")
    parser.add_argument('--delta',type=float,default=1000.,help='minimum delta for peak, default 5000.')
    parser.add_argument('-s','--saturation-percentage',type=float,default=90.,help='percentage of saturation level above which peaks are ignored')
    parser.add_argument('-d','--direction',nargs='*',help="select the direction to process, default: process all directions")
    parser.add_argument('-n','--serial-number',nargs='*',help="select the spectrometer to process, default: process all spectrometers")
    parser.add_argument('-w','--wavelength',type=float,help="optimise for wavelength by applying a Gaussian weight centred at wavelength")
    parser.add_argument('-g','--gaussian-width',type=float,default=100.,help='width of gaussian in nm, default=100.')
    parser.add_argument('--shift',action='store_true',default=False,help='shift wavelengths to match center wavelength used for Gaussian weight')
    parser.add_argument('-v','--version',action='store_true',default=False,help="print version and exit")
    
    args = parser.parse_args()

    if args.version:
        from utils import __version__
        print __version__
        sys.exit(0)

    if args.config is not None:
        cfg = CalibrateConfig()
        cfg.readCfg(args.config)
        calibrate = cfg.cfg['calibrate']
    else:
        if args.spectral_lines is not None:
            spectralLinesName = args.spectral_lines
        else:
            spectralLinesName=os.path.join(os.path.dirname(sys.argv[0]),'..','share','piccolo2-util','HgArLines.csv')
        if not os.path.isfile(spectralLinesName):
            parser.error('could not find file containing spectra lines')
            sys.exit(1)       
            
        calibrate = {}
        c = os.path.basename(spectralLinesName)
        calibrate[c] = {}
        calibrate[c]['spectral_lines'] = spectralLinesName
        calibrate[c]['spectra'] = args.spectra
        

    spectralLines = {}
    # loop over all spectral_lines
    for c in calibrate:
        spectralLines[c] = PiccoloSpectralLines(calibrate[c]['spectral_lines'])

    calibration ={}

    # load data and match spectral lines
    for c in calibrate:
        for sf in calibrate[c]['spectra']:
            indata = open(sf,'r').read()
            spectra = PiccoloSpectraList(data=indata)

            for s in spectra:
                sn = s['SerialNumber']
                dr = s['Direction']
                if args.serial_number is not None and sn not in args.serial_number:
                    continue
                if sn not in calibration:
                    calibration[sn] = {}
                    calibration[sn]['SaturationLevel']=s['SaturationLevel']
                if args.direction is not None and dr not in args.direction:
                    continue                
                if dr not in calibration[sn]:
                    calibration[sn][dr] = {}
                    calibration[sn][dr]['orig_wcoeff'] = s['WavelengthCalibrationCoefficients'][::-1]
                    calibration[sn][dr]['pixels'] = []
                    calibration[sn][dr]['spectralLines'] = []

                calibration[sn][dr]['pixels'].append(s.pixels)
                calibration[sn][dr]['spectralLines'].append(c)


    ok = True
    if args.serial_number is not None:
        for sn in args.serial_number:
            if sn not in calibration:
                print 'error, could not find spectrometer with serial number %s in data set'%sn
                ok = False
    if args.direction is not None:
        for sn in calibration:
            for dr in args.direction:
                if dr not in calibration[sn]:
                    print 'error, direction %s not found in data set for spectrometer %s'%(dr,sn)
                    ok = False
    if not ok:
        sys.exit(1)
    
    # fit wavelength coefficients
    for sn in calibration:
        for dr in calibration[sn]:
            if dr == 'SaturationLevel':
                continue
            nPeaks = 0
            # start with original wavelengths coefficients
            coeff = calibration[sn][dr]['orig_wcoeff']
            while True:
                matched = []
                # find peaks
                wavelengths = numpy.poly1d(coeff)(numpy.arange(len(calibration[sn][dr]['pixels'][0])))
                for i in range(len(calibration[sn][dr]['pixels'])):
                    pixels = calibration[sn][dr]['pixels'][i]
                    spectral_lines = spectralLines[calibration[sn][dr]['spectralLines'][i]]

                    m = spectral_lines.match(wavelengths,pixels,delta=args.delta,
                                             maxval=calibration[sn]['SaturationLevel']*args.saturation_percentage/100.)
                    matched += m
                matched = numpy.array(matched)
                if args.wavelength is not None:
                    weights = 0.5+gaussian(0.5,args.wavelength,args.gaussian_width,matched[:,0])
                else:
                    weights = None
                coeff = numpy.polyfit(matched[:,0],matched[:,1],3,w=weights)

                if nPeaks == len(matched):
                    break
                nPeaks = len(matched)

            if args.wavelength is not None and args.shift:
                idx = None
                for i in range(matched.shape[0]):
                    if  abs(matched[i,1]-args.wavelength) < 0.5:
                        idx = int(matched[i,0])
                if idx is not None:
                    offset = args.wavelength-numpy.poly1d(coeff)(idx)
                    print 'shifting wavelenghts by %f to match spectral line at %f'%(offset,args.wavelength)
                    coeff[-1] += offset
                
            calibration[sn][dr]['matched'] = matched
            calibration[sn][dr]['new_wcoeff'] = coeff
            pyplot.show()


    for sn in calibration:
        for dr in calibration[sn]:
            if dr == 'SaturationLevel':
                continue
            print sn,dr
            print calibration[sn][dr]['orig_wcoeff']
            print calibration[sn][dr]['new_wcoeff']

            f,ax = pyplot.subplots(2,2)


            for c in spectralLines:
                for l in spectralLines[c].lines:
                    ax[0,0].axvline(l,color='k')
                    ax[0,1].axvline(l,color='k')

            polys = [numpy.poly1d(calibration[sn][dr]['orig_wcoeff']),
                     numpy.poly1d(calibration[sn][dr]['new_wcoeff'])]
            for j in range(len(polys)):
                poly = polys[j]
                for p in calibration[sn][dr]['pixels']:
                    ax[0,j].plot(poly(numpy.arange(len(p))),p)
                    matched = calibration[sn][dr]['matched']
                    ax[1,j].plot(matched[:,1],poly(matched[:,0])-matched[:,1],'o')

                
                s0 = poly(0)
                s1 = poly(len(p))
                for i in range(2):
                    ax[i,j].set_xlim([s0,s1])

            pyplot.suptitle('%s %s'%(sn,dr),fontsize=16)
            ax[0,0].set_title('original')
            ax[0,1].set_title('new')
            ax[1,0].set_ylabel('mismatch at peaks')
            ax[0,0].set_ylabel('counts')
            ax[1,0].set_xlabel('wavelength')
            ax[1,1].set_xlabel('wavelength')
            pyplot.show()



