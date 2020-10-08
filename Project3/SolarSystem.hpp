#ifndef SOLARSYSTEM
#define SOLARSYSTEM
#include <iostream>
#include <cmath>
#include <fstream>      // Write to file
#include <iomanip>      // Text formatting

using namespace std;

class SolarSystem {
protected:
    double m_t0;                  // Start time [yr]
    double m_tn;                  // End time [yr]
    int m_N;                      // Number of time steps
    double m_h;                   // Step size
    double *m_x;                  // Position x-axis
    double *m_y;                  // Position y-axis
    double *m_z;                  // Position z-axis
    double *m_vx;                 // Velocity x-axis
    double *m_vy;                 // Velocity y-axis
    double *m_vz;                 // Velocity z-axis
public:
    void initialize(double tn, int N, double x0, double y0, double z0, double vx0, double vy0, double vz0); // Initialize class object
    void solve_euler();                    // Solve differential equation using the Euler method
    void solve_velvet();                   // Solve differential equation using the Velvet method
    void write_to_file(string name);       // Write results to file
};
#endif