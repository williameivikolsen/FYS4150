import os
import sys

# File that compiles and runs c++ codes, plotting resulting data.

# ------------- Compilation -------------
all_cpp_codes = "./*.cpp"
os.system("echo compiling...")
os.system("c++ -o main.exe" + " " + all_cpp_codes)
# ---------------------------------------

# -------------- Execution --------------
mercury = '0'         # Parameter to check if we consider the mercury perihelion
beta = '2'            # Beta parameter for force
additional_params = '' # Possible additional parameters (filled later)

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

if name_of_problem == "sun_earth_jupiter":
    scaling_prompt = input("Keep default mass of Jupiter? Y/N: ")
    if  scaling_prompt == "N":
        scaling = input("How should Jupiter's mass be scaled? ")
        additional_params = scaling
    elif scaling_prompt != "N" or scaling_prompt != "Y":
        print("Keeping original mass of Jupiter")
    

initial_values = "./datasets/initial_conditions/initial_conditions_" + name_of_problem + ".txt"
masses = "./datasets/masses/masses_" + name_of_problem + ".txt"

os.system("echo executing...")
os.system("./main.exe" + " " + N + " " + T + " " + Nobjects + " " + initial_values + " " + masses + " " + mercury + " " + beta + " " + additional_params)    # Execute code
# -----------------------------------------

# ------ File handling and plotting -------
#First check if the directory exists. Otherwise, create it.
path = "./results/" + name_of_problem
if beta != '2':
    path += '/beta_tests'
if not os.path.exists(path):
    os.makedirs(path) #Creates the directory

if name_of_problem == 'sun_earth':
    euler_file = "Euler_" + N + "_" + T + ".txt"
    os.system("mv" + " " + euler_file + " " + path)         # Move Euler data to results directory.

verlet_file = "Verlet_" + N + "_" + T + ".txt"
os.system("mv" + " " + verlet_file + " " + path)         # Move Euler data to results directory.

os.system("python3 plot.py " + name_of_problem + " " + N + " " + Nobjects + " " + T + " " + beta)

# If we are doing beta tests, change name of result files to include beta value
if beta != '2':
    os.chdir(path)
    nums = beta.split(".")
    if name_of_problem == 'sun_earth':
        euler_rename = "Euler_" + N + "_" + T + "_beta_" + nums[0] + nums[1] + ".txt"
        os.rename(euler_file, euler_rename)
    verlet_rename = "Verlet_" + N + "_" + T + "_beta_" + nums[0] + nums[1] + ".txt"
    os.rename(verlet_file, verlet_rename)
