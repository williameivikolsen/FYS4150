import numpy as np
import matplotlib.pyplot as plt

n = [10, 100, 1000, 10000, 100000, 1000000]
maxerr_sp = []
maxerr_ge = []
for i in n:
    i_st = str(i)
    infile_sp = open("special_%s.txt" % i_st)
    infile_ge = open("general_%s.txt" % i_st)
    vlist_sp = []
    vlist_ge = []
    for line in infile_sp:
        vlist_sp.append(float(line))
    for line in infile_ge:
        vlist_ge.append(float(line))
    v_sp = np.array(vlist_sp)
    v_ge = np.array(vlist_ge)
    x = np.linspace(0, 1, i+2)
    u = 1- (1-np.exp(-10))*x - np.exp(-10*x)
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
    relerr_sp = np.abs((v_sp - u)/u)[1:-1]
    relerr_ge = np.abs((v_ge - u)/u)[1:-1]
    maxerr_sp.append(np.max(relerr_sp))
    maxerr_ge.append(np.max(relerr_ge))

plt.loglog(n, maxerr_sp, 'o', label='Special algorithm')
plt.loglog(n, maxerr_ge, 'x', label='General algorithm')
plt.title('Maximum relative error')
plt.grid(ls='--')
plt.xlabel('n')
plt.ylabel(r'$\epsilon (n)$')
plt.legend()
plt.show()