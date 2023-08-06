#ifndef CIntegrateAndFireTransferFunction_CPP
#define CIntegrateAndFireTransferFunction_CPP
#include "CIntegrateAndFireTransferFunction.h"
#include "../../../Standards/Interfacers/Swiger/CTool.h"
#include <map>
#include <array>
#include <complex>
#include <vector>
#include <string>
#include <stdio.h>
#include <iostream>


#define ONE Complex(1.0e0,0.0e0)
#define TWO Complex(2.0e0,0.0e0)
#define HALF Complex(0.5e0,0.0e0)

const double PSHRNK=-0.25;
const double PGROW=-0.2;
const double SAFETY=0.9;
const double ERRCON=1.89e-4;
const int MAXSTP=10000;
const double TINY=1e-30;
const double EPS=0.000001;
const double a1=  -1.26551223;
const double a2=  1.00002368;
const double a3=  .37409196;
const double a4=  .09678418;
const double a5=  -.18628806;
const double a6=  .27886087;
const double a7=  -1.13520398;
const double a8= 1.48851587;
const double a9= -.82215223;
const double a10= .17087277;
const double SQPI=sqrt(4.0e0*atan(1.0e0));
const double TWOPI=8.*atan(1.);
using namespace std;


/******************************************************/
/***************ZERO ORDER DYNAMIC*********************/


/***CONSTRUCTORS***/
CIntegrateAndFireTransferFunctionClass::CIntegrateAndFireTransferFunctionClass()
{
	//DoubleDict["ConstantTime"]=0.02;
	//DoubleDict["RefractoryPeriod"]=0.;
	//DoubleDict["StationaryCurrent"]=-55.;
	//DoubleDict["VoltageNoise"]=5.;
	//DoubleDict["VoltageReset"]=-70.; 
	//DoubleDict["VoltageThreshold"]=-50.;
	//DoubleDict["StationaryRate"]=0.;
	IntDict["ComputeStationary"]=1;
	IntDict["IsStationary"]=1;
}


/*** compute upper and lower bounds of the integrals***/
void CIntegrateAndFireTransferFunctionClass::computeIntegralUpperBound()
{

	//print
	/*
	cout<<"StationaryCurrent is "<<DoubleDict["StationaryCurrent"]<<endl;
	cout<<"VoltageNoise is "<<DoubleDict["VoltageNoise"]<<endl;
	cout<<endl;
	*/

	//compute
	DoubleDict["IntegralUpperBound"]=(
		DoubleDict["VoltageThreshold"]-DoubleDict["StationaryCurrent"]
	)/DoubleDict["VoltageNoise"];
}
void CIntegrateAndFireTransferFunctionClass::computeIntegralLowerBound()
{
	DoubleDict["IntegralLowerBound"]=(
		DoubleDict["VoltageReset"]-DoubleDict["StationaryCurrent"]
	)/DoubleDict["VoltageNoise"];
}


/*** compute erf function***/
double CIntegrateAndFireTransferFunctionClass::getErrorFunction(double z)
{
	static double t,ef,at;
	static double w;
	w = fabs(z);
	t = 1.0e0/(1.0e0 + 0.5e0 * w);
	at=a1+t*(a2+t*(a3+t*(a4+t*(a5+t*(a6+t*(a7+t*(a8+t*(a9+t*a10))))))));
	ef=t*exp(at);
	if(z>0.0e0)
	ef = 2.0e0*exp(w*w)-ef;  
	return(ef);
}



/***Lif static transduction function***/
double CIntegrateAndFireTransferFunctionClass::getLifStationaryRate()
{
	static double w,z,cont,ylow,intuppbound,intlowbound;
 	static int i,N;
	
	if(DoubleDict["VoltageNoise"]>0.)
	{

		//set
		intuppbound=DoubleDict["IntegralUpperBound"];
		intlowbound=DoubleDict["IntegralLowerBound"];

		N=10000;

		//algorithm integration
		w=0.;

		//Check
		if(intuppbound<-100.&&intlowbound<-100.) 
		{
			w=log(intlowbound/intuppbound
				)-0.25/pow(intuppbound,2.)+0.25/pow(
				intlowbound,2.
			);
			w=1./(DoubleDict["RefractoryPeriod"]+DoubleDict["ConstantTime"]*w);
		}
		else if(intlowbound<-100.) 
		{
			ylow=-100.; 
			N=(int)(100.*(intuppbound-ylow));
			for(i=0;i<=N;i++) 
			{
				z=ylow+(intuppbound-ylow)*(double)(i)/(double)(N);
				cont=getErrorFunction(z);
				if(i==0||i==N) {w+=0.5*cont;}
				else {w+=cont;}
			}
			w*=(intuppbound-ylow)*SQPI/(double)(N);
			w+=log(-intlowbound/100.)-0.000025+0.25/pow(intlowbound,2.);
			w=1./(DoubleDict["RefractoryPeriod"]+DoubleDict["ConstantTime"]*w);
		}	
		else 
		{
			ylow=intlowbound;
			N=(int)(100.*(intuppbound-ylow));
			for(i=0;i<=N;i++) 
			{
				z=ylow+(intuppbound-ylow)*(double)(i)/(double)(N);
				cont=getErrorFunction(z);
				if(i==0||i==N){w+=0.5*cont;}
				else{w+=cont;}
			}
			w*=(intuppbound-ylow)*SQPI/(double)(N);
			w=1./(DoubleDict["RefractoryPeriod"]+DoubleDict["ConstantTime"]*w);
		}
	}
	else
	{
		//zero noise case
		if(DoubleDict["StationaryCurrent"]>DoubleDict["VoltageThreshold"])
		{
			return 1./(DoubleDict["RefractoryPeriod"]+DoubleDict["ConstantTime"]*log(
				(DoubleDict["VoltageReset"]-DoubleDict["StationaryCurrent"]
			)/(DoubleDict["VoltageThreshold"]-DoubleDict["StationaryCurrent"])));
		}
		else
		{
			return 0.;
		}
	}
	
	//set
	if(IntDict["IsStationary"]==1){
		DoubleDict["StationaryRate"]=w;
	}

	//return
	return w;
}



/******************************************************/
/***************FIRST ORDER DYNAMIC*********************/

/***Lif Linear Perturbative Transfer Function at zero frequency***/
double CIntegrateAndFireTransferFunctionClass::getLifPerturbationNullRate(
		std::string DiffVariable="StationaryCurrent"
	)
{
	std::map<std::string,double> OutputDict;
	static double DeltaVariable,Variable,DeltaFunction,PerturbationNullRate;
	DeltaVariable=0.01;
	
	//Check
	IntDict["IsStationary"]=false;

	//temp
	Variable=DoubleDict[DiffVariable];
	
	//compute forward
	DoubleDict[DiffVariable]+=DeltaVariable;
	computeIntegralUpperBound();
	computeIntegralLowerBound();
	DeltaFunction=getLifStationaryRate();

	//compute just behind
	DoubleDict[DiffVariable]-=2.*DeltaVariable;
	computeIntegralUpperBound();
	computeIntegralLowerBound();
	DeltaFunction-=getLifStationaryRate();

	//compute
	PerturbationNullRate=DeltaFunction/(2.*DeltaVariable);

	//reset
	DoubleDict[DiffVariable]=Variable;
	computeIntegralUpperBound();
	computeIntegralLowerBound();
	
	//Check
	IntDict["IsStationary"]=true;

	/**** return OutputDict***/
	return PerturbationNullRate;
}

/***Brunel methods****/

/**** synaptic dynamic response *****/

/*
doublecomplex CIntegrateAndFireTransferFunctionClass::new_Synapse(doublecomplex lambda,double tauL,double tauR,double tauD) {
  return(Cdiv(Cexp(RCmul(-tauL,lambda)),Cmul(Cadd(ONE,RCmul(tauR,lambda)),Cadd(ONE,RCmul(tauD,lambda)))));
}
*/

/**** routines for neuronal response *****/

