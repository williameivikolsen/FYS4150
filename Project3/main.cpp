#include "SolarSystem.hpp"
#include <cstdio>

using namespace std;

void F(double x_diff, double y_diff, double z_diff, double m);

int main(int argc, char *argv[]) {
    int N = atoi(argv[1]);                              // Number of inegration points
    double tn = atof(argv[2]);                          // Time to be simulated
    int Nplanets = atoi(argv[3]);                       // Number of planets

    double *x, *y, *z, *vx, *vy, *vz;                   //To store initial conditions for each particle.
    double *mass;                                       //Store mass of particles.
    x = new double[Nplanets];
    y = new double[Nplanets];
    z = new double[Nplanets];
    vx = new double[Nplanets];
    vy = new double[Nplanets];
    vz = new double[Nplanets];
    mass = new double[Nplanets];

    char* filename_pos_vel = "positions_and_vel.txt";   //Each line of file gives initial condition for a particle on the form: x y z vx vy vz
    char* filename_mass = "masses.txt";                 //Each line of the file contains a mass for a given particle.

    //Open files
    FILE *fp_init = fopen(filename_pos_vel, "r"); //Open file to read, specified by "r".
    FILE *fp_mass = fopen(filename_mass, "r");    //Open file to read.

    //Loop over each particle and extract its mass and initial conditions:
    for (int i = 0; i < Nplanets; i++){
        fscanf(fp_init, "%lf %lf %lf %lf %lf %lf", &x[i], &y[i], &z[i], &vx[i], &vy[i], &vz[i]); // One %lf (lf=long float or double) for each floating point number on each line of the file.
        fscanf(fp_mass, "%lf", &mass[i]); //Extract mass for particle i.
    }

    fclose(fp_init); //Close file with initial conditions
    fclose(fp_mass); //Close file with masses.

    // Løser foreløpig kun for jorda (element 0)
    SolarSystem my_solver(F);
    my_solver.initialize(tn, N, x[0], y[0], z[0], vx[0], vy[0], vz[0]);
    my_solver.solve_euler();
    my_solver.write_to_file("Euler");
    my_solver.solve_velvet();
    my_solver.write_to_file("Verlet");

    return 0;
}
