#include <iostream>
#include <cmath>
#include <fstream>      // Write to file
#include <iomanip>      // Text formatting

using namespace std;

ofstream ofile;         // File to store results

// Using Forward Euler and Velocity Verlet to simulate Earth-Sun system (no object orientation)

void SolveEuler(int N, double h, double *rx, double *ry, double *vx, double *vy);
void SolveVerlet(int N, double h, double *rx, double *ry, double *vx, double *vy);
void WriteToFile(string name, double t0, double tn, int N, double h, double *rx, double *ry, double *vx, double *vy);

int main(){
    // Constants
    double t0 = 0;                      // Start time [yr]
    double tn = 2;                      // End time [yr]
    int N = 1 + 365*1;                  // Time steps
    double h = (tn-t0)/(N-1);           // Step size [yr]

    // Initialize arrays
    double *rx = new double[N];         // Position x-axis
    double *ry = new double[N];         // Position y-axis
    double *vx = new double[N];         // Velocity x-axis
    double *vy = new double[N];         // Velocity y-axis

    // Insert initial values
    rx[0] = 1;                           // r_0x = 1 AU
    ry[0] = 0;                           // r_0y = 0
    vx[0] = 0;                           // v_0x = 0
    vy[0] = 2*M_PI;                      // v_0y = 2*pi AU/yr

    // Solve motion
    SolveEuler(N, h, rx, ry, vx, vy);
    WriteToFile("Euler", t0, tn, N, h, rx, ry, vx, vy);
    SolveVerlet(N, h, rx, ry, vx, vy);
    WriteToFile("Verlet", t0, tn, N, h, rx, ry, vx, vy);

    // Clear memory
    delete[] rx;
    delete[] ry;
    delete[] vx;
    delete[] vy;

    return 0;
}

void SolveEuler(int N, double h, double *rx, double *ry, double *vx, double *vy){
    cout << "Solving with Euler's method" << endl;
    double k = 4*h*M_PI*M_PI;                             // Define k = 4*pi*pi*h
    double r3;                                            // Distance r^3
    for(int i = 0; i < N-1; i++){
        r3 = pow(rx[i]*rx[i] + ry[i]*ry[i], 1.5);
        vx[i+1] = vx[i] - k*rx[i]/r3;
        vy[i+1] = vy[i] - k*ry[i]/r3;       
        rx[i+1] = rx[i] + h*vx[i];
        ry[i+1] = ry[i] + h*vy[i];
    }
}

void SolveVerlet(int N, double h, double *rx, double *ry, double *vx, double *vy){
    cout << "Solving with velocity Verlet..." << endl;
    double k1 = 2*h*h*M_PI*M_PI;                                // Define k1 = 2*pi*pi*h*h
    double k2 = 2*h*M_PI*M_PI;                                  // Define k2 = 2*pi*pi*h
    double r3_old;                                              // Distance r^3 current step
    double r3_new;                                              // Distance r^3 next step
    for(int i = 0; i < N-1; i++){
        r3_old  = pow(rx[i]*rx[i] + ry[i]*ry[i], 1.5);
        rx[i+1] = rx[i] + h*vx[i] - k1*rx[i]/r3_old;
        ry[i+1] = ry[i] + h*vy[i] - k1*ry[i]/r3_old;

        r3_new  = pow(rx[i+1]*rx[i+1] + ry[i+1]*ry[i+1], 1.5);
        vx[i+1] = vx[i] - k2*(rx[i]/r3_old + rx[i+1]/r3_new);
        vy[i+1] = vy[i] - k2*(ry[i]/r3_old + ry[i+1]/r3_new);
    }
}
void WriteToFile(string name, double t0, double tn, int N, double h, double *rx, double *ry, double *vx, double *vy){
    string outfilename = name + "_" + to_string(N) + ".txt";
    cout << "Printing to " << outfilename << endl;
    ofile.open(outfilename);
    ofile << setw(6) << "Method" << setw(9) << "t0" << setw(9) << "tn" << setw(8) << "N" << setw(10) << "h" << endl;
    ofile << setw(6) << setprecision(1) << name << setw(9) << t0 << setw(9) << tn << setw(8) << N << setprecision(3) << setw(10) << h << endl;
    ofile << endl;
    ofile << "rx  -  ry  -  vx  -  vy" << endl;
    for(int i = 0; i < N; i++){
        ofile << scientific << setprecision(6) << rx[i] << setw(15) << ry[i] << setw(15) << vx[i] << setw(15) << vy[i] << endl;
    }
    ofile.close();
}
