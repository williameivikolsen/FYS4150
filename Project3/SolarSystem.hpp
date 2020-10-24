#ifndef SolarSystem_HPP
#define SolarSystem_HPP
#include <iostream>
#include <cmath>
#include <fstream>      // Write to file
#include <iomanip>      // Text formatting

using namespace std;

class SolarSystem {
protected:
    double m_T;                   // Total simulation time [yr]
    int m_N;                      // Number of time steps
    int m_Nobjects;               // Number of objects
    double m_h, m_hh;             // Step size, step size squared
    double *m_masses;             // Masses of the objects in the system
    double *m_x;                  // Position x-axis
    double *m_y;                  // Position y-axis
    double *m_z;                  // Position z-axis
    double *m_vx;                 // Velocity x-axis
    double *m_vy;                 // Velocity y-axis
    double *m_vz;                 // Velocity z-axis
    double m_G;                   // Gravitational constant
    double m_ax;                  // Acceleration along x-axis
    double m_ay;                  // Acceleration along y-axis
    double m_az;                  // Acceleration along z-axis
    double *m_axold;              // Old acceleration along x-axis
    double *m_ayold;              // Old acceleration along y-axis
    double *m_azold;              // Old acceleration along z-axis

public:
    SolarSystem(double T, int N, int Nobjects);   // Initialize class object
    void initialize_objects(double *x, double *y, double *z, double *vx, double *vy, double *vz, double *masses); // Sets initial values
    void Gravitational_acc(int t, int p);
    void Relativistic_gravitational_force();
    void solve_euler();                    // Solve differential equation using the Euler method
    void solve_velocity_verlet();          // Solve differential equation using the Verlet method
    void write_to_file(string name);       // Write results to file
};
#endif
