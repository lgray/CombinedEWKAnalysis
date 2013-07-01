// -*- mode: c++ -*-

#ifndef ROOATGCPROCESSSCALING
#define ROOATGCPROCESSSCALING

#include "RooEffProd.h"
#include "RooRealProxy.h"
#include "RooAbsReal.h"
  
class RooATGCProcessScaling : public RooAbsReal {
public:
  
  RooATGCProcessScaling ();
  RooATGCProcessScaling (const char * name, const char * title,
			 RooAbsReal& dkg,
			 RooAbsReal& lZ,
			 RooAbsReal& dg1,
			 RooAbsReal& func);
  RooATGCProcessScaling (const RooATGCProcessScaling& other, const char * name);
  virtual TObject * clone(const char * newname) const { 
    return new RooATGCProcessScaling(*this, newname);
  }
  
  virtual ~RooATGCProcessScaling ();
  
protected:
  
  RooRealProxy _shapeScale;
  double SM_scale;
  
  virtual double evaluate() const;
  
private:
  
  ClassDef(RooATGCProcessScaling, 1) // aTGC scaler
};

#endif
