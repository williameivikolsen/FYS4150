'''
Test program that does the following tests:
    1) Check that solutions match with circular orbit
    2) Check that potential + kinetic energy stays constant
    3) Check that angular momentum is conserved
'''
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

name_of_problem = sys.argv[1]           # Name of the system we have calculated
N = sys.argv[2]                         # Number of integration points
Nobjects = int(sys.argv[3])             # Number of objects/planets
T = sys.argv[4]                         # Simulation time
beta = sys.argv[5]                      # Beta parameter
circtest = input("Circle test? Y/N: ")
path = "./results/" + name_of_problem   # path to data
if beta != '2':
    path += '/beta_tests'               # HUSK å legge inn beta-verdien i plott!
if circtest == "Y":
    print("Circle test chosen.")
    path += '/circ_tests'
os.chdir(path)

# Start by reading data from files
filename_euler = "Euler_" + N + "_" + T + ".txt"
filename_verlet = "Verlet_" + N + "_" + T + ".txt"
infile_euler = open(filename_euler, "r")   

infile_euler.readline()                                 # Skip one line
params = infile_euler.readline().split()                # Parameters located in line 2

t0 = float(params[1])
tn = float(params[2])
h = float(params[4])

infile_euler.seek(0)                                    # Reset file handle to start
infile_euler.close()

data_euler = np.loadtxt(filename_euler, skiprows=4)       # Actual data arrays
data_verlet = np.loadtxt(filename_verlet, skiprows=4)     # Format rx-ry-vx-vy

N = int(N)
if N >= 100000:
    N = int(N/100)

steps = np.arange(N)                                    # Arrays for plotting

def test_circular(data_set, metohd_name, eps=1e-2):     # Takes in either the data_euler or data_verlet
    rx, ry = data_set[:,3], data_set[:,4]
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
    print("-----------------------------------------------------------------------")
    print("Testing if circular orbit for method {}, tolerance set to {}...".format(metohd_name, eps))
    print("-----------------------------------------------------------------------")

    if num_problems == 0:
        print("The test was passed successfully!")
        print("Max recorded deviance was {:.7f}".format(max_deviance))

    else:
        print("The test failed for {}/{} time steps".format(num_problems, N))
        print("The problems started at index {}".format(first_problem_idx))
        print("Max recorded deviance was {:.7f}".format(max_deviance))

    return deviance


def test_ang_moment_conservation(data_set, method_name, eps=1e-2, dT=float(T)/100):  
    # eps is tolerance ratio [1]
    # dT is time duration that's going to be swept over [yr]

    rx, ry = data_set[:,3], data_set[:,4]
    num_checks = int((tn-t0)/dT)     # Number of checks given a value of dT
    area = np.zeros(num_checks)
    dN = int(N/num_checks) - 1       # Number of steps for every sweep
    for i in range(num_checks):
        idx_0 = int(i*N/num_checks)  # Start inde for every sweep 
        for j in range(dN):
            pos0 = np.array([rx[idx_0 + j], ry[idx_0+j]])
            pos1 = np.array([rx[idx_0 + (j+1)], ry[idx_0+(j+1)]])
            
            # Approximate area with triangle
            base_length = np.sqrt(np.dot((pos0+pos1)/2, (pos0+pos1)/2)) 
            heigth = np.sqrt(np.dot(pos1-pos0, pos1-pos0))

            area[i] +=  0.5*base_length*heigth
    area_diff_ratio = np.abs(area - area[0])/area[0]
    return area_diff_ratio, num_checks




