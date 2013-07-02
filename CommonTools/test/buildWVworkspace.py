import pyroot_logon
import limits

from ROOT import *

basepath = '/home/lgray/CMSSW_6_2_0_pre5/src/CombinedEWKAnalysis/CommonTools/data/WV_semileptonic'

f = TFile('%s/mu_boosted.root'%basepath)

background = f.Get('background')
background_muboosted_backshapeUp = f.Get('background_muboosted_backshapeUp')
background_muboosted_backshapeDown = f.Get('background_muboosted_backshapeDown')
data_obs = f.Get('data_obs')
diboson = f.Get('diboson')

background.Add(diboson, -1.)

theWS = RooWorkspace('WV_muboosted', 'WV_muboosted')

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

data = RooDataHist('data_obs', 'data_obs_WV_mu', vars, data_obs)
bkgHist = RooDataHist('WV_semileptonic_bkg_mu',
                      'WV_semileptonic_bkg_mu',
                      vars,
                      background)
bkgHist_systUp = RooDataHist('WV_semileptonic_bkg_mu_muboosted_backshapeUp',
                             'WV_semileptonic_bkg_mu_muboosted_backshapeUp',
                             vars,
                             background_muboosted_backshapeUp)
bkgHist_systDown = RooDataHist('WV_semileptonic_bkg_mu_muboosted_backshapeDown',
                               'WV_semileptonic_bkg_mu_muboosted_backshapeDown',
                               vars,
                               background)

dibosonHist = RooDataHist('WV_semileptonic_SM_mu_rawshape',
                          'WV_semileptonic_SM_mu_rawshape',
                          vars,
                          diboson)
dibosonPdf = RooHistPdf('WV_semileptonic_SM_mu_shape',
                        'WV_semileptonic_SM_mu_shape',
                        varSet,
                        dibosonHist)

aTGC = RooATGCFunction('ATGC_shapescale_WWgammaZ_WV_atgc_semileptonic_mu',
                       'ATGC_shapescale_mu',
                       wpt,
                       lz,
                       dkg,
                       dg1, 
                       '%s/ATGC_shape_coefficients.root'%basepath)

aTGCPdf = RooEffProd('ATGCPdf_WWgammaZ_WV_atgc_semileptonic_mu',
                     'ATGCPdf_WV_mu',
                     dibosonPdf,
                     aTGC)

getattr(theWS, 'import')(data)
getattr(theWS, 'import')(bkgHist)
getattr(theWS, 'import')(bkgHist_systUp)
getattr(theWS, 'import')(bkgHist_systDown)
getattr(theWS, 'import')(aTGCPdf)

theWS.Print()

fout = TFile('mu_boosted_ws.root', 'recreate')
theWS.Write()
fout.Close()
