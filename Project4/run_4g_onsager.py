import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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
sns.set(font_scale=1.3)
# TC = np.array([2.292, 2.276, 2.288, 2.276]) # From C_V
TC = np.array([2.324, 2.304, 2.3, 2.288]) # From chi
L = np.array([40, 60, 80, 100])
a, da, b, db = linregress(1/L, TC)
print(a)
print(da)
Larray = np.linspace(29, 1000, 100)
plt.plot(1/L, TC, 'o', label='Critical temperatures')
plt.plot(1/Larray, a/Larray + b, label=r'$a/L + b$')
plt.fill_between(1/Larray, a/Larray + b + db, a/Larray + b - db, alpha=0.3, color='orange', label=r'$a/L + b \pm \Delta b$')
plt.text(0.024, 2.297, r'$L = 40$', fontsize=12)
plt.text(0.015, 2.264, r'$L = 60$', fontsize=12)
plt.text(0.011, 2.292, r'$L = 80$', fontsize=12)
plt.text(0.008, 2.265, r'$L = 100$', fontsize=12)
plt.xlabel(r'$1/L$')
plt.ylabel(r'$T_C(L)$')
plt.ylim(2.2, 2.4)
plt.legend()
plt.tight_layout()
plt.show()