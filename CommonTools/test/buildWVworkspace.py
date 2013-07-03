import pyroot_logon
import limits
import os
import sys

from ROOT import *

lType = sys.argv[1] 
codename = ""

if( lType == "muon" ) :
    codename = "mu"
elif( lType == "electron" ):
    codename = "el"
else:
    raise RuntimeError('InvalidLepton','You may only choose between "muon" and "electron" channels.')

basepath = '%s/src/CombinedEWKAnalysis/CommonTools/data/WV_semileptonic'%os.environ['CMSSW_BASE']

f = TFile('%s/%s_boosted.root'%(basepath,codename))

background = f.Get('background')
background_backshapeUp = f.Get('background_%sboosted_backshapeUp'%codename)
background_backshapeDown = f.Get('background_%sboosted_backshapeDown'%codename)
data_obs = f.Get('data_obs')
diboson = f.Get('diboson')

background.Add(diboson, -1.)

theWS = RooWorkspace('WV_%sboosted'%codename, 'WV_%sboosted'%codename)

wpt = theWS.factory('W_pt[%f,%f]' % (data_obs.GetBinLowEdge(1), 
                                     data_obs.GetBinLowEdge(data_obs.GetNbinsX())+data_obs.GetBinWidth(data_obs.GetNbinsX())))
wpt.setBins(data_obs.GetNbinsX())

lz = theWS.factory('lZ[0., -1., 1.]')
# lz = theWS.factory('lZ[0.]')
lz.setConstant(False)
dkg = theWS.factory('dkg[0., -0.5, 0.5]')
dg1 = theWS.factory('dg1[0.]')


vars = RooArgList(wpt)
varSet = RooArgSet(wpt)

data = RooDataHist('data_obs', 'data_obs_WV_%s'%codename, vars, data_obs)
bkgHist = RooDataHist('WV_semileptonic_bkg_%s'%codename,
                      'WV_semileptonic_bkg_%s'%codename,
                      vars,
                      background)
bkgHist_systUp = RooDataHist('WV_semileptonic_bkg_%s_%sboosted_backshapeUp'%(codename,codename),
                             'WV_semileptonic_bkg_%s_%sboosted_backshapeUp'%(codename,codename),
                             vars,
                             background_backshapeUp)
bkgHist_systDown = RooDataHist('WV_semileptonic_bkg_%s_%sboosted_backshapeDown'%(codename,
                                                                                 codename),
                               'WV_semileptonic_bkg_%s_%sboosted_backshapeDown'%(codename,
                                                                                 codename),
                               vars,
                               background_backshapeDown)

dibosonHist = RooDataHist('WV_semileptonic_SM_%s_rawshape'%codename,
                          'WV_semileptonic_SM_%s_rawshape'%codename,
                          vars,
                          diboson)
dibosonPdf = RooHistFunc('WV_semileptonic_SM_%s_shape'%codename,
                         'WV_semileptonic_SM_%s_shape'%codename,
                         varSet,
                         dibosonHist)



aTGC = RooATGCFunction('ATGC_shapescale_WWgammaZ_WV_atgc_semileptonic_%s'%codename,
                       'ATGC_shapescale_%s'%codename,
                       wpt,
                       lz,
                       dkg,
                       dg1, 
                       '%s/ATGC_shape_coefficients.root'%basepath)



aTGCPdf = RooATGCSemiAnalyticPdf('ATGCPdf_WWgammaZ_WV_atgc_semileptonic_%s'%codename,
                                 'ATGCPdf_WV_%s'%codename,
                                 wpt,
                                 dkg,
                                 lz,                                 
                                 dg1,
                                 dibosonPdf,
                                 '%s/ATGC_shape_coefficients.root'%basepath)

getattr(theWS, 'import')(data)
getattr(theWS, 'import')(bkgHist)
getattr(theWS, 'import')(bkgHist_systUp)
getattr(theWS, 'import')(bkgHist_systDown)
getattr(theWS, 'import')(aTGCPdf)

theWS.Print()

fout = TFile('%s_boosted_ws.root'%codename, 'recreate')
theWS.Write()
fout.Close()
