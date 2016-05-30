#!/bin/python
# May24.2016 by Fan Xia
# This template uses the skim EventTree from dir:selected as input, using user defined branches to make plots 
# region branch is to indentify the pre, sr1, sr2, cr1, cr2
# For mc, has the weight factor;for data, set weight=1

import os
import sys
import time
import datetime
import ROOT
from ROOT import *
from array import array
from leptonANA.ElectronChannel.ana_muon import *
from leptonANA.ElectronChannel.ana_ele import *
from leptonANA.ElectronChannel.ana_jet import *
from leptonANA.ElectronChannel.ana_fake import *
from leptonANA.ElectronChannel.ana_pho import *
from leptonANA.ElectronChannel.Utilfunc import *

dd=datetime.datetime.now().strftime("%b%d")
sw = ROOT.TStopwatch()
sw.Start()
print "start"
print "input: "+sys.argv[1]
print "output: "+sys.argv[2]
chain_in = ROOT.TChain("EventTree")
chain_in.Add(sys.argv[1])
if hasattr(chain_in,'totalweight'): print "The input is mc"
else: print "The input is data"

n_events = chain_in.GetEntries()
print"Total events for processing: ",n_events


os.system('mkdir -p outplot_'+dd)
os.chdir('outplot_'+dd)
file_out = ROOT.TFile("skimplot_"+sys.argv[2]+".root","recreate")

#------------define hists' bin size
#nxbin_pt=18
xbin_pt=array('d',[0,20,40,60,80,100,120,140,160,180,200,250,300,400,500,600,800,1000,1250])
#nxbin_met=11
xbin_met=array('d',[0,20,40,60,80,100,150,200,250,300,500,1000])



#--------------------define hists
pre_SingleMuPt = ROOT.TH1F("pre_SingleMuPt","",17,xbin_pt)
pre_SingleMuEta = ROOT.TH1F("pre_SingleMuEta","",60,-3,3)
pre_nPho = ROOT.TH1F("pre_nPho","",5,0,5)
pre_nFake = ROOT.TH1F("pre_nFake","",5,0,5)
pre_nJet = ROOT.TH1F("pre_nJet","",20,0,20)
preMET = ROOT.TH1F("preMET","",11,xbin_met)
pre_LeadBjetPt = ROOT.TH1F("pre_LeadBjetPt","",17,xbin_pt)
pre_nJet_nbJet = ROOT.TH2F("pre_nJet_nbJet","",20,0,20,10,0,10)
pre_jetHt = ROOT.TH1F("pre_jetHt","",18,xbin_pt)

SR1_SingleMuPt = ROOT.TH1F("SR1_SingleMuPt","",16,xbin_pt)
SR1dR_pho_mu = ROOT.TH1F("SR1dR_pho_mu","",100,0,10)
SinglePhoEt = ROOT.TH1F("SinglePhoEt","",17,xbin_pt)
SinglePhoEta = ROOT.TH1F("SinglePhoEta","",60,-3,3)
SinglePhoR9 = ROOT.TH1F("SinglePhoR9","",60,0,1.2)
SinglePhoSigmaIEtaIEta = ROOT.TH1F("SinglePhoSigmaIEtaIEta","",100,0,0.05)
SinglePhoSigmaIPhiIPhi = ROOT.TH1F("SinglePhoSigmaIPhiIPhi","",100,0,0.1)
SR1MET = ROOT.TH1F("SR1MET","",11,xbin_met)
SR1_LeadBjetPt = ROOT.TH1F("SR1_LeadBjetPt","",17,xbin_pt)
SR1_nJet_nbJet = ROOT.TH2F("SR1_nJet_nbJet","",15,0,15,10,0,10)
SR1invmupho = ROOT.TH1F("SR1invmupho","",11,xbin_met)
SR1_jetHt = ROOT.TH1F("SR1_jetHt","",18,xbin_pt)
#SR1_nJet_nbJet_ratio = ROOT.TH2F("SR1_nJet_nbJet_ratio","SR1_nJet_nbJet_ratio",15,0,15,10,0,10)


SR2phodR = ROOT.TH1F("SR2phodR","",100,0,10)
SR2_SingleMuPt = ROOT.TH1F("SR2_SingleMuPt","",16,xbin_pt)
diPhotonM = ROOT.TH1F("diPhotonM","",11,xbin_met)
SR2MET = ROOT.TH1F("SR2MET","",11,xbin_met)
SR2nPho = ROOT.TH1F("SR2nPho","",5,0,5)
diPhotonM_MET = ROOT.TH2F("diPhotonM_MET","",100,0,1000,100,0,1000)
SR2_LeadBjetPt = ROOT.TH1F("SR2_LeadBjetPt","",17,xbin_pt)
LeadPhoEt = ROOT.TH1F("LeadPhoEt","",16,xbin_pt)
TrailPhoEt = ROOT.TH1F("TrailPhoEt","",16,xbin_pt)
SR2_nJet_nbJet = ROOT.TH2F("SR2_nJet_nbJet","",15,0,15,10,0,10)
SR2_jetHt = ROOT.TH1F("SR2_jetHt","",18,xbin_pt)
#SR2_nJet_nbJet_ratio = ROOT.TH2F("SR2_nJet_nbJet_ratio","SR2_nJet_nbJet_ratio",15,0,15,10,0,10)


