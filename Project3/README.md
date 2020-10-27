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
* In case of the Sun+Earth system: if changes are to be made to the radial dependency of the gravitational force. A parameter β is chosen so  <img src="https://render.githubusercontent.com/render/math?math=\vec{F}_G \propto \frac{1}{r^2} \to \vec{F}_G \propto \frac{1}{\beta^2}">.