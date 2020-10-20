import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Program to make plots from SolarSystem class

# Open data:
name_of_problem = sys.argv[1]
N = sys.argv[2]
path = "./results/" + name_of_problem
os.chdir(path)
infile_euler = "Euler_" + N + ".txt"
# infile_verlet = "Verlet_" + N + ".txt"

# Read through infiles, structure is [x y z vx vy vz]:
data_euler = np.loadtxt(infile_euler, skiprows=4)
# data_verlet = np.loadtxt(infile_verlet, skiprows=4)

plt.plot(data_euler[:,0], data_euler[:,1])
plt.plot(data_euler[:,6], data_euler[:,7])
# plt.plot(data_verlet[:,0], data_verlet[:,1], label="Verlet")
plt.plot(0,0, marker="*", markerfacecolor="yellow", markersize=10, markeredgecolor="black", markeredgewidth=1)

plt.grid(ls="--")
plt.axis('equal')
plt.xlim([-2,2])
plt.ylim([-2,2])
# plt.legend()
plt.title("N = " + N)
plt.savefig("plot_" + N + ".png")