CR1_SingleMuPt = ROOT.TH1F("CR1_SingleMuPt","",16,xbin_pt)
CR1dR_fake_mu = ROOT.TH1F("CR1dR_fake_mu","",100,0,10)
SingleFakeEt = ROOT.TH1F("SingleFakeEt","",17,xbin_pt)
SingleFakeEta = ROOT.TH1F("SingleFakeEta","",60,-3,3)
SingleFakeR9 = ROOT.TH1F("SingleFakeR9","",60,0,1.2)
SingleFakeSigmaIEtaIEta = ROOT.TH1F("SingleFakeSigmaIEtaIEta","",100,0,0.05)
SingleFakeSigmaIPhiIPhi = ROOT.TH1F("SingleFakeSigmaIPhiIPhi","",100,0,0.1)
CR1MET = ROOT.TH1F("CR1MET","",11,xbin_met)
CR1_LeadBjetPt = ROOT.TH1F("CR1_LeadBjetPt","",17,xbin_pt)
CR1_nJet_nbJet = ROOT.TH2F("CR1_nJet_nbJet","",15,0,15,10,0,10)
CR1invmufake = ROOT.TH1F("CR1invmufake","",11,xbin_met)
CR1_jetHt = ROOT.TH1F("CR1_jetHt","",18,xbin_pt)
#CR1_nJet_nbJet_ratio = ROOT.TH2F("CR1_nJet_nbJet_ratio","CR1_nJet_nbJet_ratio",15,0,15,10,0,10)



CR2_SingleMuPt = ROOT.TH1F("CR2_SingleMuPt","",16,xbin_pt)
diFakeM = ROOT.TH1F("diFakeM","",11,xbin_met)
CR2MET = ROOT.TH1F("CR2MET","",11,xbin_met)
CR2nFake = ROOT.TH1F("CR2nFake","",5,0,5)
diFakeM_MET = ROOT.TH2F("diFakeM_MET","",100,0,1000,100,0,1000)
CR2_LeadBjetPt = ROOT.TH1F("CR2_LeadBjetPt","",17,xbin_pt)
LeadFakeEt = ROOT.TH1F("LeadFakeEt","",16,xbin_pt)
TrailFakeEt = ROOT.TH1F("TrailFakeEt","",16,xbin_pt)
CR2_nJet_nbJet = ROOT.TH2F("CR2_nJet_nbJet","",15,0,15,10,0,10)
CR2_jetHt = ROOT.TH1F("CR2_jetHt","",18,xbin_pt)
#CR2_nJet_nbJet_ratio = ROOT.TH2F("CR2_nJet_nbJet_ratio","CR2_nJet_nbJet_ratio",15,0,15,10,0,10)
#------------



TRVSR2pho1=ROOT.TLorentzVector()
TRVSR2pho2=ROOT.TLorentzVector()
TRVSR1pho=ROOT.TLorentzVector()
TRVCR2fake1=ROOT.TLorentzVector()
TRVCR2fake2=ROOT.TLorentzVector()
TRVCR1fake=ROOT.TLorentzVector()
TRVmu=ROOT.TLorentzVector()




#for i in range(1000):
for i in range(n_events):
    chain_in.GetEntry(i)
    
    if i%1000 ==0:
        print "Processing entry ", i
    if hasattr(chain_in,'totalweight'): weight=chain_in.totalweight
    else: weight=1.0

    TRVmu.SetPtEtaPhiM(chain_in.muPt,chain_in.muEta,chain_in.muPhi,0.000511)

    jetht=0
    for j in range(chain_in.njet):
        jetht=jetht+chain_in.jetPt[j]
    leadbjet_ind=max(range(chain_in.nbjet),key=lambda x: chain_in.bjetPt[x])

#-----------fill the pre region plots
    
    pre_nPho.Fill(chain_in.nPho,weight)
    pre_nFake.Fill(chain_in.nFake,weight)
    pre_SingleMuPt.Fill(chain_in.muPt,weight)
    pre_SingleMuEta.Fill(chain_in.muEta,weight)
    pre_nJet_nbJet.Fill(chain_in.njet,chain_in.nbjet,weight)
    pre_LeadBjetPt.Fill(chain_in.bjetPt[leadbjet_ind],weight)
    preMET.Fill(chain_in.pfMET,weight)
    pre_nJet.Fill(chain_in.njet,weight)
    pre_jetHt.Fill(jetht,weight)

