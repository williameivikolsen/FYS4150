import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
from diffusion_class import BlackScholes

plt.style.use('seaborn')
sns.set(font_scale=1.3)

# Program that iterates through values of volatility (sigma), and find the value that best matches market value
# Date calculation: Dec 16th 2020

E = 155             # Wanted exercise price
x_ratio = 10        # S/E ratio used for BCs
tau = 1/12          # Look at prices one month in the future
r = 0.10            # Risk-free interest rate
D = 0.056           # Yield (DNB)               

Nx, Nt = 800, 1000  # Intervals x-axis, time

V_real = 7.37       # Actual option price DNB, Jan 2021

x = np.linspace(-np.log(x_ratio), np.log(x_ratio), Nx+1)
S = E*np.exp(x)


sigma_array = np.linspace(0.37, 0.43, 7)   # All value of sigma to test
idx_E = np.abs(S - E).argmin()              # Index corresponing to E along S-axis

fig, axes = plt.subplots(2,2, gridspec_kw={'width_ratios': [2.9, 1]})
for sigma in sigma_array:
    print(f"sigma = {sigma:.3f}")

    BS_instance = BlackScholes(x_ratio, tau, Nx, Nt, E, sigma, r, D)
    solution = BS_instance.solve('CN')

    axes[0,0].plot(S, solution, "-o", label=r"$\sigma$=" + f"{sigma:.2f}" + r" yr$^{-\frac{1}{2}}$", ms=8)    # V-S curves for different sigma
    axes[1,0].plot(sigma, np.abs(solution[idx_E] - V_real)/V_real, 'o', label=fr"$\sigma =$ {sigma:3.2f}", ms=8)  # Find relative error


axes[0,0].plot(E, V_real, 'bo', label="Actual price", ms=10, markeredgecolor="black", markeredgewidth=1)
axes[0,0].set_xlabel("$S$ [NOK]")
axes[0,0].set_ylabel("$V$ [NOK]")
axes[0,0].set_xlim([153, 157])
axes[0,0].set_ylim([5.5, 9.5])

axes[1,0].set_xlabel(r"$\sigma$ [yr$^{-\frac{1}{2}}$]")
axes[1,0].set_ylabel(r"$|V(\sigma) - V_{\mathrm{real}}|/V_{\mathrm{real}}$")

axes[0,1].axis('off')
axes[1,1].axis('off')

handles, labels = axes[0,0].get_legend_handles_labels()
fig.legend(handles, labels, bbox_to_anchor=[1, 0.98], loc='upper right', frameon=True, framealpha=0.7)

plt.tight_layout()
plt.savefig('./plots/volatility.pdf')
plt.show()   