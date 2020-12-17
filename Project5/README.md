## 💸 FYS4150 - Project 5: Option Markets and the Black-Scholes Equation 📈

The files in this folder solves the [given assignment](http://compphysics.github.io/ComputationalPhysics/doc/Projects/2020/Project5/BlackScholes/pdf/BlackScholes.pdf).

Two classes are defined in the file named `diffusion_class.py`, a general purpose OneDimensionalDiffusion class with an underclass named BlackScholes. In order to solve the Black-Scholes equation, the BlackScholes class contains a solver function. This function has Forward Euler, Backward Euler and Crank-Nicolson as avaliable solution methods. Running `diffusion_class.py` shows solution examples of both an arbitrary diffusion case and a solution of the Black-Scholes equation.

The other `*.py` files are used to create the results shown in the final report, `Project5_report.pdf`. The plots made can be found in the `./plots` folder, and the closing prices of DNB options (Dec. 16th 2020) can be found in `DNB_options_closing_prices.pdf`.