#-------------------------below for signal region1 &2
    if chain_in.region==1:
        TRVSR1pho.SetPtEtaPhiM(chain_in.phoEt[0],chain_in.phoEta[0],chain_in.phoPhi[0],0.0)
        SR1MET.Fill(chain_in.pfMET,weight)
        dRphoton_mu = dR(chain_in.phoEta[0],chain_in.muEta,chain_in.phoPhi[0],chain_in.muPhi)
        SR1dR_pho_mu.Fill(dRphoton_mu,weight)
        SinglePhoEt.Fill(chain_in.phoEt[0],weight)
        SinglePhoEta.Fill(chain_in.phoEta[0],weight)
        SinglePhoR9.Fill(chain_in.phoR9[0],weight)
        SinglePhoSigmaIPhiIPhi.Fill(chain_in.phoSigmaIPhiIPhi[0],weight)
        SinglePhoSigmaIEtaIEta.Fill(chain_in.phoSigmaIEtaIEta[0],weight)
        SR1invmupho.Fill((TRVmu+TRVSR1pho).M(),weight)

        SR1_nJet_nbJet.Fill(chain_in.njet,chain_in.nbjet,weight)
#        SR1_nJet_nbJet_ratio.Fill(n_jet,n_bjet,weight)
        SR1_SingleMuPt.Fill(chain_in.muPt,weight)
        SR1_LeadBjetPt.Fill(chain_in.bjetPt[leadbjet_ind],weight)
        SR1_jetHt.Fill(jetht,weight)
    elif chain_in.region==2:    
        leadpho_ind=max(range(chain_in.nPho),key=lambda x: chain_in.phoEt[x])
        trailpho_ind=max([pp for pp in range(chain_in.nPho) if pp!=leadpho_ind],key=lambda x: chain_in.phoEt[x])
        TRVSR2pho1.SetPtEtaPhiM(chain_in.phoEt[leadpho_ind],chain_in.phoEta[leadpho_ind],chain_in.phoPhi[leadpho_ind],0.0)
        TRVSR2pho2.SetPtEtaPhiM(chain_in.phoEt[trailpho_ind],chain_in.phoEta[trailpho_ind],chain_in.phoPhi[trailpho_ind],0.0)
        phodR=TRVSR2pho1.DeltaR(TRVSR2pho2)
        SR2phodR.Fill(phodR,weight)
        SR2nPho.Fill(chain_in.nPho,weight)
        diPhotonM.Fill((TRVSR2pho1+TRVSR2pho2).M(),weight)
        SR2MET.Fill(chain_in.pfMET,weight)
        SR2_SingleMuPt.Fill(chain_in.muPt,weight)
        diPhotonM_MET.Fill((TRVSR2pho1+TRVSR2pho2).M(),chain_in.pfMET,weight)
        LeadPhoEt.Fill(chain_in.phoEt[leadpho_ind],weight)
        TrailPhoEt.Fill(chain_in.phoEt[trailpho_ind],weight)
        SR2_LeadBjetPt.Fill(chain_in.bjetPt[leadbjet_ind],weight)
        SR2_nJet_nbJet.Fill(chain_in.njet,chain_in.nbjet,weight)
        SR2_jetHt.Fill(jetht,weight)
#------------------------------below for control region 1&2 depends on fake numbers
    elif chain_in.region==3:
        TRVCR1fake.SetPtEtaPhiM(chain_in.fakeEt[0],chain_in.fakeEta[0],chain_in.fakePhi[0],0.0)
        CR1MET.Fill(chain_in.pfMET,weight)
        dRfake_mu = dR(chain_in.fakeEta[0],chain_in.muEta,chain_in.fakePhi[0],chain_in.muPhi)
        CR1dR_fake_mu.Fill(dRfake_mu,weight)
        SingleFakeEt.Fill(chain_in.fakeEt[0],weight)
        SingleFakeEta.Fill(chain_in.fakeEta[0],weight)
        SingleFakeR9.Fill(chain_in.fakeR9[0],weight)
        SingleFakeSigmaIPhiIPhi.Fill(chain_in.fakeSigmaIPhiIPhi[0],weight)
        SingleFakeSigmaIEtaIEta.Fill(chain_in.fakeSigmaIEtaIEta[0],weight)
        CR1invmufake.Fill((TRVmu+TRVCR1fake).M(),weight)

        CR1_nJet_nbJet.Fill(chain_in.njet,chain_in.nbjet,weight)
