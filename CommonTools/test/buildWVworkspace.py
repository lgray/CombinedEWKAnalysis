import pyroot_logon
import limits
import os
import sys

from ROOT import *

lType = sys.argv[1]
codename = ""
planeID = sys.argv[2]
sig_syst = sys.argv[3]

norm_sig_sm = -1
norm_bkg = -1
norm_obs = -1
if( lType == "muon" ) :
    codename = "muboosted"
elif( lType == "electron" ):
    codename = "elboosted"
else:
    raise RuntimeError('InvalidLepton','You may only choose between "muon" and "electron" channels.')

basepath = '%s/src/CombinedEWKAnalysis/CommonTools/data/WV_semileptonic'%os.environ['CMSSW_BASE']

f_errors = TFile.Open('%s/correctionError-wojetpTcut.root'%basepath,'READ')
f_errors.ls()
double_ratio_error = f_errors.Get('doubleRatio_dk05').Clone('doubleRatio_dk05_mine')
double_ratio_error.SetDirectory(0)
f_errors.Close()

f = TFile('%s/%s.root'%(basepath,codename))

background = f.Get('background')
background_backshapeUp = f.Get('background_%s_backshapeUp'%codename)
background_backshapeDown = f.Get('background_%s_backshapeDown'%codename)
data_obs = f.Get('data_obs')
diboson_ww = f.Get('ww')
diboson_wz = f.Get('wz')

diboson_ww_sigshapeUp = diboson_ww.Clone('ww_sigshape_up')
diboson_ww_sigshapeDown = diboson_ww.Clone('ww_sigshape_down')

for i in xrange(diboson_ww.GetNbinsX()):
    binCenter = diboson_ww.GetBinCenter(i+1)
    binContent = diboson_ww.GetBinContent(i+1)
    errorBin  = double_ratio_error.FindBin(binCenter)
    binError  = double_ratio_error.GetBinError(errorBin)    
    errup   = 1.0 + binError
    errdown = 1.0 - binError
    print binContent, binError, binContent*errup, binContent*errdown
    diboson_ww_sigshapeUp.SetBinContent(i+1,binContent*errup)
    diboson_ww_sigshapeDown.SetBinContent(i+1,binContent*errdown)

if False: #maybe ?
    background.Add(diboson_ww, -1.)
    background.Add(diboson_wz, -1.)
    background_backshapeUp.Add(diboson_ww, -1.)
    background_backshapeUp.Add(diboson_wz, -1.)
    background_backshapeDown.Add(diboson_ww, -1.)
    background_backshapeDown.Add(diboson_wz, -1.)


norm_sig_ww_sm = diboson_ww.Integral()
norm_sig_wz_sm = diboson_wz.Integral()
norm_bkg = background.Integral()
norm_obs = data_obs.Integral()

theWS = RooWorkspace('WV_%s'%codename, 'WV_%s'%codename)

wpt = theWS.factory('W_pt[%f,%f]' % (data_obs.GetBinLowEdge(1), 
                                     data_obs.GetBinLowEdge(data_obs.GetNbinsX())+data_obs.GetBinWidth(data_obs.GetNbinsX())))
wpt.setBins(data_obs.GetNbinsX())

lz = theWS.factory('lZ[0., -1., 1.]')
# lz = theWS.factory('lZ[0.]')
lz.setConstant(False)
dkg = theWS.factory('dkg[0.,-0.15, 0.15]')
dg1 = theWS.factory('dg1[0.,-0.1,0.1]')


vars = RooArgList(wpt)
varSet = RooArgSet(wpt)

data = RooDataHist('data_obs_WVsemileptonic_%s'%codename, 'data_obs_WVsemileptonic_%s'%codename, vars, data_obs)
bkgHist = RooDataHist('bkg_%s_WVsemileptonic_%s'%(codename,codename),
                      'bkg_%s_WVsemileptonic_%s'%(codename,codename),
                      vars,
                      background)
bkgHist_systUp = RooDataHist('bkg_%s_WVsemileptonic_%s_backshapeUp'%(codename,codename),
                             'bkg_%s_WVsemileptonic_%s_backshapeUp'%(codename,codename),
                             vars,
                             background_backshapeUp)