/*
doublecomplex CIntegrateAndFireTransferFunctionClass::new_gsurg(doublecomplex xx,doublecomplex yy) {
  static double cof[6]={76.18009172947146,-86.50532032941677,24.01409824083091,-1.231739572450155,0.1208650973866179e-2,-0.5395239384953e-5};
  int j;
  doublecomplex xdemi,xxx,xgdemi,ydemi,ygdemi,yyy,expx,expy,ser,roro,nano,rano;

  if(xx.r<=0.) {xdemi=Cadd(xx,Complex(1.5,0.0));
  xgdemi=Cadd(xx,Complex(6.5,0.0));
  xxx=Cadd(xx,Complex(2.,0.0));
  }
  else if(xx.r<=1.) {xdemi=Cadd(xx,Complex(0.5,0.0));
  xgdemi=Cadd(xx,Complex(5.5,0.0));
  xxx=Cadd(xx,Complex(1.,0.0));	}
  else {xdemi=Cadd(xx,Complex(-0.5,0.0));
  xgdemi=Cadd(xx,Complex(4.5,0.0));
  xxx=xx;
  }
  if(yy.r<=0.) {ydemi=Cadd(yy,Complex(1.5,0.0));
  ygdemi=Cadd(yy,Complex(6.5,0.0));
  yyy=Cadd(yy,Complex(2.,0.0));
  }
  else if(yy.r<=1.) {ydemi=Cadd(yy,Complex(0.5,0.0));
  ygdemi=Cadd(yy,Complex(5.5,0.0));
  yyy=Cadd(yy,Complex(1.0,0.0));	}
  else {ydemi=Cadd(yy,Complex(-0.5,0.0));
  ygdemi=Cadd(yy,Complex(4.5,0.0));		
  yyy=yy;
  }
  expx.r=log(Cabs(xgdemi));expx.i=asin(xx.i/Cabs(xgdemi));
  expy.r=log(Cabs(ygdemi));expy.i=asin(yy.i/Cabs(ygdemi));
  roro=Cmul(expx,xdemi);
  roro=Csub(roro,xgdemi);
  roro=Csub(roro,Cmul(expy,ydemi));
  roro=Cadd(roro,ygdemi);	
  nano.r=exp(roro.r)*cos(roro.i);
  nano.i=exp(roro.r)*sin(roro.i);
  ser=Complex(1.000000000190015,0.0);
  for (j=0;j<=5;j++) {
    ser=Cadd(ser,RCmul(cof[j],Cdiv(ONE,xxx)));
    xxx=Cadd(xxx,ONE);
  }
  rano=ser;
  ser=Complex(1.000000000190015,0.0);
  for (j=0;j<=5;j++) {
    ser=Cadd(ser,RCmul(cof[j],Cdiv(ONE,yyy)));
    yyy=Cadd(yyy,ONE);
  }
  rano=Cdiv(rano,ser);
  nano=Cmul(nano,rano);
  if(xx.r<=0.0) nano=Cdiv(nano,Cmul(xx,Cadd(ONE,xx)));
  else if(xx.r<=1.0) nano=Cdiv(nano,xx);
  if(yy.r<=0.0) nano=Cmul(nano,Cmul(yy,Cadd(ONE,yy)));
  else if(yy.r<=1.0) nano=Cmul(nano,yy);
  return(nano);
}

void CIntegrateAndFireTransferFunctionClass::new_onefone(doublecomplex a, doublecomplex c, doublecomplex z, doublecomplex *series, doublecomplex *deriv) {
  int n;
  doublecomplex aa,bb,cc,fac,temp;

  deriv->r=0.0e0;
  deriv->i=0.0e0;
  fac=Complex(1.0e0,0.0e0);
  temp=fac;
  aa=a;
  cc=c;
  for (n=1;n<=10000;n++) {
    fac=Cmul(fac,Cdiv(aa,cc));
    deriv->r+=fac.r;
    deriv->i+=fac.i;
    fac=Cmul(fac,RCmul(1.0e0/n,z));
    *series=Cadd(temp,fac);
    if (series->r == temp.r && series->i == temp.i) return;
    temp= *series;
    aa=Cadd(aa,ONE);
    cc=Cadd(cc,ONE);
  }
}

void CIntegrateAndFireTransferFunctionClass::new_correctionlargey(doublecomplex a, doublecomplex c, doublecomplex z, doublecomplex *series) {
  int n;
  doublecomplex aa,bb,cc,fac,temp;

  temp=ONE;
  fac=ONE;
  aa=a;
  cc=Csub(Cadd(a,ONE),c);
  for(n=1;n<=10;n++) {
    fac=Cmul(fac,Cmul(aa,cc));
    fac=Cdiv(fac,RCmul(-n,z));
    *series=Cadd(temp,fac);
    if (series->r == temp.r && series->i == temp.i) return;
    temp=*series;
    aa=Cadd(aa,ONE);
    cc=Cadd(cc,ONE);
    //printf("%d %f %f\n",n,temp.r,temp.i);
  }
}

void  CIntegrateAndFireTransferFunctionClass::new_u01(doublecomplex lm, double y, doublecomplex *seriesu, int *indic) {
  doublecomplex ah,sqom,series,deriv,asymptoty,asymptotom,ut;
  double alpha;

  ah=RCmul(0.5,lm);
  sqom=RCmul(sqrt(2.),Csqrt(lm));
  
  if(Cabs(lm)<10.5 && y>-3.5) { 
    *indic=1;
    new_onefone(ah,HALF,Complex(y*y,0.),&series,&deriv);
    ut=RCmul(0.5,Cmul(series,gsurg(ah,Cadd(HALF,ah))));
    new_onefone(Cadd(HALF,ah),Cadd(ONE,HALF),Complex(y*y,0.),&series,&deriv);
    ut=Cadd(ut,RCmul(y,series));
    ut=RCmul(2.*SQPI,Cdiv(ut,gsurg(ah,ONE)));
    *seriesu=ut;
  }
  else {
    if(y<-3.5-0.15*(Cabs(lm)-10.5)) {
      asymptoty=RCmul(pow(fabs(y),lm.r),Complex(cos(lm.i*log(fabs(y))),-sin(lm.i*log(fabs(y)))));
      new_correctionlargey(ah,HALF,Complex(y*y,0.),&series);
      asymptoty=Cmul(asymptoty,series);
    }
    if(y>-3.5-0.25*(Cabs(lm)-10.5)) { 
      asymptotom=RCmul(y,sqom);
      asymptotom=Cadd(asymptotom,RCmul(pow(y,3)/6.-y/2.,Cdiv(ONE,sqom)));
      asymptotom=Cadd(asymptotom,RCmul(-0.24*pow(y,2),Cdiv(ONE,Cmul(sqom,sqom))));
      asymptotom=Cadd(asymptotom,RCmul(-pow(y,5)/40.+pow(y,3)/12.+y/8.,Cdiv(ONE,Cmul(Cmul(sqom,sqom),sqom))));
      asymptotom=Cadd(asymptotom,RCmul(pow(y,4)/8.-pow(y,2)/4.,Cdiv(ONE,Cmul(Cmul(sqom,sqom),Cmul(sqom,sqom)))));
      asymptotom=RCmul(SQPI*exp(0.5*y*y),Cexp(asymptotom));
      asymptotom=Cdiv(asymptotom,gsurg(Cadd(HALF,ah),ONE));
    }
    if(y<-3.5-0.25*(Cabs(lm)-10.5)) {
      *indic=2;
      *seriesu=asymptoty;
    }
    else if(y>-3.5-0.15*(Cabs(lm)-10.5)) { 
      *indic=3;
      *seriesu=asymptotom;
    }
    else {
      *indic=4;
      alpha=-((y+3.5)/(Cabs(lm)-10.5)+0.15)/0.1;
      *seriesu=Cadd(RCmul(alpha,asymptoty),RCmul(1.-alpha,asymptotom));
    }
  }
}

void  CIntegrateAndFireTransferFunctionClass::new_u23(doublecomplex lm, double y, doublecomplex *seriesu, int *indic) { 
  doublecomplex ah,sqom,series,deriv,asymptoty,asymptotom,ut,prefac;
  double alpha;

  ah=RCmul(0.5,lm);
  sqom=RCmul(sqrt(2.),Csqrt(lm));
  
  if(Cabs(lm)<10.5 && y>-3.5) {
    *indic=1;
    new_onefone(Cadd(ONE,ah),Cadd(HALF,ONE),Complex(y*y,0.),&series,&deriv);
    ut=Cmul(RCmul(y,lm),Cmul(series,gsurg(ah,Cadd(HALF,ah))));
    new_onefone(Cadd(HALF,ah),HALF,Complex(y*y,0.),&series,&deriv);
    ut=Cadd(ut,series);
    ut=RCmul(2.*SQPI,Cdiv(ut,gsurg(ah,ONE)));
    *seriesu=ut;
  }
  else {
    if(y<-3.5-0.15*(Cabs(lm)-10.5)) { 
      asymptoty=RCmul(pow(fabs(y),lm.r),Complex(cos(lm.i*log(fabs(y)))/fabs(y),-sin(lm.i*log(fabs(y)))/fabs(y)));
      new_correctionlargey(Cadd(ah,ONE),Cadd(HALF,ONE),Complex(y*y,0.),&series);
      asymptoty=Cmul(asymptoty,series);
      asymptoty=Cmul(asymptoty,lm);
    }
    if(y>-3.5-0.25*(Cabs(lm)-10.5)) {
      asymptotom=RCmul(y,sqom);
      asymptotom=Cadd(asymptotom,RCmul(pow(y,3)/6.-y/2.,Cdiv(ONE,sqom)));
      asymptotom=Cadd(asymptotom,RCmul(-0.24*pow(y,2),Cdiv(ONE,Cmul(sqom,sqom))));
      asymptotom=Cadd(asymptotom,RCmul(-pow(y,5)/40.+pow(y,3)/12.+y/8.,Cdiv(ONE,Cmul(Cmul(sqom,sqom),sqom))));
      asymptotom=Cadd(asymptotom,RCmul(pow(y,4)/8.-pow(y,2)/4.,Cdiv(ONE,Cmul(Cmul(sqom,sqom),Cmul(sqom,sqom)))));
      asymptotom=RCmul(SQPI*exp(0.5*y*y),Cexp(asymptotom));
      prefac=Cadd(sqom,Complex(y,0.));
      prefac=Cadd(prefac,RCmul(0.5*y*y-0.5,Cdiv(ONE,sqom)));
      prefac=Cadd(prefac,RCmul(-0.48*y,Cdiv(ONE,Cmul(sqom,sqom))));
      prefac=Cadd(prefac,RCmul(-pow(y,4)/8.+pow(y,2)/4.+1./8.,Cdiv(ONE,Cmul(Cmul(sqom,sqom),sqom))));
      prefac=Cadd(prefac,RCmul(pow(y,3)/2.-y/2.,Cdiv(ONE,Cmul(Cmul(sqom,sqom),Cmul(sqom,sqom)))));
      asymptotom=Cdiv(Cmul(prefac,asymptotom),gsurg(Cadd(HALF,ah),ONE));
    }
    if(y<-3.5-0.25*(Cabs(lm)-10.5)) { 
      *indic=2;
      *seriesu=asymptoty;
    }
    else if(y>-3.5-0.15*(Cabs(lm)-10.5)) {
      *indic=3;
      *seriesu=asymptotom;
    }
    else { 
      *indic=4;
      alpha=-((y+3.5)/(Cabs(lm)-10.5)+0.15)/0.1;
      *seriesu=Cadd(RCmul(alpha,asymptoty),RCmul(1.-alpha,asymptotom));
    }
  }
}
*/
/**** neural response *****/

/*
doublecomplex CIntegrateAndFireTransferFunctionClass::Neuron(doublecomplex lambda) {
  doublecomplex series,deriv,numerator,denominator;
  doublecomplex assresp,assnum,assden;
  doublecomplex asymptot,asymptoh;
  doublecomplex ut,uh;
  int indicator,indict,indich,iter;
  double thetatil,hvrtil;
  doublecomplex lm;

  //set
  thetatil=DoubleDict["IntegralUpperBound"];
  hvrtil=DoubleDict["IntegralLowerBound"];
  lm=RCmul(DoubleDict["ConstantTime"],lambda);

  new_u01(lm,thetatil,&series,&indicator);
  ut=series;
  indict=indicator;
  new_u01(lm,hvrtil,&series,&indicator);
  uh=series;
  indich=indicator;
  denominator=Csub(ut,uh);
  // printf("u01t %.3f %.3f u01r %.3f %.3f %d %d\n",ut.r,ut.i,uh.r,uh.i,indict,indich); 

  new_u23(lm,thetatil,&series,&indicator);
  ut=series;
  indict=indicator;
  new_u23(lm,hvrtil,&series,&indicator);
  uh=series;
  indich=indicator;
  numerator=Csub(ut,uh);
  // printf("u23t %.3f %.3f u23r %.3f %.3f %d%d\n",ut.r,ut.i,uh.r,uh.i,indict,indich); 

  return(RCmul(DoubleDict["StationaryRate"]/DoubleDict["VoltageNoise"],Cdiv(numerator,Cmul(Cadd(lm,ONE),denominator))));
}

*/

