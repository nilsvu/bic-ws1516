#include <iostream>
#include <complex>
#include <math.h>
#include <vector>

using namespace std;


//***********************Constants
const int d = 1; //dimensions
const int tSim = 200; //simulation time
const double Dt = 30; //step size
//***********************Constants

// use command: clear; g++ -std=c++11  main.cpp -o run; ./run

double HeavisideTheta(double x){
	if(x > 0) return 1.;
	if(x < 0) return 0.;
	return 0.5;
}



int main(int argc, const char* argv[] ){
	
	//definition
	cout << "\t\tprogram started, defining\n";
	vector<double> state(d);
	
	//initialisierung
	cout << "\t\tinitialising\n";
	for(int i = 0; i< d; i++){
		state[i] = 0;
	}
	
	//integrieren
	cout << "\t\tprogramintegrating\n";
	for(int i = 0; i < tSim/Dt; i++){
		double t = i*Dt;
		
		cout << t << "\t" << state[0] << "\n";
		
			//vector<double> difference(d);
		//********************Insert correct formula here
		state[0] += Dt * 0.1 * (-state[0]+HeavisideTheta(i*Dt));
		//********************Insert correct formula here
			//state = state + difference;
	}
	
	//ausgabe
	cout << "\t\tprogram finished\n";
	
	
}
