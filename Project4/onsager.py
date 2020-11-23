import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

plt.style.use('seaborn')
TC = np.array([2.23, 2.25, 2.27, 2.26])
L = np.array([40, 60, 80, 100])
slope, intercept, r_value, p_value, std_err = stats.linregress(1/L, TC)
Larray = np.linspace(1/(L[-1]*10), 1.5/L[0], 100)
plt.plot(1/L, TC, 'o')
plt.plot(Larray, slope*Larray + intercept)
# plt.fill_between(Larray, (slope+std_err)*Larray + intercept + p_value, (slope-std_err)*Larray + intercept - p_value, alpha=0.3, color='orange')
plt.xlabel(r'$1/L$')
plt.ylabel(r'$T_C(L)$')
plt.show()