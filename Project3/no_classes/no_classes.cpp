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
void TestEarthSun(int N, double eps, double tn, double *rx, double *ry);

int main(){
    // Constants
    double t0 = 0;                      // Start time [yr]
    double tn = 2;                      // End time [yr]
    int N = 1 + 365*1;                  // Time steps
    double h = (tn-t0)/(N-1);           // Step size [yr]
    double eps = 1e-3;                  // Test tolerance [AU]

    // Initialize arrays
    double *rx = new double[N];         // Position x-axis
    double *ry = new double[N];         // Position y-axis
    double *vx = new double[N];         // Velocity x-axis
    double *vy = new double[N];         // Velocity y-axis

    // Insert initial values (real)
    // rx[0] = 9.641327723118710E-01;                          // r_0x = 1 AU
    // ry[0] = 2.465760952329768E-01;                          // r_0y = 0
    // vx[0] = -4.414756238829297E-03*365;                     // v_0x = 0
    // vy[0] = 1.662854248250772E-02*365;                      // v_0y = 2*pi AU/yr

    // Insert initial values (circle)
    rx[0] = 1;
    ry[0] = 0;
    vx[0] = 0;
    vy[0] = 2*M_PI;

    // Solve motion
    SolveEuler(N, h, rx, ry, vx, vy);
    WriteToFile("Euler", t0, tn, N, h, rx, ry, vx, vy);
    SolveVerlet(N, h, rx, ry, vx, vy);
    WriteToFile("Verlet", t0, tn, N, h, rx, ry, vx, vy);
    TestEarthSun(N, eps, tn, rx, ry);

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

void TestEarthSun(int N, double eps, double tn, double *rx, double *ry){
    // Comparison of trajectory with circular orbit, assuming radius 1 AU
    cout << "--------------------------------------------------------------------------------" << endl;
    cout << "Testing Earth orbit with circle. Max trajectory deviation allowed is eps=" << eps << "..." << endl;
    cout << "--------------------------------------------------------------------------------" << endl;

    // Start by finding coordinates of circle
    double *rx_test = new double[N];            // x-vals of circle
    double *ry_test = new double[N];            // y-vals of circle

    double theta_0 = atan2(ry[0], rx[0]);       // Initial angle, note order of ry and rx
    double delta_theta = 2*tn*M_PI/(N-1);
    for(int i = 0; i < N; i++){                 // Fill angle array with values
        rx_test[i] = cos(theta_0 + i*delta_theta);
        ry_test[i] = sin(theta_0 + i*delta_theta);
    }

    // Check that distance from circle doesn't exceed tolerance
    int i_problem = 0;                                                          // First index that exceeds tolerance
    int num_problems = 0;                                                       // Number of indexes with problems
    double deviance = sqrt(pow(rx[0]-rx_test[0], 2) + pow(ry[0]-ry_test[0],2)); // Initial deviance
    double max_deviance = 0;                                                    // Store max deviance
    for(int i = 0; i < N; i++){
        if(deviance > eps && num_problems == 0){
            i_problem = i;
            num_problems++;
        }
        else if(deviance > eps){
            num_problems++;
        }
        double new_deviance = sqrt(pow(rx[i+1]-rx_test[i+1], 2) + pow(ry[i+1]-ry_test[i+1],2));
        if(new_deviance > max_deviance){
            max_deviance = new_deviance;
        }
        deviance = new_deviance;
    }

    // Print out results
    if(num_problems == 0){
        cout << "The test was passed successfully!" << endl;
        cout << "Max recorded deviance was " << max_deviance << endl;
    }
    else{
        cout << "The test failed for " << num_problems << "/" << N << " time steps" << endl;
        cout << "The problems started at index " << i_problem << endl;
        cout << "Max recorded deviance was " << max_deviance << endl;
    }
    delete[] rx_test;
    delete[] ry_test;

}
