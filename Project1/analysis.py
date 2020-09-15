#%%
import numpy as np
import matplotlib.pyplot as plt

# Program to analyze files from tridiag.cpp

# We go through all the values of n we have used:
n = [10, 100, 1000, 1e4, 1e5, 1e6, 1e7]
# Make lists for maximum relative error of special
# and general algorithm:
maxerr_sp = []
maxerr_ge = []
maxerr_LU = []


# Make analytical solution 
x_exact = np.linspace(0, 1, 1001)
u_exact = 1- (1-np.exp(-10))*x_exact - np.exp(-10*x_exact)
for i in n[:4]: # Up to 1e5 (max number for LU-decomp)
    i = int(i)
    # Open data from special and general algorithm for n = 1:
    infile_sp = open("special_%i.txt" % i)   
    infile_ge = open("general_%i.txt" % i)
    infile_LU = open("LU_%i.txt" % i)

    # Read through infiles:
    v_sp = np.loadtxt(infile_sp)
    v_ge = np.loadtxt(infile_ge)
    v_LU = np.loadtxt(infile_LU)


    x = np.linspace(0, 1, i+2)
    u = 1- (1-np.exp(-10))*x - np.exp(-10*x)

    if i <= 100 :
        # Plot:
        plt.plot(x_exact, u_exact, label='Analytical')
        plt.plot(x, v_sp, label='Numerical, special')
        plt.plot(x, v_ge, label='Numerical, general', ls=':')
        plt.plot(x, v_LU, label='Numerical, LU', ls='-.', alpha=0.6)        
    
        #plt.title('Comparison for n = %g' % i)
        plt.grid(ls='--')
        plt.xlabel('x')
        plt.ylabel('u(x)')
        plt.legend()
        string_savefig = "plot_n" + str(i)
        plt.savefig(string_savefig)
        plt.show()
        plt.close()
    

    # Calculate relative error:
    relerr_sp = np.abs((v_sp - u)/u)[1:-1]
    relerr_ge = np.abs((v_ge - u)/u)[1:-1]
    relerr_LU = np.abs((v_LU - u)/u)[1:-1]

    # Store maximum relative error in lists:
    maxerr_sp.append(np.max(relerr_sp))
    maxerr_ge.append(np.max(relerr_ge))
    maxerr_LU.append(np.max(relerr_LU))

for i in n[4:]: # Remaining n (without LU-data)
    i = int(i)

    x = np.linspace(0, 1, i+2)
    u = 1- (1-np.exp(-10))*x - np.exp(-10*x)   
    
    infile_sp = open("special_%i.txt" % i)   
    infile_ge = open("general_%i.txt" % i)

    # Read through infiles:
    v_sp = np.loadtxt(infile_sp)
    v_ge = np.loadtxt(infile_ge)

    # Calculate relative error:
    relerr_sp = np.abs((v_sp - u)/u)[1:-1]
    relerr_ge = np.abs((v_ge - u)/u)[1:-1]

    # Store maximum relative error in lists:
    maxerr_sp.append(np.max(relerr_sp))
    maxerr_ge.append(np.max(relerr_ge))

#Plot maximum relative error as function of h:
n_arr = np.array(n)
h = 1/(n_arr+2)
plt.loglog(h, maxerr_sp, 'o', label='Special algorithm')
plt.loglog(h, maxerr_ge, 'x', label='General algorithm')
plt.loglog(h[:4], maxerr_LU, '*', label='LU-decomposition')

#plt.title('Maximum relative error')

plt.grid(ls='--')
plt.xlabel(r'$h$')
plt.ylabel(r'$\epsilon (n)$')
plt.legend()
plt.savefig('maxrel')
plt.show()
plt.close()

# Start CPU time plot -> no average, one value

time_sp = np.array([1.00e-06,1.00e-06,1.30e-05,1.40e-04,1.52e-03,1.45e-02,1.47e-01])
time_ge = np.array([1.00e-06,2.00e-06,1.60e-05,2.04e-04,1.96e-03,2.16e-02,1.95e-01])
time_LU = np.array([8.70e-05, 1.71e-04, 9.16e-02, 9.50e+00])

plt.loglog(n_arr, time_sp, 'o', label='Special algorithm')
plt.loglog(n_arr, time_ge, 'x', label='General algorithm')
plt.loglog(n_arr[:4], time_LU, '*', label='LU-decomposition')

plt.grid(ls='--')
plt.xlabel(r'$n$')
plt.ylabel(r'CPU time (s)')
plt.legend()
plt.savefig('time')
plt.show()
plt.close()



"""
Time values taken from following data from logfile

special      1.0e+01  1.00e-06     Thu Sep 10 19:41:50 2020
special      1.0e+02  1.00e-06     Thu Sep 10 19:41:50 2020
special      1.0e+03  1.30e-05     Thu Sep 10 19:41:50 2020
special      1.0e+04  1.40e-04     Thu Sep 10 19:41:50 2020
special      1.0e+05  1.52e-03     Thu Sep 10 19:41:50 2020
special      1.0e+06  1.45e-02     Thu Sep 10 19:41:50 2020
special      1.0e+07  1.47e-01     Thu Sep 10 19:41:54 2020
general      1.0e+01  1.00e-06     Thu Sep 10 19:42:31 2020
general      1.0e+02  2.00e-06     Thu Sep 10 19:42:31 2020
general      1.0e+03  1.60e-05     Thu Sep 10 19:42:31 2020
general      1.0e+04  2.04e-04     Thu Sep 10 19:42:31 2020
general      1.0e+05  1.96e-03     Thu Sep 10 19:42:31 2020
general      1.0e+06  2.16e-02     Thu Sep 10 19:42:31 2020
general      1.0e+07  1.95e-01     Thu Sep 10 19:42:36 2020
LU           1.0e+01  8.70e-05     Thu Sep 10 19:43:11 2020
LU           1.0e+02  1.71e-04     Thu Sep 10 19:43:12 2020
LU           1.0e+03  9.16e-02     Thu Sep 10 19:43:12 2020
LU           1.0e+04  9.50e+00     Thu Sep 10 19:43:27 2020
"""
# %%
