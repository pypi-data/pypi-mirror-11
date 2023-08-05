# -*- coding: utf-8 -*-
#
# This file is part of SIDEKIT.
#
# SIDEKIT is a python package for speaker verification.
# Home page: http://www-lium.univ-lemans.fr/sidekit/
#
# SIDEKIT is a python package for speaker verification.
# Home page: http://www-lium.univ-lemans.fr/sidekit/
#    
# SIDEKIT is free software: you can redistribute it and/or modify
# it under the terms of the GNU LLesser General Public License as 
# published by the Free Software Foundation, either version 3 of the License, 
# or (at your option) any later version.
#
# SIDEKIT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with SIDEKIT.  If not, see <http://www.gnu.org/licenses/>.

"""
Copyright 2014-2015 Anthony Larcher and Sylvain Meignier

:mod:`frontend` provides methods to process an audio signal in order to extract
useful parameters for speaker verification.
"""

__author__ = "Anthony Larcher and Sylvain Meignier"
__copyright__ = "Copyright 2014-2015 Anthony Larcher and Sylvain Meignier"
__license__ = "LGPL"
__maintainer__ = "Anthony Larcher"
__email__ = "anthony.larcher@univ-lemans.fr"
__status__ = "Production"
__docformat__ = 'reStructuredText'


import numpy as np
import multiprocessing
from scipy.signal import hamming
from scipy.fftpack.realtransforms import dct
from sidekit.frontend.vad import *
from sidekit.frontend.io import *
from sidekit.frontend.normfeat import *
#from memory_profiler import profile
import gc

def hz2mel(f):
    """Convert an array of frequency in Hz into mel.
    
    :param f: frequency to convert
    
    :return: the equivalene on the mel scale.
    """
    return 1127.01048 * np.log(f/700 +1)

def mel2hz(m):
    """Convert an array of mel values in Hz.
    
    :param m: ndarray of frequencies to convert in Hz.
    
    :return: the equivalent values in Hertz.
    """
    return (np.exp(m / 1127.01048) - 1) * 700

def compute_delta(features, win=3, method='filter', 
          filt=np.array([.25, .5, .25, 0, -.25, -.5, -.25])):
    """features is a 2D-ndarray  each row of features is a a frame
    
    :param features: the feature frames to compute the delta coefficients
    :param win: parameter that set the length of the computation window.
            The eize of the window is (win x 2) + 1
    :param methods: method used to compute the delta coefficients
        can be diff or filter
    :param filt: definition of the filter to use in "filter" mode, default one
        is similar to SPRO4:  filt=np.array([.2, .1, 0, -.1, -.2])
        
    :return: the delta coefficients computed on the original features.
    """
    # First and last features are appended to the begining and the end of the 
    # stream to avoid border effect
    x = np.zeros((features.shape[0] + 2* win, features.shape[1]))
    x[:win, :] = features[0, :]
    x[win:-win,:] = features
    x[-win:, :] = features[-1, :]

    delta = np.zeros(x.shape)
    
    if method == 'diff':
        filt = np.zeros(2 * win + 1)
        filt[0] = -1
        filt[-1] = 1

    for i in range(features.shape[1]):
        delta[:, i] = np.convolve(features[:, i], filt)

    return delta[win:-win, :]


def trfbank(fs, nfft, lowfreq, maxfreq, nlinfilt, nlogfilt, midfreq=1000):
    """Compute triangular filterbank for cepstral coefficient computation.
    
    :param fs: sampling frequency of the original signal.
    :param nfft: number of points for the Fourier Transform
    :param lowfreq: lower limit of the frequency band filtered 
    :param maxfreq: higher limit of the frequency band filtered
    :param nlinfilt: number of linear filters to use in low frequencies
    :param  nlogfilt: number of log-linear filters to use in high frequencies
    :param midfreq: frequency boundary between linear and log-linear filters
    
    :return: the filter bank and the central frequencies of each filter
    """
    # Total number of filters
    nfilt = nlinfilt + nlogfilt

    #------------------------
    # Compute the filter bank
    #------------------------
    # Compute start/middle/end points of the triangular filters in spectral
    # domain
    freqs = np.zeros(nfilt + 2)
    if nlogfilt == 0:
        linsc = (maxfreq - lowfreq)/ (nlinfilt + 1)
        freqs[:nlinfilt  + 2] = lowfreq + np.arange(nlinfilt + 2) * linsc
    elif (nlinfilt == 0):
        lowMel = hz2mel(lowfreq)
        maxMel = hz2mel(maxfreq)
        mels = np.zeros(nlogfilt+2)
        mels[nlinfilt:]
        melsc = (maxMel - lowMel)/ (nfilt + 1)
        mels[:nlogfilt + 2] = lowMel + np.arange(nlogfilt + 2) * melsc
        # Back to the frequency domain
        freqs = mel2hz(mels)
    else:
        # Compute linear filters on [0;1000Hz]
        linsc = (min([midfreq,maxfreq]) - lowfreq)/ (nlinfilt + 1)
        freqs[:nlinfilt] = lowfreq + np.arange(nlinfilt) * linsc
        # Compute log-linear filters on [1000;maxfreq]
        lowMel = hz2mel(min([1000,maxfreq]))
        maxMel = hz2mel(maxfreq)
        mels = np.zeros(nlogfilt+2)
        melsc = (maxMel - lowMel)/ (nlogfilt + 1)
        
        # Verify that mel2hz(melsc)>linsc
        while (mel2hz(melsc)<linsc):
            logging.debug('nlinfilt = ',nlinfilt,' nlogfilt = ',nlogfilt,' ne fonctionne pas')
            # in this case, we add a linear filter
            nlinfilt += 1
            nlogfilt -= 1
            freqs[:nlinfilt] = lowfreq + np.arange(nlinfilt) * linsc
            lowMel = hz2mel(freqs[nlinfilt-1]+2*linsc)
            maxMel = hz2mel(maxfreq)
            mels = np.zeros(nlogfilt+2)
            melsc = (maxMel - lowMel)/ (nlogfilt + 1)

        mels[:nlogfilt + 2] = lowMel + np.arange(nlogfilt + 2) * melsc
        # Back to the frequency domain
        freqs[nlinfilt:] = mel2hz(mels)

    heights = 2./(freqs[2:] - freqs[0:-2])

    # Compute filterbank coeff (in fft domain, in bins)
    fbank = np.zeros((nfilt, np.floor(nfft/2)+1))
    # FFT bins (in Hz)
    nfreqs = np.arange(nfft) / (1. * nfft) * fs
    
    for i in range(nfilt):
        low = freqs[i]
        cen = freqs[i+1]
        hi = freqs[i+2]
    
        lid = np.arange(np.floor(low * nfft / fs) + 1,
                        np.floor(cen * nfft / fs) + 1, dtype=np.int)
        lslope = heights[i] / (cen - low)
        rid = np.arange(np.floor(cen * nfft / fs) + 1,
                        min(np.floor(hi * nfft / fs) + 1,nfft), dtype=np.int)
        rslope = heights[i] / (hi - cen)
        fbank[i][lid] = lslope * (nfreqs[lid] - low)
        fbank[i][rid[:-1]] = rslope * (hi - nfreqs[rid[:-1]])

    return fbank, freqs


