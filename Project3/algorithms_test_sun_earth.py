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
circtest = sys.argv[6]                  # Circle test parameter
path = "./results/" + name_of_problem   # path to data
beta_string = ''
if beta != '2':
    path += '/beta_tests'               # HUSK å legge inn beta-verdien i plott!
    beta_string = "_beta_" + beta.split(".")[0] + beta.split(".")[1]
if circtest == "1":
    print("Circle test chosen.")
    path += '/circ_tests'
else:
    print("Circle test not chosen.")
os.chdir(path)

# Start by reading data from files
filename_euler = "Euler_" + N + "_" + T + beta_string + ".txt"
filename_verlet = "Verlet_" + N + "_" + T + beta_string + ".txt"
infile_euler = open(filename_euler, "r")

infile_euler.readline()                                 # Skip one line
params = infile_euler.readline().split()                # Parameters located in line 2

t0 = float(params[1])
tn = float(params[2])
h = float(params[4])
v0x = float(params[7])
v0y = float(params[8])
v0z = float(params[9])

infile_euler.seek(0)                                    # Reset file handle to start
infile_euler.close()

data_euler = np.loadtxt(filename_euler, skiprows=4)       # Actual data arrays
data_verlet = np.loadtxt(filename_verlet, skiprows=4)     # Format rx-ry-vx-vy

N = int(N)
steps = np.arange(N)                                    # Arrays for plotting
if N >= 100000:
    jump = 100
    N = int(N/jump)
    steps = np.arange(N)*100
    h*=jump

t = np.linspace(t0, tn, N)

def test_circular(data_set, method_name, eps=1e-2):     # Takes in either the data_euler or data_verlet
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
    print("Testing if circular orbit for method {}, tolerance set to {}...".format(method_name, eps))
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
    print("-----------------------------------------------------------------------")
    print("Testing if angular momentum conserved for method {}, tolerance set to {}...".format(method_name, eps))
    print("-----------------------------------------------------------------------")
    print("Maximum recorded deviance in angular momentum: %g" % np.max(area_diff_ratio))
    return area_diff_ratio, num_checks


def test_energy_conservation(data_set, method_name, eps=1e-4):      # eps is tolerance ratio
    rx, ry, rz = data_set[:,3], data_set[:,4], data_set[:,5]
    vx = np.gradient(rx, h)
    vy = np.gradient(ry, h)
    vz = np.gradient(rz, h)
    kin0 = 0.5*(v0x**2 + v0y**2 + v0z**2)    # Initial kinetic energy

    # SI_conv_vel = 4740.47                                     # 1 AU/yr = 4740.47 m/s
    # m = 5.972e24                                              # Earth mass [kg]
    kin_energy = 0.5*(vx**2 + vy**2 + vz**2)                     # Kin. energy per mass [AU^2/yr^2]
    kin_energy_reldiff = np.abs((kin_energy - kin0)/kin0)        # Abs. difference from initial kinetic energy 

    pot_energy = -4*np.pi**2/(np.sqrt(rx**2 + ry**2 + rz**2))           # Pot. energy per mass [AU^2/yr^2]
    pot_energy_reldiff = np.abs((pot_energy - pot_energy[0])/pot_energy[0])        # Abs. difference from initial potential energy

    tot_energy = kin_energy + pot_energy
    tot0 = kin0 + pot_energy[0] # Initial total energy
    tot_energy_reldiff = np.abs((tot_energy - tot0)/tot0)

    max_pot_reldiff = np.max(pot_energy_reldiff)
    max_kin_reldiff = np.max(kin_energy_reldiff[2:-2])  # Indices to avoid loss of precision in differentiation at boundaries
    max_tot_reldiff = np.max(tot_energy_reldiff[2:-2])  # ^Same here

    print("-----------------------------------------------------------------------")
    print("Testing if energy conserved for method {}, biggest ratio from initial value allowed is {:.3e}...".format(method_name, eps))
    print("Total initial energy: ", tot0)
    print("-----------------------------------------------------------------------")

    print("Max recorded deviance ratio from initial potential energy was {:.7e}".format(max_pot_reldiff))
    print("Max recorded deviance ratio from initial kinetic energy was {:.7e}".format(max_kin_reldiff))
    print("Max recorded deviance ratio from initial total energy was {:.7e}".format(max_tot_reldiff))

    return kin_energy_reldiff, pot_energy_reldiff, tot_energy_reldiff