/***all complex function to compute RLIF***/
doublecomplex CIntegrateAndFireTransferFunctionClass::old_gsurg(doublecomplex xx,doublecomplex yy) 
{	
	static double cof[6]={76.18009172947146,-86.50532032941677,24.01409824083091,-1.231739572450155,0.1208650973866179e-2,-0.5395239384953e-5};
	static int j;
  	static doublecomplex xdemi,xxx,xgdemi,ydemi,ygdemi,yyy,expx,expy,ser,roro,nano,rano;
	if(xx.r<=0.) 
	{
		xdemi=Cadd(xx,Complex(1.5,0.0));
		xgdemi=Cadd(xx,Complex(6.5,0.0));
		xxx=Cadd(xx,Complex(2.,0.0));
	}
	else if(xx.r<=1.) 
	{
		xdemi=Cadd(xx,Complex(0.5,0.0));
		xgdemi=Cadd(xx,Complex(5.5,0.0));
		xxx=Cadd(xx,Complex(1.,0.0));	
	}
	else 
	{
		xdemi=Cadd(xx,Complex(-0.5,0.0));
		xgdemi=Cadd(xx,Complex(4.5,0.0));
		xxx=xx;
	}
	if(yy.r<=0.) 
	{
		ydemi=Cadd(yy,Complex(1.5,0.0));
		ygdemi=Cadd(yy,Complex(6.5,0.0));
		yyy=Cadd(yy,Complex(2.,0.0));
	}
	else if(yy.r<=1.) 
	{
		ydemi=Cadd(yy,Complex(0.5,0.0));
		ygdemi=Cadd(yy,Complex(5.5,0.0));
		yyy=Cadd(yy,Complex(1.0,0.0));	
	}
	else 
	{
		ydemi=Cadd(yy,Complex(-0.5,0.0));
		ygdemi=Cadd(yy,Complex(4.5,0.0));		
		yyy=yy;
	}
	expx.r=log(Cabs(xgdemi));
	expx.i=asin(xx.i/Cabs(xgdemi));
	expy.r=log(Cabs(ygdemi));
	expy.i=asin(yy.i/Cabs(ygdemi));
	roro=Cmul(expx,xdemi);
	roro=Csub(roro,xgdemi);
	roro=Csub(roro,Cmul(expy,ydemi));
	roro=Cadd(roro,ygdemi);	
	nano.r=exp(roro.r)*cos(roro.i);
	nano.i=exp(roro.r)*sin(roro.i);
	ser=Complex(1.000000000190015,0.0);
	for (j=0;j<=5;j++) 
	{
		ser=Cadd(ser,RCmul(cof[j],Cdiv(ONE,xxx)));
		xxx=Cadd(xxx,ONE);
	}
	rano=ser;
	ser=Complex(1.000000000190015,0.0);
	for (j=0;j<=5;j++) 
	{
		ser=Cadd(ser,RCmul(cof[j],Cdiv(ONE,yyy)));
		yyy=Cadd(yyy,ONE);
	}
	rano=Cdiv(rano,ser);
	nano=Cmul(nano,rano);
	if(xx.r<=0.0) nano=Cdiv(nano,Cmul(xx,Cadd(ONE,xx)));
	else if(xx.r<=1.0) nano=Cdiv(nano,xx);
	if(yy.r<=0.0) nano=Cmul(nano,Cmul(yy,Cadd(ONE,yy)));
	else if(yy.r<=1.0) nano=Cmul(nano,yy);
	return(nano);
}


/***all complex function to compute RLif***/
std::complex<double> CIntegrateAndFireTransferFunctionClass::gsurg(std::complex<double> xx,std::complex<double> yy) 
{	
	static double cof[6]={
    76.18009172947146,
    -86.50532032941677,
    24.01409824083091,
    -1.231739572450155,
    0.1208650973866179e-2,
    -0.5395239384953e-5};
	static int j;
  static std::complex<double> xdemi,xxx,xgdemi,ydemi,ygdemi,yyy,expx,expy,ser,roro,nano,rano;
	
  //Debug
  /*
  cout<<"Erwan gsurg "<<endl;
  cout<<"xx is "<<xx.real()<<" "<<xx.imag()<<endl;
  cout<<"yy is "<<yy.real()<<" "<<yy.imag()<<endl;
  cout<<endl;
  */

  //Check
  if(xx.real()<=0.)
	{
		xdemi=xx+std::complex<double>(1.5,0.0);
		xgdemi=xx+std::complex<double>(6.5,0.0);
		xxx=xx+std::complex<double>(2.,0.0);
	}
	else if(xx.real()<=1.) 
	{
		xdemi=xx+std::complex<double>(0.5,0.0);
		xgdemi=xx+std::complex<double>(5.5,0.0);
		xxx=xx+std::complex<double>(1.,0.0);
	}
	else 
	{
		xdemi=xx+std::complex<double>(-0.5,0.0);
		xgdemi=xx+std::complex<double>(4.5,0.0);
		xxx=xx;
	}
	if(yy.real()<=0.)
	{
		ydemi=yy+std::complex<double>(1.5,0.0);
		ygdemi=yy+std::complex<double>(6.5,0.0);
		yyy=yy+std::complex<double>(2.,0.0);
	}
	else if(yy.real()<=1.)
	{
		ydemi=yy+std::complex<double>(0.5,0.0);
		ygdemi=yy+std::complex<double>(5.5,0.0);
		yyy=yy+std::complex<double>(1.0,0.0);
	}
	else 
	{
		ydemi=yy+std::complex<double>(-0.5,0.0);
		ygdemi=yy+std::complex<double>(4.5,0.0);
		yyy=yy;
	}
	expx=std::complex<double>(log(abs(xgdemi)),asin(xx.imag()/abs(xgdemi)));
	expy=std::complex<double>(log(abs(ygdemi)),asin(yy.imag()/abs(ygdemi)));
	roro=expx*xdemi-xgdemi-(expy*ydemi)+ygdemi;

  //Debug
  /*
  cout<<"Erwan gsurg "<<endl;
  cout<<"roro is "<<roro.real()<<" "<<roro.imag()<<endl;
  cout<<endl;
  */

	nano=std::complex<double>(
    exp(roro.real())*cos(roro.imag()),
    exp(roro.real())*sin(roro.imag())
  );

  //Debug
  /*
  cout<<"Erwan gsurg "<<endl;
  cout<<"nano is "<<nano.real()<<" "<<nano.imag()<<endl;
  cout<<endl;
  */

  //
	ser=std::complex<double>(1.000000000190015,0.0);
	for (j=0;j<=5;j++) 
	{
		ser+=(cof[j]*(1./xxx));
		xxx+=1.;
	}
	rano=ser;
	ser=std::complex<double>(1.000000000190015,0.0);
	for (j=0;j<=5;j++) 
	{
		ser+=(cof[j]*(1./yyy));
		yyy+=1.;
	}
	rano/=ser;
	nano*=rano;
	if(xx.real()<=0.0) nano/=(xx*(1.+xx));
	else if(xx.real()<=1.0) nano/=xx;
	if(yy.real()<=0.0) nano*=(yy*(1.+yy));
	else if(yy.real()<=1.0) nano*=yy;
	return(nano);
}


void CIntegrateAndFireTransferFunctionClass::old_onefone(doublecomplex a, doublecomplex c, doublecomplex z, doublecomplex *series, doublecomplex *deriv) 
{	
	static int n;
 	static doublecomplex aa,cc,fac,temp;
	deriv->r=0.0e0;
	deriv->i=0.0e0;
	fac=Complex(1.0e0,0.0e0);
	temp=fac;	
	aa=a;
	cc=c;
	for (n=1;n<=10000;n++) 
	{
		fac=Cmul(fac,Cdiv(aa,cc));
		deriv->r+=fac.r;
		deriv->i+=fac.i;
		fac=Cmul(fac,RCmul(1.0e0/n,z));
		*series=Cadd(temp,fac);
		if (series->r == temp.r && series->i == temp.i) return;
		temp= *series;
		aa=Cadd(aa,ONE);
		cc=Cadd(cc,ONE);
	}
}

void CIntegrateAndFireTransferFunctionClass::onefone(
	std::complex<double> a, 
	std::complex<double> c, 
	std::complex<double> z, 
	std::complex<double> *series, 
	std::complex<double> *deriv
) 
{	
	static int n;
 	static std::complex<double> aa,cc,fac,temp;
	(*deriv)=std::complex<double>(0.0e0,0.0e0);
	fac=std::complex<double>(1.0e0,0.0e0);
	temp=fac;	
	aa=a;
	cc=c;
	for (n=1;n<=10000;n++) 
	{
		fac*=(aa/cc);
		(*deriv)=std::complex<double>(fac.real(),fac.imag());
		fac*=(1.0e0/n)*z;
		*series=temp+fac;
		if ((*series).real() == temp.real() && (*series).imag() == temp.imag()) return;
		temp= *series;
		aa+=1.;
		cc+=1.;
	}
}


void CIntegrateAndFireTransferFunctionClass::old_correctionlargey(doublecomplex a, doublecomplex c, doublecomplex z, doublecomplex *series) 
{
	static int n;
 	static doublecomplex aa,cc,fac,temp;
	temp=ONE;
	fac=ONE;
	aa=a;
	cc=Csub(Cadd(a,ONE),c);
	for(n=1;n<=10;n++) 
	{
		fac=Cmul(fac,Cmul(aa,cc));
		fac=Cdiv(fac,RCmul(-n,z));
		*series=Cadd(temp,fac);
		if (series->r == temp.r && series->i == temp.i) return;
		temp=*series;
		aa=Cadd(aa,ONE);
		cc=Cadd(cc,ONE);
	}
}

void CIntegrateAndFireTransferFunctionClass::correctionlargey(std::complex<double> a, std::complex<double> c, std::complex<double> z, std::complex<double> *series) 
{
	static int n;
 	static std::complex<double> aa,cc,fac,temp;
	temp=1.;
	fac=1.;
	aa=a;
	cc=(a+1.)-c;
	for(n=1;n<=10;n++) 
	{
		fac*=aa*cc;
		fac/=((-(double)(n))*z);
		*series=temp+fac;
		if ((*series).real() == temp.real() && (*series).imag() == temp.imag()) return;
		temp=*series;
		aa+=1.;
		cc+=1.;
	}
}

