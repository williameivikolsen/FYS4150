#include "SolarSystem.hpp"

using namespace std;
ofstream ofile;


SolarSystem::SolarSystem(double T, int N, int Nobjects){
  // Constants
  m_G = 4*M_PI*M_PI;
  m_T = T;
  m_N = N;
  m_Nobjects = Nobjects;
  m_h = m_T/(m_N-1);
  m_hh = m_h*m_h;
  // Initialize arrays containing positions and velocities for all the planets
  m_masses = new double[m_N];
  m_x = new double[m_N*m_Nobjects];
  m_y = new double[m_N*m_Nobjects];
  m_z = new double[m_N*m_Nobjects];
  m_vx = new double[m_N*m_Nobjects];
  m_vy = new double[m_N*m_Nobjects];
  m_vz = new double[m_N*m_Nobjects];
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
  // Adjust initial conditions to move to C.O.M system
  double *R = new double[3];              // COM position
  double *V = new double[3];              // COM velocity
  double M = 0;                   // Total mass
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
  // Divide by total mass
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
  m_ax = 0;
  m_ay = 0;
  m_az = 0;
  for (int i = 0; i < m_Nobjects; i++) {
    if (i != p) {
      double xdiff = m_x[t*m_Nobjects + p] - m_x[t*m_Nobjects + i];
      double ydiff = m_y[t*m_Nobjects + p] - m_y[t*m_Nobjects + i];
      double zdiff = m_z[t*m_Nobjects + p] - m_z[t*m_Nobjects + i];
      double r3 = pow(xdiff*xdiff + ydiff*ydiff + zdiff*zdiff, 1.5);
      m_ax += -m_G*m_masses[i]/r3*xdiff;
      m_ay += -m_G*m_masses[i]/r3*ydiff;
      m_az += -m_G*m_masses[i]/r3*zdiff;
    }
  }
}

void SolarSystem::solve_euler() {
    cout << "Solving with Euler method..." << endl;
    for (int i = 0; i < m_N; i++) {
      for (int j = 0; j < m_Nobjects; j++) {
        Gravitational_acc(i, j); // Fiks på denne
        m_vx[(i+1)*m_Nobjects + j] = m_vx[i*m_Nobjects + j] + m_h*m_ax;
        m_vy[(i+1)*m_Nobjects + j] = m_vy[i*m_Nobjects + j] + m_h*m_ay;
        m_vz[(i+1)*m_Nobjects + j] = m_vz[i*m_Nobjects + j] + m_h*m_az;
        m_x[(i+1)*m_Nobjects + j] = m_x[i*m_Nobjects + j] + m_h*m_vx[i*m_Nobjects + j];
        m_y[(i+1)*m_Nobjects + j] = m_y[i*m_Nobjects + j] + m_h*m_vy[i*m_Nobjects + j];
        m_z[(i+1)*m_Nobjects + j] = m_z[i*m_Nobjects + j] + m_h*m_vz[i*m_Nobjects + j];
      }
    }
}

void SolarSystem::solve_velocity_verlet() {
    cout << "Solving with Verlet method ..." << endl;
    // Find initial acceleration for all the objects:

    for (int i = 0; i < m_N; i++) {
      for (int j = 0; j < m_Nobjects; j++) {
        Gravitational_acc(i, j); //
        double ax_old = m_ax;  double ay_old = m_ay; double az_old = m_az;
        m_x[(i+1)*m_Nobjects + j] = m_x[i*m_Nobjects + j] + m_h*m_vx[i*m_Nobjects + j] + m_hh*0.5*ax_old;
        m_y[(i+1)*m_Nobjects + j] = m_y[i*m_Nobjects + j] + m_h*m_vy[i*m_Nobjects + j] + m_hh*0.5*ay_old;
        m_z[(i+1)*m_Nobjects + j] = m_z[i*m_Nobjects + j] + m_h*m_vz[i*m_Nobjects + j] + m_hh*0.5*az_old;

        Gravitational_acc(i+1, j); // Acceleration in the next time step
        m_vx[(i+1)*m_Nobjects + j] = m_vx[i*m_Nobjects + j] + m_h*0.5*(ax_old + m_ax);
        m_vy[(i+1)*m_Nobjects + j] = m_vy[i*m_Nobjects + j] + m_h*0.5*(ay_old + m_ay);
        m_vz[(i+1)*m_Nobjects + j] = m_vz[i*m_Nobjects + j] + m_h*0.5*(az_old + m_az);
      }
    }
}

void SolarSystem::write_to_file(string name) {
    int jump = 1;
    if (m_N >= 100000) {
      jump = 100;
    }
    string outfilename = name + "_" + to_string(m_N) + ".txt";
    cout << "Printing to " << outfilename << endl;
    ofile.open(outfilename);
    ofile << setw(6) << "Method" << setw(9) << "t0" << setw(9) << "tn" << setw(8) << "N" << setw(10) << "h" << endl;
    ofile << setw(6) << setprecision(1) << name << setw(9) << 0 << setw(9) << m_T << setw(8) << m_N << setprecision(3) << setw(10) << m_h << endl;
    ofile << endl;
    ofile << "x  -  y  -  z  -  vx  -  vy  -  vz ........." << endl;
    for(int i = 0; i*jump < m_N; i++){
        for (int j = 0; j < m_Nobjects; j++)
          ofile << setw(15) << scientific << setprecision(6) << m_x[i*m_Nobjects + j] << setw(15) << m_y[i*m_Nobjects + j] << setw(15) << m_z[i*m_Nobjects + j] << setw(15) << m_vx[i*m_Nobjects + j] << setw(15) << m_vy[i*m_Nobjects + j] << setw(15) << m_vz[i*m_Nobjects + j];
        ofile << endl;
    }
    ofile.close();
}
