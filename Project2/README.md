## Prosjekt 2 - FYS4150
### A brief description of the different files in this folder:

`execute.py` is the program intended to be ran by the user. It asks the user if it wants to re-compile the program, what physical system to be solved, what kind of parameters to be used, and if the program is to be run in testing mode.

`main.cpp` is the C++ side of `execute.py`. It reads variables from `execute.py`, creates an instance of the right class, and runs the right functions.

`jacobi.hpp` is a header file that contains the parameters and methods of all classes. The super class *Jacobi* contains the general parameters/methods that's shared between the subclasses *Beam*, *One_electron_HO* and *Two_electron_HO*. In addition, all of the linked libraries are included here.

The code belonging to the different classes is located in `Jacobi.cpp`, `Beam.cpp`, `One_electron_HO.cpp` and `Two_electron_HO.cpp`.

The generated data/plots are stored in folders `./Beam` etc.

`plot.py` uses command line arguments to make general plots.

`iterations.txt` is a log file used to track the number of iterations used as the programs are run.

`plot_iterations.py` was created in order to automate the task of running `execute.py` with many different matrix dimensions. A comparison plot `iterations.png` is made by `plot_iterations.py`.

