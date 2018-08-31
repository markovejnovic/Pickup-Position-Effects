import matplotlib.pyplot as plt
import numpy as np
import peakutils

class GuitarWaveform:
    """Represents a guitar waveform
    
    Arguments:
        array - An array containing the values of the oscilloscope read"""

    def __init__(self, array, fs, v_scale, h_scale, name):
        array = np.array(array)
        self._fs = fs
        self._samples_n = array.size
        self._times = np.linspace(0, self._samples_n / self._fs, 
                self._samples_n)
        self._amplitudes = array * v_scale / 5
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    _dft = np.array([])
    def dft(self, force=False):
        if force or self._dft.size == 0:
            self._dft = np.fft.fft(self._amplitudes) / self._samples_n
            self._dft = self._dft[range(int(self._samples_n / 2))]
        return self._dft

    _abs_dft_freq = np.array([])
    _abs_dft = np.array([])
    def abs_dft(self, force=False):
        if force or not self._abs_dft.size or not self._abs_dft_freq.size:
            frq = np.arange(self._samples_n) * self._fs / self._samples_n
            self._abs_dft_freq = frq[range(int(self._samples_n / 2))]
            self._abs_dft = abs(self.dft())
        return self._abs_dft_freq, self._abs_dft

    _normalized_abs_dft_freq = np.array([])
    _normalized_abs_dft = np.array([])
    def normalized_abs_dft(self, force=False, cutoff_threshold=1500):
        if force or not self._normalized_abs_dft.any() or not \
                self._normalized_abs_dft.size:
            n_abs_dft = self.abs_dft()[1] / np.amax(self.abs_dft()[1])
            n_abs_dft_freq = self.abs_dft()[0]

            if cutoff_threshold:
                i = 0
                for val in n_abs_dft_freq:
                    if val > cutoff_threshold:
                        break
                    else:
                        i += 1
                self._normalized_abs_dft = n_abs_dft[0:i]
                self._normalized_abs_dft_freq = n_abs_dft_freq[0:i]

            else:
                self._normalized_abs_dft = n_abs_dft
                self._normalized_abs_dft_freq = n_abs_dft_freq

        return self._normalized_abs_dft_freq, self._normalized_abs_dft

    _peaks = np.array([])
    def ft_peaks(self, force=False, min_dist=10, thres=0.03):
        if force or not self._peaks.size:
            self._peaks = \
                    peakutils.indexes(self.normalized_abs_dft(force=force)[1],  
                        min_dist=min_dist, thres=thres)
        return self._peaks

    def plot(self, x_unc=0, y_unc=0):
        if x_unc == 0 and y_unc == 0:
            plt.plot(self._times, self._amplitudes)
        else:
            plt.errorbar(self._times, self._amplitudes, 
                    xerr=x_unc, yerr=y_unc, ecolor='r', 
                    capsize=1.5, linewidth=1)

    def plot_ft(self, length=100, ax=None, zs=0):
        x, y = self.abs_dft()
        if not ax:
            plt.plot(x[0:length], y[0:length])
        else:
            ax.plot(x[0:length], y[0:length], zs=zs, zdir='y')

    def plot_normalized_ft(self, length=100, ax=None, zs=0):
        x, y = self.normalized_abs_dft()
        if not ax:
            plt.plot(x[0:length], y[0:length])
        else:
            ax.plot(x[0:length], y[0:length], zs=zs, zdir='y')
