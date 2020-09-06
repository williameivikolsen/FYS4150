import numpy as np
import matplotlib.pyplot as plt

# Program to analyze files from tridiag.cpp

# We go through all the values of n we have used:
n = [10, 100, 1000, 10000, 100000, 1000000]
# Make lists for maximum relative error of special
# and general algorithm:
maxerr_sp = []
maxerr_ge = []
for i in n:
    i_st = str(i)   # String to open files
    # Open data from special and general algorithm for n = 1:
    infile_sp = open("special_%s.txt" % i_st)   
    infile_ge = open("general_%s.txt" % i_st)
    # Lists to store data from infiles:
    vlist_sp = []
    vlist_ge = []
    # Read through infiles:
    for line in infile_sp:
        vlist_sp.append(float(line))
    for line in infile_ge:
        vlist_ge.append(float(line))
    # Make arrays of lists:
    v_sp = np.array(vlist_sp)
    v_ge = np.array(vlist_ge)

    # Plot:
    x = np.linspace(0, 1, i+2)
    u = 1- (1-np.exp(-10))*x - np.exp(-10*x) # Analytical

    plt.plot(x, u, label='Analytical')
    plt.plot(x, v_sp, label='Numerical, special')
    plt.plot(x, v_ge, label='Numerical, general', ls='--')
    plt.title('Comparison for n = %s' % i_st)
    plt.grid(ls='--')
    plt.xlabel('x')
    plt.ylabel('u(x)')
    plt.legend()
    plt.savefig('plot_n%s' % i_st)
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
plt.close()