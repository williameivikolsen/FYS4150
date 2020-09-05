#include <iostream>
#include <cmath>
#include <fstream>      // Write to file
#include <iomanip>      // Text formatting
#include "time.h"       // Timer
#include <chrono>       // Current time
#include <ctime>        // Print current time
// use namespace for output and input
using namespace std;

ofstream ofile;     // File to store results
ofstream logfile;   // File to log time spent

double f(double x) {
    return 100*exp(-10*x);
}

void general(int n, double *d, double *a, double *b, double *c) {
    // Function that solves equation for the general
    // tridiagonal matrix case

    double *dn = new double[n];     // Updated diagonal elements of matrix
    double *bn = new double[n];     // Updated right side of equation h²f(x)
    double *v = new double[n+2];    // Solution to equation
    // Make outfile:
    string outfilename = "general_";
    outfilename.append(to_string(n));
    outfilename.append(".txt");
    ofile.open(outfilename);

    // Forward substitution:
    dn[0] = d[0];
    bn[0] = b[0];
    for(int i = 1; i < n; i++) {
        dn[i] = d[i] - (a[i-1]*c[i-1])/dn[i-1];
        bn[i] = b[i] - (a[i-1]*bn[i-1])/dn[i-1];
    }
    // Backward substitution:
    v[n+1] = 0;
    v[0] = 0;
    v[n] = bn[n-1]/dn[n-1];
    for(int i = n-1; i > 0; i--) {
        v[i] = (bn[i-1] - c[i-1]*v[i+1])/dn[i-1];
    }
    // Write to file:
    for(int i = 0; i < n+2; i++) {
        ofile << setw(15) << setprecision(8) << v[i] << endl;
    }
    
    // Clear memory
    delete [] dn; delete [] bn; delete [] v;
}

void special(int n, double *d, double *e, double *b) {
    double *dn;
    double *bn;
}

int main(int argc, char *argv[]){
    // Read number of grid points and function to be used
    if( argc != 3 ){
          cout << "Bad Usage: " << argv[0] <<
              " needs number of grid points and function when executed" << endl;
          exit(1);
    }
        else{
        int n = atoi(argv[1]);
        string function = argv[2];
    }
    // Prepare for calculation
    double h = 1.0/(n+2.0);         // Step size
    double hh = h*h;                // Step size squared
    double *d = new double[n];      // Diagonal elements of matrix 
    double *a = new double[n-1];    // Lower diagonal elements
    double *b = new double[n];      // Right side of equation, h²f(x)
    double *c = new double[n-1];    // Upper diagonal elements
    double *x = new double[n+2];    // x coordinates
    // Fill in values of arrays
    for(int i = 0; i < n+2; i++) {
        x[i] = double(i*h);
    }
    for(int i = 0; i < n-1; i++) {
        d[i] = 2;
        a[i] = -1;
        c[i] = -1;
        b[i] = hh*f(x[i+1]);
    }
    // Last elements of d and b not included in loop:
    d[n-1] = 2;
    b[n-1] = hh*f(x[n]);

    // Open log file
    logfile.open("log.txt", std::ios_base::app);
    // Check function and execute
    if(function == "general") {
        clock_t start, finish;
        start = clock();
        general(n, d, a, b, c);
        finish = clock();
        double timeused = (double) (finish - start)/(CLOCKS_PER_SEC );
        auto timenow = chrono::system_clock::to_time_t(chrono::system_clock::now());
        logfile << function << "    " << n << "    " << timeused << "    " << ctime(&timenow) << endl;
    }
        else if(function == "special") {
        double *e;
        clock_t start, finish;
        start = clock();
        special(n, d, e, b);
        finish = clock();
        double timeused = (double)(finish - start) / (CLOCKS_PER_SEC);
        auto timenow = chrono::system_clock::to_time_t(chrono::system_clock::now());
        logfile << function << "    " << n << "    " << timeused << "    " << ctime(&timenow) << endl;
    }
        else {
        cout << "The function you specified does not exist." << endl;
        exit(1);
    }

    return 0;
}