def test_energy_conservation(data_set, method_name, eps=1e-4):      # eps is tolerance ratio
    rx, ry = data_set[:,3], data_set[:,4]
    vx = np.gradient(rx, h)
    vy = np.gradient(ry, h)

    # SI_conv_vel = 4740.47                                     # 1 AU/yr = 4740.47 m/s
    # m = 5.972e24                                              # Earth mass [kg]
    kin_energy = 0.5*np.sqrt(vx**2 + vy**2)                     # Kin. energy per mass [AU^2/yr^2]
    kin_energy_reldiff = np.abs((kin_energy - kin_energy[0])/kin_energy[0])        # Abs. difference from initial kinetic energy 

    pot_energy = -4*np.pi**2/(np.sqrt(rx**2 + ry**2))           # Pot. energy per mass [AU^2/yr^2]
    pot_energy_reldiff = np.abs((pot_energy - pot_energy[0])/pot_energy[0])        # Abs. difference from initial potential energy

    tot_energy = kin_energy + pot_energy
    tot_energy_reldiff = np.abs((tot_energy - tot_energy[0])/tot_energy[0])

    max_pot_reldiff = np.max(pot_energy_reldiff)
    max_kin_reldiff = np.max(kin_energy_reldiff)
    max_tot_reldiff = np.max(tot_energy_reldiff)
    
    num_fail = 0                                                # Number of failed tests

    print("-----------------------------------------------------------------------")
    print("Testing if energy conserved for method {}, biggest ratio from initial value allowed is {:.3e}...".format(method_name, eps))
    print("Total initial energy: ", tot_energy[0])
    print("-----------------------------------------------------------------------")

    if max_pot_reldiff > eps:
        print("The test failed for potential energy")
        print("Max recorded deviance ratio from initial energy was {:.7e}".format(max_pot_reldiff))
        num_fail += 1

    if max_kin_reldiff > eps:
        print("The test failed for kinetic energy")
        print("Max recorded deviance ratio from initial energy was {:.7e}".format(max_kin_reldiff))
        num_fail += 1

    if max_tot_reldiff > eps:
        print("The test failed for total energy")
        print("Max recorded deviance ratio from initial energy was {:.7e}".format(max_tot_reldiff))
        num_fail += 1

    if num_fail == 0:
        print("The tests (kinetic/potential/total energy) were passed successfully!")
        print("Max recorded deviance ratio (total energy) was {:.7e}".format(max_tot_reldiff))

    return kin_energy_reldiff, pot_energy_reldiff, tot_energy_reldiff


# Plot 1: Deviance from circle with different methods

deviance_verlet_circle = test_circular(data_verlet, "Verlet")
deviance_euler_cirlce = test_circular(data_euler, "Euler")

plt.figure(1)
plt.plot(steps, deviance_euler_cirlce, label="Euler")
plt.plot(steps, deviance_verlet_circle, label="Verlet")
plt.xlabel("N")
plt.ylabel("Deviation [AU]")
plt.yscale("log")
plt.legend()
plt.tight_layout()

# Plot 2: Deviance from initial energies

verlet_kin_reldiff, verlet_pot_reldiff, verlet_tot_reldiff = test_energy_conservation(data_verlet, "Verlet")
euler_kin_reldiff, euler_pot_reldiff, euler_tot_reldiff = test_energy_conservation(data_euler, "Euler")

plt.figure(2, figsize=(15,4))

plt.subplot(1,3,1)
plt.plot(steps, verlet_kin_reldiff, label="Kinetic energy Verlet")
plt.plot(steps, euler_kin_reldiff, label="Kinetic energy Euler")
plt.xlabel("N")
plt.ylabel("Absolute ratio of deviation [1]")
plt.yscale("log")
plt.legend()

plt.subplot(1,3,2)
plt.plot(steps, verlet_pot_reldiff, label="Potential energy Verlet")
plt.plot(steps, euler_pot_reldiff, label="Potential energy Euler")
plt.xlabel("N")
plt.yscale("log")
plt.legend()

plt.subplot(1,3,3)
plt.plot(steps, verlet_tot_reldiff, label="Total energy Verlet")
plt.plot(steps, euler_tot_reldiff, label="Total energy Euler")
plt.xlabel("N")
plt.yscale("log")
plt.legend()
plt.tight_layout()

# Plot 3: Constant angular velocity: check if area swept over is constant
plt.figure(3)
area_diff_ratio_verlet, num_checks_verlet = test_ang_moment_conservation(data_verlet, "Verlet")
area_diff_ratio_euler, num_checks_euler = test_ang_moment_conservation(data_euler, "Euler")

plt.plot(area_diff_ratio_euler, label="Euler")
plt.plot(area_diff_ratio_verlet,label="Verlet")

plt.xlabel("Sweep " + r"$i$")
plt.ylabel(r"$\left|(A_i - A_0)/A_0\right|$")

plt.yscale("log")
plt.tight_layout()

plt.show()