#        SR1_nJet_nbJet_ratio.Fill(n_jet,n_bjet,weight)
        CR1_SingleMuPt.Fill(chain_in.muPt,weight)
        CR1_LeadBjetPt.Fill(chain_in.bjetPt[leadbjet_ind],weight)
        CR1_jetHt.Fill(jetht,weight)
    elif chain_in.region==4:    
        leadfake_ind=max(range(chain_in.nFake),key=lambda x: chain_in.fakeEt[x])
        trailfake_ind=max([pp for pp in range(chain_in.nFake) if pp!=leadfake_ind],key=lambda x: chain_in.fakeEt[x])
        TRVCR2fake1.SetPtEtaPhiM(chain_in.fakeEt[leadfake_ind],chain_in.fakeEta[leadfake_ind],chain_in.fakePhi[leadfake_ind],0.0)
        TRVCR2fake2.SetPtEtaPhiM(chain_in.fakeEt[trailfake_ind],chain_in.fakeEta[trailfake_ind],chain_in.fakePhi[trailfake_ind],0.0)
        CR2nFake.Fill(chain_in.nFake,weight)
        diFakeM.Fill((TRVCR2fake1+TRVCR2fake2).M(),weight)
        CR2MET.Fill(chain_in.pfMET,weight)
        CR2_SingleMuPt.Fill(chain_in.muPt,weight)
        diFakeM_MET.Fill((TRVCR2fake1+TRVCR2fake2).M(),chain_in.pfMET,weight)
        LeadFakeEt.Fill(chain_in.fakeEt[leadfake_ind],weight)
        TrailFakeEt.Fill(chain_in.fakeEt[trailfake_ind],weight)
        CR2_LeadBjetPt.Fill(chain_in.bjetPt[leadbjet_ind],weight)
        CR2_nJet_nbJet.Fill(chain_in.njet,chain_in.nbjet,weight)
        CR2_jetHt.Fill(jetht,weight)

#-------------------print plots and save to root file

gStyle.SetTitleOffset(1.2, "xy")
gStyle.SetOptStat(0)

#gStyle.SetPadBottomMargin(0.2)
#gStyle.SetTitleFont(63,"xy")
#gStyle.SetTitleY(0.7)
gROOT.ForceStyle()


c=ROOT.TCanvas("c","Plots",1000,800)
Header=ROOT.TPaveText(0.06,0.901,0.38,0.94,"NDC")
Header.SetFillColor(0)
Header.SetFillStyle(0)
Header.SetLineColor(0)
Header.SetBorderSize(0)
Header.AddText("2015 pp #sqrt{s} = 13 TeV")
preComment=ROOT.TPaveText(0.55,0.55,0.85,0.65,"NDC")
preComment.SetFillColor(0)
preComment.SetFillStyle(0)
preComment.SetLineColor(0)
preComment.SetBorderSize(0)
preComment.AddText("Pre-selection muon")
preComment.SetTextColor(601)

sr1Comment=ROOT.TPaveText(0.57,0.57,0.83,0.63,"NDC")
sr1Comment.SetFillColor(0)
sr1Comment.SetFillStyle(0)
sr1Comment.SetLineColor(0)
sr1Comment.SetBorderSize(0)
sr1Comment.AddText("SR1 muon")
sr1Comment.SetTextColor(601)

sr2Comment=ROOT.TPaveText(0.57,0.57,0.83,0.63,"NDC")
sr2Comment.SetFillColor(0)
sr2Comment.SetFillStyle(0)
sr2Comment.SetLineColor(0)
sr2Comment.SetBorderSize(0)
sr2Comment.AddText("SR2 muon")
sr2Comment.SetTextColor(601)

cr1Comment=ROOT.TPaveText(0.57,0.57,0.83,0.63,"NDC")
cr1Comment.SetFillColor(0)
cr1Comment.SetFillStyle(0)
cr1Comment.SetLineColor(0)
cr1Comment.SetBorderSize(0)
cr1Comment.AddText("CR1 muon")
cr1Comment.SetTextColor(601)

cr2Comment=ROOT.TPaveText(0.57,0.57,0.83,0.63,"NDC")
cr2Comment.SetFillColor(0)
cr2Comment.SetFillStyle(0)
cr2Comment.SetLineColor(0)
cr2Comment.SetBorderSize(0)
cr2Comment.AddText("CR2 muon")
cr2Comment.SetTextColor(601)

gStyle.SetTitleOffset(1.2, "xy")
gStyle.SetOptStat(0)
#gStyle.SetPadBottomMargin(0.2)
gStyle.SetTitleFont(42,"xy")
#gStyle.SetTitleY(0.7)
gROOT.ForceStyle()


c.cd()
pre_nPho.Sumw2()
pre_nPho.Draw("HIST")
pre_nPho.SetTitle(";N_{#gamma}; N_events    ")
Header.Draw("same")
preComment.Draw("same")
pre_nPho.UseCurrentStyle()
gPad.SetLogy()
#gPad.Update()
c.Print(sys.argv[2]+".pdf(")

