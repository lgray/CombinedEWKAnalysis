from CombinedEWKAnalysis.CommonTools.AnomalousCouplingModel import *
import ROOT as r
import os

basepath = '%s/src/CombinedEWKAnalysis/CommonTools/data/WV_semileptonic'%os.environ['CMSSW_BASE']
filename = '%s/ATGC_shape_coefficients.root'%basepath  

#this model is in the equal couplings scenario of HISZ or something similar
#it does the old style limits of setting the other parameter to zero
class HagiwaraAndZeppenfeldTwoDimensionalModel(AnomalousCouplingModel):
    def __init__(self,mode):
        AnomalousCouplingModel.__init__(self)
        self.processes = ['WWgammaZ']
        self.channels  = ['WV_atgc_semileptonic']
        self.pois      =  ['dkg','dg1','lZ']
        self.mode      = mode
        self.anomCoupSearchWindows = {'dkg':['-1.5e-1','1.5e-1'],
                                      'dg1':['-5e-1','5e-1'],
                                      'lZ' :['-3e-2','3e-2']     }
        
        self.verbose = False

    def buildScaling(self,process,channel):        
        scalerName = 'bork'        
        if ( self.mode == 'dkglZ' ):
            scalerName = '%s_%s'%(process,channel)
            self.modelBuilder.out.var('dg1').setVal(0)
            self.modelBuilder.out.var('dg1').setConstant(True)            
        elif ( self.mode == 'dkgdg1' ):
            scalerName = '%s_%s'%(process,channel)
            self.modelBuilder.out.var('lZ').setVal(0)
            self.modelBuilder.out.var('lZ').setConstant(True)            
        else:
            raise RuntimeError('InvalidCouplingChoice',
                               'We can only use [dkg,lZ] and [dkg,dg1]'\
                               ' as POIs right now!')
              
        f = r.TFile('%s/mu_boosted.root'%basepath,'READ')
        SM_diboson_shape = f.Get('diboson').Clone('SM_wv_semil_mu_shape_for_scale')
        SM_diboson_shape.SetDirectory(0)
        f.Close()
        self.modelBuilder.out._import(SM_diboson_shape)
        SM_diboson_shape_dhist = r.RooDataHist('DHIST_SM_wv_semil_mu_shape_for_scale',
                    'DHIST_SM_wv_semil_mu_shape_for_scale',
                    r.RooArgList(self.modelBuilder.out.var('W_pt')),
                    self.modelBuilder.out.obj('SM_wv_semil_mu_shape_for_scale'))
        self.modelBuilder.out._import(SM_diboson_shape_dhist)        
        self.modelBuilder.factory_('RooHistFunc::Scaling_base_pdf_%s({W_pt},DHIST_SM_wv_semil_mu_shape_for_scale)'%(scalerName))              
        self.modelBuilder.factory_('RooATGCProcessScaling::Scaling_%s(W_pt,dkg,lZ,dg1,Scaling_base_pdf_%s,"%s")'%(scalerName,scalerName,filename))
        return scalerName
        

dkglZModel = HagiwaraAndZeppenfeldTwoDimensionalModel('dkglZ')
dkgdg1Model = HagiwaraAndZeppenfeldTwoDimensionalModel('dkgdg1')
