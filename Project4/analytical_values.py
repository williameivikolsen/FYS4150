import numpy as np

"""
Calculating analytical values of thermodynamical identities for the
two-dimensional system with L=2.
Boltzmanns constant k=1 so that temperature has unit energy
and the coupling constant J = 1
"""

T = 1                   # Temperature with dimension of energy
beta = 1/T              # Boltzmann's constant k is set to 1
Z = 4*np.cosh(8*beta) + 12
mean_E = -32*np.sinh(8*beta)/Z
mean_E2 = 256*np.cosh(8*beta)/Z
mean_absM = 8*(np.exp(8*beta)+2)/Z
mean_M2 = 32*(np.exp(8*beta)+1)/Z
CV = 1/T**2*(mean_E2 - mean_E**2)
chi = 1/T*mean_M2
print('E = ', mean_E)
print('|M| = ', mean_absM)
print('C_V = ', CV)
print('chi = ', chi)