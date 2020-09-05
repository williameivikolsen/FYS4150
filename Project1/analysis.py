import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 1, 101)
u = 1- (1-np.exp(-10))*x - np.exp(-10*x)
plt.plot(x, u)
plt.grid(ls='--')
plt.xlabel('x')
plt.ylabel('u(x)')
plt.show()