bkgHist_systDown = RooDataHist('bkg_%s_WVsemileptonic_%s_backshapeDown'%(codename,codename),
                               'bkg_%s_WVsemileptonic_%s_backshapeDown'%(codename,codename),
                               vars,
                               background_backshapeDown)

wwHist = RooDataHist('WW_SM_semileptonic_%s_rawshape'%codename,
                     'WW_SM_semileptonic_%s_rawshape'%codename,
                     vars,
                     diboson_ww)
wwPdf = RooHistFunc('WW_SM_semileptonic_%s_shape'%codename,
                    'WW_SM_semileptonic_%s_shape'%codename,
                    varSet,
                    wwHist)

wwHist_up = RooDataHist('WW_SM_semileptonic_%s_sigShapeUp_rawshape'%codename,
                        'WW_SM_semileptonic_%s_sigShapeUp_rawshape'%codename,
                        vars,
                        diboson_ww_sigshapeUp)
wwPdf_up = RooHistFunc('WW_SM_semileptonic_%s_sigShapeUp_shape'%codename,
                       'WW_SM_semileptonic_%s_sigShapeUp_shape'%codename,
                       varSet,
                       wwHist_up)

wwHist_down = RooDataHist('WW_SM_semileptonic_%s_sigShapeDown_rawshape'%codename,
                          'WW_SM_semileptonic_%s_sigShapeDown_rawshape'%codename,
                          vars,
                          diboson_ww_sigshapeDown)
wwPdf_down = RooHistFunc('WW_SM_semileptonic_%s_sigShapeDown_shape'%codename,
                         'WW_SM_semileptonic_%s_sigShapeDown_shape'%codename,
                         varSet,
                         wwHist_down)

wzHist = RooDataHist('WZ_SM_semileptonic_%s_rawshape'%codename,
                     'WZ_SM_semileptonic_%s_rawshape'%codename,
                     vars,
                     diboson_wz)
wzPdf = RooHistFunc('WZ_SM_semileptonic_%s_shape'%codename,
                    'WZ_SM_semileptonic_%s_shape'%codename,
                    varSet,
                    wzHist)

#aTGC_ww = RooATGCFunction('ATGC_shapescale_WWgammaZ_WW_atgc_semileptonic_%s'%codename,
#                          'ATGC_shapescale_ww_%s'%codename,
#                          wpt,
#                          lz,
#                          dkg,
#                          dg1, 
#                          '%s/ww_ATGC_shape_coefficients.root'%basepath)

#aTGC_wz = RooATGCFunction('ATGC_shapescale_WWgammaZ_WZ_atgc_semileptonic_%s'%codename,
#                          'ATGC_shapescale_wz_%s'%codename,
#                          wpt,
#                          lz,
#                          dkg,
#                          dg1, 
#                          '%s/wz_ATGC_shape_coefficients.root'%basepath)

limtype = -1

print 'setting up for %s plane!'%planeID
if ( planeID == 'dkglZ' ):
    limtype = 0
elif ( planeID == 'dg1lZ' ):
    limtype = 1
elif ( planeID == 'dkgdg1'):
    limtype = 2
else:
    raise RuntimeError('InvalidCouplingChoice',
                       'We can only use [dkg,lZ], [dg1,lZ], and [dkg,dg1]'\
                       ' as POIs right now!')

print limtype

aTGCPdf_ww = RooATGCSemiAnalyticPdf('ATGCPdf_WWgammaZ_WW_WVsemileptonic_%s__'%codename,
                                    'ATGCPdf_WW_%s'%codename,
                                    wpt,
                                    dkg,
                                    lz,                                 
                                    dg1,
                                    wwPdf,
                                    '%s/ww_ATGC_shape_coefficients.root'%basepath,
                                    limtype)

aTGCPdf_ww_up = RooATGCSemiAnalyticPdf('ATGCPdf_WWgammaZ_WW_WVsemileptonic_%s_sigShapeUp'%codename,
                                       'ATGCPdf_WW_%s'%codename,
                                       wpt,
                                       dkg,
                                       lz,
                                       dg1,
                                       wwPdf_up,
                                       '%s/ww_ATGC_shape_coefficients.root'%basepath,
                                       limtype)

