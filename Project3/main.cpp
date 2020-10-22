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

    SolarSystem my_solver(T, N, Nobjects);
    // Set initial conditions
    my_solver.initialize_objects(x, y, z, vx, vy, vz, mass);

    if (mercury == 0) {
      // Run simulation with Newtonian gravotational force and write to file
        my_solver.solve_euler();
        my_solver.write_to_file("Euler");
        my_solver.solve_velocity_verlet();
        my_solver.write_to_file("Verlet");
    }
    else if (mercury == 1) {
        // Run simulation with relativistically corrected gravotational force
    }

    return 0;
}
