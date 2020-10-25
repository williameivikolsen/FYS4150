import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Program to make plots from SolarSystem class
# Open data:
name_of_problem = sys.argv[1]           # Name of the system we have calculated
N = sys.argv[2]                         # Number of integration points
Nobjects = int(sys.argv[3])             # Number of objects/planets
T = sys.argv[4]                         # Simulation time
beta = sys.argv[5]                      # Beta parameter

path = "./results/" + name_of_problem   # path to data
if beta != '2':
    path += '/beta_tests'               # HUSK å legge inn beta-verdien i plott!

if len(sys.argv) > 6:
    additional_params = sys.argv[6]         # Additional params for special cases (Jupiter scaling, Earth inital values)
    if name_of_problem == "sun_earth_jupiter" and additional_params != "":
        scaling = additional_params
        scaling_str0 = scaling.split(".")
        if len(scaling_str0) > 1:                                       # If decimal number in scaling
            scaling_str = scaling_str0[0] + "_" + scaling_str0[1]
        else:
            scaling_str = scaling_str0[0]

        path += "/" + scaling_str

os.chdir(path)

filename_verlet = "Verlet_" + N + "_" + T + ".txt"
infile_verlet = open(filename_verlet, 'r')
infile_verlet.readline()                                 # Skip one line
params = infile_verlet.readline().split()          # Parameters located in line 2
t0 = params[1]
tn = params[2]
# h = params[4]
infile_verlet.seek(0)

if name_of_problem == "sun_earth":
    filename_euler = "Euler_" + N + "_" + T + ".txt"
    infile_euler = open(filename_euler,'r')
    data_euler = np.loadtxt(filename_euler, skiprows=4)

data_verlet = np.loadtxt(filename_verlet, skiprows=4)       # Structure is [x y z vx vy vz ...]

for i in range(1,Nobjects):                                 # Skips sun
    plt.plot(data_verlet[:,3*i], data_verlet[:,3*i+1], label="Verlet")
    if name_of_problem == "sun_earth":
        plt.plot(data_euler[:,3*i], data_euler[:,3*i+1], label = "Euler")
plt.plot(0,0, marker="*", markerfacecolor="yellow", markersize=10, markeredgecolor="black", markeredgewidth=1)

plt.grid(ls="--")
plt.axis('equal')
# plt.xlim([-2,2])
# plt.ylim([-2,2])
plt.legend()
plt.title("T = " + tn + " N = " + N)
figname = "plot" + "_N" + N + "_T" + T + ".pdf"
if beta != '2':
    nums = beta.split(".")
    figname = "plot" + "_N" + N + "_T" + T + "_beta" + nums[0] + nums[1] + ".pdf"
plt.savefig(figname)
plt.show()