void CIntegrateAndFireTransferFunctionClass::old_u01(double omc, double y, doublecomplex *seriesu, int *indic) 
{	
	static doublecomplex ah,sqom,series,deriv,asymptoty,asymptotom,ut;
  	static double alpha;
	ah=Complex(0.,0.5*omc);
	

	//Debug
	/*
	cout<<"Old BRUNEL u01 omc "<<omc<<endl;
	cout<<"ah is "<<ah.r<<" "<<ah.i<<endl;
	cout<<"y is "<<y<<endl;
	cout<<endl;
	*/

	//Check
	if(omc<10.5 && y>-3.5) 
	{

		//Debug
		/*
		cout<<"old BRUNEL u01"<<endl;
		cout<<"We use normal series"<<endl;
		cout<<endl;
		*/

		*indic=1;
		old_onefone(ah,HALF,Complex(y*y,0.),&series,&deriv);
		ut=RCmul(0.5,Cmul(series,old_gsurg(ah,Cadd(HALF,ah))));

		//Debug
		/*
		cout<<"BRUNEL u01 after first onefone"<<endl;
		cout<<"series is "<<series.r<<" "<<series.i<<endl,
		cout<<"ut is "<<ut.r<<" "<<ut.i<<endl;
		cout<<endl;
		*/

		//compute
		old_onefone(Cadd(HALF,ah),Cadd(ONE,HALF),Complex(y*y,0.),&series,&deriv);
		ut=Cadd(ut,RCmul(y,series));
		ut=RCmul(2.*SQPI,Cdiv(ut,old_gsurg(ah,ONE)));
		*seriesu=ut;
	}
	else 
	{
		if(y<-3.5-0.15*(omc-10.5)) 
		{ 
			//compute
			asymptoty=Complex(cos(omc*log(fabs(y))),-sin(omc*log(fabs(y))));

			//Debug
			/*
			cout<<"old BRUNEL u01 first part large y expansion"<<endl;
			cout<<"asymptoty is "<<asymptoty.r<<" "<<asymptoty.i<<endl,
			cout<<endl;
			*/

			//compute
			old_correctionlargey(ah,HALF,Complex(y*y,0.),&series);
			asymptoty=Cmul(asymptoty,series);

			//Debug
			/*
			cout<<"old BRUNEL u01 second part large y expansion"<<endl;
			cout<<"asymptoty is "<<asymptoty.r<<" "<<asymptoty.i<<endl,
			cout<<endl;
			*/

		}
		if(y>-3.5-0.25*(omc-10.5)) 
		{
			//set
			//sqom=RCmul(sqrt(2.),Complex(0.,omc));
			sqom=RCmul(sqrt(2.),Csqrt(Complex(0.,omc)));

			//Debug
			/*
			cout<<"old BRUNEL u01 large omega expansion "<<endl;
			cout<<"sqom is "<<sqom.r<<" "<<sqom.i<<endl;
			cout<<endl;
			*/
			
			//set
			asymptotom=RCmul(y,sqom);
			asymptotom=Cadd(asymptotom,RCmul(pow(y,3)/6.-y/2.,Cdiv(ONE,sqom)));
			asymptotom=Cadd(asymptotom,RCmul(-0.24*pow(y,2),Cdiv(ONE,Cmul(sqom,sqom))));
			asymptotom=Cadd(asymptotom,RCmul(-pow(y,5)/40.+pow(y,3)/12.+y/8.,Cdiv(ONE,Cmul(Cmul(sqom,sqom),sqom))));
			asymptotom=Cadd(asymptotom,RCmul(pow(y,4)/8.-pow(y,2)/4.,Cdiv(ONE,Cmul(Cmul(sqom,sqom),Cmul(sqom,sqom)))));
			asymptotom=RCmul(SQPI*exp(0.5*y*y),Cexp(asymptotom));
			asymptotom=Cdiv(asymptotom,old_gsurg(Cadd(HALF,ah),ONE));
		}
		if(y<-3.5-0.25*(omc-10.5)) 
		{
			*indic=2;
			*seriesu=asymptoty;
		}
		else if(y>-3.5-0.15*(omc-10.5)) 
		{ 
			*indic=3;
			*seriesu=asymptotom;
		}
		else { 
			*indic=4;
			alpha=-((y+3.5)/(omc-10.5)+0.15)/0.1;
			*seriesu=Cadd(RCmul(alpha,asymptoty),RCmul(1.-alpha,asymptotom));
		}
	}
}


void CIntegrateAndFireTransferFunctionClass::u01(
	std::complex<double> lmt, 
	double y, 
	std::complex<double> *seriesu, 
	int *indic
)
{	
	//define
	static std::complex<double> ah,_sqom,sqom,gsur,series,deriv,asymptoty,asymptotom,ut;
  	static double alpha;

  	//Debug
  	/*
  	cout<<"ERWAN u01 lmt is "<<lmt.real()<<" "<<lmt.imag()<<endl;
  	cout<<"y is "<<y<<" "<<endl;
  	cout<<endl;
	*/

  	//set
	//ah=getComplex(-0.5*lmt.imag(),0.5*lmt.real());
	ah=0.5*lmt;
	
	//Debug
	/*
	cout<<"ERWAN u01 lmt "<<lmt.real()<<" "<<lmt.imag()<<endl;
  cout<<"ah is "<<ah.real()<<" "<<ah.imag()<<endl;
  cout<<"y is "<<y<<endl;
  cout<<endl;
	*/

	//Check
	if(abs(lmt)<10.5 && y>-3.5)
	{
		//Debug
		/*
		cout<<"ERWAN u01"<<endl;
		cout<<"We use normal series"<<endl;
		cout<<endl;
		*/

		//onefone
		*indic=1;
		onefone(
				ah,
				0.5,
				std::complex<double>(y*y,0.),
				&series,
				&deriv
			);
		ut=0.5*series*gsurg(ah,0.5+ah);

		//Debug
		/*
		cout<<"ERWAN u01 after first onefone"<<endl;
		cout<<"series is "<<series.real()<<" "<<series.imag()<<endl,
		cout<<"ut is "<<ut.real()<<" "<<ut.imag()<<endl;
		cout<<endl;
		*/

		//onefone
		onefone(
					0.5+ah,
					1.+0.5,
					std::complex<double>(y*y,0.),
					&series,
					&deriv
				);
		ut+=(y*series);
		ut*=2.*SQPI/gsurg(ah,1.);

		//Debug
		/*
		cout<<"after second onefone"<<endl;
		cout<<"ut is "<<ut.real()<<" "<<ut.imag()<<endl;
		cout<<endl;
		*/

		//point
		*seriesu=ut;

	}
	else {


		if(y<-3.5-0.15*(abs(lmt)-10.5))
		{ 	

			/****** large y expansion *****/

			//asymptoty=Complex(cos(lmt*log(fabs(y))),-sin(lmt*log(fabs(y))));
			//asymptoty=exp(-getComplex(0.,1.)*log(fabs(y))*lmt);
			asymptoty=pow(
				fabs(y),lmt.real()
			)*getComplex(
				cos(lmt.imag()*log(fabs(y))),
				-sin(lmt.imag()*log(fabs(y)))
			);
			
			//Debug
			/*
			cout<<"ERWAN u01 first part large y expansion"<<endl;
			cout<<"asymptoty is "<<asymptoty.real()<<" "<<asymptoty.imag()<<endl,
			cout<<endl;
			*/

			//compute
			correctionlargey(ah,0.5,std::complex<double>(y*y,0.),&series);
			asymptoty*=series;

			//Debug
			/*
			cout<<"ERWAN u01 second part large y expansion"<<endl;
			cout<<"asymptoty is "<<asymptoty.real()<<" "<<asymptoty.imag()<<endl,
			cout<<endl;
			*/
		}
		if(y>-3.5-0.25*(abs(lmt)-10.5))
		{ 

			//Debug
			//cout<<"We use large omega expansion"<<endl;
			//cout<<endl;

			//set
			//sqom=getComplex(sqrt(abs(lmt)),sqrt(abs(lmt)));
			sqom=sqrt(2.)*myCsqrt(lmt);
			//sqom=getComplex(sqrt(abs(lmt)),sqrt(abs(lmt)));
			//sqom=sqrt(abs(lmt))*exp(getComplex(0.,arg(lmt)/2.));
			//sqom=_sqom+getComplex(0.,1.)*_sqom;

			//Debug
      /*
			cout<<"ERWAN u01 large omega expansion "<<endl;
			cout<<"sqom is "<<sqom.real()<<" "<<sqom.imag()<<endl;
			cout<<endl;
      */

			/******* large omega expansion *********/
			asymptotom=y*sqom;
			asymptotom+=(pow(y,3)/6.-y/2.)/sqom;
			asymptotom+=(-0.24*pow(y,2))/(sqom*sqom);
			asymptotom+=((-pow(y,5)/40.)+pow(y,3)/12.+y/8.)/(sqom*sqom*sqom);
			asymptotom+=((pow(y,4)/8.)-pow(y,2)/4.)/(sqom*sqom*sqom*sqom);
			asymptotom=SQPI*exp(0.5*y*y)*exp(asymptotom);
      gsur=gsurg(0.5+ah,1.);
      if(gsur==0.){
        gsur=std::complex<double>(exp(-99.),0.);
      }
			asymptotom/=gsur;

      //Debug
      /*
      cout<<"ERWAN u01 second large omega expansion "<<endl;
      cout<<"gsur is "<<gsur.real()<<" "<<gsur.imag()<<endl;
      cout<<endl;
      */

		}


		if(y<-3.5-0.25*(abs(lmt)-10.5))
		{ 
			/****** large y expansion *****/
			*indic=2;
			*seriesu=asymptoty;

      //Debug
      /*
      cout<<"ERWAN u01 large y last "<<endl;
      cout<<"asymptoty is "<<asymptoty.real()<<" "<<asymptoty.imag()<<endl;
      cout<<endl;
      */
		}
		else if(y>-3.5-0.15*(abs(lmt)-10.5))
		{
			 /******* large omega expansion *********/
			*indic=3;
			*seriesu=asymptotom;

      //Debug
      /*
      cout<<"ERWAN u01 large omega last "<<endl;
      cout<<"asymptotom is "<<asymptotom.real()<<" "<<asymptotom.imag()<<endl;
      cout<<endl;
      */
		}
		else { 
			/****** interpolate between large y and large omega expansions ***/

      //Debug
      /*
      cout<<"ERWAN u01 interpolate "<<endl;
      cout<<endl;
      */

			*indic=4;
			alpha=-((y+3.5)/(abs(lmt)-10.5)+0.15)/0.1;
			*seriesu=alpha*asymptoty+(1.-alpha)*asymptotom;
		}
	}
}

