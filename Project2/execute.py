import os
import sys

# File that compiles and runs c++ codes, storing and plotting resulting data.


# ------------- Compilation -------------
compile = input("Compile? [Y/N]: ")
if compile != "Y" and compile != "N":
    print('Command not recognized. Skipping compilation...')

all_cpp_codes = "./*.cpp"
compiler_flags = "-larmadillo"              # Linker to Armadillo.
if compile == "Y":
    os.system("echo compiling...")
    os.system("c++ -o main.exe" + " " + all_cpp_codes + " " + compiler_flags)
# ---------------------------------------


# -------------- Execution --------------
system = input("Choose system: [beam/HO1/HO2]: ")
if system != "beam" and system != "HO1" and system != "HO2":
    print("The system you chose is not recognized. Aborting...")
    sys.exit()
parameters = input("Choose parameters? [Y/N]: ")
if parameters != "Y" and parameters != "N":
    print('Command not recognized. Setting standard parameters...')
# Standard parameters:
n = "16"
maxit = "1000"
epsilon = "1e-8"

if parameters == "Y":
    n = input("Give number of mesh points n: ")
    epsilon = input("Choose tolerance: ")
    maxit = input("Choose max number of iterations: ")

filename = system + "_" + n + ".txt"
path = "./" + system

test = input("Test? [Y/N]: ")
if test != "Y" and test != "N":
    print('Command not recognized. Skipping test...')
    os.system("echo executing...")
    os.system("./main.exe" + " " + system + " " + n + " " + epsilon + " " + maxit + " " + filename)                     # Execute code
if test == "Y":
    num_tests = input("Number of (evenly spaced out) tests to be performed per test function: ")
    os.system("echo executing...")
    os.system("./main.exe" + " " + system + " " + n + " " + epsilon + " " + maxit + " " + filename + " test " + num_tests)            # Execute code with test

# -----------------------------------------

print("made it here")
print(path)
print(filename)
print(system)



# ------ File handling and plotting -------
#First check if the directory exists. Otherwise, create it.
if not os.path.exists(path):
    os.makedirs(path) #Creates the directory
os.system("mv" + " " + filename + " " + path) # Move data file to results directory.
os.system("python3 plot.py" + " " + system + " " + n)

# -----------------------------------------