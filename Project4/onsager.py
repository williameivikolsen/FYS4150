import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def linregress(x, y):
    n = len(x)
    D = np.dot(x, x) - 1/n*np.sum(x)**2
    E = np.dot(x, y) - 1/n*np.sum(x)*np.sum(y)
    F = np.dot(y, y) - 1/n*np.sum(y)**2
    m = E/D
    c = np.mean(y) - m*np.mean(x)
    delta_m = np.sqrt(1/(n-2)*(D*F-E**2)/D**2)
    delta_c = np.sqrt(1/(n-2)*(D/n + np.mean(x)**2)*(D*F-E**2)/D**2)
    return m, delta_m, c, delta_c

plt.style.use('seaborn')
TC = np.array([2.2, 2.275, 2.15, 2.05])
L = np.array([40, 60, 80, 100])
# slope, intercept, r_value, p_value, std_err = stats.linregress(1/L, TC)
slope, delta_slope, intercept, delta_intercept = linregress(1/L, TC)
print(intercept)
print(delta_intercept)
Larray = np.linspace(20, 1000, 100)
plt.plot(1/L, TC, 'o')
plt.plot(1/Larray, slope/Larray + intercept)
# plt.fill_between(Larray, (slope+std_err)*Larray + intercept + p_value, (slope-std_err)*Larray + intercept - p_value, alpha=0.3, color='orange')
plt.xlabel(r'$1/L$')
plt.ylabel(r'$T_C(L)$')
plt.ylim(1.9, 2.4)
plt.show()