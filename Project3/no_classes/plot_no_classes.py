import numpy as np
import matplotlib.pyplot as plt

# Program to make plots from no_classes.cpp

# Manually go through desired values of n:
n = [366, 1826, 73001]


for i in n:
    i = int(i)
    # Open data from special and general algorithm for n = 1:
    infile_euler = open("Euler_%i.txt" % i)   
    infile_verlet = open("Verlet_%i.txt" % i)

    # Read through infiles, structure is [rx ry vx vy]:
    data_euler = np.loadtxt(infile_euler, skiprows=4)
    data_verlet = np.loadtxt(infile_verlet, skiprows=4)

    plt.plot(data_euler[:,0], data_euler[:,1], label="Euler")
    plt.plot(data_verlet[:,0], data_verlet[:,1], label="Verlet")
    plt.plot(0,0, marker="*", markerfacecolor="yellow", markersize=10, markeredgecolor="black", markeredgewidth=1)

    plt.grid(ls="--")
    plt.axis('equal')
    plt.xlim([-2,2])
    plt.ylim([-2,2])
    plt.legend()
    plt.title("N = %i" % i)
    plt.savefig("N_%i.png" % i)
    plt.close()
