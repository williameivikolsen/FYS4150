#include <iostream>
#include <cmath>
#include <fstream>
#include <iomanip>
#include "time.h"
#include <chrono>
#include <ctime>
// use namespace for output and input
using namespace std;

//outputfile as global variable
ofstream ofile;
ofstream logfile;

double f(double x) {
    return 100*exp(-10*x);
}

void general(int n, double *d, double *a, double *b, double *c) {
    double *dn, *bn, *v;     // Updated values after forward substitution and unkown
    dn = new double[n]; bn = new double[n]; v = new double[n+2];
    // Lager outfile:
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
        v[i] = (bn[i]-(c[i]*v[i+1]))/dn[i];
    }
    for(int i = 0; i < n+2; i++) {
        ofile << setw(15) << setprecision(8) << v[i] << endl;
    }
    

    delete [] dn; delete [] bn; delete [] v;
}

void special(int n, double *d, double *e, double *b) {
    double *dn;
    double *bn;
}

int main(int argc, char *argv[]){
    // Read output file name and number of grid points
    int n;
    string function;
    if( argc != 3 ){
          cout << "Bad Usage: " << argv[0] <<
              " needs number of grid points and function when executed" << endl;
          exit(1);
    }
        else{
        n = atoi(argv[1]);
        function = argv[2];
    }

    double h = 1.0/(n+2.0);     // Step size
    double hh = h*h;
    double *d, *a, *b, *c, *x;
    d = new double[n]; a = new double[n-1]; b = new double[n]; c = new double[n-1]; x = new double[n+2];  // Se algoritmetekst
    for(int i = 0; i < n+2; i++) {
        x[i] = double(i*h);
    }
    for(int i = 0; i < n-1; i++) {
        d[i] = 2;
        a[i] = -1;
        c[i] = -1;
        b[i] = hh*f(x[i+1]);
    }
    d[n-1] = 2;
    b[n-1] = hh*f(x[n]);
    logfile.open("log.txt", std::ios_base::app);
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