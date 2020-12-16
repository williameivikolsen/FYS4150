import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
from diffusion_class import BlackScholes

plt.style.use('seaborn')
sns.set(font_scale=1.3)

# Program that iterates through values of volatility (sigma), and find the value that best matches market value
# Date calculation: Dec 16th 2020

x_ratio = 10        # S/E ratio used for BCs
r = 0.10            # Risk-free interest rate
D = 0.056           # Yield (DNB)          
sigma = 0.50        # Volatility (DNB)     

closing_price = 160.00  # Closing price (DNB) 16/12/20

Nx, Nt = 500, 1000  # Intervals x-axis, time

V_real = 8.82       # Actual option price DNB, Jan 2021


E_array_jan = np.linspace(140, 175, 15)             # Strike prices for January 2021
V_real_jan = np.array([20.17, 17.79, 15.48, 13.26, 11.18, 9.23, 7.37, 5.72, 4.30, 3.09, 2.28, 1.57, 1.07, 0.61, 0.43]) # Closing prices options
V_calc_jan = np.zeros(len(V_real_jan))

E_array_feb = E_array_jan.copy()
V_real_feb = np.array([20.67, 18.46, 16.37, 14.33, 12.44, 10.64, 9.06, 7.51, 6.15, 4.95, 3.94, 3.08, 2.43, 1.89, 1.50]) 
V_calc_feb = np.zeros(len(V_real_feb))

E_array_mar = np.linspace(140, 175, 8)
V_real_mar = np.array([20.94, 16.85, 12.95, 9.44, 6.65, 4.44, 2.93, 1.89])
V_calc_mar = np.zeros(len(V_real_mar))

x = np.linspace(-np.log(x_ratio), np.log(x_ratio), Nx+1)

tau_jan = 1/12
for i, E in enumerate(E_array_jan):
    print(f"Jan., E = {E:.1f}")
    S = E*np.exp(x)
    idx_closing_price = np.abs(S - closing_price).argmin()              # Index corresponding to closing price along S-axis.

    BS_instance = BlackScholes(x_ratio, tau_jan, Nx, Nt, E, sigma, r, D)
    V_calc_jan[i]  = BS_instance.solve('CN')[idx_closing_price]

tau_feb = 2/12
for i, E in enumerate(E_array_feb):
    print(f"Feb., E = {E:.1f}")
    S = E*np.exp(x)
    idx_closing_price = np.abs(S - closing_price).argmin()              # Index corresponding to closing price along S-axis.

    BS_instance = BlackScholes(x_ratio, tau_feb, Nx, Nt, E, sigma, r, D)
    V_calc_feb[i]  = BS_instance.solve('CN')[idx_closing_price]

tau_mar = 3/12
for i, E in enumerate(E_array_mar):
    print(f"Mar., E = {E:.1f}")
    S = E*np.exp(x)
    idx_closing_price = np.abs(S - closing_price).argmin()              # Index corresponding to closing price along S-axis.

    BS_instance = BlackScholes(x_ratio, tau_mar, Nx, Nt, E, sigma, r, D)
    V_calc_mar[i]  = BS_instance.solve('CN')[idx_closing_price]

plt.figure(1)
plt.plot(E_array_jan, V_real_jan, '-o', label="Option prices (DNB)")
plt.plot(E_array_jan, V_calc_jan, '-o', label="Calculated option prices")
plt.xlabel("$E$ [NOK]")
plt.ylabel("$V$ [NOK]")
plt.title("January")

plt.plot(E_array_feb, V_real_feb, '-o', label="Option prices (DNB)")
plt.plot(E_array_feb, V_calc_feb, '-o', label="Calculated option prices")
plt.xlabel("$E$ [NOK]")
plt.ylabel("$V$ [NOK]")
plt.title("February")


plt.plot(E_array_mar, V_real_mar, '-o', label="Option prices (DNB)")
plt.plot(E_array_mar, V_calc_mar, '-o', label="Calculated option prices")
plt.xlabel("$E$ [NOK]")
plt.ylabel("$V$ [NOK]")
plt.title("March")

plt.legend()
plt.show()



