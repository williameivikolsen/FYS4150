import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
from diffusion_class import BlackScholes

plt.style.use('seaborn')
sns.set(font_scale=1.3)

# Program that iterates through values of volatility (sigma), and find the value that best matches market value
# Date calculation: Dec 16th 2020

E = 155             # Wanted xercise price
x_ratio = 10        # S/E ratio used for BCs
tau = 1/12          # Look at prices one month in the future
r = 0.10            # Risk-free interest rate
D = 0.056           # Yield (DNB)               


Nx, Nt = 500, 1000  # Intervals x-axis, time

V_real = 8.82       # Actual option price DNB, Jan 2021
x = np.linspace(-np.log(x_ratio), np.log(x_ratio), Nx+1)
S = E*np.exp(x)


sigma_array = np.linspace(0.47, 0.53, 7)   # All value of sigma to test
idx_E = np.abs(S - E).argmin()              # Index corresponing to E along S-axis

fig, axes = plt.subplots(1,2, figsize=(12,6))
for sigma in sigma_array:
    print(f"sigma = {sigma:.3f}")

    BS_instance = BlackScholes(x_ratio, tau, Nx, Nt, E, sigma, r, D)
    solution = BS_instance.solve('CN')

    axes[0].plot(S, solution, "-o", label=fr"$\sigma =$ {sigma:3.2f}", ms=4)    # V-S curves for different sigma
    axes[1].plot(sigma, np.abs(solution[idx_E] - V_real)/V_real, 'o', label=fr"$\sigma =$ {sigma:3.2f}", ms=6)  # Find relative error


axes[0].plot(E, V_real, 'bo', label="Actual price", ms=8, markeredgecolor="black", markeredgewidth=1)
axes[0].set_xlabel("$S$ [NOK]")
axes[0].set_ylabel("$V$ [NOK]")
axes[0].set_xlim([153, 157])
axes[0].set_ylim([6.5, 12.5])

axes[1].set_xlabel("$S$ [NOK]")
axes[1].set_ylabel(r"$|V(\sigma) - V_{\mathrm{real}}|/V_{\mathrm{real}}$")

handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, bbox_to_anchor=(0.25,0.97), loc='upper right', frameon=True, framealpha=0.7)

plt.tight_layout()
plt.show()   