c.Clear()
pre_nFake.Sumw2()
pre_nFake.Draw("hist")
pre_nFake.SetTitle(";N_{fake}; N_events    ")
Header.Draw("same")
preComment.Draw("same")
pre_nFake.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
pre_nJet.Sumw2()
pre_nJet.Draw("hist")
pre_nJet.SetTitle(";N_{Jet}; N_events    ")
Header.Draw("same")
preComment.Draw("same")
pre_nJet.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
preMET.Sumw2()
preMET.Scale(1,"width")
preMET.Draw("hist")
Header.Draw("same")
preComment.Draw("same")
preMET.UseCurrentStyle()
preMET.SetTitle(";pfMET (GeV);N_events / GeV    ")
c.Print(sys.argv[2]+".pdf")


c.Clear()
pre_SingleMuPt.Sumw2()
pre_SingleMuPt.Scale(1,"width")
pre_SingleMuPt.Draw("hist")
Header.Draw("same")
preComment.Draw("same")
pre_SingleMuPt.UseCurrentStyle()
pre_SingleMuPt.SetTitle(";#mu_{Pt} (GeV/c);N_events / GeV    ")
c.Print(sys.argv[2]+".pdf")


c.Clear()
pre_SingleMuEta.Sumw2()
pre_SingleMuEta.Draw("hist")
Header.Draw("same")
preComment.Draw("same")
pre_SingleMuEta.UseCurrentStyle()
pre_SingleMuEta.SetTitle(";#mu_Eta;N_events    ")
c.Print(sys.argv[2]+".pdf")


c.Clear()
pre_LeadBjetPt.Sumw2()
pre_LeadBjetPt.Scale(1,"width")
pre_LeadBjetPt.Draw("hist")
Header.Draw("same")
preComment.Draw("same")
pre_LeadBjetPt.UseCurrentStyle()
pre_LeadBjetPt.SetTitle(";Lead bjet_Pt (GeV/c);N_events / GeV    ")
c.Print(sys.argv[2]+".pdf")


c.Clear()
pre_jetHt.Sumw2()
pre_jetHt.Scale(1,"width")
pre_jetHt.Draw("HIST")
Header.Draw("same")
preComment.Draw("same")
pre_jetHt.UseCurrentStyle()
pre_jetHt.SetTitle("; H_{T}_jets;N_events / GeV    ")
c.Print(sys.argv[2]+".pdf")

c.Clear()
SR1MET.Sumw2()
SR1MET.Scale(1,"width")
SR1MET.Draw("hist")
SR1MET.SetTitle(";pfMET (GeV);N_events / GeV   ")
Header.Draw("same")
sr1Comment.Draw("same")
SR1MET.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")

c.Clear()
SR1dR_pho_mu.Sumw2()
SR1dR_pho_mu.Draw("hist")
Header.Draw("same")
sr1Comment.Draw("same")
SR1dR_pho_mu.UseCurrentStyle()
SR1dR_pho_mu.SetTitle(";#deltaR #mu,#gamma;N_events   ")
c.Print(sys.argv[2]+".pdf")

c.Clear()
SR1_SingleMuPt.Sumw2()
SR1_SingleMuPt.Scale(1,"width")
SR1_SingleMuPt.Draw("hist")
SR1_SingleMuPt.SetTitle(";mu_P_{T} (GeV/c);N_events / GeV   ")
Header.Draw("same")
sr1Comment.Draw("same")
SR1_SingleMuPt.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
SinglePhoR9.Sumw2()
SinglePhoR9.Draw("hist")
SinglePhoR9.SetTitle(";#gamma_{R9};N_events   ")
Header.Draw("same")
sr1Comment.Draw("same")
SinglePhoR9.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
SinglePhoSigmaIEtaIEta.Sumw2()
SinglePhoSigmaIEtaIEta.Draw("hist")
SinglePhoSigmaIEtaIEta.SetTitle(";#gamma: #sigma_{i#etai#eta};N_events   ")
Header.Draw("same")
sr1Comment.Draw("same")
SinglePhoSigmaIEtaIEta.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
SinglePhoSigmaIPhiIPhi.Sumw2()
SinglePhoSigmaIPhiIPhi.Draw("hist")
SinglePhoSigmaIPhiIPhi.SetTitle(";#gamma: #sigma_{i#phii#phi};N_events   ")
Header.Draw("same")
sr1Comment.Draw("same")
SinglePhoSigmaIPhiIPhi.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
SinglePhoEt.Sumw2()
SinglePhoEt.Scale(1,"width")
SinglePhoEt.Draw("hist")
SinglePhoEt.SetTitle(";#gamma_{E_{T}} (GeV);N_events / GeV   ")
Header.Draw("same")
sr1Comment.Draw("same")
SinglePhoEt.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")

