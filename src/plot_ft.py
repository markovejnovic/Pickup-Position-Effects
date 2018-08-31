#!/usr/bin/env python

from data_reader import read
import matplotlib.pyplot as plt
import sys

gtr_w = read(sys.argv[-1])
gtr_w.plot_normalized_ft()
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude [V]')
plt.show()
