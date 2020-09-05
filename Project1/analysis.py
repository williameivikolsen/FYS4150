import numpy as np
import matplotlib.pyplot as plt

infile_sp = open("special_1000.txt")
infile_ge = open("general_1000.txt")
n = 1000
vlist_sp = []
vlist_ge = []
for line in infile_sp:
    vlist_sp.append(float(line))
for line in infile_ge:
    vlist_ge.append(float(line))
v_sp = np.array(vlist_sp)
v_ge = np.array(vlist_ge)
x = np.linspace(0, 1, n+2)
x_nice = np.linspace(0, 1, 10001)
u = 1- (1-np.exp(-10))*x_nice - np.exp(-10*x_nice)
plt.plot(x_nice, u, label='Analytisk')
plt.plot(x, v_sp, label='Numerisk, spesiell')
plt.plot(x, v_ge, label='Numerisk, generell', ls='--')
plt.grid(ls='--')
plt.xlabel('x')
plt.ylabel('u(x)')
plt.legend()
plt.show()