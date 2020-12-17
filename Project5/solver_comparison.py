import os
import sys
import numpy as np
from matplotlib import rcParams
import matplotlib.pyplot as plt
import seaborn as sns
from diffusion_class import BlackScholes

plt.style.use('seaborn')
sns.set(font_scale=1.3)
os.chdir("./plots/")

x_ratio = 10       # S/E ratio used for BCs
E = 50             # Excercise price
r = 0.04           # Risk-free interest rate
sigma = 0.4        # Volatility

Nx, Nt = 100, 1000      # Number of intervals for x and tau

x = np.linspace(-np.log(x_ratio), np.log(x_ratio), Nx+1)        # The transformed spacial variable
S = E*np.exp(x)                                                 # Price of underlying asset
tau_array = np.linspace(0.0, 1.0, 4)                            # Time until expiration date

def BS_solution(x, S, tau_array):
    fig, axes = plt.subplots(2)
    for tau in tau_array:
        instance1 = BlackScholes(x_ratio, tau, Nx, Nt, E, sigma, r, D=0)    # Object with D = 0
        instance2 = BlackScholes(x_ratio, tau, Nx, Nt, E, sigma, r, D=0.12) # Object with D = 0.12
        sol1 = instance1.solve('CN')        #Solve using Crank Nicolson
        sol2 = instance2.solve('CN')        #Solve using Crank Nicolson
        axes[0].plot(S, sol1, label=rf"$\tau$ = {tau:3.1f} yr")
        axes[1].plot(S, sol2, label=rf"$\tau$ = {tau:3.1f} yr")

    for ax in axes:
        ax.set_xlabel(r"$S$ [NOK]")
        ax.set_ylabel(r"$V$ [NOK]")
        ax.set_xlim([20, 100])
        ax.set_ylim([-1, 50])
        ax.legend()
    plt.tight_layout()
    plt.savefig("BS_solution.pdf", dpi=300)
    plt.show()

# BS_solution(x,S,tau_array)

def solver_comparison(x, S):
    fig,axes = plt.subplots(2)
    tau = 1.0                       # Time until expiration date
    instance = BlackScholes(x_ratio, tau, Nx, Nt, E, sigma, r, D=0)
    sol1 = instance.solve('FE')     # Solve using Forward Euler
    sol2 = instance.solve('CN')     # Solve using Crank Nicolson
    analytic = instance.analytical_solution()   # The analytic solution 

    axes[0].plot(S, sol1, 'o', label= "Forward Euler")
    axes[0].plot(S, analytic, label= "Analytic solution")
    axes[0].plot(S, sol2, '--', label= "Crank-Nicolson")
    axes[1].plot(S, np.abs(sol1-analytic), label="Forward Euler")
    axes[1].plot(S, np.abs(sol2-analytic), label="Crank-Nicolson")

    axes[0].set_xlim([0, 100])
    axes[0].set_ylim([-1, 50])
    axes[0].set_xlabel(r"$S$ [NOK]")
    axes[0].set_ylabel(r"$V$ [NOK]")
    axes[0].legend()

    axes[1].set_xlabel(r"$S$ [NOK]")
    axes[1].set_ylabel(r"Absolute error [NOK]")
    plt.legend()
    plt.tight_layout()
    plt.savefig("solver_comparison.pdf", dpi=300)
    plt.show()
solver_comparison(x,S)
