import numpy as np
import matplotlib.pyplot as plt
import os

os.chdir("./results/")
data = np.loadtxt('mctest.txt')
cycles = data[:, 2]
energy = data[:, 3]
magnetization = data[:, 4]

plt.plot(cycles, energy)
plt.xscale('log')
plt.xlabel('Cycles')
plt.ylabel('Average energy')
plt.show()

plt.plot(cycles, magnetization)
plt.xscale('log')
plt.xlabel('Cycles')
plt.ylabel('Average magnetization')
plt.show()