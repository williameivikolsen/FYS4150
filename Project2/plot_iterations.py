import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

data = np.loadtxt("iterations.txt", skiprows=1, usecols=(0,1))
n = data[:, 0]
its = data[:, 1]
slope, intercept, r_value, p_value, std_err = stats.linregress(np.log10(n), np.log10(its))
plt.plot(np.log10(n), np.log10(its), 'o', label='Data points')
plt.plot(np.log10(n), slope*np.log10(n) + intercept, label='Linear fit')
plt.xlabel(r'$\log 10 (n)$')
plt.ylabel('Log10 of iterations')
plt.grid(ls='--')
plt.legend()
plt.savefig('iterations.png')