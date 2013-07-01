from CombinedEWKAnalysis.CommonTools.AnomalousCouplingModel import *
import ROOT

#this model is in the equal couplings scenario of HISZ or something similar
#it does the old style limits of setting the other parameter to zero
class HagiwaraAndZeppenfeldTwoDimensionalModel(AnomalousCouplingModel):
    def __init__(self):
        AnomalousCouplingModel.__init__(self)
        self.processes = ['WWgammaZ']
        self.channels  = ['WV_atgc_semileptonic_mu']
        self.pois    =  ['dkg','dg1','lZ']
        self.anomCoupSearchWindows = {'dkg':['-5e-1','5e-1'],
                                      'dg1':['-5e-1','5e-1'],
                                      'lZ' :['-5e-1','5e-1']     }
        
        self.verbose = False

    def buildScaling(self,process,channel):        
        scalerName = 'bork'        
        if ( 'dkg' in self.pois and
             'lZ' in self.pois  and
             'dg1' not in self.pois ):
            scalerName = '%s_%s'%(process,channel)
            self.modelBuilder.factory_('RooATGCProcessScaling::Scaling_%s(dkg,lZ,dg1,ATGCPdf_%s)'%(scalerName,scalerName))
        elif ( 'dkg' in self.pois and
               'dg1' in self.pois and
               'lZ' not in self.pois  ):
            scalerName = '%s_%s'%(process,channel)
            self.modelBuilder.factory_('RooATGCProcessScaling::Scaling_%s(dkg,lZ,dg1,ATGCPdf_%s)'%(scalerName,scalerName))
        else:
            raise RuntimeError('InvalidCouplingChoice',
                               'We can only use [dkg,lZ] and [dkg,dg1]'\
                               ' as POIs right now!')
        return scalerName
        

dkglZModel = HagiwaraAndZeppenfeldTwoDimensionalModel()
dkglZModel.pois = ['dkg','lZ']
dkgdg1Model = HagiwaraAndZeppenfeldTwoDimensionalModel()
dkgdg1Model.pois = ['dkg','dg1']
