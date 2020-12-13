import numpy as np
import scipy.sparse
import scipy.sparse.linalg 

class OneDimensionalDiffusion:
    # Class for solving 1D diffusion equation without source term 
    def __init__(self, x_start, x_end, T, Nx, Nt, I, BCL, BCR, D=1):
        # Constants
        self.x_start = x_start              # x-axis start position
        self.x_end = x_end                  # x-axis end position
        self.T = T                          # Final time
        self.Nx = Nx                        # Number of intervals x-axis
        self.Nt = Nt                        # Number of intervals time
        self.D = D                          # Diffusion constant

        # Functions
        self.I = I                          # Initial condtion I(x)
        self.BCL = BCL                      # Boundary condition BCL(x=x_start, t)
        self.BCR = BCR                      # Boundary condition BCL(x=x_end, t)

        # Set up arrays
        x = np.linspace(x_start,x_end,Nx+1) # Position array
        t = np.linspace(0, T, Nt+1)         # Time array
        dx = x[1] - x[0]
        self.dt = t[1] - t[0]
        self.F = D*self.dt/dx**2            # Mesh Fourier number (stability requirement)

        # Fill in initial values
        self.u0 = np.zeros(Nx+1)            # u0 is initial values of u
        for i in range(0, Nx+1):
            self.u0[i] = I(x[i])


    def solve(self, method, stabilitycheck=True):
        # The PDE is solved using the chosen method, returns solution u
        assert method in ['FE', 'BE', 'CN'], \
            f"Method name has to be 'FE' (Forward Euler), 'BE' (Backward Euler) or 'CN' (Crank-Nicholson)"

        if method == 'FE':
            solution = self.__ForwardEuler(stabilitycheck)
        elif method == 'BE':
            solution = self.__BackwardEuler()
        elif method == 'CN':
            solution = self.__CrankNicholson()

        return solution

    # Private methods for different solving schemes
    def __ForwardEuler(self, stabilitycheck):
        if stabilitycheck == True:
            assert self.F <= 0.5, \
                f"Error: Stability criteria for Forward Euler not met, F = {self.F:.3f}, which is greater than 0.5."        
        elif self.F >= 0.5:
            print(f"Warning: Stability criteria for Forward Euler not met, F = {self.F:.3f}, which is greater than 0.5.")

        u = self.u0.copy()                                     # Current time step
        Nx, F = self.Nx, self.F
        u_new = np.zeros(len(u))                        # Next time step (to be calculated)

        for n in range(0, self.Nt):                     # Loop over time
            # Use vectorization to efficiently find u_new
            u_new[1:Nx] = u[1:Nx] + self.F*(u[0:Nx-1] - 2*u[1:Nx] + u[2:Nx+1])

            u_new[0] = self.BCL(n*self.dt)              # Boundary condition left
            u_new[Nx] = self.BCR(n*self.dt)             # Boundary condition right

            u_new, u = u, u_new                         # Switch u and u_new before next time iteration
        return u


    def __BackwardEuler(self):
        u = self.u0.copy()                              # Current time step
        Nx, F = self.Nx, self.F
        u_new = np.zeros(len(u))                        # Next time step (to be calculated)

        # Create tridiagonal matrix A to be solved
        main = np.ones(Nx+1)*(1 + 2*F)
        lower = np.ones(Nx)*(-F)
        upper = np.ones(Nx)*(-F)

        main[0] = main[Nx] = 1              # Include boundary conditions in A (left)
        upper[0] = lower[Nx-1] = 0          # Include boundary conditions in A (right)

        A = scipy.sparse.diags(diagonals=[main,lower,upper],
                offsets=[0, -1, 1], shape=(Nx+1, Nx+1), format='csr')   # CSR: Compressed sparse row 
        
        # Solve A*u_new = u for every time step
        for n in range(0, self.Nt):
            u_new[0] = self.BCL(n*self.dt)              # Boundary condition left
            u_new[Nx] = self.BCR(n*self.dt)             # Boundary condition right
            
            u_new = scipy.sparse.linalg.spsolve(A, u)   # Use scipy sparse matrix solver
            u_new, u = u, u_new                         # Switch u and u_new before next time iteration
        return u


    def __CrankNicholson(self):
        # In order to find next time-iteration of u, we solve the system A*u_new = b, where b = B*u. 
        u = self.u0.copy()                              # Current time step
        Nx, F = self.Nx, self.F
        u_new = np.zeros(len(u))                        # Next time step (to be calculated)
        b = np.zeros(len(u))                            # Intermediate step array (to be calculated)
    
        # Create tridiagonal matrix A to be solved
        main = np.ones(Nx+1)*(1 + F)
        lower = np.ones(Nx)*(-F/2)
        upper = np.ones(Nx)*(-F/2)

        main[0] = main[Nx] = 1              # Include boundary conditions in A (left)
        upper[0] = lower[Nx-1] = 0          # Include boundary conditions in A (right)

        A = scipy.sparse.diags(diagonals=[main,lower,upper],
                offsets=[0, -1, 1], shape=(Nx+1, Nx+1), format='csr')   # CSR: Compressed sparse row 
       
        # Now, start actually solving the problem
        for n in range(0, self.Nt):
            # Calculate b = B*u
            b[1:Nx] = u[1:Nx] + F*(0.5*u[0:Nx-1] - u[1:Nx] + 0.5*u[2:Nx+1])
            b[0] = self.BCL(n*self.dt)                  # Boundary condition left
            b[Nx] = self.BCR(n*self.dt)                 # Boundary condition right
            
            # Solve A*u_new = b
            u_new = scipy.sparse.linalg.spsolve(A, b)   # Use scipy sparse matrix solver
            u_new, u = u, u_new                         # Switch u and u_new before next time iteration
        return u



# class BlackScholes(OneDimensionalDiffusion):
#     def __init__(self, input_vars_BS):
#         # Make transformations..... 
#         super().__init__(L,T,Nx,Nt,I,D=1)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    plt.style.use('seaborn')

    x_start = -5; x_end = 5; T = 10
    Nx = 60; Nt = 1000
    
    IC = lambda x: np.sin(np.pi*x/x_end)**2 + x/4      # Initial conditions
    BCL = lambda t: IC(x_start)                        # Boundary condition at x=x_start 
    BCR = lambda t: IC(x_end)                          # Boundary condition at x=x_end

    test_object = OneDimensionalDiffusion(x_start, x_end, T, Nx, Nt, IC, BCL, BCR)
    u_array1 = test_object.solve('FE')
    u_array2 = test_object.solve('BE')
    u_array3 = test_object.solve('CN')

    x_array = np.linspace(x_start,x_end,Nx+1)
    plt.plot(x_array, u_array1, label='FE')
    plt.plot(x_array, u_array2, label='BE')
    plt.plot(x_array, u_array3, label='CN')

    plt.plot(x_array, IC(x_array))
    plt.legend()
    plt.show()

    print(IC(-5), IC(5))