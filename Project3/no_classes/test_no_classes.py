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

steps = np.arange(N)                                    # Arrays for plotting

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


def test_ang_moment_conservation(data_set, method_name, eps=1e-2, dT=0.1):  
    # eps is tolerance ratio [1]
    # dT is time duration that's going to be swept over [yr]

    rx, ry = data_set[:,0], data_set[:,1]
    num_checks = int((tn-t0)/dT)     # Number of checks given a value of dT
    area = np.zeros(num_checks)
    dN = int(N/num_checks)           # Number of steps for every sweep
    for i in range(num_checks):
        idx_0 = int(i*N/num_checks)  # Start inde for every sweep 
        for j in range(dN):
            pos0 = np.array([rx[idx_0 + i], ry[idx_0+i]])
            pos1 = np.array([rx[idx_0 + (i+1)], ry[idx_0+(i+1)]])
            
            # Approximate area with triangle
            base_length = np.sqrt(np.dot((pos0+pos1)/2, (pos0+pos1)/2)) 
            heigth = np.sqrt(np.dot(pos1-pos0, pos1-pos0))

            area[i] +=  0.5*base_length*heigth

    return area




def test_energy_conservation(data_set, method_name, eps=1e-4):      # eps is tolerance ratio
    rx, ry = data_set[:,0], data_set[:,1]
    vx, vy = data_set[:,2], data_set[:,3]

    # SI_conv_vel = 4740.47                                     # 1 AU/yr = 4740.47 m/s
    # m = 5.972e24                                              # Earth mass [kg]
    kin_energy = 0.5*np.sqrt(vx**2 + vy**2)                     # Kin. energy per mass [AU^2/yr^2]
    kin_energy_diff = np.abs(kin_energy - kin_energy[0])        # Abs. difference from initial kinetic energy 

    pot_energy = -4*np.pi**2/(np.sqrt(rx**2 + ry**2))           # Pot. energy per mass [AU^2/yr^2]
    pot_energy_diff = np.abs(pot_energy - pot_energy[0])        # Abs. difference from initial potential energy

    tot_energy = kin_energy + pot_energy
    tot_energy_diff = np.abs(tot_energy - tot_energy[0])    

    max_pot_diff = np.max(pot_energy_diff)
    max_kin_diff = np.max(kin_energy_diff)
    max_tot_diff = np.max(tot_energy_diff)
    
    num_fail = 0                                                # Number of failed tests

    print("-----------------------------------------------------------------------")
    print("Testing if energy conserved for method {}, biggest ratio from initial value allowed is {:.3e}...".format(method_name, eps))
    print("-----------------------------------------------------------------------")

    if max_pot_diff/np.abs(pot_energy[0]) > eps:
        print("The test failed for potential energy")
        print("Max recorded deviance ratio from initial energy was {:.7e}".format(max_pot_diff/np.abs(pot_energy[0])))
        num_fail += 1

    if max_kin_diff/np.abs(kin_energy[0]) > eps:
        print("The test failed for kinetic energy")
        print("Max recorded deviance ratio from initial energy was {:.7e}".format(max_kin_diff/np.abs(kin_energy[0])))
        num_fail += 1

    if max_tot_diff/np.abs(tot_energy[0]) > eps:
        print("The test failed for total energy")
        print("Max recorded deviance ratio from initial energy was {:.7e}".format(max_tot_diff/np.abs(tot_energy[0])))
        num_fail += 1

    if num_fail == 0:
        print("The tests (kinetic/potential/total energy) were passed successfully!")
        print("Max recorded deviance ratio (total energy) was {:.7e}".format(max_tot_diff/np.abs(tot_energy[0])))

    return kin_energy_diff, pot_energy_diff, tot_energy_diff


# Plot 1: Deviance from circle with different methods

deviance_verlet_circle = test_circular(data_verlet, "Verlet")
deviance_euler_cirlce = test_circular(data_euler, "Euler")


plt.plot(steps, deviance_euler_cirlce, label="Euler")
plt.plot(steps, deviance_verlet_circle, label="Verlet")
plt.xlabel("N")
plt.ylabel("Deviation [AU]")
plt.yscale("log")
plt.title("N = {}".format(N))
plt.legend()
# plt.show()

# Plot 2: Deviance from initial energies

verlet_kin_diff, verlet_pot_diff, verlet_tot_diff = test_energy_conservation(data_verlet, "Verlet")
euler_kin_diff, euler_pot_diff, euler_tot_diff = test_energy_conservation(data_euler, "Euler")

plt.figure(figsize=(15,4))

plt.subplot(1,3,1)
plt.plot(steps, verlet_kin_diff, label="Kinetic energy Verlet")
plt.plot(steps, euler_kin_diff, label="Kinetic energy Euler")
plt.xlabel("N")
plt.ylabel("Absolute ratio of deviation [1]")
plt.yscale("log")
plt.legend()

plt.subplot(1,3,2)
plt.plot(steps, verlet_pot_diff, label="Potential energy Verlet")
plt.plot(steps, euler_pot_diff, label="Potential energy Euler")
plt.xlabel("N")
plt.yscale("log")
plt.title("N = {}".format(N))
plt.legend()

plt.subplot(1,3,3)
plt.plot(steps, verlet_tot_diff, label="Total energy Verlet")
plt.plot(steps, euler_tot_diff, label="Total energy Euler")
plt.xlabel("N")
plt.yscale("log")
plt.legend()

plt.show()

# Plot 3: Constant angular velocity: check if area swept over is constant
area = test_ang_moment_conservation(data_verlet, "Verlet")
plt.plot(area)
plt.show()