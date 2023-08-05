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
Copyright 2014-2015 Sylvain Meignier and Anthony Larcher

    :mod:`features_server` provides methods to manage features

"""

__license__ = "LGPL"
__author__ = "Anthony Larcher"
__copyright__ = "Copyright 2014-2015 Anthony Larcher"
__license__ = "LGPL"
__maintainer__ = "Anthony Larcher"
__email__ = "anthony.larcher@univ-lemans.fr"
__status__ = "Production"
__docformat__ = 'reStructuredText'


import logging
from sidekit.frontend.features import *
from sidekit.frontend.vad import *
from sidekit.frontend.io import *
from sidekit.frontend.normfeat import *
from sidekit.sidekit_io import read_pickle, write_pickle
import numpy as np
import ctypes
import multiprocessing


class FeaturesServer:
    """
    A class for acoustic feature management.
    FeaturesServer should be used to extract acoustic features (MFCC or LFCC)
    from audio files in SPHERE, WAV or RAW PCM format.
    It can also be used to read and write acoustic features from and to disk
    in SPRO4 or HTK format.

    :attr input_dir: directory where to load audio or feature files
    :attr input_file_extension: extension of the incoming files
    :attrlabel_dir: directory where to read and write label files
    :attr label_files_extension: extension of label files to read and write
    :attr from_file: format of the input files to read, can be `audio`, `spro4`
        or `htk`, for audio files, format is given by the extension
    :attr config: pre-defined configuration for speaker diarization or recognition
        in 8 or 16kHz. Default is speaker recognition 8kHz
    :attr single_channel_extension: list with a single extension to add to 
        the audio filename when processing a single channel file. 
        Default is empty, means the feature file has the same name as 
        the audio file
    :attr double_channel_extension: list of two channel extension to add 
        to the audio filename when processing two channel files. 
        Default is ['_a', '_b']
    :attr sampling_frequency: sample frequency in Hz, default is None, 
        determine when reading the audio file
    :attr lower_frequency: lower frequency limit of the filter bank
    :attr higher_frequency: higher frequency limit of the filter bank
    :attr linear_filters: number of linear filters to use for LFCC extraction
    :attr log_filters: number of linear filters to use for MFCC extraction
    :attr window_size: size of the sliding window in seconds
    :attr shift: time shift between two feature vectors
    :attr ceps_number: number of cepstral coefficients to extract
    :attr snr: snr level to consider for SNR-based voice activity detection
    :attr vad: type of voice activity detection to use, can be 'snr', 'energy' 
        (using a three Gaussian detector) or 'label' when reading the info from 
        pre-computed label files
    :attr feat_norm: normalization of the acoustic features, can be 
        'cms' for cepstral mean subtraction, 'mvn' for mean variance 
        normalization or 'stg' for short term Gaussianization
    :attr log_e: boolean, keep log energy
    :attr delta: boolean, add the first derivative of the cepstral coefficients
    :attr double_delta: boolean, add the second derivative of the cepstral 
        coefficients
    :attr rasta: boolean, perform RASTA filtering
    :attr keep_all_features: boolean, if False, only features labeled as 
        "speech" by the vad are saved if True, all features are saved and 
        a label file is produced

    """

    def __init__(self, input_dir='./',
                 input_file_extension='.sph',
                 label_dir='./',
                 label_file_extension='.lbl',
                 from_file='audio',
                 config='sid_8k',
                 single_channel_extension=[''],
                 double_channel_extension=['_a','_b'],
                 sampling_frequency=None,
                 lower_frequency=None,
                 higher_frequency=None,
                 linear_filters=None,
                 log_filters=None,
                 window_size=None,
                 shift=None,
                 ceps_number=None,
                 snr=None,
                 vad=None,
                 feat_norm=None,
                 log_e=None,
                 delta=None,
                 double_delta=None,
                 rasta=None,
                 keep_all_features=None,
                 spec=False,
                 mspec=False
    ):
        """ Process of extracting the feature frames (LFCC or MFCC) from an audio signal.
        Speech Activity Detection, MFCC (or LFCC) extraction and normalization.
        Can include RASTA filtering, Short Term Gaussianization, MVN and delta
        computation.

        :param input_dir: directory where to find the audio files.
                Default is ./
        :param input_file_extension: extension of the audio files to read.
                Default is 'sph'.
        :param label_dir: directory where to store label files is required.
                Default is ./
        :param label_file_extension: extension of the label files to create.
                Default is '.lbl'.
        :param configuration file : 'diar_16k', 'sid_16k', 'diar_8k' or 'sid_8k'
        """

        self.spec = False
        self.mspec = False
        self.snr = None
        self.input_dir = input_dir
        self.label_dir = label_dir
        self.label_file_extension = label_file_extension
        self.input_file_extension = input_file_extension
        self.from_file = from_file
        self.audio_filename = 'empty'
        self.filter = None
        self.spec = False
        self.vad = None
        self.feat_norm = None

        if config == 'diar_16k':
            self._config_diar_16k()
        elif config == 'diar_8k':
            self._config_diar_8k()
        elif config == 'sid_8k':
            self._config_sid_8k()
        elif config == 'sid_16k':
            self._config_sid_16k()
        elif config == 'fb_8k':
            self._config_fb_8k()
        elif config is None:
            pass
        else:
            raise Exception('unknown configuration value')

        #self.input_dir = input_dir
        #self.label_dir = label_dir
        #self.label_file_extension = label_file_extension
        #self.input_file_extension = input_file_extension
        #self.from_file = from_file
        #self.audio_filename = 'empty'
        #self.filter = None
        #self.spec = False
        #self.vad = None
        #self.feat_norm = None

        if sampling_frequency is not None:
            self.sampling_frequency = sampling_frequency
        if lower_frequency is not None:
            self.lower_frequency = lower_frequency
        if higher_frequency is not None:
            self.higher_frequency = higher_frequency
        if linear_filters is not None:
            self.linear_filters = linear_filters
        if log_filters is not None:
            self.log_filters = log_filters
        if window_size is not None:
            self.window_size = window_size
        if shift is not None:
            self.shift = shift
        if ceps_number is not None:
            self.ceps_number = ceps_number
        if snr is not None:
            self.snr = snr
        if vad is not None:
            self.vad = vad
        if feat_norm is not None:
            self.feat_norm = feat_norm
        if log_e is not None:
            self.log_e = log_e
        if delta is not None:
            self.delta = delta
        if double_delta is not None:
            self.double_delta = double_delta
        if rasta is not None:
            self.rasta = rasta
        if keep_all_features is not None:
            self.keep_all_features = keep_all_features
        if single_channel_extension is not None:
            self.single_channel_extension = single_channel_extension
        if double_channel_extension is not None:
            self.double_channel_extension = double_channel_extension
        if not self.lower_frequency:
            self.lower_frequency = 0
        if not self.higher_frequency:
            self.higher_frequency = self.sampling_frequency / 2.
        if spec:
            self.spec = True
        if mspec:
            self.mspec = True
        

        self.cep = []
        self.label = []
        self.show = 'empty'

    def __repr__(self):
        ch = '\t show: {} keep_all_features: {} from_file: {}\n'.format(
            self.show, self.keep_all_features, self.from_file)
        ch += '\t inputDir: {} inputFileExtension: {} \n'.format(self.input_dir,
                                                                 self.input_file_extension)
        ch += '\t labelDir: {}  labelFileExtension: {} \n'.format(
            self.label_dir, self.label_file_extension)
        ch += '\t lower_frequency: {}  higher_frequency: {} \n'.format(
            self.lower_frequency, self.higher_frequency)
        ch += '\t sampling_frequency: {} '.format(self.sampling_frequency)
        ch += '\t linear_filters: {}  or log_filters: {} \n'.format(
            self.linear_filters, self.log_filters)
        ch += '\t ceps_number: {}  window_size: {} shift: {} \n'.format(
            self.ceps_number, self.window_size, self.shift)
        ch += '\t vad: {}  snr: {} \n'.format(self.vad, self.snr)
        ch += '\t feat_norm: {} rasta: {} \n'.format(self.feat_norm, self.rasta)
        ch += '\t log_e: {} delta: {} double_delta: {} \n'.format(self.log_e,
                                                                  self.delta,
                                                                  self.double_delta)
        return ch;

    def _config_diar_16k(self):
        """
        12 MFCC + E, no norm
        """
        self.sampling_frequency = 16000
        self.lower_frequency = 133.3333
        self.higher_frequency = 6855.4976
        self.linear_filters = 0
        self.log_filters = 40
        self.window_size = 0.0256
        self.shift = 0.01
        self.ceps_number = 12
        self.snr = 40
        self.vad = None
        self.feat_norm = None
        self.log_e = True
        self.delta = False
        self.double_delta = False
        self.rasta = False
        self.keep_all_features = True

    def _config_diar_8k(self):
        """
        12 MFCC + E, no norm
        """
        self.sampling_frequency = 8000
        self.lower_frequency = None
        self.higher_frequency = None
        self.linear_filters = 0
        self.log_filters = 24
        self.window_size = 0.0256
        self.shift = 0.01
        self.ceps_number = 12
        self.snr = 40
        self.vad = None
        self.feat_norm = None
        self.log_e = True
        self.delta = False
        self.double_delta = False
        self.rasta = False
        self.keep_all_features = True

    def _config_sid_16k(self):
        """
        19 MFCC + E + D + DD, norm cmvn
        """
        self.sampling_frequency = 16000
        self.lower_frequency = 133.3333
        self.higher_frequency = 6855.4976
        self.linear_filters = 0
        self.log_filters = 40
        self.window_size = 0.0256
        self.shift = 0.01
        self.ceps_number = 13
        self.snr = 40
        self.vad = 'snr'
        self.feat_norm = 'cmvn'
        self.log_e = True
        self.delta = True
        self.double_delta = True
        self.rasta = True
        self.keep_all_features = False

    def _config_sid_8k(self):
        """
        19 MFCC + E + D + DD, norm cmvn
        """
        self.sampling_frequency = 8000
        self.lower_frequency = 300
        self.higher_frequency = 3400
        self.linear_filters = 0
        self.log_filters = 24
        self.window_size = 0.0256
        self.shift = 0.01
        self.ceps_number = 13
        self.snr = 40
        self.vad = 'snr'
        self.feat_norm = 'cmvn'
        self.log_e = True
        self.delta = True
        self.double_delta = True
        self.rasta = True
        self.keep_all_features = False

    def _config_fb_8k(self):
        """
        19 MFCC + E + D + DD, norm cmvn
        """
        self.sampling_frequency = 8000
        self.lower_frequency = 300
        self.higher_frequency = 3400
        self.linear_filters = 0
        self.log_filters = 40
        self.window_size = 0.0250
        self.shift = 0.01
        self.ceps_number = 0
        self.snr = 40
        self.vad = None
        self.feat_norm = None
        self.log_e = False
        self.delta = False
        self.double_delta = False
        self.rasta = False
        self.keep_all_features = True
        self.mspec = True
        

    def _features(self, show):
        cep = None
        label = None
        window_sample = int(self.window_size * self.sampling_frequency)
        shift_sample = int(self.shift * self.sampling_frequency)

        d = self.input_dir.format(s=show)
        audio_filename = os.path.join(d, show + self.input_file_extension)
        if not os.path.isfile(audio_filename):
            logging.error('%s %s %s %s', self.input_dir, d, show,
                          self.input_file_extension)
            raise IOError('File ' + audio_filename + ' not found')
        logging.info('read audio')
        logging.debug(audio_filename)
        x, rate = read_audio(audio_filename, self.sampling_frequency)
        if rate != self.sampling_frequency:
            raise (
            "file rate don't match the rate of the feature server configuration")
        self.audio_filename = audio_filename
        logging.info(' size of signal: %f len %d type size %d', x.nbytes/1024/1024, len(x), x.nbytes/len(x))

        if x.ndim == 1:
            x = x[:, np.newaxis]

        channel_ext = []
        channel_nb = x.shape[1]
        np.random.seed(0)
        x[:,0] += 0.0001 * np.random.randn(x.shape[0])

        if channel_nb == 1:
            channel_ext.append('')
            # Random noise is added to the input signal to avoid zero frames.
        elif channel_nb == 2:
            channel_ext.append('_a')
            channel_ext.append('_b')
            x[:,1] += 0.0001 * np.random.randn(x.shape[0])

        # Process channels one by one
        for chan, chan_ext in enumerate(channel_ext):
            l = x.shape[0]
            dec = shift_sample * 250 * 25000 + window_sample
            dec2 = window_sample - shift_sample
            start = 0
            end = min(dec, l)
            while start < l - dec2 :
                # if end < l:
                logging.info('process part : %f %f %f',
                             start / self.sampling_frequency,
                             end / self.sampling_frequency,
                             l / self.sampling_frequency)
                tmp = self._features_chan(show, channel_ext, x[start:end, chan])

                if cep is None:
                    cep = []
                    label = []
                    cep.append(tmp[0])
                    label.append(tmp[1])

                else:
                    cep.append(tmp[0])
                    label.append(tmp[1])
                start = end - dec2
                end = min(end + dec, l)
                logging.info('!! size of signal cep: %f len %d type size %d', cep[-1].nbytes/1024/1024, len(cep[-1]), cep[-1].nbytes/len(cep[-1]))
        del x
       # Smooth the labels and fuse the channels if more than one.
        logging.info('Smooth the labels and fuse the channels if more than one')
        label = label_fusion(label)
        cep = self._normalize(label, cep)

        # Keep only the required features and save the appropriate files
        # which are either feature files alone or feature and label files
        if not self.keep_all_features:
            logging.debug('no keep all')
            for chan, chan_ext in enumerate(channel_ext):
                cep[chan] = cep[chan][label[chan]]
                label[chan] = label[chan][label[chan]]

        return cep, label


    def _features_chan(self, show, channel_ext, x):

        """Compelete the overwhole process of extracting the feature frames
        (LFCC or MFCC) from an audio signal.
        Speech Activity Detection, MFCC (or LFCC) extraction and normalization.
        Can include RASTA filtering, Short Term Gaussianization, MVN and delta
        computation.

        :param show: name of the file.
        """
        # Extract cepstral coefficients
        window_sample = int(self.window_size * self.sampling_frequency)
        c = mfcc(x, fs=self.sampling_frequency,
                 lowfreq=self.lower_frequency,
                 maxfreq=self.higher_frequency,
                 nlinfilt=self.linear_filters,
                 nwin=window_sample, nlogfilt=self.log_filters,
                 nceps=self.ceps_number, get_spec=self.spec, 
                 get_mspec=self.mspec)
        
        if self.ceps_number == 0 and self.mspec:
            cep  = c[3]
            label = np.ones((cep.shape[0]), dtype='bool')
            
        else:
            label = self._vad(c[1], x, channel_ext, show)
    
            cep = self._log_e(c)
            cep, label = self._rasta(cep, label)
            cep = self._delta_and_2delta(cep)
        return cep, label


    def _log_e(self, c):
        """If required, add the log energy as last coefficient"""
        if self.log_e:
            logging.info('keep log_e')
            return np.hstack((c[1][:, np.newaxis], c[0]))
        else:
            logging.info('don\'t keep c0')
            return c[0]

    def _vad(self, logEnergy, x , channel_ext, show):
        """
        Apply Voice Activity Detection.
        :param x:
        :param channel:
        :param window_sample:
        :param channel_ext:
        :param show:
        :return:
        """
        label = None
        if self.vad is None:
            logging.info('no vad')
            label = np.array([True] * x.shape[0])
        elif self.vad == 'snr':
            logging.info('vad : snr')
            window_sample = int(self.window_size * self.sampling_frequency)
            label = vad_snr(x, self.snr, fs=self.sampling_frequency,
                            shift=self.shift, nwin=window_sample)

        elif self.vad == 'energy':
            logging.info('vad : energy')
            label = vad_energy(logEnergy, distribNb=3,
                               nbTrainIt=8, flooring=0.0001,
                               ceiling=1.5, alpha=2)
        elif self.vad == 'lbl':  # load existing labels as reference
            logging.info('vad : lbl')
            for ext in channel_ext:
                label_filename = os.path.join(self.label_dir, show + ext
                                              + self.label_file_extension)
                label = read_label(label_filename)
        else:
            logging.warrning('Wrong VAD type')
        return label

    def _rasta(self, cep, label):
        """
        Performs RASTA filtering if required.
        The two first frames are copied from the third to keep
        the length consistent
        !!! if vad is None: label[] is empty

        :param channel: name of the channel
        :return:
        """
        if self.rasta:
            logging.info('perform RASTA %s', self.rasta)
            cep = rasta_filt(cep)
            cep[:2, :] = cep[2, :]
            label[:2] = label[2]
            
        return cep, label

    def _delta_and_2delta(self, cep):
        """
        Add deltas and double deltas.
        :param channel: name of the channel
        :return:
        """
        if self.delta:
            logging.info('add delta')
            delta = compute_delta(cep)
            cep = np.column_stack((cep, delta))
        if self.double_delta:
            logging.info('add delta delta')
            double_delta = compute_delta(delta)
            cep = np.column_stack((cep, double_delta))
        return cep

    def _normalize(self, label, cep):
        """

        :param label:
        :return:
        """
        # Perform feature normalization on the entire session.
        if self.feat_norm is None:
            logging.info('no norm')
            pass
        if self.feat_norm == 'cms':
            logging.info('cms norm')
            for chan, c in enumerate(cep):
                cep[chan] = cms(c, label[chan])
        elif self.feat_norm == 'cmvn':
            logging.info('cmvn norm')
            for chan, c in enumerate(cep):
                cep[chan] = cmvn(c, label[chan])
        elif self.feat_norm == 'stg':
            logging.info('stg norm')
            for chan, c in enumerate(cep):
                cep[chan] = stg(c, label=label[chan])
            else:
                logging.warrning('Wrong feature normalisation type')
        return cep

    def load(self, show):
        """
        Load a cep from audio or mfcc file. This method loads all channels
        available in the file.
        
        :param show: the name of the show to load
        
        :return: the cep array and the label array
        """
        # test if features is already computed
        if self.show == show:
            # logging.debug('get precomputed mfcc: ' + show)
            return self.cep, self.label
        self.show = show
        if self.from_file == 'audio':
            logging.debug('compute MFCC: ' + show)
            logging.debug(self.__repr__())
            self.cep, self.label = self._features(show)
        else:
            if self.from_file == 'pickle':
                logging.debug('load pickle: ' + show)
                input_filename = os.path.join(self.input_dir.format(s=show),
                                              show + self.input_file_extension)
                self.cep = [read_pickle(input_filename)]
            elif self.from_file == 'spro4':
                logging.debug('load spro4: ' + show)
                input_filename = os.path.join(self.input_dir.format(s=show),
                                              show + self.input_file_extension)
                self.cep = [read_spro4(input_filename)]
            elif self.from_file == 'htk':
                logging.debug('load htk: ' + show)
                input_filename = os.path.join(self.input_dir.format(s=show),
                                              show + self.input_file_extension)
                self.cep = [read_htk(input_filename)[0]]
            else:
                raise Exception('unknown from_file value')

            input_filename = os.path.join(self.label_dir.format(s=show),
                                              show + self.label_file_extension)
            if os.path.isfile(input_filename):
                self.label = [read_label(input_filename)]
                if self.label[0].shape[0] != self.cep[0].shape[0]:
                    missing = np.zeros(self.cep[0].shape[0] - self.label[0].shape[0], dtype='bool')
                    self.label[0] = np.hstack((self.label[0], missing))
            else:
                self.label = [np.array([True] * self.cep[0].shape[0])]

        if self.filter is not None:
            self.cep[0] = self._filter(self.cep[0])
            if len(self.cep == 2):
                self.cep[1] = self._filter(self.cep[1])

        if not self.keep_all_features:
            logging.warning('!!! no keep all feature !!!')
            for chan in range(len(self.cep)):
                self.cep[chan] = self.cep[chan][self.label[chan]]
                self.label[chan] = self.label[chan][self.label[chan]]

        return self.cep, self.label

    def _filter(self, cep):
        """
        keep only the MFCC index present in the filter list
        :param cep:
        :return: return the list of MFCC given by filter list
        """
        if len(self.filter) == 0:
            raise Exception('filter list is empty')
        logging.debug('applied filter')
        return cep[:, self.filter]

    def save(self, show, filename, mfcc_format, and_label=True):
        """
        Save the cep array in file
        
        :param show: the name of the show to save (loaded if need)
        :param filename: the file name of the mffc file or a list of 2 filenames
            for the case of double channel files
        :param mfcc_format: format of the mfcc file taken in values
            ['pickle', 'spro4', 'htk']
        
        :raise: Exception if feature format is unknown
        """
        self.load(show)
        
        if len(self.cep) == 2:
            root, ext = os.path.splitext(filename)
            filename = [root + self.double_channel_extension[0] + ext, 
                        root + self.double_channel_extension[1] + ext]

        if mfcc_format.lower() == 'pickle':
            if len(self.cep) == 1 and self.cep[0].shape[0] > 0:
                logging.info('save pickle format: %s', filename)
                write_pickle(self.cep[0].astype(np.float32), filename)
            elif len(self.cep) == 2:
                logging.info('save pickle format: %s', filename[0])
                logging.info('save pickle format: %s', filename[1])
                if self.cep[0].shape[0] > 0:
                    write_pickle(self.cep[0].astype(np.float32), filename[0])
                if self.cep[1].shape[0] > 0:    
                    write_pickle(self.cep[1].astype(np.float32), filename[1])
        elif mfcc_format.lower() == 'text':
            if len(self.cep) == 1 and self.cep[0].shape[0] > 0:
                logging.info('save text format: %s', filename)
                np.savetxt(filename, self.cep)
            elif len(self.cep) == 2:
                logging.info('save text format: %s', filename[0])
                logging.info('save text format: %s', filename[1])
                if self.cep[0].shape[0] > 0:
                    np.savetxt(filename[0], self.cep[0])
                if self.cep[1].shape[0] > 0:    
                    np.savetxt(filename[1], self.cep[1])
        elif mfcc_format.lower() == 'spro4':
            if len(self.cep) == 1 and self.cep[0].shape[0] > 0:
                logging.info('save spro4 format: %s', filename)
                write_spro4(self.cep[0], filename)
            elif len(self.cep) == 2:
                logging.info('save spro4 format: %s', filename[0])
                logging.info('save spro4 format: %s', filename[1])
                if self.cep[0].shape[0] > 0:
                    write_spro4(self.cep[0], filename[0])
                if self.cep[1].shape[0] > 0:
                    write_spro4(self.cep[1], filename[1])
        elif mfcc_format.lower() == 'htk':
            if len(self.cep) == 1 and self.cep[0].shape[0] > 0:
                logging.info('save htk format: %s', filename)
                write_spro4(self.cep, filename)
            elif len(self.cep) == 2:
                logging.info('save htk format: %s', filename[0])
                logging.info('save htk format: %s', filename[1])
                if self.cep[0].shape[0] > 0:
                    write_htk(self.cep[0], filename[0])
                if self.cep[1].shape[0] > 0:
                    write_htk(self.cep[1], filename[1])
        else:
            raise Exception('unknown feature format')
        if and_label:
            if len(self.cep) == 1:
                output_filename = os.path.splitext(filename)[0] \
                                    + self.label_file_extension
                save_label(output_filename, self.label[0])
            elif len(self.cep) == 2:
                output_filename = [os.path.splitext(filename[0])[0] \
                                    + self.label_file_extension,
                                    os.path.splitext(filename[1])[0] \
                                    + self.label_file_extension]
                save_label(output_filename[0], self.label[0])
                save_label(output_filename[1], self.label[1])

    def save_list(self, audio_file_list, feature_file_list, mfcc_format, feature_dir, 
                  feature_file_extension, and_label=False):
        """
        Function that takes a list of audio files and extract features
        
        :param audio_file_list: an array of string containing the name of the feature 
            files to load
        """
        logging.info(self)
        size = 0
        for audio_file, feature_file in zip(audio_file_list, feature_file_list):
            cep_filename = os.path.join(feature_dir, feature_file + 
                feature_file_extension)                    
            logging.info('process %s', cep_filename)
            self.save(audio_file, cep_filename, mfcc_format, and_label)

    def dim(self):
        if self.show != 'empty':
            return self.cep.shape[1]
        dim = self.ceps_number
        if self.log_e:
            dim += 1
        if self.delta:
            dim *= 2
        if self.double_delta:
            dim *= 2
        logging.warning('cep dim computed using featureServer parameters')
        return dim

    def save_parallel(self, input_audio_list, output_feature_list, mfcc_format, feature_dir, 
                         feature_file_extension, and_label=False, numThread=1):
        """
        Extract features from audio file using parallel computation
        
        :param input_audio_list: an array of string containing the name 
            of the audio files to process
        :param output_feature_list: an array of string containing the 
            name of the features files to save
        :param numThread: number of parallel process to run
        """
        # Split the features to process for multi-threading
        loa = np.array_split(input_audio_list, numThread)
        lof = np.array_split(output_feature_list, numThread)
    
        jobs = []
        multiprocessing.freeze_support()
        for idx, feat in enumerate(loa):
            p = multiprocessing.Process(target=self.save_list,
                    args=(loa[idx], lof[idx], mfcc_format, feature_dir, 
                          feature_file_extension, and_label))                                       
            jobs.append(p)
            p.start()
        for p in jobs:
            p.join()

    def _load_and_stack_worker(self, input, output):
        """Load a list of feature files into a multiprocessing.Queue object
        
        :param input: a multiprocessing.JoinableQueue object
        :param output: a list of multiprocessing.Queue objects to fill
        """
        while True:
            next_task = input.get()
            
            if next_task is None:
                # Poison pill means shutdown
                output.put(None)
                input.task_done()
                break
            
            #check which channel to keep from the file
            if next_task.endswith(self.double_channel_extension[0]) and \
                        (self.from_file == 'audio'):
                next_task = next_task[:-len(self.double_channel_extension[0])]
                output.put(self.load(next_task)[0][0])
            if next_task.endswith(self.double_channel_extension[1]) and \
                        self.from_file == 'audio':
                next_task = next_task[:-len(self.double_channel_extension[1])]
                output.put(self.load(next_task)[0][1])
            else:
                cep = self.load(next_task)[0][0]
                output.put(cep)
            
            input.task_done()



    def load_and_stack(self, fileList, numThread=1):
        """Load a list of feature files and stack them in a unique ndarray. 
        The list of files to load is splited in sublists processed in parallel
        
        :param fileList: a list of files to load
        :param numThread: numbe of thead (optional, default is 1)
        """
        queue_in = multiprocessing.JoinableQueue(maxsize=len(fileList)+numThread)
        queue_out = []
        
        # Start worker processes
        jobs = []
        for i in range(numThread):
            queue_out.append(multiprocessing.Queue())
            p = multiprocessing.Process(target=self._load_and_stack_worker, 
                                        args=(queue_in, queue_out[i]))
            jobs.append(p)
            p.start()
        
        # Submit tasks
        for task in fileList:
            queue_in.put(task)

        for task in range(numThread):
            queue_in.put(None)
        
        # Wait for all the tasks to finish
        queue_in.join()
                   
        output = []
        for q in queue_out:
            while True:
                data = q.get()
                if data is None:
                    break
                output.append(data)

        for p in jobs:
            p.join()
        all_cep = np.concatenate(output, axis=0)

        return all_cep