# Plot 1: Deviance from circle with different methods

if circtest == '1':
    deviance_verlet_circle = test_circular(data_verlet, "Verlet")
    deviance_euler_cirlce = test_circular(data_euler, "Euler")

    plt.plot(t, deviance_euler_cirlce, label="Euler")
    plt.plot(t, deviance_verlet_circle, label="Velocity Verlet")
    plt.xlabel("Time [yrs]")
    plt.ylabel(r"$\left|\mathbf{r}_i - \mathbf{r}_0\right|/\left|\mathbf{r}_0\right|$")
    plt.yscale("log")
    plt.legend()
    plt.tight_layout()
    plt.show()

# Plot 2: Deviance from initial energies

verlet_kin_reldiff, verlet_pot_reldiff, verlet_tot_reldiff = test_energy_conservation(data_verlet, "Verlet")
euler_kin_reldiff, euler_pot_reldiff, euler_tot_reldiff = test_energy_conservation(data_euler, "Euler")
sections = 1 # Average over every section'th value. Must be a factor of N

if circtest == '1':
    # Plot kinetic energy (Slice boundary values because of bad precision in differentiation here)
    plt.plot(t[0::sections][1:-2], np.mean(verlet_kin_reldiff.reshape(-1, sections), axis=1)[1:-2], label="Velocity Verlet")
    plt.plot(t[0::sections][1:-2], np.mean(euler_kin_reldiff.reshape(-1, sections), axis=1)[1:-2], label="Euler")
    plt.xlabel("Time [yrs]")
    plt.ylabel(r"$\left|(E_{k,i}-E_{k,0})/E_{k,0}\right|$")
    plt.yscale("log")
    plt.legend()
    plt.tight_layout()
    plt.show()

    plt.plot(t[0::sections], np.mean(verlet_pot_reldiff.reshape(-1, sections), axis=1), label="Velocity Verlet")
    plt.plot(t[0::sections], np.mean(euler_pot_reldiff.reshape(-1, sections), axis=1), label="Euler")
    plt.xlabel("Time [yrs]")
    plt.ylabel(r"$\left|(E_{p,i}-E_{p,0})/E_{p,0}\right|$")
    plt.yscale("log")
    plt.legend()
    plt.tight_layout()
    plt.show()

    plt.plot(t[0::sections][1:-2], np.mean(verlet_tot_reldiff.reshape(-1, sections), axis=1)[1:-2], label="Velocity Verlet")
    plt.plot(t[0::sections][1:-2], np.mean(euler_tot_reldiff.reshape(-1, sections), axis=1)[1:-2], label="Euler")
    plt.xlabel("Time [yrs]")
    plt.ylabel(r"$\left|(E_i-E_0/E_0\right|$")
    plt.yscale("log")
    plt.legend()
    plt.tight_layout()
    plt.show()

else:
    plt.plot(t[0::sections], np.mean(verlet_tot_reldiff.reshape(-1, sections), axis=1), label="Velocity Verlet")
    plt.plot(t[0::sections], np.mean(euler_tot_reldiff.reshape(-1, sections), axis=1), label="Euler")
    plt.xlabel("Time [yrs]")
    plt.yscale("log")
    plt.ylabel(r"$\left|(E_i-E_0/E_0\right|$")
    plt.legend()
    plt.tight_layout()
    plt.show()

# Plot 3: Constant angular velocity: check if area swept over is constant
area_diff_ratio_verlet, num_checks_verlet = test_ang_moment_conservation(data_verlet, "Verlet")
area_diff_ratio_euler, num_checks_euler = test_ang_moment_conservation(data_euler, "Euler")

plt.plot(area_diff_ratio_euler, label="Euler")
plt.plot(area_diff_ratio_verlet,label="Velocity Verlet")

plt.xlabel("Area sweep " + r"$i$")
plt.ylabel(r"$\left|(A_i - A_0)/A_0\right|$")

plt.yscale("log")
plt.tight_layout()
plt.show()
