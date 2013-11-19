from CombinedEWKAnalysis.CommonTools.AnomalousCouplingModel import *
import ROOT as r
import os

basepath = '%s/src/CombinedEWKAnalysis/CommonTools/data/WV_semileptonic'%os.environ['CMSSW_BASE']
 

#this model is in the equal couplings scenario of HISZ or something similar
#it does the old style limits of setting the other parameter to zero
class HagiwaraAndZeppenfeldTwoDimensionalModel(AnomalousCouplingModel):
    def __init__(self,mode):
        AnomalousCouplingModel.__init__(self)
        self.processes = ['WWgammaZ']
        self.channels  = ['WW_atgc_semileptonic_mu',
                          'WW_atgc_semileptonic_el',
                          'WZ_atgc_semileptonic_mu',
                          'WZ_atgc_semileptonic_el']
        self.pois      =  ['dkg','dg1','lZ']
        self.mode      = mode
        self.anomCoupSearchWindows = {'dkg':['-1.5e-1','1.5e-1'],
                                      'dg1':['-1.5e-1','1.5e-1'],
                                      'lZ' :['-3e-2','3e-2']     }

        self.nameMapParents = {'WZ':'wz','WW':'ww'}
        self.nameMapChildren = {'_el':'el','_mu':'mu'}
        
        self.verbose = False

    def buildScaling(self,process,channel):        
        scalerName = '%s_%s'%(process,channel)

        parent = None
        for p in self.nameMapParents.keys():
            if p in channel:
                parent = self.nameMapParents[p]
        child = None
        for c in self.nameMapChildren.keys():
            if c in channel:
                child = self.nameMapChildren[c]

        print scalerName, parent, child

        filename = '%s/%s_ATGC_shape_coefficients.root'%(basepath,parent)
        
        
        f = r.TFile('%s/%s_boosted.root'%(basepath,child),'READ')
        SM_diboson_shape = f.Get(parent).Clone('SM_%s_semil_%s_shape_for_scale'%(parent,child))
        SM_diboson_shape.SetDirectory(0)
        f.Close()
        self.modelBuilder.out._import(SM_diboson_shape)
        SM_diboson_shape_dhist = r.RooDataHist('DHIST_SM_%s_semil_%s_shape_for_scale'%(parent,child),
                    'DHIST_SM_%s_semil_%s_shape_for_scale'%(parent,child),
                    r.RooArgList(self.modelBuilder.out.var('W_pt')),
                    self.modelBuilder.out.obj('SM_%s_semil_%s_shape_for_scale'%(parent,child)))
        self.modelBuilder.out._import(SM_diboson_shape_dhist)        
        self.modelBuilder.factory_('RooHistFunc::Scaling_base_pdf_%s({W_pt},DHIST_SM_%s_semil_%s_shape_for_scale)'%(scalerName,parent,child))              
        self.modelBuilder.factory_('RooATGCProcessScaling::Scaling_%s(W_pt,dkg,lZ,dg1,Scaling_base_pdf_%s,"%s")'%(scalerName,scalerName,filename))

        if ( self.mode == 'dkglZ' ):
            self.modelBuilder.out.function('Scaling_%s'%scalerName).setLimitType(0)
            self.modelBuilder.out.var('dg1').setVal(0)
            self.modelBuilder.out.var('dg1').setConstant(True)
        elif ( self.mode == 'dg1lZ' ):
            self.modelBuilder.out.function('Scaling_%s'%scalerName).setLimitType(1)
            self.modelBuilder.out.var('dkg').setVal(0)
            self.modelBuilder.out.var('dkg').setConstant(True)  
        elif ( self.mode == 'dkgdg1' ):
            self.modelBuilder.out.function('Scaling_%s'%scalerName).setLimitType(2)
            self.modelBuilder.out.var('lZ').setVal(0)
            self.modelBuilder.out.var('lZ').setConstant(True)            
        else:
            raise RuntimeError('InvalidCouplingChoice',
                               'We can only use [dkg,lZ], [dg1,lZ], and [dkg,dg1]'\
                               ' as POIs right now!')
        
        return scalerName
        

dkglZModel = HagiwaraAndZeppenfeldTwoDimensionalModel('dkglZ')
dg1lZModel = HagiwaraAndZeppenfeldTwoDimensionalModel('dg1lZ')
dkgdg1Model = HagiwaraAndZeppenfeldTwoDimensionalModel('dkgdg1')