c.Clear()
SinglePhoEta.Sumw2()
SinglePhoEta.Draw("hist")
SinglePhoEta.SetTitle(";#gamma_Eta;N_events   ")
Header.Draw("same")
sr1Comment.Draw("same")
SinglePhoEta.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
SR1_LeadBjetPt.Sumw2()
SR1_LeadBjetPt.Scale(1,"width")
SR1_LeadBjetPt.Draw("hist")
SR1_LeadBjetPt.SetTitle(";Lead bjet_Pt (GeV/c);N_events / GeV   ")
Header.Draw("same")
sr1Comment.Draw("same")
SR1_LeadBjetPt.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
SR1invmupho.Sumw2()
SR1invmupho.Scale(1,"width")
SR1invmupho.SetTitle(";m_{e#gamma};N_events / GeV   ")
SR1invmupho.Draw("hist")
Header.Draw("same")
sr1Comment.Draw("same")
SR1invmupho.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
SR1_jetHt.Sumw2()
SR1_jetHt.Scale(1,"width")
SR1_jetHt.Draw("hist")
Header.Draw("same")
sr1Comment.Draw("same")
SR1_jetHt.UseCurrentStyle()
SR1_jetHt.SetTitle("; H_{T}_jets;N_events / GeV   ")
c.Print(sys.argv[2]+".pdf")


c.Clear()
SR2phodR.Sumw2()
SR2phodR.Draw("hist")
SR2phodR.SetTitle(";#deltaR(#gamma,#gamma);N_events   ")
Header.Draw("same")
sr2Comment.Draw("same")
SR2phodR.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")



c.Clear()
SR2_SingleMuPt.Sumw2()
SR2_SingleMuPt.Scale(1,"width")
SR2_SingleMuPt.Draw("hist")
SR2_SingleMuPt.SetTitle(";mu_Pt (GeV/c);N_events / GeV   ")
Header.Draw("same")
sr2Comment.Draw("same")
SR2_SingleMuPt.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
SR2MET.Sumw2()
SR2MET.Scale(1,"width")
SR2MET.Draw("e")
SR2MET.SetTitle(";pfMET (GeV);N_events / GeV   ")
gPad.SetLogy()
gPad.Update()
Header.Draw("same")
sr2Comment.Draw("same")
SR2MET.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")

c.Clear()
diPhotonM.Sumw2()
diPhotonM.Scale(1,"width")
diPhotonM.Draw("e")
diPhotonM.SetTitle(";m_{#gamma#gamma} (GeV);N_events / GeV   ")
Header.Draw("same")
sr2Comment.Draw("same")
diPhotonM.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
SR2nPho.Sumw2()
SR2nPho.Draw("hist")
SR2nPho.SetTitle(";N_{#gamma};N_events   ")
Header.Draw("same")
sr2Comment.Draw("same")
SR2nPho.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
LeadPhoEt.Sumw2()
LeadPhoEt.Scale(1,"width")
LeadPhoEt.Draw("hist")
LeadPhoEt.SetTitle(";Lead #gamma_Et(GeV);N_events / GeV   ")
Header.Draw("same")
sr2Comment.Draw("same")
LeadPhoEt.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
TrailPhoEt.Sumw2()
TrailPhoEt.Scale(1,"width")
TrailPhoEt.Draw("hist")
TrailPhoEt.SetTitle(";Trail #gamma_Et(GeV);N_events / GeV   ")
Header.Draw("same")
sr2Comment.Draw("same")
TrailPhoEt.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
SR2_LeadBjetPt.Sumw2()
SR2_LeadBjetPt.Scale(1,"width")
SR2_LeadBjetPt.Draw("hist")
SR2_LeadBjetPt.SetTitle(";Lead bjet_Pt (GeV/c);N_events / GeV   ")
Header.Draw("same")
sr2Comment.Draw("same")
c.Print(sys.argv[2]+".pdf")


c.Clear()
SR2_jetHt.Sumw2()
SR2_jetHt.Scale(1,"width")
SR2_jetHt.Draw("hist")
SR2_jetHt.SetTitle("; HT_jets;N_events / GeV   ")
Header.Draw("same")
sr2Comment.Draw("same")
SR2_jetHt.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")

