from diffusion_class import BlackScholes
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn')

x_ratio = 10
tau = 10
E = 50
r = 0.04
D = 0.12
sigma = 0.4
Nx, Nt = 100, 1000
x = np.linspace(-np.log(x_ratio), np.log(x_ratio), Nx+1)
S = E*np.exp(x)

epsilon = 1e-8  # To compute derivatives
N_tau = 5
tau_arr = np.linspace(0, 1, N_tau)
delta_tau = np.zeros((N_tau, Nx+1))
gamma_tau = np.zeros((N_tau, Nx+1))
vega_tau = np.zeros((N_tau, Nx+1))
theta_tau = np.zeros((N_tau, Nx+1))
rho_tau = np.zeros((N_tau, Nx+1))
greeks = {'delta': delta_tau, 'gamma': gamma_tau, 'vega': vega_tau, 'theta': theta_tau, 'rho': rho_tau}

for i in range(N_tau):
    delta_inst = BlackScholes(x_ratio, tau_arr[i], Nx, Nt, E, sigma, r, D)              # Instance for delta/gamma
    vega1_inst = BlackScholes(x_ratio, tau_arr[i], Nx, Nt, E, sigma - epsilon, r, D)    # Instance 1 for vega
    vega2_inst = BlackScholes(x_ratio, tau_arr[i], Nx, Nt, E, sigma + epsilon, r, D)    # Instance 2 for vega
    theta1_inst = BlackScholes(x_ratio, tau_arr[i] - epsilon, Nx, Nt, E, sigma, r, D)   # Instance 1 for theta
    theta2_inst = BlackScholes(x_ratio, tau_arr[i] + epsilon, Nx, Nt, E, sigma, r, D)   # Instance 2 for theta
    rho1_inst = BlackScholes(x_ratio, tau_arr[i], Nx, Nt, E, sigma, r - epsilon, D)     # Instance 1 for rho
    rho2_inst = BlackScholes(x_ratio, tau_arr[i], Nx, Nt, E, sigma, r + epsilon, D)     # Instance 2 for rho

    delta_tau[i] = np.gradient(delta_inst.solve('BE'))
    gamma_tau[i] = np.gradient(delta_tau[i])
    vega_tau[i] = (vega2_inst.solve('BE') - vega1_inst.solve('BE'))/(2*epsilon)
    theta_tau[i] = -(theta2_inst.solve('BE') - theta1_inst.solve('BE'))/(2*epsilon)
    rho_tau[i] = (rho2_inst.solve('BE') - rho1_inst.solve('BE'))/(2*epsilon)

for i in range(N_tau):
    plt.plot(S, vega_tau[i], label = r'$\tau = $' + '%g' % tau_arr[i])
plt.xlabel(r'$S$')
plt.ylabel(r'$\nu$')
plt.legend()
plt.tight_layout()
plt.show()