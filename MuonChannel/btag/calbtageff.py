#!/bin/python
#To calculate btag efficiencies in mc
#Author: Fan Xia 6016-7-14

import os
import sys
import time
import datetime
import ROOT
from ROOT import *

from leptonANA.ElectronChannel.ana_jet import *

chain_in = ROOT.TChain("ggNtuplizer/EventTree_pre")
#chain_in.Add("../preselected/reduced_Muchannel_dataSingleMu.root")
chain_in.Add(sys.argv[1])
chain_in.SetBranchStatus("AK8*",0)
n_events = chain_in.GetEntries()
print"Total events for processing: ",n_events

file_out = ROOT.TFile("btageff_"+sys.argv[2]+".root","recreate")
file_out.cd()

ptNBins=200
ptMin=0
ptMax=1000
etaNBins=24
etaMin=-2.4
etaMax=2.4

num_bjets = ROOT.TH2F("bjets", "bjets", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_bjets.Sumw2();
num_btags = ROOT.TH2F("btags", "btags", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_btags.Sumw2();
num_cjets = ROOT.TH2F("cjets", "cjets", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_cjets.Sumw2();
num_ctags = ROOT.TH2F("ctags", "ctags", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_ctags.Sumw2();
num_ljets = ROOT.TH2F("ljets", "ljets", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_ljets.Sumw2();
num_ltags = ROOT.TH2F("ltags", "ltags", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_ltags.Sumw2();

#num_tempjets = ROOT.TH2F("tempjets", "tempjets", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_tempjets.Sumw2();
#num_temptags = ROOT.TH2F("temptags", "temptags", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_temptags.Sumw2();



for eve in range(n_events):
    chain_in.GetEntry(eve)
    if eve %10000==0: print "processing event ",eve


    for j in range(chain_in.nJet):
        Loosejet=good_LooseJet(chain_in.jetPt[j],chain_in.jetEta[j], chain_in.jetPFLooseId[j])
        Btagged=btagged(chain_in.jetpfCombinedInclusiveSecondaryVertexV2BJetTags[j])

        #----------using jetPartonID for this version
        flavor=chain_in.jetPartonID[j]

        if Loosejet: 
            if flavor in [0,1,2,3,21,-1,-2,-3]:        #light
                num_ljets.Fill(chain_in.jetPt[j],chain_in.jetEta[j])
                if Btagged: num_ltags.Fill(chain_in.jetPt[j],chain_in.jetEta[j])
            elif abs(flavor)==4:      #charm
                num_cjets.Fill(chain_in.jetPt[j],chain_in.jetEta[j])
                if Btagged: num_ctags.Fill(chain_in.jetPt[j],chain_in.jetEta[j])
            elif abs(flavor)==5:     #bottom
                num_bjets.Fill(chain_in.jetPt[j],chain_in.jetEta[j])
                if Btagged: num_btags.Fill(chain_in.jetPt[j],chain_in.jetEta[j])

#            elif flavor==0:     #other
#                num_tempjets.Fill(chain_in.jetPt[j],chain_in.jetEta[j])
#                if Btagged: num_temptags.Fill(chain_in.jetPt[j],chain_in.jetEta[j])


            else: continue





        #---------The following using jet hadron flavor(recommanded by BTV POG) which is not included in ggNtuplizer7-14
        # flavor=chain_in.jetHadFlvr[j]

        # if Loosejet: 
        #     if flavor==0:        #light
        #         num_ljets.Fill(chain_in.jetPt[j],chain_in.jetEta[j])
        #         if btagged: num_ltags.Fill(chain_in.jetPt[j],chain_in.jetEta[j])
        #     elif flavor==4:      #charm
        #         num_cjets.Fill(chain_in.jetPt[j],chain_in.jetEta[j])
        #         if btagged: num_ctags.Fill(chain_in.jetPt[j],chain_in.jetEta[j])
        #     elif flavor==5:     #bottom
        #         num_bjets.Fill(chain_in.jetPt[j],chain_in.jetEta[j])
        #         if btagged: num_btags.Fill(chain_in.jetPt[j],chain_in.jetEta[j])
        #     else: continue


lEff=num_ltags.Clone("lEff")
lEff.Divide(num_ljets)

cEff=num_ctags.Clone("cEff")
cEff.Divide(num_cjets)

bEff=num_btags.Clone("bEff")
bEff.Divide(num_bjets)

#tempEff=num_temptags.Clone("tempEff")
#tempEff.Divide(num_tempjets)
    

file_out.Write()
file_out.Close()