c.Clear()
CR1MET.Sumw2()
CR1MET.Scale(1,"width")
CR1MET.Draw("e")
CR1MET.SetTitle(";pfMET (GeV);N_events / GeV   ")
gPad.SetLogy()
gPad.Update()
Header.Draw("same")
cr1Comment.Draw("same")
CR1MET.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
CR1dR_fake_mu.Sumw2()
CR1dR_fake_mu.Draw("hist")
CR1dR_fake_mu.SetTitle(";#deltaR(fake,#mu);N_events   ")
Header.Draw("same")
cr1Comment.Draw("same")
CR1dR_fake_mu.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
CR1_SingleMuPt.Sumw2()
CR1_SingleMuPt.Scale(1,"width")
CR1_SingleMuPt.Draw("hist")
CR1_SingleMuPt.SetTitle(";mu_Pt (GeV/c);N_events / GeV   ")
Header.Draw("same")
cr1Comment.Draw("same")
CR1_SingleMuPt.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
SingleFakeR9.Sumw2()
SingleFakeR9.Draw("hist")
SingleFakeR9.SetTitle(";fake_R9;N_events   ")
Header.Draw("same")
cr1Comment.Draw("same")
SingleFakeR9.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
SingleFakeSigmaIEtaIEta.Sumw2()
SingleFakeSigmaIEtaIEta.Draw("hist")
SingleFakeSigmaIEtaIEta.SetTitle(";fake: #sigma_{i#etai#eta};N_events   ")
Header.Draw("same")
cr1Comment.Draw("same")
SingleFakeSigmaIEtaIEta.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
SingleFakeSigmaIPhiIPhi.Sumw2()
SingleFakeSigmaIPhiIPhi.Draw("hist")
SingleFakeSigmaIPhiIPhi.SetTitle(";fake: #sigma_{i#phii#phi};N_events   ")
Header.Draw("same")
cr1Comment.Draw("same")
SingleFakeSigmaIPhiIPhi.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")

#c.print("CR1_SingleFakeSigmaIPhiIPhi.pdf","pdf")

c.Clear()
SingleFakeEt.Sumw2()
SingleFakeEt.Scale(1,"width")
SingleFakeEt.Draw("hist")
SingleFakeEt.SetTitle(";fake_{Et} (GeV);N_events / GeV   ")
Header.Draw("same")
cr1Comment.Draw("same")
SingleFakeEt.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")

c.Clear()
SingleFakeEta.Sumw2()
SingleFakeEta.Draw("hist")
SingleFakeEta.SetTitle(";fake_#eta;N_events   ")
Header.Draw("same")
cr1Comment.Draw("same")
SingleFakeEta.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")



c.Clear()
CR1_LeadBjetPt.Sumw2()
CR1_LeadBjetPt.Scale(1,"width")
CR1_LeadBjetPt.Draw("hist")
CR1_LeadBjetPt.SetTitle(";Lead bjet_Pt (GeV/c);N_events / GeV   ")
Header.Draw("same")
cr1Comment.Draw("same")
CR1_LeadBjetPt.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")



c.Clear()
CR1invmufake.Sumw2()
CR1invmufake.Scale(1,"width")
CR1invmufake.SetTitle(";m_{e-fake};N_events / GeV   ")
CR1invmufake.Draw("hist")
Header.Draw("same")
cr1Comment.Draw("same")
CR1invmufake.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
CR1_jetHt.Sumw2()
CR1_jetHt.Scale(1,"width")
CR1_jetHt.Draw("hist")
Header.Draw("same")
cr1Comment.Draw("same")
CR1_jetHt.SetTitle("; HT_jets;N_events / GeV   ")
CR1_jetHt.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")

c.Clear()
CR2_SingleMuPt.Sumw2()
CR2_SingleMuPt.Scale(1,"width")
CR2_SingleMuPt.Draw("hist")
CR2_SingleMuPt.SetTitle(";mu_Pt (GeV/c);N_events / GeV   ")
Header.Draw("same")
cr2Comment.Draw("same")
CR2_SingleMuPt.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
CR2MET.Sumw2()
CR2MET.Scale(1,"width")
CR2MET.Draw("e")
CR2MET.SetTitle(";pfMET (GeV);N_events / GeV   ")
gPad.SetLogy()
gPad.Update()
Header.Draw("same")
cr2Comment.Draw("same")
CR2MET.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
diFakeM.Sumw2()
diFakeM.Scale(1,"width")
diFakeM.Draw("e")
diFakeM.SetTitle(";m_{ff} (GeV);N_events / GeV   ")
Header.Draw("same")
cr2Comment.Draw("same")
diFakeM.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
CR2nFake.Sumw2()
CR2nFake.Draw("hist")
CR2nFake.SetTitle(";n_{fake};N_events   ")
Header.Draw("same")
cr2Comment.Draw("same")
CR2nFake.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
LeadFakeEt.Sumw2()
LeadFakeEt.Scale(1,"width")
LeadFakeEt.Draw("hist")
LeadFakeEt.SetTitle(";Lead fake_Et(GeV);N_events / GeV   ")
Header.Draw("same")
cr2Comment.Draw("same")
LeadFakeEt.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
TrailFakeEt.Sumw2()
TrailFakeEt.Scale(1,"width")
TrailFakeEt.Draw("hist")
TrailFakeEt.SetTitle(";Trail fake_Et(GeV);N_events / GeV   ")
Header.Draw("same")
cr2Comment.Draw("same")
TrailFakeEt.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")



