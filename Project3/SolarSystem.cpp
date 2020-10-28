#include "SolarSystem.hpp"

using namespace std;
ofstream ofile;

SolarSystem::SolarSystem(double T, int N, int Nobjects, int mercury, double beta){
  // Constants
  m_G = 4*M_PI*M_PI;                // Gravitational constant times Sun mass [AU^3/yr^2]
  m_T = T;
  m_N = N;
  m_Nobjects = Nobjects;
  m_h = m_T/(m_N-1);
  m_hh = m_h*m_h;
  m_beta = beta;
  m_mercury = mercury;

  // Initialize arrays containing positions and velocities for all the planets
  m_masses = new double[m_N];
  m_x = new double[m_N*m_Nobjects];
  m_y = new double[m_N*m_Nobjects];
  m_z = new double[m_N*m_Nobjects];
  m_vx = new double[m_Nobjects];
  m_vy = new double[m_Nobjects];
  m_vz = new double[m_Nobjects];
  m_axold = new double[m_Nobjects];
  m_ayold = new double[m_Nobjects];
  m_azold = new double[m_Nobjects];
  m_v0x = new double[m_Nobjects];
  m_v0y = new double[m_Nobjects];
  m_v0z = new double[m_Nobjects];
}

void SolarSystem::initialize_objects(double *x, double *y, double *z, double *vx, double *vy, double *vz, double *masses) {
  // Fill initial conditions into member arrays.
  for (int i = 0; i < m_Nobjects; i++){
    m_x[i] = x[i];
    m_y[i] = y[i];
    m_z[i] = z[i];
    m_vx[i] = vx[i];
    m_vy[i] = vy[i];
    m_vz[i] = vz[i];
    m_masses[i] = masses[i];
  }
  if (m_mercury == 1) {
    m_lc = 3*(pow(m_y[1]*m_vz[1] - m_z[1]*m_vy[1], 2)
      + pow(m_x[1]*m_vz[1] - m_z[1]*m_vx[1], 2)
      + pow(m_x[1]*m_vy[1] - m_y[1]*m_vx[1], 2))/3999424081;
  }

  // Adjust initial conditions to move to C.O.M system
  double *R = new double[3];              // COM position
  double *V = new double[3];              // COM velocity
  double M = 0;                           // Total mass
  // Initialize to zero
  for (int i = 0; i < 3; i++){
    R[i] = 0;
    V[i] = 0;
  }
  for (int i = 0; i < m_Nobjects; i++){
    R[0] += m_masses[i] * m_x[i];
    R[1] += m_masses[i] * m_y[i];
    R[2] += m_masses[i] * m_z[i];
    V[0] += m_masses[i] * m_vx[i];
    V[1] += m_masses[i] * m_vy[i];
    V[2] += m_masses[i] * m_vz[i];
    M += m_masses[i];
  }
  // Divide by total mass to find pos/vel of COM
  for (int i = 0; i < 3; i++){
    R[i] = R[i]/M;
    V[i] = V[i]/M;
  }
  // Remove COM position and velocity from all initial conditions
  for (int i = 0; i < m_Nobjects; i++){
    m_x[i] -= R[0];
    m_y[i] -= R[1];
    m_z[i] -= R[2];
    m_vx[i] -= V[0];
    m_vy[i] -= V[1];
    m_vz[i] -= V[2];
    // Store initial velocities:
    m_v0x[i] = m_vx[i];
    m_v0y[i] = m_vy[i];
    m_v0z[i] = m_vz[i];
  }

  delete[] x;
  delete[] y;
  delete[] z;
  delete[] vx;
  delete[] vy;
  delete[] vz;
  delete[] masses;
  delete[] R;
  delete[] V;
}

void SolarSystem::Gravitational_acc(int t, int p) {
  // Parameter "t" is time index, "p" is planet index
  m_ax = 0;
  m_ay = 0;
  m_az = 0;
  for (int i = 0; i < m_Nobjects; i++) {
    if (i != p) {
      double xdiff = m_x[t*m_Nobjects + p] - m_x[t*m_Nobjects + i];
      double ydiff = m_y[t*m_Nobjects + p] - m_y[t*m_Nobjects + i];
      double zdiff = m_z[t*m_Nobjects + p] - m_z[t*m_Nobjects + i];
      double r3 = pow(xdiff*xdiff + ydiff*ydiff + zdiff*zdiff, (m_beta+1.0)/2);   // m_beta = 2 for normal square inverse law
      m_ax += -m_G*m_masses[i]/r3*xdiff;
      m_ay += -m_G*m_masses[i]/r3*ydiff;
      m_az += -m_G*m_masses[i]/r3*zdiff;
      if (m_mercury == 1) {
        m_ax += -m_G*m_masses[i]/pow(r3, 5.0/3)*xdiff*m_lc;
        m_ay += -m_G*m_masses[i]/pow(r3, 5.0/3)*ydiff*m_lc;
        m_az += -m_G*m_masses[i]/pow(r3, 5.0/3)*zdiff*m_lc;
      }
    }
  }
}

