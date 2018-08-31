#!/usr/bin/env python
from mpl_toolkits.mplot3d import Axes3D
import sys
import data_reader
import matplotlib.pyplot as plt
import numpy as np

D_MIN = 31.6 #mm
D_ERROR = 1.01 #mm
LENGTH = 100

UNC=False
CONNECT=False
CONNECT_N = 3
EXPECTED=False
PLOT=False

if __name__ == '__main__':
    if '-u' in sys.argv:
        UNC=True

    if '-c' in sys.argv:
        CONNECT=True

    if '-e' in sys.argv:
        EXPECTED=True

    if '-p' in sys.argv:
        PLOT=True

    gtr_waves = data_reader.read(sys.argv[-1], strings=['E'], frets=['0'])
    peaks_all = []

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    if PLOT:
        i = 0
        for gtr_wave in gtr_waves:
            x_s, y_s = gtr_wave.normalized_abs_dft()
            peaks = gtr_wave.ft_peaks(min_dist=0.001, thres=0.2)
            peaks_all.append(peaks)

            ax.plot(x_s, np.full(x_s.size, i) + D_MIN, y_s) # Plots the waveform

            for peak in peaks:
                ax.plot([x_s[peak]], [i+D_MIN], [y_s[peak]], marker='o', color='r', 
                        markersize=1.2)

            if UNC:
                for j in range(0, x_s.size):
                    ax.plot([x_s[j], x_s[j]], 
                            [i - D_ERROR, i + D_ERROR], 
                            [y_s[j], y_s[j]],
                            marker='_', color='b')

            i += 10

    if CONNECT:
        colors = ['g', 'b', 'r']
        for i in range(0, CONNECT_N):
            ax.plot([gtr_wave.normalized_abs_dft()[0][
                        gtr_wave.ft_peaks(min_dist=0.001, thres=0.2)[i]] 
                        for gtr_wave in gtr_waves],
                    np.array([0, 10, 20, 30, 40, 50]) + D_MIN,
                    [gtr_wave.normalized_abs_dft()[1][
                        gtr_wave.ft_peaks(min_dist=0.001, thres=0.2)[i]]
                        for gtr_wave in gtr_waves],
                    color=colors[i], label=('Harmonic ' + str(i+2)))

    if EXPECTED:
        colors = ['g', 'b', 'r']
        offsets = [0.2, 0, 0]
        for i in range(2, CONNECT_N + 2):
            wav = gtr_waves[0]
            ax.plot(np.full(np.linspace(D_MIN, D_MIN + 50, num=100).size, 
                wav.normalized_abs_dft()[0][wav.ft_peaks(min_dist=0.001, thres=0.2)[i-2]]), 
                    np.linspace(D_MIN, D_MIN + 50, num=100),
                    [np.sin(i * np.pi * (val+D_MIN) / 648) + offsets[i-2] for val in np.linspace(0, D_MIN + 50, num=100)],
                    linestyle=':', color=colors[i-2])

    ax.set_xlabel('The frequency')
    ax.set_ylabel('The distance of the pickup [mm]')
    ax.set_zlabel('Relative amplitude')
    ax.legend()
    plt.show()
