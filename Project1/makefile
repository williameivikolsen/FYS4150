all: compile execute

compile:
	c++ -o tridiag.exe tridiag.cpp -larmadillo

execute:
	./tridiag.exe 10 special
	./tridiag.exe 10 general
	./tridiag.exe 100 special
	./tridiag.exe 100 general
	./tridiag.exe 1000 special
	./tridiag.exe 1000 general
	./tridiag.exe 10000 special
	./tridiag.exe 10000 general
	./tridiag.exe 100000 special
	./tridiag.exe 100000 general
	./tridiag.exe 1000000 special
	./tridiag.exe 1000000 general
	./tridiag.exe 10000000 special
	./tridiag.exe 10000000 general
	./tridiag.exe 10 LU
	./tridiag.exe 100 LU
	./tridiag.exe 1000 LU
	./tridiag.exe 10000 LU
