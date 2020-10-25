import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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
os.chdir(path)


filename_verlet = "Verlet_" + N + "_" + T + ".txt"
infile_verlet = open(filename_verlet, 'r')
infile_verlet.readline()                                 # Skip one line
params = infile_verlet.readline().split()          # Parameters located in line 2
t0 = params[1]
tn = params[2]
# h = params[4]
infile_verlet.seek(0)

planet_names = ["The sun", "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"] # Names of objects in the solar system

data_verlet = np.loadtxt(filename_verlet, skiprows=4)       # Structure is [x y z vx vy vz ...]

if name_of_problem == "sun_earth":
    filename_euler = "Euler_" + N + "_" + T + ".txt"
    infile_euler = open(filename_euler,'r')
    data_euler = np.loadtxt(filename_euler, skiprows=4)

    for i in range(1,Nobjects):                       # Skips sun
        plt.plot(data_verlet[:,3*i], data_verlet[:,3*i+1], label= "Velocity Verlet")
        plt.plot(data_euler[:,3*i], data_euler[:,3*i+1], label = "Forward Euler")

    plt.plot(0,0, marker="*", markerfacecolor="yellow", markersize=10, markeredgecolor="black", markeredgewidth=1)

elif name_of_problem == "sun_earth_jupiter":
    name = ["Sun","Earth", "Jupiter"]
    for i in range(0,Nobjects):
        plt.plot(data_verlet[:,3*i], data_verlet[:,3*i+1], label = name[i])

else:
    for i in range(1,Nobjects):       # Skips sun
        plt.plot(data_verlet[:,3*i], data_verlet[:,3*i+1], label = planet_names[i])
    plt.plot(0,0, marker="*", markerfacecolor="yellow", markersize=10, markeredgecolor="black", markeredgewidth=1)


plt.grid(ls="--")
#plt.axis('equal')
plt.xlabel("x [AU]")
plt.ylabel("y [AU]")
# plt.xlim([-2,2])
# plt.ylim([-2,2])
plt.legend()
#plt.title("T = " + tn + " N = " + N)
figname = "plot" + "N_" + N + "_T" + T + ".pdf"
if beta != "2":
    nums = beta.split(".")
    figname = "plot" + "N_" + N + "_T" + T + "_beta" + nums[0] + nums[1] + ".pdf"
plt.savefig(figname)
plt.show()

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
        figname = "plot3D" + "_N" + N + "_T" + T + ".pdf"
        plt.savefig(figname)
        plt.show()
