#include "SolarSystem.hpp"

using namespace std;
ofstream ofile;


SolarSystem::SolarSystem(int Nobjects, int N){
  // Constants
  m_N = N;
  m_Nobjects = Nobjects;
  m_T = T;
  m_N = N;
  m_h = m_T/(m_N-1);
  m_hh = m_h*m_h;
  // Initialize arrays
  m_masses = new double[m_N];
  m_x = new double[m_N*m_Nobjects];
  m_y = new double[m_N*m_Nobjects];
  m_z = new double[m_N*m_Nobjects];
  m_vx = new double[m_N*m_Nobjects];
  m_vy = new double[m_N*m_Nobjects];
  m_vz = new double[m_N*m_Nobjects];
}
void SolarSystem::initialize_objects(double *x, double *y, double *z, double *vx, double *vy, double *vz, double *masses) {
  //Fill initial conditions into member arrays.
  for (int i = 0; i < m_Nobjects; i++){
    m_x[i] = x[i];
    m_y[i] = y[i];
    m_z[i] = z[i];
    m_vx[i] = vx[i];
    m_vy[i] = vy[i];
    m_vz[i] = vz[i];
    m_masses[i] = masses[i];
  }

  delete[] x;
  delete[] y;
  delete[] z;
  delete[] vx;
  delete[] vy;
  delete[] vz;
  delete[] masses;
}

void SolarSystem::Gravitational_force() {

}

void SolarSystem::Relativistic_gravitational_force() {

}


void SolarSystem::solve_euler() {
    cout << "Solving with Euler method..." << endl;
    double k = 4*m_h*M_PI*M_PI;                             // Define k = 4*pi*pi*h
    double r3;                                              // Distance r^3
    for(int i = 0; i < m_N-1; i++){
        r3 = pow(m_x[i]*m_x[i] + m_y[i]*m_y[i]+ m_z[i]*m_z[i], 1.5);
        m_vx[i+1] = m_vx[i] - k*m_x[i]/r3;
        m_vy[i+1] = m_vy[i] - k*m_y[i]/r3;
        m_vz[i+1] = m_vz[i] - k*m_z[i]/r3;
        m_x[i+1] = m_x[i] + m_h*m_vx[i];
        m_y[i+1] = m_y[i] + m_h*m_vy[i];
        m_z[i+1] = m_z[i] + m_h*m_vz[i];
    }
}

void SolarSystem::solve_velocity_verlet() {
    cout << "Solving with Verlet method ..." << endl;
    double k1 = 2*m_h*m_h*M_PI*M_PI;                            // Define k1 = 2*pi*pi*h*h
    double k2 = 2*m_h*M_PI*M_PI;                                // Define k2 = 2*pi*pi*h
    double r3_old;                                              // Distance r^3 current step
    double r3_new;                                              // Distance r^3 next step
    r3_old = pow(m_x[0]*m_x[0] + m_y[0]*m_y[0] + m_z[0]*m_z[0], 1.5);
    for(int i = 0; i < m_N-1; i++){
        m_x[i+1] = m_x[i] + m_h*m_vx[i] - k1*m_x[i]/r3_old;
        m_y[i+1] = m_y[i] + m_h*m_vy[i] - k1*m_y[i]/r3_old;
        m_z[i+1] = m_z[i] + m_h*m_vz[i] - k1*m_z[i]/r3_old;

        r3_new  = pow(m_x[i+1]*m_x[i+1] + m_y[i+1]*m_y[i+1] + m_z[i+1]*m_z[i+1], 1.5);
        m_vx[i+1] = m_vx[i] - k2*(m_x[i]/r3_old + m_x[i+1]/r3_new);
        m_vy[i+1] = m_vy[i] - k2*(m_y[i]/r3_old + m_y[i+1]/r3_new);
        m_vz[i+1] = m_vz[i] - k2*(m_z[i]/r3_old + m_z[i+1]/r3_new);
        r3_old = r3_new;
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
    for(int i = 0; i < m_N*m_Nobjects; i++){
        ofile << scientific << setprecision(6) << m_x[i] << setw(15) << m_y[i] << setw(15) << m_z[i] << setw(15) << m_vx[i] << setw(15) << m_vy[i] << setw(15) << m_vz[i] << endl;
    }
    ofile.close();
}
