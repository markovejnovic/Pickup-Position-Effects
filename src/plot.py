#!/usr/bin/env python

from data_reader import read
import matplotlib.pyplot as plt
import sys

gtr_w = read(sys.argv[-1])
gtr_w.plot(y_unc=0.002)
plt.xlabel('Time [s]')
plt.ylabel('Amplitude [V]')
plt.show()
