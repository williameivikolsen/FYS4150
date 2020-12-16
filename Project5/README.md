## 💸 FYS4150 - Project 5: Option Markets and the Black-Scholes Equation 📈

The files in this folder solves the [given assignment](http://compphysics.github.io/ComputationalPhysics/doc/Projects/2020/Project5/BlackScholes/pdf/BlackScholes.pdf).

The calculations are done using the BlackScholes class, an underclass of the OneDimensionalDiffusion class. Both are defined in `diffusion_class.py`.

The BlackScholes class contains a solve function where the user specifies the method to be used in the calculations. The methods are inherited from the OneDimensionalDiffusion class. The avaliable methods are Forward Euler, Backward Euler and Crank-Nicolson.
