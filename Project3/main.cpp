#include "SolarSystem.hpp"
#include <cstdio>
#include <iostream>

using namespace std;

int main(int argc, char *argv[]) {
    int N = atoi(argv[1]);                              // Number of inegration points
    double T = atof(argv[2]);                           // Time to be simulated
    int Nobjects = atoi(argv[3]);                       // Number of planets
    char* initial_conditions = argv[4];                 // File containing initial conditions for chosen system
    char* masses = argv[5];                             // File containing masses for chosen system
    int mercury = atoi(argv[6]);                        // Parameter to check if we consider the mercury perihelion
    double beta = atof(argv[7]);                        // Beta parameter in gravitational force
    double jupiter_scaling;                             // Jupiter mass scaling factor
    double *x, *y, *z, *vx, *vy, *vz;                   //To store initial conditions for each particle.
    double *mass;                                       //Store mass of particles.
    x = new double[Nobjects];
    y = new double[Nobjects];
    z = new double[Nobjects];
    vx = new double[Nobjects];
    vy = new double[Nobjects];
    vz = new double[Nobjects];
    mass = new double[Nobjects];

    //Open files
    FILE *fp_init = fopen(initial_conditions, "r"); //Open file to read, specified by "r".
    FILE *fp_mass = fopen(masses, "r");    //Open file to read.

    //Loop over each particle and extract its mass and initial conditions:
    for (int i = 0; i < Nobjects; i++){
        fscanf(fp_init, "%lf %lf %lf %lf %lf %lf", &x[i], &y[i], &z[i], &vx[i], &vy[i], &vz[i]); // One %lf (lf=long float or double) for each floating point number on each line of the file.
        fscanf(fp_mass, "%lf", &mass[i]); //Extract mass for particle i.
    }

    fclose(fp_init); //Close file with initial conditions
    fclose(fp_mass); //Close file with masses.

    if (mercury == 1) {
        // Set initial conditions for Sun:
        x[0] = 0; y[0] = 0; z[0] = 0;
        vx[0] = 0; vy[0] = 0; vz[0] = 0;
        // Set initial conditions for Mercury:
        x[1] = 0.3075; y[1] = 0; z[1] = 0;
        vx[1] = 0; vy[1] = 12.44; vz[1] = 0;
    }

    // If we study Sun-Earth-Jupiter system (equivalent to N=3), allow for scaling of Jupiter mass:
    if (Nobjects == 3 && argc > 8) {
        jupiter_scaling = atof(argv[8]);
        cout << jupiter_scaling << endl;
        mass[2] *= jupiter_scaling;
    }

    // If we study Sun-Earth system (equivalent to N=2 and mercury==0), allow for custom inital vals
    // These additional params are on form x0 - y0 - vx0 - vy0
    if (Nobjects == 2 && mercury == 0 && argc > 8) {
        cout << "Made it here" << endl;
        // Set initial conditions for Sun:
        x[0] = 0; y[0] = 0; z[0] = 0;
        vx[0] = 0; vy[0] = 0; vz[0] = 0;
        // Set initial conditions for Earth:
        x[1] = atof(argv[8]); y[1] = atof(argv[9]); z[1] = 0;
        vx[1] = atof(argv[10]); vy[1] = atof(argv[11]); vz[1] = 0;

          cout << x[1] << y[1] <<  vx[1] << vy[1] << endl;
    }

    SolarSystem my_solver(T, N, Nobjects, mercury, beta);
    // Set initial conditions
    my_solver.initialize_objects(x, y, z, vx, vy, vz, mass);

    if (mercury == 0) {
      // Run simulation with Newtonian gravitational force and write to file
        if (Nobjects == 2) {
            my_solver.solve_euler();
            my_solver.write_to_file("Euler");
        }
        my_solver.solve_velocity_verlet();
        my_solver.write_to_file("Verlet");
    }
    else if (mercury == 1) {
        // Run simulation with relativistically corrected gravitational force
        my_solver.solve_velocity_verlet();
        my_solver.write_to_file("Verlet");
    }

    return 0;
}
