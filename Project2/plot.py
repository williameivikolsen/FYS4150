import matplotlib.pyplot as plt
import numpy as np
import sys
import os

system = sys.argv[1]
n = sys.argv[2]
filename = system + "_" + n + ".txt"
path = "./" + system
plotname = system + "_" + n + ".png"

os.chdir(path)

data = np.loadtxt(filename, skiprows=2)
eigenvalues = data[0]
eigenvectors = data[1:]

valmin = np.min(eigenvalues)        # Smallest eigenvalue
idxmin = np.argmin(eigenvalues)     # Index of smallest eigenvalue
vecmin = eigenvectors[:, idxmin]       # Eigenvector with smallest eigenvaluel

rhomin = 0
rhomax = 1
rho = np.linspace(rhomin, rhomax, int(n))

plt.plot(rho, vecmin)
plt.xlabel(r'$\rho$')
plt.ylabel(r'$u(\rho)$')
plt.grid(ls='--')
plt.savefig(plotname)