void CIntegrateAndFireTransferFunctionClass::old_u23(double omc, double y, doublecomplex *seriesu, int *indic) 
{ 
	static doublecomplex ah,sqom,series,deriv,asymptoty,asymptotom,ut,prefac;
  	static double alpha;
	ah=Complex(0.,0.5*omc);

	//Debug
	/*
	cout<<"old BRUNEL u23 omc "<<omc<<endl;
  cout<<"ah is "<<ah.r<<" "<<ah.i<<endl;
  cout<<"y is "<<y<<endl;
  cout<<endl;
  */

  //Check
	if(omc<10.5 && y>-3.5)
 	{
		*indic=1;
		old_onefone(Cadd(ONE,ah),Cadd(HALF,ONE),Complex(y*y,0.),&series,&deriv);
		ut=Cmul(Complex(0.,omc*y),Cmul(series,old_gsurg(ah,Cadd(HALF,ah))));
		old_onefone(Cadd(HALF,ah),HALF,Complex(y*y,0.),&series,&deriv);
		ut=Cadd(ut,series);
		ut=RCmul(2.*SQPI,Cdiv(ut,old_gsurg(ah,ONE)));
		*seriesu=ut;
	}
	else {
		if(y<-3.5-0.15*(omc-10.5)) 
		{
			//compute
			asymptoty=Complex(cos(omc*log(fabs(y)))/fabs(y),-sin(omc*log(fabs(y)))/fabs(y));
			
			//Debug
			/*
			cout<<"old BRUNEL u23 second part large y expansion"<<endl;
			cout<<"asymptoty is "<<asymptoty.r<<" "<<asymptoty.i<<endl,
			cout<<endl;
			*/

			old_correctionlargey(Cadd(ah,ONE),Cadd(HALF,ONE),Complex(y*y,0.),&series);
			asymptoty=Cmul(asymptoty,series);
			asymptoty=Cmul(asymptoty,Complex(0.,omc));

			//Debug
			/*
			cout<<"old BRUNEL u23 second part large y expansion"<<endl;
			cout<<"asymptoty is "<<asymptoty.r<<" "<<asymptoty.i<<endl,
			cout<<endl;
			*/

		}
		if(y>-3.5-0.25*(omc-10.5)) 
		{ 
			sqom=Complex(sqrt(omc),sqrt(omc));	
			asymptotom=RCmul(y,sqom);
			asymptotom=Cadd(asymptotom,RCmul(pow(y,3)/6.-y/2.,Cdiv(ONE,sqom)));
			asymptotom=Cadd(asymptotom,RCmul(-0.24*pow(y,2),Cdiv(ONE,Cmul(sqom,sqom))));
			asymptotom=Cadd(asymptotom,RCmul(-pow(y,5)/40.+pow(y,3)/12.+y/8.,Cdiv(ONE,Cmul(Cmul(sqom,sqom),sqom))));
			asymptotom=Cadd(asymptotom,RCmul(pow(y,4)/8.-pow(y,2)/4.,Cdiv(ONE,Cmul(Cmul(sqom,sqom),Cmul(sqom,sqom)))));
			asymptotom=RCmul(SQPI*exp(0.5*y*y),Cexp(asymptotom));
			prefac=Cadd(sqom,Complex(y,0.));
			prefac=Cadd(prefac,RCmul(0.5*y*y-0.5,Cdiv(ONE,sqom)));
			prefac=Cadd(prefac,RCmul(-0.48*y,Cdiv(ONE,Cmul(sqom,sqom))));
			prefac=Cadd(prefac,RCmul(-pow(y,4)/8.+pow(y,2)/4.+1./8.,Cdiv(ONE,Cmul(Cmul(sqom,sqom),sqom))));
			prefac=Cadd(prefac,RCmul(pow(y,3)/2.-y/2.,Cdiv(ONE,Cmul(Cmul(sqom,sqom),Cmul(sqom,sqom)))));
			asymptotom=Cdiv(Cmul(prefac,asymptotom),old_gsurg(Cadd(HALF,ah),ONE));
		}
		if(y<-3.5-0.25*(omc-10.5))
		{
			*indic=2;
			*seriesu=asymptoty;
		}
		else if(y>-3.5-0.15*(omc-10.5)) 
		{ 
			*indic=3;
			*seriesu=asymptotom;
		}
		else { 
			*indic=4;
			alpha=-((y+3.5)/(omc-10.5)+0.15)/0.1;
			*seriesu=Cadd(RCmul(alpha,asymptoty),RCmul(1.-alpha,asymptotom));
		}
	}
}

void CIntegrateAndFireTransferFunctionClass::u23(std::complex<double> lmt, double y, std::complex<double> *seriesu, int *indic)
{ 	
	static std::complex<double> ah,_sqom,sqom,gsur,series,deriv,asymptoty,asymptotom,ut,prefac;
  	static double alpha;
	//ah=getComplex(-0.5*lmt.imag(),0.5*lmt.real());
	ah=0.5*lmt;

	//Debug
  /*
	cout<<"ERWAN u23 lmt "<<lmt.real()<<" "<<lmt.imag()<<endl;
  cout<<"ah is "<<ah.real()<<" "<<ah.imag()<<endl;
  cout<<"y is "<<y<<endl;
  cout<<endl;
  */

  //Check
	if(abs(lmt)<10.5 && y>-3.5)
	{
	 	/***** use normal series ******/
		*indic=1;
		onefone(1.+ah,1.5,std::complex<double>(y*y,0.),&series,&deriv);
		ut=y*lmt*series*gsurg(ah,0.5+ah);

		onefone(0.5+ah,0.5,std::complex<double>(y*y,0.),&series,&deriv);
		ut+=series;
		ut*=(2.*SQPI)/gsurg(ah,1.);
		*seriesu=ut;

		/*
		old_onefone(Cadd(ONE,ah),Cadd(HALF,ONE),Complex(y*y,0.),&series,&deriv);
		ut=Cmul(Complex(0.,lmt*y),Cmul(series,old_gsurg(ah,Cadd(HALF,ah))));
		old_onefone(Cadd(HALF,ah),HALF,Complex(y*y,0.),&series,&deriv);
		ut=Cadd(ut,series);
		ut=RCmul(2.*SQPI,Cdiv(ut,old_gsurg(ah,ONE)));
		*/
	}
	else 
	{
		if(y<-3.5-0.15*(abs(lmt)-10.5))
 		{ 
			/****** large y expansion *****/
			asymptoty=pow(
				fabs(y),lmt.real()
			)*getComplex(
				cos(lmt.imag()*log(fabs(y)))/fabs(y),
				-sin(lmt.imag()*log(fabs(y)))/fabs(y)
			);

			//Debug
			/*
			cout<<"ERWAN u23 first part large y expansion"<<endl;
			cout<<"asymptoty is "<<asymptoty.real()<<" "<<asymptoty.imag()<<endl,
			cout<<endl;
			*/

			correctionlargey(ah+1.,1.5,std::complex<double>(y*y,0.),&series);
			asymptoty*=series;
			asymptoty*=std::complex<double>(0.,abs(lmt));

			//Debug
			/*
			cout<<"ERWAN u23 second part large y expansion"<<endl;
			cout<<"asymptoty is "<<asymptoty.real()<<" "<<asymptoty.imag()<<endl,
			cout<<endl;
			*/

		}
		if(y>-3.5-0.25*(abs(lmt)-10.5))
		{

			//set
			//sqom=getComplex(sqrt(abs(lmt)),sqrt(abs(lmt)));
			sqom=sqrt(2.)*myCsqrt(lmt);
			//_sqom=sqrt(abs(lmt))*exp(getComplex(0.,arg(lmt)/2.));
			//sqom=_sqom+getComplex(0.,1.)*_sqom;

      //Debug
      /*
      cout<<"ERWAN u23 large omega expansion "<<endl;
      cout<<"sqom is "<<sqom.real()<<" "<<sqom.imag()<<endl;
      cout<<endl;
      */

			/******* large omega expansion *********/
			asymptotom=y*sqom;
			asymptotom+=(pow(y,3)/6.-y/2.)/sqom;
			asymptotom+=-0.24*pow(y,2)/(sqom*sqom);
			asymptotom+=(-pow(y,5)/40.+pow(y,3)/12.+y/8.)/(sqom*sqom*sqom);
			asymptotom+=(pow(y,4)/8.-pow(y,2)/4.)/(sqom*sqom*sqom*sqom);
			asymptotom=SQPI*exp(0.5*y*y)*exp(asymptotom);
			prefac=sqom+std::complex<double>(y,0.);
			prefac+=(0.5*y*y-0.5)/sqom;
			prefac+=-0.48*y/(sqom*sqom);
			prefac+=(-pow(y,4)/8.+pow(y,2)/4.+1./8.)/(sqom*sqom*sqom);
			prefac+=(pow(y,3)/2.-y/2.)/(sqom*sqom*sqom*sqom);
      gsur=gsurg(0.5+ah,1.);
      
      if(gsur==0.){
        gsur=std::complex<double>(exp(-99.),0.);
      }

      //Debug
      /*
      cout<<"ERWAN u23 large omega expansion ensuite "<<endl;
      cout<<"asymptotom is "<<asymptotom.real()<<" "<<asymptotom.imag()<<endl;
      cout<<"prefac is "<<prefac.real()<<" "<<prefac.imag()<<endl;
      cout<<"gsur is "<<gsur.real()<<" "<<gsur.imag()<<endl;
      cout<<endl;
      */

      //set
      prefac/=gsur;
			asymptotom*=prefac;


		}
		if(y<-3.5-0.25*(abs(lmt)-10.5)) {
			 /****** large y expansion *****/
			*indic=2;
			*seriesu=asymptoty;

      //Debug
      /*
      cout<<"ERWAN u23 large y last "<<endl;
      cout<<"asymptoty is "<<asymptoty.real()<<" "<<asymptoty.imag()<<endl;
      cout<<endl;
      */
		}
		else if(y>-3.5-0.15*(abs(lmt)-10.5)) {
			/******* large omega expansion *********/
			*indic=3;
			*seriesu=asymptotom;

      //Debug
      /*
      cout<<"ERWAN u23 large omega last "<<endl;
      cout<<"asymptotom is "<<asymptotom.real()<<" "<<asymptotom.imag()<<endl;
      cout<<endl;
      */

		}
		else { 
			/****** interpolate between large y and large omega expansions ***/
			*indic=4;
			alpha=-((y+3.5)/(abs(lmt)-10.5)+0.15)/0.1;
			*seriesu=(alpha*asymptoty)+(1.-alpha)*asymptotom;

      //Debug
      /*
      cout<<"ERWAN u23 interpolate "<<endl;
      cout<<"asymptotom is "<<asymptotom.real()<<" "<<asymptotom.imag()<<endl;
      cout<<"asymptoty is "<<asymptoty.real()<<" "<<asymptoty.imag()<<endl;
      cout<<endl;
      */

		}
	}
}

