'''
Test program that does the following tests:
    1) Check that solutions match with circular orbit
    2) Check that potential + kinetic energy stays constant
    3) Check that angular momentum is conserved
'''
import os
import numpy as np
import matplotlib.pyplot as plt

# N = int(input("Which value of step size N to test for? "))
# assert open("Euler_%i.txt" % N), "Output files not found for this value of N. Try again after computing results."
N=73001

# Start by reading data from files
infile_euler = open("Euler_%i.txt" % N, "r")   
infile_verlet = open("Verlet_%i.txt" % N, "r")

infile_euler.readline()                                 # Skip one line
params = infile_euler.readline().split()                # Parameters located in line 2

t0 = float(params[1])
tn = float(params[2])
h = float(params[4])

infile_euler.seek(0)                                    # Reset file handle to start

data_euler = np.loadtxt(infile_euler, skiprows=4)       # Actual data arrays
data_verlet = np.loadtxt(infile_verlet, skiprows=4)     # Format rx-ry-vx-vy

infile_euler.close()
infile_verlet.close()

def test_circular(data_set, metohd_name, eps=1e-2):     # Takes in either the data_euler or data_verlet
    rx, ry = data_set[:,0], data_set[:,1]
    theta0 = np.arctan2(ry[0], rx[0])                   # Initial angle
    delta_theta = 2*tn*np.pi/(N-1)                      # Change of angle assuming circular orbit

    rx_test = np.zeros(N)                               # Make arrays for circular orbit
    ry_test = np.zeros(N)
    for i in range(N):
        rx_test[i] = np.cos(theta0 + i*delta_theta)
        ry_test[i] = np.sin(theta0 + i*delta_theta)


    deviance = np.sqrt((rx-rx_test)**2 + (ry-ry_test)**2)   # Deviance from circle for every step
    max_deviance = np.max(deviance)                         # Max deviance
    num_problems = np.sum(deviance > eps)                   # Number of steps exceeding deviance
    if num_problems != 0:
        first_problem_idx = np.min(np.where(deviance > eps))    # First index that exceeds deviance
    
    # Print out results
    print("Testing for method {}, tolerance set to {}...".format(metohd_name, eps))
    if num_problems == 0:
        print("The test was passed successfully!")
        print("Max recorded deviance was {:.7f}".format(max_deviance))

    else:
        print("The test failed for {}/{} time steps".format(num_problems, N))
        print("The problems started at index {}".format(first_problem_idx))
        print("Max recorded deviance was {:.7f}".format(max_deviance))

    return deviance


def test_ang_moment_conservation(data_set, metohd_name, eps=1e-2):
    pass
def test_energy_conservation(data_set, method_name, eps=1e-2):
    pass


deviance_verlet_circle = test_circular(data_verlet, "Verlet")
deviance_euler_cirlce = test_circular(data_euler, "Euler")

steps = np.arange(N)
plt.plot(steps, deviance_euler_cirlce, label="Euler")
plt.plot(steps, deviance_verlet_circle, label="Verlet")
plt.xlabel("N")
plt.ylabel("Deviation [AU]")
plt.yscale("log")
plt.title("N = {}".format(N))
plt.legend()
plt.show()