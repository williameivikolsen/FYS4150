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
problem = input( " [1] The Sun and Earth \n [2] Sun, Earth and Jupiter \n [3] The solar system \n [4] The Sun and Mercury \n Choose system: ")
if problem == '1':
    Nobjects = '2'
    name_of_problem = 'sun_earth'
    # beta = input('Select value for beta: ')
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

initial_values = "./datasets/initial_conditions/initial_conditions_" + name_of_problem + ".txt"
masses = "./datasets/masses/masses_" + name_of_problem + ".txt"

os.system("echo executing...")
os.system("./main.exe" + " " + N + " " + T + " " + Nobjects + " " + initial_values + " " + masses + " " + mercury)    # Execute code
# -----------------------------------------

# ------ File handling and plotting -------
#First check if the directory exists. Otherwise, create it.
path = "./results/" + name_of_problem
if not os.path.exists(path):
    os.makedirs(path) #Creates the directory

euler_file = "Euler_" + N + ".txt"
verlet_file = "Verlet_" + N + ".txt"
os.system("mv" + " " + euler_file + " " + path)         # Move Euler data to results directory.
os.system("mv" + " " + verlet_file + " " + path)         # Move Euler data to results directory.

os.system("python3 plot.py " + name_of_problem + " " + N + " " + Nobjects)



# Open plot:
# os.chdir(path)
# os.system("code " + plot + "_" + N + ".png")
# -----------------------------------------
