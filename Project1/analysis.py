import numpy as np
import matplotlib.pyplot as plt

infile = open("general_101.txt")
n = 101
vlist = []
for line in infile:
    vlist.append(float(line))
v = np.array(vlist)
x = np.linspace(0, 1, n+2)
u = 1- (1-np.exp(-10))*x - np.exp(-10*x)
plt.plot(x, u, label='Analytisk')
plt.plot(x, v, label='Numerisk')
plt.grid(ls='--')
plt.xlabel('x')
plt.ylabel('u(x)')
plt.legend()
plt.savefig("bild.png")
plt.show()