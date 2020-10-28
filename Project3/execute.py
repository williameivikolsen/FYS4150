import os
import sys

# File that compiles and runs c++ codes, plotting resulting data.

# ------------- Compilation -------------
all_cpp_codes = "./*.cpp"
os.system("echo compiling...")
os.system("c++ -o main.exe" + " " + all_cpp_codes)
# ---------------------------------------

# -------------- Execution --------------

# Default values of parameters
mercury = '0'          # Parameter to check if we consider the mercury perihelion
beta = '2'             # Beta parameter for force
additional_params = '' # Possible additional parameters (filled later)
circtest = '0'

problem = input( " [1] The Sun and Earth \n [2] Sun, Earth and Jupiter \n [3] The solar system \n [4] The Sun and Mercury \nChoose system: ")
if problem == '1':
    Nobjects = '2'
    name_of_problem = 'sun_earth'
elif problem == '2':
    Nobjects = '3'
    name_of_problem = 'sun_earth_jupiter'
elif problem == '3':
    Nobjects = '10'
    name_of_problem = 'full_system'
elif problem == '4':
    Nobjects = '2'
    mercury = '1'
    name_of_problem = 'sun_mercury'
else:
    print('Problem must be 1, 2, 3 or 4!')
    sys.exit()

T = input("Select simulation time (years): ")
N = input("Select number of integration points: ")

if name_of_problem == "sun_earth":
    beta_prompt = input("Keep default value of beta (β=2)? Y/N: ")
    if  beta_prompt == "N":
        beta = input("What value should beta have? ")

    elif beta_prompt != "N" or beta_prompt != "Y":
        print("Keeping beta = 2")
        circtest_prompt = input("Perform circle test? Y/N: ")
        if circtest_prompt == 'Y':
            print("Performing circle test.")
            circtest = '1'
        else:
            print("Skipping circle test.")

    ellipse_prompt = input("Keep default initial values of Earth position? ('N' gives ellipse) Y/N: ")
    if  ellipse_prompt == "N":
        # This can be changed so that the initial values of the Earth is arbitrary. The Sun is fixed at the origin.
        print("You shall see an ellipse")
        additional_params = "1 0 0 5"                   # x0 - y0 - vx0 - vy0
    else:
        print("Keeping default values")



if name_of_problem == "sun_earth_jupiter":
    scaling_prompt = input("Keep default mass of Jupiter? Y/N: ")
    if  scaling_prompt == "N":
        scaling = input("How should Jupiter's mass be scaled? ")
        additional_params = scaling
        scaling_str0 = scaling.split(".")
        if len(scaling_str0) > 1:                                       # If decimal number in scaling
            scaling_str = scaling_str0[0] + "_" + scaling_str0[1]
        else:
            scaling_str = scaling_str0[0]
    else:
        print("Keeping original mass of Jupiter")

initial_values = "./datasets/initial_conditions/initial_conditions_" + name_of_problem + ".txt"
masses = "./datasets/masses/masses_" + name_of_problem + ".txt"

os.system("echo  ")
os.system("echo executing...")
os.system("./main.exe" + " " + N + " " + T + " " + Nobjects + " " + initial_values + " " + masses + " " + mercury + " " + beta + " " + circtest + " " + additional_params)    # Execute code
# -----------------------------------------

# ------ File handling and plotting -------

path = "./results/" + name_of_problem

# Make subfolder if beta not equal to 2 (Sun-Earth)
if beta != '2':
    path += '/beta_tests'
# Make subfolder for circtests (Sun-Earth)
if circtest == '1':
    path += '/circ_tests'
# Make subfolder for scaled Jupiter mass (Sun-Earth-Jupiter)
if name_of_problem == 'sun_earth_jupiter' and additional_params != "":
    path += "/" + scaling_str

# First check if the directory exists. Otherwise, –––create it.

if not os.path.exists(path):
    os.makedirs(path) #Creates the directory

if name_of_problem == 'sun_earth':
    euler_file = "Euler_" + N + "_" + T + ".txt"
    os.system("mv" + " " + euler_file + " " + path)         # Move Euler data to results directory.

verlet_file = "Verlet_" + N + "_" + T + ".txt"
os.system("mv" + " " + verlet_file + " " + path)            # Move Euler data to results directory.

os.system("python3 plot.py " + name_of_problem + " " + N + " " + Nobjects + " " + T + " " + beta + " " + circtest + " " + additional_params)


# If we are doing beta tests, change name of result files to include beta value
if beta != '2':
    os.chdir(path)
    nums = beta.split(".")
    if name_of_problem == 'sun_earth':
        euler_rename = "Euler_" + N + "_" + T + "_beta_" + nums[0] + nums[1] + ".txt"
        os.rename(euler_file, euler_rename)
    verlet_rename = "Verlet_" + N + "_" + T + "_beta_" + nums[0] + nums[1] + ".txt"
    os.rename(verlet_file, verlet_rename)

# If changing mass of Jupiter, put files in appopriate subfolder (named after scaling factor)
if name_of_problem == 'sun_earth_jupiter' and additional_params != "":
    os.chdir(path)
    verlet_rename = "Verlet_" + N + "_" + T + "_jupiter_scaling_" + scaling_str + ".txt"
    os.rename(verlet_file, verlet_rename)
