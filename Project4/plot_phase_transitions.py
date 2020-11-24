import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


plt.style.use('seaborn')
sns.set(font_scale=1.3)

os.chdir('./results')
data = np.loadtxt('phase_transitions.txt', skiprows=1)
# data = np.loadtxt('phase_transitions_copy_nov24.txt', skiprows=1)

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
    plt.plot(T[idx], CV[idx], '-o', label='L = %i' % L)
plt.xlabel(r'$T$ [kT/J]')
plt.ylabel(r'$\chi /N$')
plt.legend()
plt.tight_layout()
plt.show()


TC = {}
for L in Lvals:
    idx = idx_dict[L]
    TC[L] = T[np.argmax(chi[idx])]
print(TC)