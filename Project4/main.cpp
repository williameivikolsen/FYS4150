#include "IsingModel.hpp"
#include <cstdio>
#include <iostream>
#include <omp.h>

using namespace std;

int main(int argc, char *argv[]){
    if(argc < 6){
        cout << "Not enough command line arguments provided." << endl;
        cout << "Expected input: int L - double T - int cycles - bool random_config - int threads - double cutoff_fraction (optional)" << endl;
        cout << "Aborting..." << endl;
        return 1;
    }
    int L = atoi(argv[1]);
    double T = atof(argv[2]);
    int cycles = atoi(argv[3]);
    bool random_config = atoi(argv[4]);         // 1 gives random initialization of spin system, 0 gives fully aligned system
    int threads = atoi(argv[5]);                // Requested number of threads to be used
    double cutoff_fraction = 0.1;               // Fraction of cycles to be disgarded before computing expectation values
    if(argc == 7){
        cutoff_fraction = atof(argv[6]);
    }
    int N = L*L;

    if(threads==1){
        clock_t start, finish;
        start = clock();

        IsingModel my_solver;
        my_solver.Initialize(L, T, cycles, random_config, cutoff_fraction);
        my_solver.MonteCarlo();


        finish = clock();
        double time_used = (double)(finish - start) / (CLOCKS_PER_SEC);
        my_solver.WriteToFile(time_used);
    }

    else{
        if(threads > omp_get_max_threads()){
            cout << "Warning: requested number of threads (" << threads << ") is greater than omp_get_max_threads (" << omp_get_max_threads() << ")" << endl;
            cout << "Changing number of threads to omp_get_max_threads..." << endl;
            threads = omp_get_max_threads();
        }
        omp_set_num_threads(threads);

        double global_Eavg = 0.0;                   // Final Eavg will be average of Eavg for different threads
        double global_Mavg = 0.0;                   // Final Mavg will be average of Eavg for different threads
        double global_Esqavg = 0.0;                 // Final Esqavg will be average of Esqavg for different threads
        double global_Msqavg = 0.0;                 // Final Msqavg will be average of Msqavg for different threads
        double global_acceptancerate = 0.0;         // Acceptance rate will also be averaged over threads
        double global_C_v;
        double global_chi;

        double start_time, end_time;

        #pragma omp parallel
        {
            int ID = omp_get_thread_num();
            int cycles_per_thread = cycles/threads;     // Remainder will be added to master thread later
            #pragma omp master
            {
                if(threads > omp_get_num_threads()) cout << "Warning: Number of threads actually set to be" << omp_get_num_threads() << endl;
                cycles_per_thread += cycles % threads;  // Add remaining cycles
                start_time = omp_get_wtime();    // Master thread keeps track of time
            }
            IsingModel my_solver;
            my_solver.Initialize(L, T, cycles_per_thread, random_config, cutoff_fraction, ID);
            my_solver.MonteCarlo();

            #pragma omp for reduction (+:global_Eavg, global_Mavg, global_Esqavg, global_Msqavg, global_acceptancerate) schedule(static)
            for (int i = 0; i < threads; i++)
            {
                global_Eavg += my_solver.m_Eavg;
                global_Mavg += my_solver.m_Mavg;
                global_Esqavg += my_solver.m_Esqavg;
                global_Msqavg += my_solver.m_Msqavg;
                global_acceptancerate += my_solver.m_acceptancerate;
            }

            #pragma omp master
            {
                global_Eavg /= threads;
                global_Mavg /= threads;
                global_Esqavg /= threads;
                global_Msqavg /= threads;
                global_acceptancerate /= threads;

                double E_varians = (global_Esqavg*N - global_Eavg*global_Eavg*(N*N));
                double M_varians = (global_Msqavg*N - global_Mavg*global_Mavg*(N*N));

                global_C_v = E_varians/(double)(T*T*N);
                global_chi = M_varians/(double)(T*N);

                end_time = omp_get_wtime();
                double time_used = end_time - start_time;

                my_solver.WriteSpins();
                my_solver.WriteToFileParallelized(global_Eavg, global_Mavg, global_C_v, global_chi, cycles, threads, time_used, global_acceptancerate);
            }
        }
    }
    return 0;
}
