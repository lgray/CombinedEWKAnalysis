/***************************************************************************** 
 * Project: RooFit                                                           * 
 *                                                                           * 
 * This code was autogenerated by RooClassFactory                            * 
 *****************************************************************************/ 

// Your description goes here... 

#include "Riostream.h" 

#include "CombinedEWKAnalysis/CommonTools/interface/RooATGCFunction.h" 

#include <math.h> 
#include "TMath.h" 

#include "TFile.h"

ClassImpUnique(RooATGCFunction,MAGICWORDOFSOMESORT) 

RooATGCFunction::RooATGCFunction() : 
  P_dk(0), P_dg1(0)
{
  initializeProfiles();
}

RooATGCFunction::RooATGCFunction(const char *name, const char *title, 
                                 RooAbsReal& _x,
                                 RooAbsReal& _lZ,
                                 RooAbsReal& _dkg,
                                 RooAbsReal& _dg1,
                                 const char * parFilename) :
   RooAbsReal(name,title), 
   x("x","x",this,_x),
   lZ("lZ","lZ",this,_lZ),
   dkg("dkg","dkg",this,_dkg),
   dg1("dg1","dg1",this,_dg1),
   profileFilename(parFilename),
   P_dk(0), P_dg1(0)
{ 
  initializeProfiles();
  const char* pwd = gDirectory->GetPath();
  TFile *f = TFile::Open(parFilename,"READ");  
  gDirectory->cd(pwd);
  std::cout << "opened the input file!" << std::endl;
  readProfiles(*f);
  f->Close();
} 

RooATGCFunction::RooATGCFunction(const RooATGCFunction& other, 
                                 const char* name) :  
  RooAbsReal(other,name), 
  x("x",this,other.x),
  lZ("lZ",this,other.lZ),
  dkg("dkg",this,other.dkg),
  dg1("dg1",this,other.dg1),
  profileFilename(other.profileFilename),
  P_dk(0), P_dg1(0)
{ 
  initializeProfiles();
  readProfiles(other);
} 

void RooATGCFunction::initializeProfiles() {
  P_dk = new TProfile2D*[7]();
  P_dg1 = new TProfile2D*[7]();
}

void RooATGCFunction::readProfiles(TDirectory& dir) const {

  int i;
  for(i=0; i<=6; ++i) {
    
    if (P_dk[i]) delete P_dk[i];
    TString dkname = TString::Format("p%i_lambda_dkg", i);
    P_dk[i] = dynamic_cast<TProfile2D *>(dir.Get(dkname)->Clone(dkname+"new"));
    P_dk[i]->SetDirectory(0);
    if (P_dg1[i]) delete P_dg1[i];
    TString dg1name = TString::Format("p%i_lambda_dg1", i);
    P_dg1[i] = dynamic_cast<TProfile2D *>(dir.Get(dg1name)->Clone(dg1name+"new"));
    P_dg1[i]->SetDirectory(0);
  }

  // for (i=0; i<=6; i++) {
  //   std::cout << 'P' << i << "_dk " << P_dk[i]->GetName() << '\n';
  // }
}

void RooATGCFunction::readProfiles(RooATGCFunction const& other) {
  for (int i = 0; i<=6; ++i) {
    P_dk[i] = new TProfile2D(*(other.P_dk[i]));
    P_dk[i]->SetDirectory(0);
    P_dg1[i] = new TProfile2D(*(other.P_dg1[i]));
    P_dg1[i]->SetDirectory(0);
  }
}

RooATGCFunction::~RooATGCFunction() {
  for(int i = 0; i<7; ++i) {
    if (P_dk[i])
      delete P_dk[i];
    if (P_dg1[i])
      delete P_dg1[i];
  }
  delete[] P_dk;
  delete[] P_dg1;
}

Double_t RooATGCFunction::evaluate() const 
{ 
  // ENTER EXPRESSION IN TERMS OF VARIABLE ARGUMENTS HERE 

  TProfile2D ** P = P_dg1;
  double v1(lZ), v2(dg1);
  if(TMath::Abs(dg1)<0.000001) {
    P = P_dk;
    v2 = dkg;
  }

  if (not P[0]) {
    TFile f(profileFilename);
    readProfiles(f);
    f.Close();
  }

  if (v1 < P[0]->GetXaxis()->GetXmin())
    v1 = P[0]->GetXaxis()->GetXmin();
  if (v1 > P[0]->GetXaxis()->GetXmax())
    v1 = P[0]->GetXaxis()->GetXmax();
  if (v2 < P[0]->GetYaxis()->GetXmin())
    v2 = P[0]->GetYaxis()->GetXmin();
  if (v2 > P[0]->GetYaxis()->GetXmax())
    v2 = P[0]->GetYaxis()->GetXmax();
 
  double ret(0.);
  for(int i = 0; i<= 6; i++) {
    // std::cout << P_dk[i]->GetName() << '\n';
    ret += P[i]->Interpolate(v1, v2)*TMath::Power(x, i);
  }

  if (ret < 0.) ret = 0.;
  return ret; 
}