/*** compute the oscillatory rate component for LIF neuron***/
doublecomplex CIntegrateAndFireTransferFunctionClass::RLIF(double _omega,int i) 
{	
	static doublecomplex series,numerator,denominator,hypergeo,rate,rlif;
	static doublecomplex u01_yt,u01_yr,u23_yt,u23_yr;
  	static int indicator,indict,indich;
  	static double omt,thetatil,hvrtil;	

  //set
	thetatil=DoubleDict["IntegralUpperBound"];
	hvrtil=DoubleDict["IntegralLowerBound"];
	omt=_omega*DoubleDict["ConstantTime"];
	
	/***** numerator  numu *****/
	old_u23(omt,thetatil,&series,&indicator);
	u23_yt=series;
	indict=indicator;
	old_u23(omt,hvrtil,&series,&indicator);
	u23_yr=series;
	indich=indicator;
	numerator=Csub(u23_yt,u23_yr);
	
	/***** denominator numu *****/
		
	old_u01(omt,thetatil,&series,&indicator);
	u01_yt=series;
	indict=indicator;
	old_u01(omt,hvrtil,&series,&indicator);
	u01_yr=series;
	indich=indicator;
	denominator=Csub(u01_yt,u01_yr);

	//Debug
	/*
	cout<<"old BRUNEL u23_yt Complex "<<u23_yt.r<<" "<<u23_yt.i<<" "<<endl;
	cout<<"old BRUNEL u23_yr Complex "<<u23_yr.r<<" "<<u23_yr.i<<" "<<endl;
	cout<<"old BRUNEL u01_yt Complex "<<u01_yt.r<<" "<<u01_yt.i<<" "<<endl;
	cout<<"old BRUNEL u01_yr Complex "<<u01_yr.r<<" "<<u01_yr.i<<" "<<endl;
	*/

	/****** LIF perturbation*****/
	hypergeo=Cdiv(numerator,denominator);
	//cout<<"hypergeo CState Real "<<hypergeo.r<<" "<<hypergeo.i<<endl;
	
	/******* rate low-pass filter*************/
	rate=Cdiv(Complex(1.,0.),Complex(1.,omt));
	//cout<<"rate CState Real "<<rate.r<<' '<<rate.i<<endl;
	
	/******* build everything ******/
	rlif=Cmul(RCmul(DoubleDict["StationaryRate"]/(DoubleDict["VoltageNoise"]),
		rate),hypergeo);
	//cout<<"rlif CState Real "<<rlif.r<<" "<<rlif.i<<" "<<indich<<endl;

	//Debug
	/*
	cout<<"old BRUNEL mean is "<<rlif.r<<" "<<rlif.i<<endl;
	cout<<endl;
	*/

	//return
	return rlif;
}



/***compute the perturbative complex rate comp1.nt for Lif neuron***/ 
void CIntegrateAndFireTransferFunctionClass::setBrunelLifPerturbationRate(
	std::complex<double> lambda
)
{
	static std::complex<double> u01_yt,u01_yr,u23_yt,u23_yr,denominator,numerator;
	static std::complex<double> lmt,series,mean,noise;
	static double rate0,yup,ylow;
	static int indicator,indict,indich;

	//set
	lmt=DoubleDict["ConstantTime"]*lambda;
	
  //print
  //cout<<"BRUNEL "<<abs(lmt)<<endl;
  //cout<<"DoubleDict['ConstantTime'] is "<<DoubleDict["ConstantTime"]<<endl;

	/***** omega nul exception*****/
	if(abs(lmt)==0.)
	{
		//print
		/*
		cout<<"BRUNEL lmt=0 "<<endl;
		*/

		//compute
		DoubleDict["PerturbationMean"]=getLifPerturbationNullRate();
		DoubleDict["PerturbationNoise"]=getLifPerturbationNullRate("VoltageNoise");
	}
	else
	{
		//set
		yup=DoubleDict["IntegralUpperBound"];
		ylow=DoubleDict["IntegralLowerBound"];

		//call the brunel old one
		//RLIF(lambda.imag(),0);

		/****** U23 numerators*****/

		/***** numerator  numu *****/
		u23(lmt,yup,&series,&indicator);
		u23_yt=series;
		indict=indicator;
		u23(lmt,ylow,&series,&indicator);
		u23_yr=series;
		indich=indicator;
		
		/****** U01 denominators*****/
		u01(lmt,yup,&series,&indicator);
		u01_yt=series;
		indict=indicator;
		u01(lmt,ylow,&series,&indicator);
		u01_yr=series;
		indich=indicator;

		//print
    /*
		cout<<"ERWAN u23_yt Complex "<<u23_yt.real()<<" "<<u23_yt.imag()<<" "<<endl;
		cout<<"ERWAN u23_yr Complex "<<u23_yr.real()<<" "<<u23_yr.imag()<<" "<<endl;
		cout<<"ERWAN u01_yt Complex "<<u01_yt.real()<<" "<<u01_yt.imag()<<" "<<endl;
		cout<<"ERWAN u01_yr Complex "<<u01_yr.real()<<" "<<u01_yr.imag()<<" "<<endl;
    */
    
		/******* compute stationary maybe*************/
		if(IntDict["ComputeStationary"]==1){
			DoubleDict["StationaryRate"]=getLifStationaryRate();
		}
		
		/******* build mean ***********/
    numerator=u23_yt-u23_yr;
    denominator=u01_yt-u01_yr;
    //if(denominator==0.){
    //  denominator=std::complex<double>(exp(-99.),0.);
    //}
    if(numerator!=0.){
  		mean=(numerator)/((1.+lmt)*(denominator));
    }
    else{
      mean=std::complex<double>(0.,0.);
    }

		//normalize
		mean*=DoubleDict[
				"StationaryRate"
			]/DoubleDict[
				"VoltageNoise"
			];
		
		//Debug
		//cout<<"Erwan set PerturbationMean mean is "<<mean.real()<<" "<<mean.imag()<<endl;
		//cout<<endl;
    
		/*** set ****/
		ComplexDict["PerturbationMean"]=mean;

		/******* build noise ***********/
		if(IntDict["ComputeNoise"]==1){

			/*** compute ****/
			noise=yup*u23_yt-ylow*u23_yr;
			noise/=u01_yt-u01_yr;
			noise+=lmt;
			noise*=DoubleDict[
				"StationaryRate"
			]/(
				DoubleDict["VoltageNoise"]*DoubleDict["VoltageNoise"]
			);
			noise/=(2.+lmt);
			//cout<<"BRUNEL rlif Complex "<<OutputDict["PerturbationMean"].real()<<" "<<OutputDict["PerturbationMean"].imag()<<" "<<indich<<endl;
		
			/*** set ****/
			ComplexDict["PerturbationNoise"]=noise;

		}
	
	}
	
	//cout<<"BRUNEL rate Complex "<<mu_rate.real()<<" "<<mu_rate.imag()<<endl;
}

/****Hakim and Ostojic Methods***/
void CIntegrateAndFireTransferFunctionClass::rkck(std::vector<std::complex<double> > y, std::vector<std::complex<double> > dydx, double x,  double h, std::vector<std::complex<double> >& yout, std::vector<std::complex<double> >& yerr, std::complex<double> lamda, void (CIntegrateAndFireTransferFunctionClass::*derivs)(double, vector<std::complex<double> >&, std::vector<std::complex<double> >&, std::complex<double> )) {

  int i;
  double a2=0.2,a3=0.3,a4=0.6,a5=1.0,a6=0.875,b21=0.2,
    b31=3.0/40.0,b32=9.0/40.0,b41=0.3,b42 = -0.9,b43=1.2,
    b51 = -11.0/54.0, b52=2.5,b53 = -70.0/27.0,b54=35.0/27.0,
    b61=1631.0/55296.0,b62=175.0/512.0,b63=575.0/13824.0,
    b64=44275.0/110592.0,b65=253.0/4096.0,c1=37.0/378.0,
    c3=250.0/621.0,c4=125.0/594.0,c6=512.0/1771.0,
    dc5 = -277.00/14336.0;
  double dc1=c1-2825.0/27648.0,dc3=c3-18575.0/48384.0,
    dc4=c4-13525.0/55296.0,dc6=c6-0.25;
  
  int n=y.size();
  std::vector<std::complex<double> >  ak2(n), ak3(n), ak4(n), ak5(n), ak6(n);
  std::vector<std::complex<double> >  ytemp(n);
  
  for (i=0;i<n;i++)
    ytemp[i]=y[i]+b21*h*dydx[i];
  (*this.*derivs)(x+a2*h,ytemp,ak2,lamda);
  for (i=0;i<n;i++)
    ytemp[i]=y[i]+h*(b31*dydx[i]+b32*ak2[i]);
  (*this.*derivs)(x+a3*h,ytemp,ak3,lamda);
  for (i=0;i<n;i++)
    ytemp[i]=y[i]+h*(b41*dydx[i]+b42*ak2[i]+b43*ak3[i]);
  (*this.*derivs)(x+a4*h,ytemp,ak4,lamda);
  for (i=0;i<n;i++)
    ytemp[i]=y[i]+h*(b51*dydx[i]+b52*ak2[i]+b53*ak3[i]+b54*ak4[i]);
  (*this.*derivs)(x+a5*h,ytemp,ak5,lamda);
  for (i=0;i<n;i++)
    ytemp[i]=y[i]+h*(b61*dydx[i]+b62*ak2[i]+b63*ak3[i]+b64*ak4[i]+b65*ak5[i]);
  (*this.*derivs)(x+a6*h,ytemp,ak6,lamda);
  for (i=0;i<n;i++){
    yout[i]=y[i]+h*(c1*dydx[i]+c3*ak3[i]+c4*ak4[i]+c6*ak6[i]);
  }
  for (i=0;i<n;i++)
    yerr[i]=h*(dc1*dydx[i]+dc3*ak3[i]+dc4*ak4[i]+dc5*ak5[i]+dc6*ak6[i]);
}

