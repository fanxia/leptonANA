#!/bin/python

import ROOT
import sys
import os
from ROOT import *

idsf=TFile.Open('MuonID_Z_RunCD_Reco74X_Dec1.root')
isosf=TFile.Open('MuonIso_Z_RunCD_Reco74X_Dec1.root')
trgsf=TFile.Open('SingleMuonTrigger_Z_RunCD_Reco74X_Dec1.root')
newfile=ROOT.TFile("muonsf.root","recreate")

h_idsf=ROOT.TH2F()
h_isosf=ROOT.TH2F()
h_trgsf=ROOT.TH2F()

h_idsf=idsf.Get("NUM_TightIDandIPCut_DEN_genTracks_PAR_pt_spliteta_bin1/pt_abseta_ratio").Clone('tightidsf')
h_isosf=isosf.Get("NUM_TightRelIso_DEN_TightID_PAR_pt_spliteta_bin1/pt_abseta_ratio").Clone('tightisosf')
h_trgsf=trgsf.Get("runD_IsoMu20_OR_IsoTkMu20_HLTv4p3_PtEtaBins/pt_abseta_ratio").Clone('trigsf')

newfile.Write()
newfile.Close()
