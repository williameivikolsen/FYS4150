#include "SolarSystem.hpp"

using namespace std;
ofstream ofile;

void SolarSystem::initialize(double tn, int N, double x0, double y0, double z0, double vx0, double vy0, double vz0) {
    // Constants
    m_t0 = 0.0;
    m_tn = tn;
    m_N = N;
    m_h = (m_tn - m_t0)/m_N;        // Riktig å dele på N her?

    // Initialize arrays
    double *m_x = new double[m_N];
    double *m_y = new double[m_N];
    double *m_z = new double[m_N];
    double *m_vx = new double[m_N];
    double *m_vy = new double[m_N];
    double *m_vz = new double[m_N];

    // Insert initial values
    m_x[0] = x0;
    m_y[0] = y0;
    m_z[0] = z0;
    m_vx[0] = vx0;
    m_vy[0] = vy0;
    m_vz[0] = vz0;
}

void SolarSystem::solve_euler() {
    cout << "Solving with Euler method..." << endl;
    double k = 4*m_h*M_PI*M_PI;                             // Define k = 4*pi*pi*h
    double r3;                                              // Distance r^3
    for(int i = 0; i < m_N-1; i++){
        r3 = pow(m_x[i]*m_x[i] + m_y[i]*m_y[i], 1.5);
        m_vx[i+1] = m_vx[i] - k*m_x[i]/r3;
        m_vy[i+1] = m_vy[i] - k*m_y[i]/r3;
        m_vz[i+1] = m_vz[i] - k*m_z[i]/r3;     
        m_x[i+1] = m_x[i] + m_h*m_vx[i];
        m_y[i+1] = m_y[i] + m_h*m_vy[i];
        m_z[i+1] = m_z[i] + m_h*m_vz[i];
    }
}

void SolarSystem::solve_velvet() {
    cout << "Solving with Verlet method ..." << endl;
    double k = 4*m_h*m_h*M_PI*M_PI;                             // Define k = 4*pi*pi*h
    double r3;
    for(int i = 0; i < m_N-1; i++){
        r3 = pow(m_x[i]*m_x[i] + m_y[i]*m_y[i], 1.5);
        m_x[i+1] = 2*m_x[i] - m_x[i-1] - k*m_x[i]/r3;
        m_y[i+1] = 2*m_y[i] - m_y[i-1] - k*m_y[i]/r3;
        m_z[i+1] = 2*m_z[i] - m_z[i-1] - k*m_z[i]/r3;
    }
}

void SolarSystem::write_to_file(string name) {
    string outfilename = name + "_" + to_string(m_N) + ".txt";
    cout << "Printing to " << outfilename << endl;
    ofile.open(outfilename);
    ofile << setw(6) << "Method" << setw(9) << "t0" << setw(9) << "tn" << setw(8) << "N" << setw(10) << "h" << endl;
    ofile << setw(6) << setprecision(1) << name << setw(9) << m_t0 << setw(9) << m_tn << setw(8) << m_N << setprecision(3) << setw(10) << m_h << endl;
    ofile << endl;
    ofile << "x  -  y  -  z  -  vx  -  vy  -  vz" << endl;
    for(int i = 0; i < m_N; i++){
        ofile << scientific << setprecision(6) << m_x[i] << setw(15) << m_y[i] << setw(15) << m_z[i] << setw(15) << m_vx[i] << setw(15) << m_vy[i] << setw(15) << m_vz[i] << endl;
    }
    ofile.close();
}