void SolarSystem::solve_euler() {
    cout << "Solving with Euler method..." << endl;
    clock_t start, finish;
    start = clock();
    for (int i = 0; i < m_N; i++) {
      for (int j = 0; j < m_Nobjects; j++) {
        Gravitational_acc(i, j);
        m_vx[j] += m_h*m_ax;
        m_vy[j] += m_h*m_ay;
        m_vz[j] += m_h*m_az;
        m_x[(i+1)*m_Nobjects + j] = m_x[i*m_Nobjects + j] + m_h*m_vx[j];
        m_y[(i+1)*m_Nobjects + j] = m_y[i*m_Nobjects + j] + m_h*m_vy[j];
        m_z[(i+1)*m_Nobjects + j] = m_z[i*m_Nobjects + j] + m_h*m_vz[j];
      }
    }
    finish = clock();
    m_timeused = (double)(finish - start) / (CLOCKS_PER_SEC);
    // Reset velocity arrays to initial values after completion
    for (int j = 0; j < m_Nobjects; j++) {
      m_vx[j] = m_v0x[j]; m_vy[j] = m_v0y[j]; m_vz[j] = m_v0z[j];
    }
}

void SolarSystem::solve_velocity_verlet() {
    cout << "Solving with Verlet method ..." << endl;
    clock_t start, finish;
    start = clock();
    for (int i = 0; i < m_N; i++) {
      for (int j = 0; j < m_Nobjects; j++) {
        Gravitational_acc(i, j);              // Acceleration in current time step
        m_axold[j] = m_ax; m_ayold[j] = m_ay; m_azold[j] = m_az;    // Saves current acc so it's not overwritten
        m_x[(i+1)*m_Nobjects + j] = m_x[i*m_Nobjects + j] + m_h*m_vx[j] + m_hh*0.5*m_ax;
        m_y[(i+1)*m_Nobjects + j] = m_y[i*m_Nobjects + j] + m_h*m_vy[j] + m_hh*0.5*m_ay;
        m_z[(i+1)*m_Nobjects + j] = m_z[i*m_Nobjects + j] + m_h*m_vz[j] + m_hh*0.5*m_az;
      }
      for (int j = 0; j < m_Nobjects; j++) {
        Gravitational_acc(i+1, j);            // Acceleration in next time step
        m_vx[j] += m_h*0.5*(m_axold[j] + m_ax);
        m_vy[j] += m_h*0.5*(m_ayold[j] + m_ay);
        m_vz[j] += m_h*0.5*(m_azold[j] + m_az);
      }
    }
    finish = clock();
    m_timeused = (double)(finish - start) / (CLOCKS_PER_SEC);
    // Reset velocity arrays to initial values after completion
    for (int j = 0; j < m_Nobjects; j++) {
      m_vx[j] = m_v0x[j]; m_vy[j] = m_v0y[j]; m_vz[j] = m_v0z[j];
    }
}

void SolarSystem::write_to_file(string name) {
    int jump = 1;
    if (m_N >= 100000 && m_mercury != 1) { // Keep small increments for Mercury
      jump = 100;
    }
    int T_int = (int) m_T;
    string outfilename = name + "_" + to_string(m_N) + "_" + to_string(T_int) + ".txt";
    cout << "Printing to " << outfilename << endl;
    ofile.open(outfilename);
    ofile << setw(6) << "Method" << setw(9) << "t0" << setw(9) << "tn" << setw(11) << "N" << setw(10) << "h" << setw(6) << "beta" << setw(19) << "Time used [s]" << setw(20) << "Initial vx, vy, vz" << endl;
    ofile << setw(6) << setprecision(1) << name << setw(9) << 0 << setw(9) << m_T << setw(11) << m_N << setprecision(3) << setw(10) << m_h << setw(10) << to_string(m_beta) << setw(15) << to_string(m_timeused) << setw(15) << to_string(m_v0x[1]) << setw(15) << to_string(m_v0y[1]) << setw(15) << to_string(m_v0z[1]) << endl;
    ofile << endl;
    ofile << "x  -  y  -  z  ........." << endl;
    for(int i = 0; i < m_N; i+=jump){
        for (int j = 0; j < m_Nobjects; j++)
          ofile << setw(15) << scientific << setprecision(6) << m_x[i*m_Nobjects + j] << setw(15) << m_y[i*m_Nobjects + j] << setw(15) << m_z[i*m_Nobjects + j];
        ofile << endl;
    }
    ofile.close();
}