aTGCPdf_ww_down = RooATGCSemiAnalyticPdf('ATGCPdf_WWgammaZ_WW_WVsemileptonic_%s_sigShapeDown'%codename,
                                         'ATGCPdf_WW_%s'%codename,
                                         wpt,
                                         dkg,
                                         lz,
                                         dg1,
                                         wwPdf_down,
                                         '%s/ww_ATGC_shape_coefficients.root'%basepath,
                                         limtype)

aTGCPdf_wz = RooATGCSemiAnalyticPdf('ATGCPdf_WWgammaZ_WZ_WVsemileptonic_%s'%codename,
                                    'ATGCPdf_WZ_%s'%codename,
                                    wpt,                                    
                                    dkg,
                                    lz,                                 
                                    dg1,
                                    wzPdf,
                                    '%s/wz_ATGC_shape_coefficients.root'%basepath,
                                    limtype)


getattr(theWS, 'import')(data)
getattr(theWS, 'import')(bkgHist)
getattr(theWS, 'import')(bkgHist_systUp)
getattr(theWS, 'import')(bkgHist_systDown)
getattr(theWS, 'import')(wwHist)
getattr(theWS, 'import')(aTGCPdf_ww)
getattr(theWS, 'import')(wwHist_up)
getattr(theWS, 'import')(aTGCPdf_ww_up)
getattr(theWS, 'import')(wwHist_down)
getattr(theWS, 'import')(aTGCPdf_ww_down)
getattr(theWS, 'import')(wzHist)
getattr(theWS, 'import')(aTGCPdf_wz)

theWS.Print()

fout = TFile('WVsemileptonic_%s_%s_ws.root'%(codename,planeID), 'recreate')
theWS.Write()
fout.Close()

### make the card for this channel and plane ID
card = """
# Simple counting experiment, with one signal and a few background processes 
imax 1  number of channels
jmax *  number of backgrounds
kmax *  number of nuisance parameters (sources of systematical uncertainties)
------------
shapes bkg_{codename} WVsemileptonic_{codename} ./WVsemileptonic_{codename}_{planeID}_ws.root WV_{codename}:$PROCESS_$CHANNEL WV_{codename}:$PROCESS_$SYSTEMATIC
shapes data_obs       WVsemileptonic_{codename} ./WVsemileptonic_{codename}_{planeID}_ws.root WV_{codename}:$PROCESS_$CHANNEL
shapes WWgammaZ_WZ    WVsemileptonic_{codename} ./WVsemileptonic_{codename}_{planeID}_ws.root WV_{codename}:ATGCPdf_$PROCESS_$CHANNEL
shapes WWgammaZ_WW    WVsemileptonic_{codename} ./WVsemileptonic_{codename}_{planeID}_ws.root WV_{codename}:ATGCPdf_$PROCESS_$CHANNEL_{sig_syst}
------------
bin WVsemileptonic_{codename} 
observation {norm_obs}
------------
bin                         WVsemileptonic_{codename}     WVsemileptonic_{codename}     WVsemileptonic_{codename}
process                     WWgammaZ_WW                   WWgammaZ_WZ                   bkg_{codename}
process                     -1			          0			        1		
rate                        {norm_sig_ww_sm}		  {norm_sig_wz_sm}		{norm_bkg}	

------------
lumi_8TeV                       lnN     1.026    		  1.026  		    -
CMS_eff_{codename[0]}           lnN     1.02                      1.02                      -
CMS_trigger_{codename[0]}       lnN     1.01                      1.01                      -
WVsemileptonic_{codename}_backshape            shape1  -                         -                         1.0 
sigXSsyst                       lnN     1.034                     1.034                     -
""".format(codename=codename,planeID=planeID,
           norm_sig_ww_sm=norm_sig_ww_sm,
           norm_sig_wz_sm=norm_sig_wz_sm,
           sig_syst=sig_syst,
           norm_bkg=norm_bkg,norm_obs=norm_obs)

print card

cardfile = open('wv_semil_%s_%s_%s.txt'%(codename,planeID,sig_syst),'w')
cardfile.write(card)
cardfile.close()