void CIntegrateAndFireTransferFunctionClass::rkqs(std::vector<std::complex<double> >& y, std::vector<std::complex<double> > dydx,  double& x, const double htry, const double eps, const std::vector<double>& yscal, double& hdid, double& hnext, std::complex<double> lamda, void (CIntegrateAndFireTransferFunctionClass::*derivs)(double, std::vector<std::complex<double> >&, std::vector<std::complex<double> >&, std::complex<double> )) {
  int n=y.size();
  int i;
  double errmax,h,htemp,xnew;
  std::vector<std::complex<double> > yerr(n), ytemp(n);
  h=htry;
  for (;;) {
    rkck(y,dydx,x,h,ytemp,yerr,lamda,derivs);
    errmax=0.0;
    for (i=0;i<n;i++) errmax = max(errmax, abs(yerr[i]/yscal[i]));
    errmax /= eps;
    if (errmax <= 1.0) break;
    htemp=SAFETY*h*pow(errmax,PSHRNK);
    h=(h >= 0.0 ? max(htemp,0.1*h) : min(htemp,0.1*h));
    xnew=(x)+h;
    if (xnew == x){
      cout<<"stepsize underflow in rkqs; if running crossoverfield quintessence, J may be too low\n";
      exit(0);
    }
  }  
  if (errmax > ERRCON) hnext=SAFETY*h*pow(errmax,PGROW);
  else hnext=5.0*h;
  x += (hdid=h);
  for (i=0;i<n;i++) y[i]=ytemp[i];  
}

double CIntegrateAndFireTransferFunctionClass::inside_integ(double x)
{
  float w;
  float y,ymin=-20.;
  int i,N=10000;
  w=0.0e0;
  for(i=0;i<=N;i++) {       
    y=ymin+(x-ymin)*(double)(i)/(double)(N);
    if(i==0||i==N) w+=0.5*pow(getErrorFunction(y)*exp(0.5*(x*x-y*y)),2.);
    else w+=pow(getErrorFunction(y)*exp(0.5*(x*x-y*y)),2.);
  }
  w*=(x-ymin)/(double)(N);
  return(w);
}


void CIntegrateAndFireTransferFunctionClass::phi_derivs(double y, std::vector<std::complex<double> >& phi, std::vector<std::complex<double> >& dphi, std::complex<double> lamda){

  dphi[0]=phi[1];
  dphi[1]=2.*((lamda-1.)*phi[0]-y*phi[1]);
}

void CIntegrateAndFireTransferFunctionClass::phi_t_derivs(double y, std::vector<std::complex<double> >& phi, std::vector<std::complex<double> >& dphi, std::complex<double> lamda){

  dphi[0]=phi[1];
  dphi[1]=2.*(lamda*phi[0]+y*phi[1]);
}

double CIntegrateAndFireTransferFunctionClass::odeint(vector<std::complex<double> >& ystart, const double x1, const double x2, const double eps, const double h1,  const double hmin, std::complex<double> lamda, void (CIntegrateAndFireTransferFunctionClass::*derivs)(double, std::vector<std::complex<double> >&, std::vector<std::complex<double> >&, std::complex<double>)){
  int nstp,i;
  double x,hdid,h,hnext;
  double sum=0;  
  int nvar=ystart.size();
  std::vector<double> yscal(nvar);
  std::vector<std::complex<double> > y(nvar), dydx(nvar);
  x=x1;
  (h1*(x2-x1)<0)?h=-1:h=1;
  for (i=0;i<nvar;i++) y[i]=ystart[i];
  for (nstp=1;nstp<=MAXSTP;nstp++) {
 
    (*this.*derivs)(x,y,dydx,lamda);
    for (i=0;i<nvar;i++) yscal[i]=abs(y[i])+abs(dydx[i]*h)+TINY;
    
    if ((x+h-x2)*(x+h-x1) > 0.0) h=x2-x;
    
    rkqs(y,dydx,x,h,eps, yscal ,hdid,hnext,lamda,derivs);
    sum=sum+hdid*real(y[0]);

    if ((x-x2)*(x2-x1) >= 0.0) {
      for (i=0;i<nvar;i++) ystart[i]=y[i];
      return sum;
    }
    if (fabs(hnext) <= hmin){
      cout<<"Step size too small in odeint\n";
    }
    h=hnext;
  }
  return 0.;
}


std::complex<double> CIntegrateAndFireTransferFunctionClass::phi_t_rka(double y, std::complex<double> lambda, std::complex<double>& phi_pr){
  int nb_steps=10000; 
  double eps=0.000001;
  double h1=0.2;
  double hmin=0.000000001;
 
  std::complex<double> out;
  double y_start=DoubleDict["IntegralLowerBound"]-15.;
  if(y<y_start){
    cout<<"phi2: y too small\n";
  }
  std::vector< std::complex<double> > phi_start(2);
  phi_start[0]=std::complex<double>(1.,0.);
  phi_start[1]=std::complex<double>(2.*y_start,0.);
  deriv=&CIntegrateAndFireTransferFunctionClass::phi_t_derivs;
  double nstp=odeint(phi_start,y_start,y,eps,h1,hmin,lambda,deriv);
  out=phi_start[0];
  phi_pr=phi_start[1];

  return out;
}

void CIntegrateAndFireTransferFunctionClass::setHakimLifPerturbationRate(std::complex<double> lambda){
	
	static std::complex<double> lmt,mean,noise;
	static double rate0;
	//lmt=getComplex(0.,1.)*DoubleDict["ConstantTime"]*lambda;
	lmt=DoubleDict["ConstantTime"]*lambda;

	/****** hypergeo compute*****/
	std::complex<double> u23_yt;
	std::complex<double> u01_yt=phi_t_rka(
		DoubleDict["IntegralUpperBound"],lmt,u23_yt
	);
	std::complex<double> u23_yr;
	std::complex<double> u01_yr=phi_t_rka(
		DoubleDict["IntegralLowerBound"],lmt,u23_yr
	);

	//print
	/*
	cout<<"HAKIM u23_yt Complex "<<u23_yt.real()<<" "<<u23_yt.imag()<<" "<<endl;
	cout<<"HAKIM u23_yr Complex "<<u23_yr.real()<<" "<<u23_yr.imag()<<" "<<endl;
	cout<<"HAKIM u01_yt Complex "<<u01_yt.real()<<" "<<u01_yt.imag()<<" "<<endl;
	cout<<"HAKIM u01_yr Complex "<<u01_yr.real()<<" "<<u01_yr.imag()<<" "<<endl;
	*/

	/******* compute stationary*************/
	if(IntDict["ComputeStationary"]==1){
		DoubleDict["StationaryRate"]=getLifStationaryRate();
	}

	/**** build mean ***/
	mean=(u23_yt-u23_yr)/((1.+lmt)*(u01_yt-u01_yr));

	//normalize
	mean*=DoubleDict[
		"StationaryRate"
	]/DoubleDict[
		"VoltageNoise"
	];

	//Debug
	/*
	cout<<"HAKIM mean is "<<mean.real()<<" "<<mean.imag()<<endl;
	cout<<endl;
	*/
	
	/**** set ***/
	ComplexDict["PerturbationMean"]=mean;

	/*** build noise ***/
	if(IntDict["ComputeNoise"]==1){

		noise=((
		DoubleDict["IntegralLowerBound"]*u23_yr-DoubleDict["IntegralUpperBound"]*u23_yt
		)/(u01_yr-u01_yt)-2.)/(2.+lmt)+1.;
		noise*=DoubleDict["StationaryRate"]/(
			DoubleDict["VoltageNoise"]*DoubleDict["VoltageNoise"]
		);

		/**** set ***/
		ComplexDict["PerturbationNoise"]=noise;
	}
	
	
	

}