c.Clear()
CR2_LeadBjetPt.Sumw2()
CR2_LeadBjetPt.Scale(1,"width")
CR2_LeadBjetPt.Draw("hist")
CR2_LeadBjetPt.SetTitle(";Lead bjet_Pt (GeV/c);N_events / GeV   ")
Header.Draw("same")
cr2Comment.Draw("same")
CR2_LeadBjetPt.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")


c.Clear()
CR2_jetHt.Sumw2()
CR2_jetHt.Scale(1,"width")
CR2_jetHt.Draw("hist")
CR2_jetHt.SetTitle("; HT_jets;N_events / GeV   ")
Header.Draw("same")
cr2Comment.Draw("same")
CR2_jetHt.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")




c.Clear()
c.SetRightMargin(0.14)
pre_nJet_nbJet.Draw("colz")
pre_nJet_nbJet.SetTitle(";n_{Jet};n_{bJet}")
gStyle.SetOptStat(0)
pre_nJet_nbJet.UseCurrentStyle()
gPad.SetLogz()
Header.Draw("same")
preComment.Draw("same")
c.Print(sys.argv[2]+".pdf")
#gPad.SetLogy(0)
#gPad.SetLogz()                                                
#gPad.Update()
#c.print("pre_nJet_nbJet.pdf","pdf")

c.Clear()
c.SetRightMargin(0.14)
SR1_nJet_nbJet.Draw("colz")
SR1_nJet_nbJet.SetTitle(";n_{Jet};n_{bJet}")
gStyle.SetOptStat(0)
SR1_nJet_nbJet.UseCurrentStyle()
gPad.SetLogy(0)
gPad.SetLogz()                                                            
gPad.Update()
Header.Draw("same")
sr1Comment.Draw("same")
c.Print(sys.argv[2]+".pdf")
#c.print("SR1_nJet_nbJet.pdf","pdf")


c.Clear()
c.SetRightMargin(0.14)
SR2_nJet_nbJet.Draw("colz")
SR2_nJet_nbJet.SetTitle(";n_{Jet};n_{bJet}")
gStyle.SetOptStat(0)
Header.Draw("same")
sr2Comment.Draw("same")
SR2_nJet_nbJet.UseCurrentStyle()
c.Print(sys.argv[2]+".pdf")
#gPad.SetLogy(0)
#gPad.SetLogz()                                                
#gPad.Update()
#c.print("SR2_nJet_nbJet.pdf","pdf")

c.Clear()
c.SetRightMargin(0.14)
c.SetLeftMargin(0.12)
diPhotonM_MET.Draw("colz")
diPhotonM_MET.SetTitle(";m_{#gamma#gamma} (GeV); pfMET")
diPhotonM_MET.GetYaxis().SetTitleOffset(1.5)
diPhotonM_MET.UseCurrentStyle()
gStyle.SetOptStat(0)
Header.Draw("same")
sr2Comment.Draw("same")
c.Print(sys.argv[2]+".pdf")
#gPad.SetLogy(0)
#gPad.SetLogz()
#gPad.Update()
#c.print("SR2_diPhotonM_MET.pdf","pdf")


c.Clear()
c.SetRightMargin(0.14)
CR1_nJet_nbJet.Draw("colz")
CR1_nJet_nbJet.SetTitle(";n_{Jet};n_{bJet}")
CR1_nJet_nbJet.UseCurrentStyle()
gStyle.SetOptStat(0)
gPad.SetLogy(0)
gPad.SetLogz()                                                            
gPad.Update()
Header.Draw("same")
cr1Comment.Draw("same")
c.Print(sys.argv[2]+".pdf")
#c.print("CR1_nJet_nbJet.pdf","pdf")


c.Clear()
c.SetRightMargin(0.14)
CR2_nJet_nbJet.Draw("colz")
CR2_nJet_nbJet.SetTitle(";n_{Jet};n_{bJet}")
CR2_nJet_nbJet.UseCurrentStyle()
gStyle.SetOptStat(0)
Header.Draw("same")
cr2Comment.Draw("same")
c.Print(sys.argv[2]+".pdf")
#gPad.SetLogy(0)
#gPad.SetLogz()                                                
#gPad.Update()
#c.print("CR2_nJet_nbJet.pdf","pdf")

c.Clear()
c.SetRightMargin(0.14)
c.SetLeftMargin(0.12)
diFakeM_MET.Draw("colz")
diFakeM_MET.SetTitle(";m_{ff} (GeV); pfMET")
diFakeM_MET.GetYaxis().SetTitleOffset(1.5)
diFakeM_MET.UseCurrentStyle()
gStyle.SetOptStat(0)
Header.Draw("same")
cr2Comment.Draw("same")
c.Print(sys.argv[2]+".pdf)")
#gPad.SetLogy(0)
#gPad.SetLogz()
#gPad.Update()
#c.print("CR2_diFakeM_MET.pdf","pdf")


file_out.Write()
file_out.Close()


sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"


