import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Program to make plots from SolarSystem class

# Open data:
name_of_problem = sys.argv[1]
N = sys.argv[2]
Nobjects = int(sys.argv[3])
path = "./results/" + name_of_problem
os.chdir(path)
filename_euler = "Euler_" + N + ".txt"
filename_verlet = "Verlet_" + N + ".txt"

infile_euler = open(filename_euler, 'r')
infile_euler.readline()                                 # Skip one line
params = infile_euler.readline().split()                # Parameters located in line 2
t0 = params[1]
tn = params[2]
h = params[4]
infile_euler.seek(0)

# Read through infiles, structure is [x y z vx vy vz]:
data_euler = np.loadtxt(filename_euler, skiprows=4)
# data_verlet = np.loadtxt(infile_verlet, skiprows=4)

for i in range(Nobjects):
    plt.plot(data_euler[:,6*i], data_euler[:,6*i+1])
# plt.plot(data_verlet[:,0], data_verlet[:,1], label="Verlet")
plt.plot(0,0, marker="*", markerfacecolor="yellow", markersize=10, markeredgecolor="black", markeredgewidth=1)

plt.grid(ls="--")
plt.axis('equal')
# plt.xlim([-2,2])
# plt.ylim([-2,2])
# plt.legend()
plt.title("T = " + tn + " N = " + N)
plt.savefig("plot_" + N + ".pdf")
plt.show()