def mfcc(input, lowfreq=100, maxfreq=8000, nlinfilt=0, nlogfilt=24,
         nwin=256, nfft=512, fs=16000, nceps=13, midfreq = 1000, shift=0.01,
         get_spec=False, get_mspec=False):
    """Compute Mel Frequency Cepstral Coefficients.

    :param input: input signal from which the coefficients are computed. 
            Input audio is supposed to be RAW PCM 16bits
    :param lowfreq: lower limit of the frequency band filtered. 
            Default is 100Hz.
    :param maxfreq: higher limit of the frequency band filtered.
            Default is 8000Hz.
    :param nlinfilt: number of linear filters to use in low frequencies.
            Default is 0.
    :param nlogfilt: number of log-linear filters to use in high frequencies.
            Default is 24.
    :param nwin: length of the sliding window.
            Default is 256.
    :param nfft: number of points for the Fourier Transform. Default is 512.
    :param fs: sampling frequency of the original signal. Default is 16000Hz.
    :param nceps: number of cepstral coefficients to extract. 
            Default is 13.
    :param midfreq: frequency boundary between linear and log-linear filters.
            Default is 1000Hz.
    :param shift: shift between two analyses. Default is 0.01 (10ms).

    :return: the cepstral coefficients in a ndaray as well as 
            the Log-spectrum in the mel-domain in a ndarray.

    .. note:: MFCC are computed as follows:
        
            - Pre-processing in time-domain (pre-emphasizing)
            - Compute the spectrum amplitude by windowing with a Hamming window
            - Filter the signal in the spectral domain with a triangular filter-bank, whose filters are approximatively linearly spaced on the mel scale, and have equal bandwith in the mel scale
            - Compute the DCT of the log-spectrom
            - Log-energy is returned as first coefficient of the feature vector.
    
    For more details, refer to [Davis80]_.
    """


    # Pre-emphasis factor (to take into account the -6dB/octave rolloff of the
    # radiation at the lips level)
    prefac = 0.97
    logging.debug('pre emphasis')
    extract = pre_emphasis(input, prefac)

    # Compute the overlap of frames and cut the signal in frames of length nwin
    # overlaping by "overlap" samples
    logging.debug('axis')
    w = hamming(nwin, sym=0)
    overlap = nwin - int(shift * fs)
    framed = segment_axis(extract, nwin, overlap)

    l = framed.shape[0]
    spec = np.ones((l, nfft/2+1))
    logEnergy = np.ones(l)

    dec = 10000
    start = 0
    stop = min(dec, l)
    while start < l:
        # logging.debug('fft start: %d stop: %d', start, stop)
        # Compute the spectrum magnitude
        tmp = framed[start:stop,:] * w
        spec[start:stop,:] = np.abs(np.fft.rfft(tmp, nfft, axis=-1))
        # Compute the log-energy of each frame
        logEnergy[start:stop] = 2.0 * np.log(np.sqrt(np.sum(np.square(tmp), axis=1)))
        start = stop
        stop = min(stop + dec, l)

    del framed
    del extract
    logging.debug('log10')

    # Filter the spectrum through the triangle filterbank
    # Prepare the hamming window and the filter bank
    logging.debug('trf bank')
    fbank = trfbank(fs, nfft, lowfreq, maxfreq, nlinfilt, nlogfilt)[0]
    mspec = np.log10(np.dot(spec, fbank.T))
    del fbank

    logging.debug('dct')

    # Use the DCT to 'compress' the coefficients (spectrum -> cepstrum domain)
    # The C0 term is removed as it is the constant term
    ceps = dct(mspec, type=2, norm='ortho', axis=-1)[:, 1:nceps + 1]
    lst = list()
    lst.append(ceps)
    lst.append(logEnergy)
    if get_spec:
        lst.append(spec)
    else:
        lst.append(None)
        del spec
    if get_mspec:
        lst.append(mspec)
    else:
        lst.append(None)
        del mspec

    return lst

