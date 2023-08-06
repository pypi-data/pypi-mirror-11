#ifndef CIntegrateAndFireTransferFunction_H
#define  CIntegrateAndFireTransferFunction_H
#include "../../../Standards/Interfacers/Swiger/CTool.h"
#include <map>
#include <iostream>
#include <cstdlib>
#include <iostream>
#include <cstdio>
#include <math.h>
#include <string>
#include <vector>

typedef struct DOUBLECOMPLEX { double r, i; } doublecomplex;


class CIntegrateAndFireTransferFunctionClass : public CToolClass
{
	public:

		/*
		double JEE,JEI,JIE,JII;
		double taumE,taumI;
		double tauLEE,tauLEI,tauLIE,tauLII;
		double tauLEE,tauREI,tauRIE,tauRII;
		double tauDEE,tauDEI,tauDIE,tauDII;
		*/

		/*** COMPUTE METHODS ***/

		/*** CONSTRUCTOR ***/
		CIntegrateAndFireTransferFunctionClass();
		
		/*** INTEGRALS BOUNDARIES***/
		void computeIntegralUpperBound();
		void computeIntegralLowerBound();
		
		/*** GET METHODS ***/
		
		/*** STATIONARY RATES ****/
		double getErrorFunction(double z);
		double getLifStationaryRate();
		
		/*** LINEAR PERTURBATIONS ***/
		/*
		doublecomplex new_Synapse(
			doublecomplex lambda,
			double tauL,
			double tauR,
			double tauD
		);
		doublecomplex new_gsurg(
			doublecomplex xx,
			doublecomplex yy
		); 
		void new_onefone(
			doublecomplex a, 
			doublecomplex c, 
			doublecomplex z, 
			doublecomplex *series, 
			doublecomplex *deriv
		);
		void new_correctionlargey(
			doublecomplex a, 
			doublecomplex c, 
			doublecomplex z, 
			doublecomplex *series
		);
		void new_u01(
			doublecomplex omc, 
			double y, 
			doublecomplex *seriesu, 
			int *indic
		);
		void new_u23(
			doublecomplex omc, double y, doublecomplex *seriesu, int *indic
		);
		doublecomplex Neuron(doublecomplex lambda);
		*/
		doublecomplex old_gsurg(doublecomplex xx,doublecomplex yy);
		void old_onefone(doublecomplex a, doublecomplex c, 
			doublecomplex z, doublecomplex *series, doublecomplex *deriv); 
		void old_correctionlargey(doublecomplex a, 
			doublecomplex c, doublecomplex z, doublecomplex *series); 
		void old_u01(
			double omc, double y, doublecomplex *seriesu, int *indic
		);
		void old_u23(
			double omc, double y, doublecomplex *seriesu, int *indic
		);
		//doublecomplex Y(doublecomplex lambda);
		doublecomplex RLIF(double _omega,int i); 
		doublecomplex Complex(double re, double im); //defined in inline functions
		doublecomplex Cadd(doublecomplex a, doublecomplex b); //defined in inline functions
		doublecomplex Csub(doublecomplex a, doublecomplex b); //defined in inline functions
		doublecomplex Cmul(doublecomplex a, doublecomplex b); //defined in inline functions
		doublecomplex Cdiv(doublecomplex a, doublecomplex b); //defined in inline functions
		doublecomplex Conjg(doublecomplex z); //defined in inline functions
		doublecomplex Csqrt(doublecomplex z); //defined in inline functions
		std::complex<double> myCsqrt(std::complex<double> z);
		doublecomplex Cexp(doublecomplex a); //defined in inline functions
		doublecomplex RCmul(double x, doublecomplex a); //defined in inline functions
		double Cabs(doublecomplex z); //defined in inline functions
		double Carg(doublecomplex z); //defined in inline functions

		/*** Lif perturbation at zero frequency***/
		double getLifPerturbationNullRate(std::string DiffVariable);
		
		/*** Brunel Methods ***/
		std::complex<double> gsurg(std::complex<double> xx,std::complex<double> yy);
		void onefone(std::complex<double> a, std::complex<double> c, std::complex<double> z, std::complex<double> *series, std::complex<double> *deriv);
		void correctionlargey(std::complex<double> a, std::complex<double> c, std::complex<double> z, std::complex<double> *series); 
		void u01(std::complex<double> omc, double y, std::complex<double> *seriesu, int *indic);
		void u23(std::complex<double> omc, double y, std::complex<double> *seriesu, int *indic);
		void setBrunelLifPerturbationRate(std::complex<double> lambda);
		
		/*** Hakim Ostojic Methods ***/
		double inside_integ(double x);
		void (CIntegrateAndFireTransferFunctionClass::*deriv)(double, std::vector<std::complex<double> >&, std::vector<std::complex<double> >&, std::complex<double>);//pointer to functions like derivs
		void phi_derivs(double y, std::vector<std::complex<double> >& phi, std::vector<std::complex<double> >& dphi, std::complex<double> lamda);
		void phi_t_derivs(double y, std::vector<std::complex<double> >& phi, std::vector<std::complex<double> >& dphi, std::complex<double> lamda);
		void rkck(std::vector<std::complex<double> > y, std::vector<std::complex<double> > dydx, double x,  double h, std::vector<std::complex<double> >& yout, std::vector<std::complex<double> >& yerr, std::complex<double> lamda, void (CIntegrateAndFireTransferFunctionClass::*derivs)(double, std::vector<std::complex<double> >&, std::vector<std::complex<double> >&, std::complex<double> ));
		void rkqs(std::vector<std::complex<double> >& y, std::vector<std::complex<double> > dydx,  double& x, const double htry, const double eps, const std::vector<double>& yscal, double& hdid, double& hnext, std::complex<double> lamda, void (CIntegrateAndFireTransferFunctionClass::* derivs)(double, std::vector<std::complex<double> >&, std::vector<std::complex<double> >&, std::complex<double> ));
		double odeint(std::vector<std::complex<double> >& ystart, const double x1, const double x2, const double eps, const double h1,  const double hmin, std::complex<double> lamda,
						void (CIntegrateAndFireTransferFunctionClass::*derivs)(double, std::vector<std::complex<double> >&, std::vector<std::complex<double> >&, std::complex<double>));
		std::complex<double> phi_t_rka(double y, std::complex<double> lamda, std::complex<double>& phi_pr);
		void setHakimLifPerturbationRate(std::complex<double> lamda);
		

};



#endif



