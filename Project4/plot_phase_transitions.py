import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use('seaborn')

os.chdir('./results')
data = np.loadtxt('phase_transitions.txt', skiprows=1)
L = data[:, 0]
T = data[:, 1]
cycles = data[:, 2]
E = data[:, 3]
M = data[:, 4]
CV = data[:, 5]
chi = data[:, 6]

Lvals = [40, 60, 80, 100]
idx_dict = {i: np.where(L == i) for i in Lvals}

for L in Lvals:
    idx = idx_dict[L]
    plt.plot(T[idx], M[idx], '-o', label='L = %i' % L)
plt.xlabel(r'$T$')
plt.ylabel(r'$\langle|M|\rangle$')
plt.legend()
plt.show()