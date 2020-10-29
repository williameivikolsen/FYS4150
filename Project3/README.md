## Project 3 - FYS4150

### A brief description of the different files in this folder

The files in this folder solves the [given assignment](http://compphysics.github.io/ComputationalPhysics/doc/Projects/2020/Project3/pdf/Project3.pdf).

`execute.py` is the main program intended to be ran by the user. It asks the user

* What physical system to be solved
  1. Sun and Earth
  2. Sun, Earth and Jupiter
  3. All planets in the solar system (+ Pluto!)
  4. Sun and Mercury
* How long to simulate for (in years)
* The number of integration points
* In case of the Sun+Earth system: if changes are to be made to the radial dependency of the gravitational force. A parameter β is chosen so that <img src="https://render.githubusercontent.com/render/math?math=F_G \propto \frac{1}{r^2} \to F_G \propto \frac{1}{\beta^2}">
* In case of the Sun+Earth system: if we want to simulte Earth's orbit as a more eccentric ellipse
* In case of the Sun+Earth+Jupiter system: if we want to scale Jupiter's mass with a chosen factor
* In case of the Sun+Earth system: if we to test for circular path and conservation of energy/angular momentum. This will later run `algorithms_test_sun_earth.py`
* In case of the Sun+Mercury system: if we to test the precession of Mercury's orbit. This will later run `algorithms_test_sun_mercury.py`

`execute.py` then takes the input and sends it to `main.cpp`, which creates an instance of SolarSystem and makes the appropriate calculations. As an example, if the system "Sun+Mercury" is chosen, `main.cpp` will make sure that a relativistic correction to the gravitational force is added.

The header file of the SolarSystem class is `SolarSystem.hpp`, and its member functions are defined in `SolarSystem.cpp`.

`execute.py` also runs `plot.py` in order to make plots showing the resulting orbits. These two programs make sure that produced data files and plots are moved to the appropriate subfolder under `./results`

The masses and the initial values of the Sun and the planets' position and velocity are found in the `./datasets` folder. These data are taken from [NASA](https://ssd.jpl.nasa.gov/horizons.cgi), and are dated midnight 2020-Oct-09 Barycentric Dynamical Time. The file `./datasets/initial_conditions/read.py` makes the special initual value data files for the different physical systems.

`set_axes_equal.py` containts a function that gives matplotlib the ability have equal axes scaling for 3D plots. This is an analogue to the ax.axis('equal') for regular 2D plots.

`log.txt` is a text file that was used to keep track of hours put into the project before we started to have daily briefing meetings.

The files in `.\no_classes` implements the Euler and velocity Verlet algorithm without the use of object orientation. Compiling and executing  `.\no_classes\no_classes.cpp` is done with `.\no_classes\makefile`, and plots/tests of the results can be made with `.\no_classes\plot_no_classes.py` and `.\no_classes\test_no_classes.py`.

Finally, `Project_3_complete.pdf` contains the final report for the project.
