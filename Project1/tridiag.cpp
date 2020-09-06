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

double f(double x);
void general(int n, double *d, double *a, double *b, double *c);
void special(int n, double *b);

int main(int argc, char *argv[]){
    // Read dimension of matrix and function to be used
    int n; string function;
    if( argc != 3 ){
          cout << "Bad Usage: " << argv[0] <<
              " needs dimension of matrix (n) and name of function to be called (general/special)" << endl;
          exit(1);
    }
        else{
        n = atoi(argv[1]);
        function = argv[2];
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
        d[i] = 2.0;
        a[i] = -1.0;
        c[i] = -1.0;
        b[i] = hh*f(x[i+1]);
    }
    // Last elements of d and b not included in loop:
    d[n-1] = 2;
    b[n-1] = hh*f(x[n]);

    // Open log file
    logfile.open("log.txt", std::ios_base::app);
    // Check function and execute
    if(function == "general") {
        general(n, d, a, b, c);
    }
        else if(function == "special") {
        special(n, b);
    }
        else {
        cout << "The function you specified does not exist." << endl;
        exit(1);
    }
    // Close log file
    logfile.close();

    return 0;
}

double f(double x)
{
    return 100 * exp(-10 * x);
}

void general(int n, double *d, double *a, double *b, double *c)
{
    // Function that solves equation for the general
    // tridiagonal matrix case

    double *dn = new double[n];    // Updated diagonal elements of matrix
    double *bn = new double[n];    // Updated right side of equation h²f(x)
    double *v = new double[n + 2]; // Solution to equation
    // Make outfile:
    string outfilename = "general_";
    outfilename.append(to_string(n));
    outfilename.append(".txt");
    ofile.open(outfilename);

    // Make ready for forward/backward substitution:
    dn[0] = d[0];
    bn[0] = b[0];
    v[n + 1] = 0;
    v[0] = 0;
    clock_t start, finish;
    start = clock();
    // Forward substitution:
    for (int i = 1; i < n; i++)
    {
        dn[i] = d[i] - (a[i - 1] * c[i - 1]) / dn[i - 1];
        bn[i] = b[i] - (a[i - 1] * bn[i - 1]) / dn[i - 1];
    }
    v[n] = bn[n - 1] / dn[n - 1];
    // Backward substitution:
    for (int i = n - 1; i > 0; i--)
    {
        v[i] = (bn[i - 1] - c[i - 1] * v[i + 1]) / dn[i - 1];
    }
    finish = clock();
    double timeused = (double)(finish - start) / (CLOCKS_PER_SEC);
    auto timenow = chrono::system_clock::to_time_t(chrono::system_clock::now());
    double float_n = (double)n;
    logfile << "general      " << scientific << setprecision(1) << float_n << setw(10) << setprecision(2) << timeused << setw(30) << ctime(&timenow);
    // Write to file:
    for (int i = 0; i < n + 2; i++)
    {
        ofile << setw(15) << setprecision(8) << v[i] << endl;
    }

    // Clear memory
    delete[] dn;
    delete[] bn;
    delete[] v;
    // Close outfile
    ofile.close();
}

void special(int n, double *b)
{
    // Function that solves equation for the general
    // tridiagonal matrix case

    double *dn = new double[n];    // Updated diagonal elements of matrix
    double *bn = new double[n];    // Updated right side of equation h²f(x)
    double *v = new double[n + 2]; // Solution to equation
    // Make outfile:
    string outfilename = "special_";
    outfilename.append(to_string(n));
    outfilename.append(".txt");
    ofile.open(outfilename);

    // We have analytical expression for dn in special case:
    for (int i = 1; i < n + 1; i++)
    {
        dn[i - 1] = (1.0 + i) / i;
    }
    // Make ready for forward/backward substitution:
    bn[0] = b[0];
    v[n + 1] = 0;
    v[0] = 0;
    clock_t start, finish;
    start = clock();
    // Forward substitution:
    for (int i = 1; i < n; i++)
    {
        bn[i] = b[i] + bn[i - 1] / dn[i - 1];
    }
    v[n] = bn[n - 1] / dn[n - 1];
    // Backward substitution:
    for (int i = n - 1; i > 0; i--)
    {
        v[i] = (bn[i - 1] + v[i + 1]) / dn[i - 1];
    }
    finish = clock();
    double timeused = (double)(finish - start) / (CLOCKS_PER_SEC);
    auto timenow = chrono::system_clock::to_time_t(chrono::system_clock::now());
    double float_n = (double)n;
    logfile << "special      " << scientific << setprecision(1) << float_n << setw(10) << setprecision(2) << timeused << setw(30) << ctime(&timenow);
    // Write to file:
    for (int i = 0; i < n + 2; i++)
    {
        ofile << setw(15) << setprecision(8) << v[i] << endl;
    }

    // Clear memory
    delete[] dn;
    delete[] bn;
    delete[] v;
    // Close outfile
    ofile.close();
}