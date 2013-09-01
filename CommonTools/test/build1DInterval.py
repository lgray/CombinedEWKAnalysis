import sys

import ROOT
from ROOT import *

inputFileName = sys.argv[3]
minmax = [float(sys.argv[1]),float(sys.argv[2])]
parm = sys.argv[4]
file = TFile.Open(inputFileName,'READ')
limit = file.Get('limit')

nEntries = limit.GetEntries()-1

histo = TH1F('LLHscan','',nEntries,minmax[0],minmax[1])
limit.Draw("dkg >> LLHscan","deltaNLL",'goff')

minBin = histo.GetMinimumBin()
minBinCenter = histo.GetBinCenter(minBin)
minVal = histo.GetBinContent(minBin)

print 'Found profile-likelihood mimimum value %.3f at %.3f'%(minVal,
                                                             minBinCenter)
#skip best fit value which is entry 0
bounds = []
lastBelowErr = False
lastAboveErr = True
for i in xrange(nEntries):
    limit.GetEntry(i+1)
    NLL = limit.GetLeaf("deltaNLL").GetValue()
    if NLL - minVal <= 0.5:
        if lastAboveErr:
            bounds.append([])
            bounds[-1].append(limit.GetLeaf(parm).GetValue())
        lastBelowErr = True
        lastAboveErr = False
    else:
        if lastBelowErr:
            bounds[-1].append(limit.GetLeaf(parm).GetValue())
        lastBelowErr = False
        lastAboveErr = True
file.Close()

boundstext = ['[%.3g,%.3g]'%(b[0],b[1]) for b in bounds]
print 'U'.join(boundstext)


