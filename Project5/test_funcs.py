import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse
import scipy.sparse.linalg 
from diffusion_class import OneDimensionalDiffusion

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


    # plt.plot(x, u, label=f"t = {t[0]}")                      # Plot: initial

    for n in range(0, Nt):              # Loop over time
        """ Option 1: Thrashy for-loop """
        # for i in range(1, Nx):
        #     u_new[i] = u[i] + F*(u[i-1] - 2*u[i] + u[i+1])

        """ Option 2: Vectorization """
        u_new[1:Nx] = u[1:Nx] + F*(u[0:Nx-1] - 2*u[1:Nx] + u[2:Nx+1])

        u_new[0] = I(x[0])              # Boundary condition left (constant)
        u_new[Nx] = I(x[Nx])            # Boundary condition right (constant)

        u_new, u = u, u_new             # Switch u and u_new before next time iteration

    plt.plot(x, u, label=f"t = {t[n+1]}, FE")

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

    # Set initial conditions
    for i in range(0, Nx+1):
        u[i] = I(x[i])

    # plt.plot(x, u, label=f"t = {t[0]}")                      # Plot: initial

    # Actually solve A*u_new = u 
    for n in range(0, Nt):
        u[0] = I(x[0])              # Boundary condition left (constant)
        u[Nx] = I(x[Nx])            # Boundary condition right (constant)
        u_new = scipy.sparse.linalg.spsolve(A, u)

        u_new, u = u, u_new        

    plt.plot(x, u, label=f"t = {t[n+1]}, BE")
    plt.legend()

def CrankNicholson():
    # In order to find next time-iteration of u, we solve the system A*u_new = b, where b = B*u. 
    
    # Create matrix A to be solved
    A_main = np.ones(Nx+1)*(1 + F)
    A_lower = np.ones(Nx)*(-F/2)
    A_upper = np.ones(Nx)*(-F/2)

    A_main[0] = A_main[Nx] = 1              # Boundary conditions
    A_upper[0] = A_lower[Nx-1] = 0          # Boundary conditions as well

    A = scipy.sparse.diags(diagonals=[A_main,A_lower,A_upper],
            offsets=[0, -1, 1], shape=(Nx+1, Nx+1), format='csr')   # CSR: Compressed sparse row 


    # Make array u, and set initial conditions
    u = np.zeros(Nx+1)                  # Known u at current time step 
    b = np.zeros(Nx+1)

    for i in range(0, Nx+1):
        u[i] = I(x[i])

    plt.plot(x, u, label=f"t = {t[0]}")                      # Plot: initial

    # Actually solve A*u_new = u 
    for n in range(0, Nt):
        b[1:Nx] = u[1:Nx] + F*(0.5*u[0:Nx-1] - u[1:Nx] + 0.5*u[2:Nx+1])
        b[0] = I(x[0])              # Boundary condition left (constant)
        b[Nx] = I(x[Nx])            # Boundary condition right (constant)

        u_new = scipy.sparse.linalg.spsolve(A, b)
        u_new, u = u, u_new        

 
    plt.plot(x, u, label=f"t = {t[n+1]}, CN ")

    plt.legend()

plt.figure(1)
ForwardEuler()

# plt.figure(2)
BackwardsEuler()
# plt.figure(3)
CrankNicholson()
# ############################3
x_start = -5; x_end = 5; T = 10
Nx = 60; Nt = 1000
x_array = np.linspace(x_start,x_end,Nx+1)



BCL = lambda t: I(x_start)                        # Boundary condition at x=x_start 
BCR = lambda t: I(x_end)                          # Boundary condition at x=x_end

test_object = OneDimensionalDiffusion(-5, 5, 10, 60, 1000, I, BCL, BCR)
u_array1 = test_object.solve('FE')
u_array2 = test_object.solve('BE')
u_array3 = test_object.solve('CN')
u_array4 = test_object.solve('FE')


plt.plot(x_array, u_array1, 'o', label='FE')
plt.plot(x_array, u_array2, 'o',label='BE')
plt.plot(x_array, u_array3, 'o',label='CN')

# ###############################


plt.legend()
plt.show()