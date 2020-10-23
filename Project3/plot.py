import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Program to make plots from SolarSystem class
# Open data:
name_of_problem = sys.argv[1]           # Name of the system we have calculated
N = sys.argv[2]                         # Number of integration points
Nobjects = int(sys.argv[3])             # Number of objects/planets
path = "./results/" + name_of_problem   # path to data
os.chdir(path)

filename_verlet = "Verlet_" + N + ".txt"
infile_verlet = open(filename_verlet, 'r')
infile_verlet.readline()                                 # Skip one line
params = infile_verlet.readline().split()          # Parameters located in line 2
t0 = params[1]
tn = params[2]
h = params[4]
infile_verlet.seek(0)

if name_of_problem == "sun_earth":
    filename_euler = "Euler_" + N + ".txt"
    infile_euler = open(filename_euler,'r')
    data_euler = np.loadtxt(filename_euler, skiprows=4)

data_verlet = np.loadtxt(filename_verlet, skiprows=4)       # Structure is [x y z vx vy vz ...]

for i in range(1,Nobjects):                                 # Skips sun
    plt.plot(data_verlet[:,6*i], data_verlet[:,6*i+1], label="Verlet")
    if name_of_problem == "sun_earth":
        plt.plot(data_euler[:,6*i], data_euler[:,6*i+1], label = "Euler")
plt.plot(0,0, marker="*", markerfacecolor="yellow", markersize=10, markeredgecolor="black", markeredgewidth=1)

plt.grid(ls="--")
plt.axis('equal')
# plt.xlim([-2,2])
# plt.ylim([-2,2])
plt.legend()
plt.title("T = " + tn + " N = " + N)
plt.savefig("plot_" + N + ".pdf")
plt.show()
