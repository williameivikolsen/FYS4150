import numpy as np

"""
Calculating analytical values of thermodynamical identities for the
two-dimensional system with L=2.
Boltzmanns constant k=1 so that temperature has unit energy
and the coupling constant J = 1
"""

def Z(beta):                        # The partition function
    return 4*np.cosh(8*beta) + 12

def mean_E(beta,Z):                 # Mean energy
    return -32*np.sinh(8*beta)/Z

def mean_E2(beta,Z):                # Mean energy squared
    return 256*np.cosh(8*beta)/Z

def mean_absM(beta,Z):              # Mean absolute value of magnetization
    return 8*(np.exp(8*B)+2)/Z

def mean_M2(beta,Z):                # Mean magnetization squared
    return 32*(np.exp(8*B)+1)/Z

T = 1                   # Temperature with dimension of energy
beta = 1/T              # Boltzmann's constant k is set to 1

print(mean_E(beta,Z(beta)))
