import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import os
from set_axes_equal import set_axes_equal

# Program to make plots from SolarSystem class

# Program parameters are taken from execute.py, and can be run from command line if beta=2 and no Jupiter mass scaling/special initial conditions
name_of_problem = sys.argv[1]           # Name of the system we have calculated
N = sys.argv[2]                         # Number of integration points
Nobjects = int(sys.argv[3])             # Number of objects/planets
T = sys.argv[4]                         # Simulation time
beta = sys.argv[5]                      # Beta parameter
circtest = sys.argv[6]                  # Check if circle test

path = "./results/" + name_of_problem   # path to data

if beta != '2':
    path += '/beta_tests'               # HUSK å legge inn beta-verdien i plott!
if circtest == '1':
    path += '/circ_tests'

elif len(sys.argv) > 7:
    additional_params = sys.argv[7]         # Additional params for special cases (Jupiter scaling, Earth inital values)
    if name_of_problem == "sun_earth_jupiter" and additional_params != "":
        scaling = additional_params
        scaling_str0 = scaling.split(".")
        if len(scaling_str0) > 1:                                       # In case of decimal number in scaling parameter
            scaling_str = scaling_str0[0] + "_" + scaling_str0[1]
        else:
            scaling_str = scaling_str0[0]

        path += "/" + scaling_str

os.chdir(path)

planet_names = ["The sun", "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"] # Names of objects in the solar system

filename_verlet = "Verlet_" + N + "_" + T + ".txt"
data_verlet = np.loadtxt(filename_verlet, skiprows=4)       # Structure is [x y z vx vy vz ...]

if name_of_problem == "sun_earth":
    filename_euler = "Euler_" + N + "_" + T + ".txt"
    infile_euler = open(filename_euler,'r')
    data_euler = np.loadtxt(filename_euler, skiprows=4)

    plt.plot(data_verlet[:,3], data_verlet[:,4], label= "Velocity Verlet")
    plt.plot(data_euler[:,3], data_euler[:,4], label = "Forward Euler", ls='--')

    plt.plot(0,0, marker="*", markerfacecolor="yellow", markersize=10, markeredgecolor="black", markeredgewidth=1)
    plt.xlim(-1.5, 1.5)
    plt.ylim(-1.5, 1.5)

elif name_of_problem == "sun_earth_jupiter":
    name = ["Sun","Earth", "Jupiter"]
    for i in range(Nobjects):
        plt.plot(data_verlet[:,3*i], data_verlet[:,3*i+1], label = name[i])

else:
    for i in range(1,Nobjects):       # Range starting on 1 -> Sun not plotted.
        plt.plot(data_verlet[:,3*i], data_verlet[:,3*i+1], label = planet_names[i])
    plt.plot(0,0, marker="*", markerfacecolor="yellow", markersize=10, markeredgecolor="black", markeredgewidth=1)

plt.grid(ls="--")
plt.axis('equal')
plt.xlabel("x [AU]")
plt.ylabel("y [AU]")
plt.legend()
figname = "plot" + "N_" + N + "_T" + T + ".pdf"

# Add extension to figure filename if beta != 2
if beta != "2":
    nums = beta.split(".")
    if len(nums) > 1:
        figname = "plot" + "N_" + N + "_T" + T + "_beta" + nums[0] + nums[1] + ".pdf"
    else:
        figname = "plot" + "N_" + N + "_T" + T + "_beta" + nums[0] + ".pdf"

plt.tight_layout()
plt.savefig(figname)
plt.show()

# If looking at whole solar system, ask if user wants 3D plot
if name_of_problem == "full_system":
    plot3d = input("Do you want to plot the solar system in 3D? Y/N: ")
    if plot3d == "Y":
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        for i in range(1,Nobjects):       # Skips sun
            ax.plot(data_verlet[:,3*i], data_verlet[:,3*i+1], data_verlet[:,3*i+2], label = planet_names[i])
        ax.set_zlabel("z [AU]")
        ax.set_xlabel("x [AU]")
        ax.set_ylabel("y [AU]")
        plt.legend()
        plt.tight_layout()
        set_axes_equal(ax)
        # plt.savefig("3D" + figname)
        # plt.plot(0,0, marker="*", markerfacecolor="yellow", markersize=10, markeredgecolor="black", markeredgewidth=1)
        # plt.savefig("3D" + "inner" + "N_" + N + "_T" + T + ".pdf")
        plt.show()
