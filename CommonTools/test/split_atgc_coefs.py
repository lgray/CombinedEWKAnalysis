import ROOT
from ROOT import TFile
import sys

to_split = ['ww','wz']

fname = sys.argv[1]
infile = TFile.Open(fname,'READ')

for pfx in to_split:
    outfile = TFile.Open('%s_%s'%(pfx,fname.split('/')[-1]),'RECREATE')
    for i in range(7):
        lambda_dkg = infile.Get('%s_p%i_lambda_dkg'%(pfx,i))
        if not not lambda_dkg:
            lambda_dkg = lambda_dkg.Clone('p%i_lambda_dkg'%i)
            lambda_dkg.SetDirectory(outfile)
            lambda_dkg.Write()
        lambda_dg1 = infile.Get('%s_p%i_lambda_dg1'%(pfx,i))
        if not not lambda_dg1:
            lambda_dg1 = lambda_dg1.Clone('p%i_lambda_dg1'%i)
            lambda_dg1.SetDirectory(outfile)
            lambda_dg1.Write()
        dkg_dg1    = infile.Get('%s_p%i_dkg_dg1'%(pfx,i))
        if not not dkg_dg1:
            dkg_dg1 = dkg_dg1.Clone('p%i_dkg_dg1'%i)
            dkg_dg1.SetDirectory(outfile)
            dkg_dg1.Write()
    outfile.Close()
infile.Close()
