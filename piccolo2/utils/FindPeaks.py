# Copyright 2018- The Piccolo Team
#
# This file is part of piccolo2-client.
#
# piccolo2-utils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# piccolo2-utils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with piccolo2-utils.  If not, see <http://www.gnu.org/licenses/>.

__all__  = ['peakdet','peakdet2']

import numpy
from scipy.signal import find_peaks

def peakdet(v, delta, maxval=None, x = None):
    """
    Converted from MATLAB script at http://billauer.co.il/peakdet.html
    https://gist.github.com/endolith/250860
   
    Returns two arrays
    
    function [maxtab, mintab]=peakdet(v, delta, x)
    %PEAKDET Detect peaks in a vector
    %        [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local
    %        maxima and minima ("peaks") in the vector V.
    %        MAXTAB and MINTAB consists of two columns. Column 1
    %        contains indices in V, and column 2 the found values.
    %      
    %        With [MAXTAB, MINTAB] = PEAKDET(V, DELTA, X) the indices
    %        in MAXTAB and MINTAB are replaced with the corresponding
    %        X-values.
    %
    %        A point is considered a maximum peak if it has the maximal
    %        value, and was preceded (to the left) by a value lower by
    %        DELTA.
    
    % Eli Billauer, 3.4.05 (Explicitly not copyrighted).
    % This function is released to the public domain; Any use is allowed.
    
    """
    maxtab = []
    mintab = []
       
    if x is None:
        x = numpy.arange(len(v))
    
    v = numpy.asarray(v)
    
    if len(v) != len(x):
        raise ValueError, 'Input vectors v and x must have same length'
    
    if not numpy.isscalar(delta):
        raise ValueError, 'Input argument delta must be a scalar'
    
    if delta <= 0:
        raise ValueError, 'Input argument delta must be positive'
    
    mn, mx = numpy.Inf, -numpy.Inf
    mnpos, mxpos = numpy.NaN, numpy.NaN
    
    lookformax = True
   
    for i in numpy.arange(len(v)):
        this = v[i]

        if maxval is not None and this> maxval:
            continue
        
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]
        
        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return numpy.array(maxtab), numpy.array(mintab)

def peakdet2(v, delta, maxval=None, x = None):

    if maxval is not None:
        h = [delta,maxval]
    else:
        h = delta
    peaks, _ = find_peaks(v,height=h)
    return peaks