/*
void CIntegrateAndFireTransferFunctionClass::u01Complex(doublecomplex omc, double y, doublecomplex *seriesu, int *indic) 
{	
	static doublecomplex ah,sqom,series,deriv,asymptoty,asymptotom,ut;
  	static double alpha;
	ah=RCmul(0.5,omc);
	sqom=RCmul(sqrt(2*Cabs(omc)),Cexp(Complex(0.,Carg(omc)/2)));
		
	if(Cabs(omc)<10.5 && y>-3.5) 
	{
		*indic=1;
		onefone(ah,0.5,Complex(y*y,0.),&series,&deriv);
		ut=RCmul(0.5,Cmul(series,gsurg(ah,Cadd(0.5,ah))));
		onefone(Cadd(0.5,ah),Cadd(1.,0.5),Complex(y*y,0.),&series,&deriv);
		ut=Cadd(ut,RCmul(y,series));
		ut=RCmul(2.*SQPI,Cdiv(ut,gsurg(ah,1.)));
		*seriesu=ut;
	}
	else {
		if(y<-3.5-0.15*(Cabs(omc)-10.5)) 
		{ 	
			asymptoty=RCmul(exp(-omc.r*log(fabs(y))),Complex(cos(omc.i*log(fabs(y))),-sin(omc.i*log(fabs(y)))));
			correctionlargey(ah,0.5,Complex(y*y,0.),&series);
			asymptoty=Cmul(asymptoty,series);
		}
		if(y>-3.5-0.25*(Cabs(omc)-10.5)) 
		{ 
			asymptotom=RCmul(y,sqom);
			asymptotom=Cadd(asymptotom,RCmul(pow(y,3)/6.-y/2.,Cdiv(1.,sqom)));
			asymptotom=Cadd(asymptotom,RCmul(-0.24*pow(y,2),Cdiv(1.,Cmul(sqom,sqom))));
			asymptotom=Cadd(asymptotom,RCmul(-pow(y,5)/40.+pow(y,3)/12.+y/8.,Cdiv(1.,Cmul(Cmul(sqom,sqom),sqom))));
			asymptotom=Cadd(asymptotom,RCmul(pow(y,4)/8.-pow(y,2)/4.,Cdiv(1.,Cmul(Cmul(sqom,sqom),Cmul(sqom,sqom)))));
			asymptotom=RCmul(SQPI*exp(0.5*y*y),Cexp(asymptotom));
			asymptotom=Cdiv(asymptotom,gsurg(Cadd(0.5,ah),1.));
		}
		if(y<-3.5-0.25*(Cabs(omc)-10.5)) 
		{ 
			*indic=2;
			*seriesu=asymptoty;
		}
		else if(y>-3.5-0.15*(Cabs(omc)-10.5)) 
		{
			*indic=3;
			*seriesu=asymptotom;
		}
		else { 
			*indic=4;
			alpha=-((y+3.5)/(Cabs(omc)-10.5)+0.15)/0.1;
			*seriesu=Cadd(RCmul(alpha,asymptoty),RCmul(1.-alpha,asymptotom));
		}
	}
}
	
void CIntegrateAndFireTransferFunctionClass::u23Complex(doublecomplex omc, double y, doublecomplex *seriesu, int *indic) 
{ 	
	static doublecomplex ah,sqom,series,deriv,asymptoty,asymptotom,ut,prefac;
  	static double alpha;
	ah=RCmul(0.5,omc);
	sqom=RCmul(sqrt(2*Cabs(omc)),Cexp(Complex(0.,Carg(omc)/2)));	
	if(Cabs(omc)<10.5 && y>-3.5) 
	{
		*indic=1;
		onefone(Cadd(1.,ah),Cadd(0.5,1.),Complex(y*y,0.),&series,&deriv);
		ut=Cmul(RCmul(y,omc),Cmul(series,gsurg(ah,Cadd(0.5,ah))));
		onefone(Cadd(0.5,ah),0.5,Complex(y*y,0.),&series,&deriv);
		ut=Cadd(ut,series);
		ut=RCmul(2.*SQPI,Cdiv(ut,gsurg(ah,1.)));
		*seriesu=ut;
	}
	else 
	{
		if(y<-3.5-0.15*(Cabs(omc)-10.5))
 		{ 
			asymptoty=RCmul(exp(-omc.r*log(fabs(y))/fabs(y)),Complex(cos(omc.i*log(fabs(y)))/fabs(y),-sin(omc.i*log(fabs(y)))/fabs(y)));
			correctionlargey(Cadd(ah,1.),Cadd(0.5,1.),Complex(y*y,0.),&series);
			asymptoty=Cmul(asymptoty,series);
			asymptoty=Cmul(asymptoty,Complex(0.,Cabs(omc)));
		}
		if(y>-3.5-0.25*(Cabs(omc)-10.5)) 
		{
			asymptotom=RCmul(y,sqom);
			asymptotom=Cadd(asymptotom,RCmul(pow(y,3)/6.-y/2.,Cdiv(1.,sqom)));
			asymptotom=Cadd(asymptotom,RCmul(-0.24*pow(y,2),Cdiv(1.,Cmul(sqom,sqom))));
			asymptotom=Cadd(asymptotom,RCmul(-pow(y,5)/40.+pow(y,3)/12.+y/8.,Cdiv(1.,Cmul(Cmul(sqom,sqom),sqom))));
			asymptotom=Cadd(asymptotom,RCmul(pow(y,4)/8.-pow(y,2)/4.,Cdiv(1.,Cmul(Cmul(sqom,sqom),Cmul(sqom,sqom)))));
			asymptotom=RCmul(SQPI*exp(0.5*y*y),Cexp(asymptotom));
			prefac=Cadd(sqom,Complex(y,0.));
			prefac=Cadd(prefac,RCmul(0.5*y*y-0.5,Cdiv(1.,sqom)));
			prefac=Cadd(prefac,RCmul(-0.48*y,Cdiv(1.,Cmul(sqom,sqom))));
			prefac=Cadd(prefac,RCmul(-pow(y,4)/8.+pow(y,2)/4.+1./8.,Cdiv(1.,Cmul(Cmul(sqom,sqom),sqom))));
			prefac=Cadd(prefac,RCmul(pow(y,3)/2.-y/2.,Cdiv(1.,Cmul(Cmul(sqom,sqom),Cmul(sqom,sqom)))));
			asymptotom=Cdiv(Cmul(prefac,asymptotom),gsurg(Cadd(0.5,ah),1.));
		}
		if(y<-3.5-0.25*(Cabs(omc)-10.5)) {
			*indic=2;
			*seriesu=asymptoty;
		}
		else if(y>-3.5-0.15*(Cabs(omc)-10.5)) { 
			*indic=3;
			*seriesu=asymptotom;
		}
		else { 
			*indic=4;
			alpha=-((y+3.5)/(Cabs(omc)-10.5)+0.15)/0.1;
			*seriesu=Cadd(RCmul(alpha,asymptoty),RCmul(1.-alpha,asymptotom));
		}
	}
}
 
doublecomplex CIntegrateAndFireTransferFunctionClass::RLifComplex(doublecomplex lambda,int i) 
{		
	static doublecomplex series,numerator,denominator;
	static doublecomplex ut,uh,omt;
	static int indicator,indict,indich;
	static double thetatil,hvrtil;
	thetatil=(V_threshold[i]-mu0[i])/(sigmaNoise[i]);
	hvrtil=(V_reset[i]-mu0[i])/(sigmaNoise[i]);
	omt=RCmul(taum[i],lambda);
		
	u01Complex(omt,thetatil,&series,&indicator);
	ut=series;
	indict=indicator;
	u01Complex(omt,hvrtil,&series,&indicator);
	uh=series;
	indich=indicator;
	denominator=Csub(ut,uh);
		
	u23Complex(omt,thetatil,&series,&indicator);
	ut=series;
	indict=indicator;
	u23Complex(omt,hvrtil,&series,&indicator);
	uh=series;
	indich=indicator;
	numerator=Csub(ut,uh);
		
	return (RCmul(r0[i]/(sigmaNoise[i]),Cdiv(numerator,Cmul(Cadd(Complex(1.,0.),omt),denominator))));
}
*/

/***COMPLEX NUMBER METHODS***/

/***create a complex number***/
doublecomplex CIntegrateAndFireTransferFunctionClass::Complex(double re, double im) 
{
	static doublecomplex c;
	c.r=re;
	c.i=im;
	return c;
}

/***addition of two complex numbers***/
doublecomplex CIntegrateAndFireTransferFunctionClass::Cadd(doublecomplex a,doublecomplex b) {
	static doublecomplex c;
	c.r=a.r+b.r;
	c.i=a.i+b.i;
	return c;
}

/***substraction of two complex numbers***/
doublecomplex CIntegrateAndFireTransferFunctionClass::Csub(doublecomplex a, doublecomplex b) {
	static doublecomplex c;
	c.r=a.r-b.r;
	c.i=a.i-b.i;
	return c;
}

/***multiplication of two complex numbers***/
doublecomplex CIntegrateAndFireTransferFunctionClass::Cmul(doublecomplex a, doublecomplex b) {
	static doublecomplex c;
	c.r=a.r*b.r-a.i*b.i;
	c.i=a.i*b.r+a.r*b.i;
	return c;
}

/***division of two complex numbers***/
doublecomplex CIntegrateAndFireTransferFunctionClass::Cdiv(doublecomplex a, doublecomplex b) {
	static doublecomplex c;
	double r,den;
	if (fabs(b.r) >= fabs(b.i)) {
	r=b.i/b.r;
	den=b.r+r*b.i;
	c.r=(a.r+r*a.i)/den;
	c.i=(a.i-r*a.r)/den;
	} else {
	r=b.r/b.i;
	den=b.i+r*b.r;
	c.r=(a.r*r+a.i)/den;
	c.i=(a.i*r-a.r)/den;
	}
	return c;
}

/***conjugate of a complex numbers***/
doublecomplex CIntegrateAndFireTransferFunctionClass::Conjg(doublecomplex z) {
	static doublecomplex c;
	c.r=z.r;
	c.i = -z.i;
	return c;
}

/***square root a complex numbers***/
doublecomplex CIntegrateAndFireTransferFunctionClass::Csqrt(doublecomplex z) {
	static doublecomplex c;
	static double x,y,w,r;
	if ((z.r == 0.0e0) && (z.i == 0.0e0)) {
		c.r=0.0e0;
		c.i=0.0e0;
	return c;
	} 
	else {
		x=fabs(z.r);
		y=fabs(z.i);
	if (x >= y) {
		r=y/x;
		w=sqrt(x)*sqrt(0.5e0*(1.0e0+sqrt(1.0e0+r*r)));
	} 
	else {
		r=x/y;
		w=sqrt(y)*sqrt(0.5e0*(r+sqrt(1.0e0+r*r)));
	}
	if (z.r >= 0.0e0) {
		c.r=w;
		c.i=z.i/(2.0e0*w);
	} 
	else {
    c.i=(z.i >= 0.0e0) ? w : -w;
		c.r=z.i/(2.0e0*c.i);	
	}
	return c;
	}
}

std::complex<double> CIntegrateAndFireTransferFunctionClass::myCsqrt(std::complex<double> z) {
	static std::complex<double> c;
	static double x,y,w,r,imag;

  //Debug
  /*
  cout<<"myCsqrt z is "<<z.real()<<" "<<z.imag()<<endl;
  cout<<endl;
  */

  //Check
	if ((z.real() == 0.0e0) && (z.imag() == 0.0e0)) {
		c=std::complex<double>(0.,0.);
		return c;
	} 
	else {
		x=fabs(z.real());
		y=fabs(z.imag());
	if (x >= y) {
		r=y/x;
		w=sqrt(x)*sqrt(0.5e0*(1.0e0+sqrt(1.0e0+r*r)));
	} 
	else {
		r=x/y;
		w=sqrt(y)*sqrt(0.5e0*(r+sqrt(1.0e0+r*r)));
	}
	if (z.real() >= 0.0e0) {
		c=std::complex<double>(w,z.imag()/(2.0e0*w));
	} 
	else {
    imag=(z.imag() >= 0.0e0) ? w : -w;
		c=std::complex<double>(
			z.imag()/(2.0e0*imag),
      imag
		);
	}
	return c;
	}
}

/***exponential of a  complex numbers***/
doublecomplex CIntegrateAndFireTransferFunctionClass::Cexp(doublecomplex a) {
	static doublecomplex c;
	c.r=exp(a.r)*cos(a.i);
	c.i=exp(a.r)*sin(a.i);
	return c;
}

/***multiplication of a complex numbers with a real***/
doublecomplex CIntegrateAndFireTransferFunctionClass::RCmul(double x, doublecomplex a) {
	static doublecomplex c;
	c.r=x*a.r;
	c.i=x*a.i;
	return c;
}

/***module of a complex numbers ***/
double CIntegrateAndFireTransferFunctionClass::Cabs(doublecomplex z) 
{
	static double x,y,ans,temp;
	x=fabs(z.r);
	y=fabs(z.i);
	if (x == 0.0e0)
		ans=y;
	else if (y == 0.0e0)
		ans=x;
	else if (x > y) {
		temp=y/x;
		ans=x*sqrt(1.0e0+temp*temp);
	} 
	else {
		temp=x/y;
		ans=y*sqrt(1.0e0+temp*temp);
	}
	return ans;
}

/***argument of a complex numbers ***/
double CIntegrateAndFireTransferFunctionClass::Carg(doublecomplex a)
{
	return (2.*atan(a.i/(sqrt((a.i)*(a.i)+(a.r)*(a.r))+a.r)));
}

#endif




