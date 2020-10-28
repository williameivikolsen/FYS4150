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
* In case of the Sun+Earth system: if changes are to be made to the radial dependency of the gravitational force. A parameter β is chosen so that <img src="https://render.githubusercontent.com/render/math?math=\vec{F}_G \propto \frac{1}{r^2} \to \vec{F}_G \propto \frac{1}{\beta^2}">.
* In case of the Sun+Earth system: whether to do tests? CHECK William gjorde rare ting her!s
* In case of the Sun+Earth system: if we want to simulte Earth's orbit as a more eccentric ellipse
* In case of the Sun+Earth+Jupiter system: if we want to scale Jupiter's mass with a chosen factor


`execute.py` then takes the input and sends it to `main.cpp`, which creates an instance of SolarSystem and makes the appropriate calculations. As an example, if the system "Sun+Mercury" is chosen, `main.cpp` will make sure that a relativistic correction to the gravitational force is added.

The header file of the SolarSystem class is `SolarSystem.hpp`, and its member functions are de
