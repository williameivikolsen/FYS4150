import numpy as np
import matplotlib.pyplot as plt

# Program to analyze files from tridiag.cpp

# We go through all the values of n we have used:
n = [10, 100, 1000, 10000, 100000, 1000000, 10000000]
# Make lists for maximum relative error of special
# and general algorithm:
maxerr_sp = []
maxerr_ge = []

# Make analytical solution 
x_exact = np.linspace(0, 1, 1001)
u_exact = 1- (1-np.exp(-10))*x_exact - np.exp(-10*x_exact)

for i in n:
    # Open data from special and general algorithm for n = 1:
    infile_sp = open("special_%i.txt" % i)   
    infile_ge = open("general_%i.txt" % i)
    # Read through infiles:
    v_sp = np.loadtxt(infile_sp)
    v_ge = np.loadtxt(infile_ge)

    # Plot:
    x = np.linspace(0, 1, i+2)
    u = 1- (1-np.exp(-10))*x - np.exp(-10*x)
    plt.plot(x_exact, u_exact, label='Analytical')
    plt.plot(x, v_sp, label='Numerical, special')
    plt.plot(x, v_ge, label='Numerical, general', ls='--')
    plt.title('Comparison for n = %g' % i)
    plt.grid(ls='--')
    plt.xlabel('x')
    plt.ylabel('u(x)')
    plt.legend()
    plt.savefig('plot_n%.0e' % i)
    plt.show()
    plt.close()
    

    # Calculate relative error:
    relerr_sp = np.abs((v_sp - u)/u)[1:-1]
    relerr_ge = np.abs((v_ge - u)/u)[1:-1]
    # Store maximum relative error in lists:
    maxerr_sp.append(np.max(relerr_sp))
    maxerr_ge.append(np.max(relerr_ge))

# Plot maximum relative error as function of h:
n_arr = np.array(n)
h = 1/(n_arr+2)
plt.loglog(h, maxerr_sp, 'o', label='Special algorithm')
plt.loglog(h, maxerr_ge, 'x', label='General algorithm')
plt.title('Maximum relative error')
plt.grid(ls='--')
plt.xlabel(r'$h$')
plt.ylabel(r'$\epsilon (n)$')
plt.legend()
plt.savefig('maxrel')
plt.show()
plt.close()