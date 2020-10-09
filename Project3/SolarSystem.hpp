#ifndef SOLARSYSTEM
#define SOLARSYSTEM
#include <iostream>
#include <cmath>
#include <fstream>      // Write to file
#include <iomanip>      // Text formatting

using namespace std;

class SolarSystem {
protected:
    double m_T;                  // Total simulation time [yr]
    int m_N, m_Nobjects;                      // Number of time steps
    double m_h, m_hh;                   // Step size
    double *m_masses;             //Masses of the objects in the system
    double *m_x;                  // Position x-axis
    double *m_y;                  // Position y-axis
    double *m_z;                  // Position z-axis
    double *m_vx;                 // Velocity x-axis
    double *m_vy;                 // Velocity y-axis
    double *m_vz;                 // Velocity z-axis
    void (*m_F)(double x_diff, double y_diff, double z_diff, double m, double *a);
public:
    SolarSystem(void F(double x_diff, double y_diff, double z_diff, double m, double *a));
    void initialize(double tn, int N, double x0, double y0, double z0, double vx0, double vy0, double vz0); // Initialize class object
    void solve_euler();                    // Solve differential equation using the Euler method
    void solve_verlet();                   // Solve differential equation using the Verlet method
    void write_to_file(string name);       // Write results to file
};
#endif
