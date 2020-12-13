import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse
import scipy.sparse.linalg 

plt.style.use('seaborn')

" Make solver for Forwards Euler"

L = 5
T = 10
D = 1                       # Diffusion constant
Nx = 60                     # Intervals x-axis
Nt = 1000                    # Intervals t-axis

def I(x):
    return np.sin(np.pi*x/L)**2 + x/4

x = np.linspace(-L, L, Nx+1)
dx = x[1] - x[0]

t = np.linspace(0, T, Nt+1)
dt = t[1] - t[0]

F = D*dt/dx**2                      # Mesh Fourier number (stability requirement)

def ForwardEuler():
    assert F <= 0.5, f"This is not stable, F = {F}"

    u = np.zeros(Nx+1)                  # Known u at current time step 
    u_new = np.zeros(Nx+1)              # Unknown u at next time step


    # Set initial conditions
    for i in range(0, Nx+1):
        u[i] = I(x[i])


    plt.plot(x, u, label=f"t = {t[0]}")                      # Plot: initial

    for n in range(0, Nt):              # Loop over time
        """ Option 1: Thrashy for-loop """
        # for i in range(1, Nx):
        #     u_new[i] = u[i] + F*(u[i-1] - 2*u[i] + u[i+1])

        """ Option 2: Vectorization """
        u_new[1:Nx] = u[1:Nx] + F*(u[0:Nx-1] - 2*u[1:Nx] + u[2:Nx+1])

        u_new[0] = I(x[0])              # Boundary condition left (constant)
        u_new[Nx] = I(x[Nx])            # Boundary condition right (constant)

        u_new, u = u, u_new             # Switch u and u_new before next time iteration

        if Nt % (10*(n+1)) == 0:        # Plot some of the intermediate steps  (every 5)      
            plt.plot(x, u, label=f"t = {t[n+1]}")

    plt.legend()

def BackwardsEuler():
    u = np.zeros(Nx+1)                  # Known u at current time step 

    # Create matrix A to be solved
    main = np.ones(Nx+1)*(1 + 2*F)
    lower = np.ones(Nx)*(-F)
    upper = np.ones(Nx)*(-F)

    main[0] = main[Nx] = 1              # Boundary conditions
    upper[0] = lower[Nx-1] = 0          # Boundary conditions as well

    A = scipy.sparse.diags(diagonals=[main,lower,upper],
            offsets=[0, -1, 1], shape=(Nx+1, Nx+1), format='csr')   # CSR: Compressed sparse row 
    print(A.todense())

    # Set initial conditions
    for i in range(0, Nx+1):
        u[i] = I(x[i])

    plt.plot(x, u, label=f"t = {t[0]}")                      # Plot: initial

    # Actually solve A*u_new = u 
    for n in range(0, Nt):
        u[0] = I(x[0])              # Boundary condition left (constant)
        u[Nx] = I(x[Nx])            # Boundary condition right (constant)
        u_new = scipy.sparse.linalg.spsolve(A, u)

        u_new, u = u, u_new        

        if Nt % (10*(n+1)) == 0:        # Plot some of the intermediate steps  (every 5)      
            plt.plot(x, u, label=f"t = {t[n+1]}")

    plt.legend()

def CrankNicholson():
    u = np.zeros(Nx+1)                  # Known u at current time step 

    # Create matrix A to be solved
    main = np.ones(Nx+1)*(1 + F)
    lower = np.ones(Nx)*(-F/2)
    upper = np.ones(Nx)*(-F/2)

    main[0] = main[Nx] = 1              # Boundary conditions
    upper[0] = lower[Nx-1] = 0          # Boundary conditions as well

    A = scipy.sparse.diags(diagonals=[main,lower,upper],
            offsets=[0, -1, 1], shape=(Nx+1, Nx+1), format='csr')   # CSR: Compressed sparse row 
    print(A.todense())

    # Set initial conditions
    for i in range(0, Nx+1):
        u[i] = I(x[i])

    plt.plot(x, u, label=f"t = {t[0]}")                      # Plot: initial
    

    # Actually solve A*u_new = u 
    for n in range(0, Nt):
        u[0] = I(x[0])              # Boundary condition left (constant)
        u[Nx] = I(x[Nx])            # Boundary condition right (constant)
        u_new = scipy.sparse.linalg.spsolve(A, u)

        u_new, u = u, u_new        

        if Nt % (10*(n+1)) == 0:        # Plot some of the intermediate steps  (every 5)      
            plt.plot(x, u, label=f"t = {t[n+1]}")

    plt.legend()

plt.figure(1)
ForwardEuler()
plt.figure(2)
BackwardsEuler()
plt.figure(3)
CrankNicholson()
plt.show()