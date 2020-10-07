import os
import sys

# File that compiles and runs c++ codes, plotting resulting data.


# ------------- Compilation -------------
all_cpp_codes = "./*.cpp"
os.system("echo compiling...")
os.system("c++ -o main.exe" + " " + all_cpp_codes)
# ---------------------------------------

# -------------- Execution --------------
N = input("Select number of integration points: ")
tn = input("Select simulation time (years): ")
Nplanets = input("Select number of planets: ")
os.system("echo executing...")
os.system("./main.exe" + " " + N + " " + tn + " " + Nplanets)                     # Execute code
# -----------------------------------------

# ------ File handling and plotting -------
#First check if the directory exists. Otherwise, create it.
path = "./results"
if not os.path.exists(path):
    os.makedirs(path) #Creates the directory
euler_file = "Euler_" + N + ".txt"
verlet_file = "Verlet_" + N + ".txt"
os.system("mv" + " " + euler_file + " " + path)         # Move Euler data to results directory.
os.system("mv" + " " + verlet_file + " " + path)         # Move Euler data to results directory.
os.system("python3 plot.py " + N)
# Open plot:
# os.chdir(path)
# os.system("code " + plot + "_" + N + ".png")
# -----------------------------------------