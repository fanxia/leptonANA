#!/bin/python
# 3.31.2016 by Fan Xia
# This template uses the skim EventTree from dir:selected as input, using existing branched to make plots 
# region branch is to indentify the pre, sr1, sr2, cr1, cr2
# For mc, has the weight factor

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
n_events = chain_in.GetEntries()
print"Total events for processing: ",n_events


os.system('mkdir -p outplot_'+sys.argv[2]+dd)
os.chdir('outplot_'+sys.argv[2]+dd)
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
SR1dR_pho_mu = ROOT.TH1F("SR1dR_pho_mu","SR1dR_pho_mu",100,0,10)
SinglePhoEt = ROOT.TH1F("SinglePhoEt","SinglePhoEt",17,xbin_pt)
SinglePhoEta = ROOT.TH1F("SinglePhoEta","SinglePhoEta",60,-3,3)
SinglePhoR9 = ROOT.TH1F("SinglePhoR9","SinglePhoR9",60,0,1.2)
SinglePhoSigmaIEtaIEta = ROOT.TH1F("SinglePhoSigmaIEtaIEta","SinglePhoSigmaIEtaIEta",100,0,0.05)
SinglePhoSigmaIPhiIPhi = ROOT.TH1F("SinglePhoSigmaIPhiIPhi","SinglePhoSigmaIPhiIPhi",100,0,0.1)
SR1MET = ROOT.TH1F("SR1MET","SR1MET",11,xbin_met)
SR1_LeadBjetPt = ROOT.TH1F("SR1_LeadBjetPt","SR1_LeadBjetPt",17,xbin_pt)
SR1_nJet_nbJet = ROOT.TH2F("SR1_nJet_nbJet","SR1_nJet_nbJet",15,0,15,10,0,10)
SR1invmupho = ROOT.TH1F("SR1invmupho","SR1invmupho",11,xbin_met)
SR1_jetHt = ROOT.TH1F("SR1_jetHt","SR1_jetHt",18,xbin_pt)
#SR1_nJet_nbJet_ratio = ROOT.TH2F("SR1_nJet_nbJet_ratio","SR1_nJet_nbJet_ratio",15,0,15,10,0,10)


SR2phodR = ROOT.TH1F("SR2phodR","SR2phodR",100,0,10)
SR2_SingleMuPt = ROOT.TH1F("SR2_SingleMuPt","SR2_SingleMuPt",16,xbin_pt)
diPhotonM = ROOT.TH1F("diPhotonM","diPhotonM",11,xbin_met)
SR2MET = ROOT.TH1F("SR2MET","SR2MET",11,xbin_met)
SR2nPho = ROOT.TH1F("SR2nPho","SR2nPho",5,0,5)
diPhotonM_MET = ROOT.TH2F("diPhotonM_MET","diPhotonM_MET",100,0,1000,100,0,1000)
SR2_LeadBjetPt = ROOT.TH1F("SR2_LeadBjetPt","SR2_LeadBjetPt",17,xbin_pt)
LeadPhoEt = ROOT.TH1F("LeadPhoEt","LeadPhoEt",16,xbin_pt)
TrailPhoEt = ROOT.TH1F("TrailPhoEt","TrailPhoEt",16,xbin_pt)
SR2_nJet_nbJet = ROOT.TH2F("SR2_nJet_nbJet","SR2_nJet_nbJet",15,0,15,10,0,10)
SR2_jetHt = ROOT.TH1F("SR2_jetHt","SR2_jetHt",18,xbin_pt)
#SR2_nJet_nbJet_ratio = ROOT.TH2F("SR2_nJet_nbJet_ratio","SR2_nJet_nbJet_ratio",15,0,15,10,0,10)


CR1_SingleMuPt = ROOT.TH1F("CR1_SingleMuPt","CR1_SingleMuPt",16,xbin_pt)
CR1dR_fake_mu = ROOT.TH1F("CR1dR_fake_mu","CR1dR_fake_mu",100,0,10)
SingleFakeEt = ROOT.TH1F("SingleFakeEt","SingleFakeEt",17,xbin_pt)
SingleFakeEta = ROOT.TH1F("SingleFakeEta","SingleFakeEta",60,-3,3)
SingleFakeR9 = ROOT.TH1F("SingleFakeR9","SingleFakeR9",60,0,1.2)
SingleFakeSigmaIEtaIEta = ROOT.TH1F("SingleFakeSigmaIEtaIEta","SingleFakeSigmaIEtaIEta",100,0,0.05)
SingleFakeSigmaIPhiIPhi = ROOT.TH1F("SingleFakeSigmaIPhiIPhi","SingleFakeSigmaIPhiIPhi",100,0,0.1)
CR1MET = ROOT.TH1F("CR1MET","CR1MET",11,xbin_met)
CR1_LeadBjetPt = ROOT.TH1F("CR1_LeadBjetPt","CR1_LeadBjetPt",17,xbin_pt)
CR1_nJet_nbJet = ROOT.TH2F("CR1_nJet_nbJet","CR1_nJet_nbJet",15,0,15,10,0,10)
CR1invmufake = ROOT.TH1F("CR1invmufake","CR1invmufake",11,xbin_met)
CR1_jetHt = ROOT.TH1F("CR1_jetHt","CR1_jetHt",18,xbin_pt)
#CR1_nJet_nbJet_ratio = ROOT.TH2F("CR1_nJet_nbJet_ratio","CR1_nJet_nbJet_ratio",15,0,15,10,0,10)



CR2_SingleMuPt = ROOT.TH1F("CR2_SingleMuPt","CR2_SingleMuPt",16,xbin_pt)
diFakeM = ROOT.TH1F("diFakeM","diFakeM",11,xbin_met)
CR2MET = ROOT.TH1F("CR2MET","CR2MET",11,xbin_met)
CR2nFake = ROOT.TH1F("CR2nFake","CR2nFake",5,0,5)
diFakeM_MET = ROOT.TH2F("diFakeM_MET","diFakeM_MET",100,0,1000,100,0,1000)
CR2_LeadBjetPt = ROOT.TH1F("CR2_LeadBjetPt","CR2_LeadBjetPt",17,xbin_pt)
LeadFakeEt = ROOT.TH1F("LeadFakeEt","LeadFakeEt",16,xbin_pt)
TrailFakeEt = ROOT.TH1F("TrailFakeEt","TrailFakeEt",16,xbin_pt)
CR2_nJet_nbJet = ROOT.TH2F("CR2_nJet_nbJet","CR2_nJet_nbJet",15,0,15,10,0,10)
CR2_jetHt = ROOT.TH1F("CR2_jetHt","CR2_jetHt",18,xbin_pt)
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

    jetht=jetht+chain_in.jetPt[j]
    TRVmu.SetPtEtaPhiM(chain_in.muPt,chain_in.muEta,chain_in.muPhi,0.000511)


    
    pre_nPho.Fill(len(,weight)
    pre_nFake.Fill(len(fakelist),weight)
    pre_SingleMuPt.Fill(chain_in.muPt[mu_ind],weight)
    pre_SingleMuEta.Fill(chain_in.muEta[mu_ind],weight)
    pre_nJet_nbJet.Fill(n_jet,n_bjet,weight)
    pre_LeadBjetPt.Fill(chain_in.jetPt[leadbjet_ind],weight)
    preMET.Fill(chain_in.pfMET,weight)
    pre_nJet.Fill(n_jet,weight)
    pre_jetHt.Fill(jetht,weight)

#-------------------------below for signal region1 &2
    if chain_in.region==1:
        TRVSR1pho.SetPtEtaPhiM(chain_in.phoEt,chain_in.phoEta,chain_in.phoPhi,0.0)
        SR1MET.Fill(chain_in.pfMET,weight)
        dRphoton_mu = dR(chain_in.phoEta,chain_in.muEta,chain_in.phoPhi,chain_in.muPhi)
        SR1dR_pho_mu.Fill(dRphoton_mu,weight)
        SinglePhoEt.Fill(chain_in.phoEt[singlepho_ind],weight)
        SinglePhoEta.Fill(chain_in.phoEta[singlepho_ind],weight)
        SinglePhoR9.Fill(chain_in.phoR9[singlepho_ind],weight)
        SinglePhoSigmaIPhiIPhi.Fill(chain_in.phoSigmaIPhiIPhi[singlepho_ind],weight)
        SinglePhoSigmaIEtaIEta.Fill(chain_in.phoSigmaIEtaIEta[singlepho_ind],weight)
        SR1invmupho.Fill((TRVmu+TRVSR1pho).M(),weight)

        SR1_nJet_nbJet.Fill(n_jet,n_bjet,weight)
#        SR1_nJet_nbJet_ratio.Fill(n_jet,n_bjet,weight)
        SR1_SingleMuPt.Fill(chain_in.muPt[mu_ind],weight)
        SR1_LeadBjetPt.Fill(chain_in.jetPt[leadbjet_ind],weight)
        SR1_jetHt.Fill(jetht,weight)
    elif len(pholist)>=2:    
        region[0]=2
        leadpho_ind=max(pholist,key=lambda x: chain_in.phoEt[x])
        trailpho_ind=max([pp for pp in pholist if pp!=leadpho_ind],key=lambda x: chain_in.phoEt[x])
#        sr2pho_index[0]=leadpho_ind
#        sr2pho_index[1]=trailpho_ind
        TRVSR2pho1.SetPtEtaPhiM(chain_in.phoEt[leadpho_ind],chain_in.phoEta[leadpho_ind],chain_in.phoPhi[leadpho_ind],0.0)
        TRVSR2pho2.SetPtEtaPhiM(chain_in.phoEt[trailpho_ind],chain_in.phoEta[trailpho_ind],chain_in.phoPhi[trailpho_ind],0.0)
        (n_SR2)+=1
        (nweight_SR2)+=weight

        
        phodR=TRVSR2pho1.DeltaR(TRVSR2pho2)
        SR2phodR.Fill(phodR,weight)

        SR2nPho.Fill(len(pholist),weight)
        diPhotonM.Fill((TRVSR2pho1+TRVSR2pho2).M(),weight)
        SR2MET.Fill(chain_in.pfMET,weight)
        SR2_SingleMuPt.Fill(chain_in.muPt[mu_ind],weight)
        diPhotonM_MET.Fill((TRVSR2pho1+TRVSR2pho2).M(),chain_in.pfMET,weight)
        LeadPhoEt.Fill(chain_in.phoEt[leadpho_ind],weight)
        TrailPhoEt.Fill(chain_in.phoEt[trailpho_ind],weight)
        SR2_LeadBjetPt.Fill(chain_in.jetPt[leadbjet_ind],weight)
        SR2_nJet_nbJet.Fill(n_jet,n_bjet,weight)
        SR2_jetHt.Fill(jetht,weight)
#------------------------------below for control region 1&2 depends on fake numbers
    if len(fakelist)==1 and len(pholist)==0:
        region[0]=3
        singlefake_ind=fakelist[0]
#        cr1fake_index[0]=singlefake_ind
        (n_CR1)+=1
        (nweight_CR1)+=weight
        TRVCR1fake.SetPtEtaPhiM(chain_in.phoEt[singlefake_ind],chain_in.phoEta[singlefake_ind],chain_in.phoPhi[singlefake_ind],0.0)
        CR1MET.Fill(chain_in.pfMET,weight)
        dRfake_mu = dR(chain_in.phoEta[singlefake_ind],chain_in.muEta[mu_ind],chain_in.phoPhi[singlefake_ind],chain_in.muPhi[mu_ind])
        CR1dR_fake_mu.Fill(dRfake_mu,weight)
        SingleFakeEt.Fill(chain_in.phoEt[singlefake_ind],weight)
        SingleFakeEta.Fill(chain_in.phoEta[singlefake_ind],weight)
        SingleFakeR9.Fill(chain_in.phoR9[singlefake_ind],weight)
        SingleFakeSigmaIPhiIPhi.Fill(chain_in.phoSigmaIPhiIPhi[singlefake_ind],weight)
        SingleFakeSigmaIEtaIEta.Fill(chain_in.phoSigmaIEtaIEta[singlefake_ind],weight)
        CR1invmufake.Fill((TRVmu+TRVCR1fake).M(),weight)

        CR1_nJet_nbJet.Fill(n_jet,n_bjet,weight)
#        SR1_nJet_nbJet_ratio.Fill(n_jet,n_bjet,weight)
        CR1_SingleMuPt.Fill(chain_in.muPt[mu_ind],weight)
        CR1_LeadBjetPt.Fill(chain_in.jetPt[leadbjet_ind],weight)
        CR1_jetHt.Fill(jetht,weight)
    elif len(fakelist)>=2 and len(pholist)==0:    
        region[0]=4
        leadfake_ind=max(fakelist,key=lambda x: chain_in.phoEt[x])
        trailfake_ind=max([pp for pp in fakelist if pp!=leadfake_ind],key=lambda x: chain_in.phoEt[x])
#        cr2fake_index[0]=leadfake_ind
#        cr2fake_index[1]=trailfake_ind
        TRVCR2fake1.SetPtEtaPhiM(chain_in.phoEt[leadfake_ind],chain_in.phoEta[leadfake_ind],chain_in.phoPhi[leadfake_ind],0.0)
        TRVCR2fake2.SetPtEtaPhiM(chain_in.phoEt[trailfake_ind],chain_in.phoEta[trailfake_ind],chain_in.phoPhi[trailfake_ind],0.0)
        (n_CR2)+=1
        (nweight_CR2)+=weight
        CR2nFake.Fill(len(fakelist),weight)
        diFakeM.Fill((TRVCR2fake1+TRVCR2fake2).M(),weight)
        CR2MET.Fill(chain_in.pfMET,weight)
        CR2_SingleMuPt.Fill(chain_in.muPt[mu_ind],weight)
        diFakeM_MET.Fill((TRVCR2fake1+TRVCR2fake2).M(),chain_in.pfMET,weight)
        LeadFakeEt.Fill(chain_in.phoEt[leadfake_ind],weight)
        TrailFakeEt.Fill(chain_in.phoEt[trailfake_ind],weight)
        CR2_LeadBjetPt.Fill(chain_in.jetPt[leadbjet_ind],weight)
        CR2_nJet_nbJet.Fill(n_jet,n_bjet,weight)
        CR2_jetHt.Fill(jetht,weight)

    tree_out.Fill()

    bjetPt.clear()
    bjetEta.clear()
    bjetPhi.clear()

    jetPt.clear()
    jetEta.clear()
    jetPhi.clear()

    phoEt.clear()
    phoEta.clear()
    phoPhi.clear()

    fakeEt.clear()
    fakeEta.clear()
    fakePhi.clear()




print "----------------------"
print "TotalEventNumber = ", n_events
print "n_singleMu pass = ", n_singleMu
print "n_pre selection = ",n_pre
print "n_SR1 = ", n_SR1
print "n_SR2 = ", n_SR2
print "n_CR1 = ", n_CR1
print "n_CR2 = ", n_CR2
print "nweight_pre selection = ",nweight_pre
print "nweight_SR1 = ", nweight_SR1
print "nweight_SR2 = ", nweight_SR2
print "nweight_CR1 = ", nweight_CR1
print "nweight_CR2 = ", nweight_CR2
print "----------------------"


#### to write in logpre.txt
log.write("############################################################\n")
log.write("INPUT %s"%sys.argv[1])
log.write("\nOutPUT %s\n"%sys.argv[2])
log.write("%s"%datetime.datetime.now())
log.write("\nTotalEventNumber = %s"%n_events)
log.write( "\nn_singleMu pass =%s "%n_singleMu)
log.write("\nn_pre selection = %s"%n_pre)
log.write("\nn_SR1 =%s "%n_SR1)
log.write("\nn_SR2 =%s "%n_SR2)
log.write("\nn_CR1 =%s "%n_CR1)
log.write("\nn_CR2 =%s "%n_CR2)
log.write("\nnweight_pre selection = %s"%nweight_pre)
log.write("\nnweight_SR1 =%s "%nweight_SR1)
log.write("\nnweight_SR2 =%s "%nweight_SR2)
log.write("\nnweight_CR1 =%s "%nweight_CR1)
log.write("\nnweight_CR2 =%s "%nweight_CR2)
log.write( "\n----------------------\n\n")
log.close()



c=ROOT.TCanvas("c","Plots",800,800)
Header=ROOT.TPaveText(0.06,0.901,0.45,0.94,"NDC")
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
#preComment=ROOT.TLatex(0.9,0.9,"Pre-selection muon")
sr1Comment=ROOT.TLatex(0.9,0.9,"SR1 muon")
sr2Comment=ROOT.TLatex(0.9,0.9,"SR2 muon")


c.cd()
pre_nPho.Draw("HIST")
Header.Draw("same")
preComment.Draw("same")
gPad.SetLogy()
gPad.Update()
c.Print(sys.argv[2]+".pdf(")

c.Clear()
pre_nFake.Draw()
Header.Draw("same")
preComment.Draw("same")
gPad.SetLogy()
gPad.Update()
c.Print(sys.argv[2]+".pdf")
#c.print("pre_nFake.pdf","pdf")


c.Clear()
pre_nJet.Draw()
Header.Draw("same")
preComment.Draw("same")
c.Print(sys.argv[2]+".pdf")
#c.print("pre_nJet.pdf","pdf")


c.Clear()
preMET.Scale(1,"width")
preMET.Draw("e")
Header.Draw("same")
preComment.Draw("same")
#preMET.SetBins()
preMET.SetTitle(";MET (GeV);N_events/GeV")
c.Print(sys.argv[2]+".pdf")
#c.print("preMET.pdf","pdf")


c.Clear()
pre_SingleMuPt.Scale(1,"width")
pre_SingleMuPt.Draw()
Header.Draw("same")
preComment.Draw("same")
pre_SingleMuPt.SetTitle(";mu_Pt (GeV/c);N_events/GeV")
c.Print(sys.argv[2]+".pdf")
#c.print("pre_SingleMu.pdf","pdf")

c.Clear()
pre_SingleMuEta.Draw()
Header.Draw("same")
preComment.Draw("same")
pre_SingleMuEta.SetTitle(";mu_Eta;Number of Events")
c.Print(sys.argv[2]+".pdf")
#c.print("pre_SingleMuEta.pdf","pdf")


c.Clear()
pre_LeadBjetPt.Scale(1,"width")
pre_LeadBjetPt.Draw()
Header.Draw("same")
preComment.Draw("same")
pre_LeadBjetPt.SetTitle(";Lead bjet_Pt (GeV/c);N_events/GeV")
c.Print(sys.argv[2]+".pdf")
#c.print("pre_LeadBjetPt.pdf","pdf")

c.Clear()
pre_jetHt.Scale(1,"width")
pre_jetHt.Draw()
Header.Draw("same")
preComment.Draw("same")
pre_jetHt.SetTitle("; HT_jets;N_events/GeV")
c.Print(sys.argv[2]+".pdf")

c.Clear()
SR1MET.Scale(1,"width")
SR1MET.Draw("e")
SR1MET.SetTitle("MuChannel SR1:MET;MET (GeV);N_events/GeV")
gPad.SetLogy()
gPad.Update()
c.Print(sys.argv[2]+".pdf")
#c.print("SR1MET.pdf","pdf")


c.Clear()
SR1dR_pho_mu.Draw()
SR1dR_pho_mu.SetTitle("MuChannel SR1: dR(#gammamu);;")
#c.print("SR1dR_pho_mu.pdf","pdf")

c.Clear()
SR1_SingleMuPt.Scale(1,"width")
SR1_SingleMuPt.Draw()
SR1_SingleMuPt.SetTitle("MuChannel SR1;mu_Pt (GeV/c);N_events/GeV")
c.Print(sys.argv[2]+".pdf")
#gPad.SetLogy()
#gPad.Update()
#c.print("SR1_SingleMu.pdf","pdf")


c.Clear()
SinglePhoR9.Draw()
SinglePhoR9.SetTitle("SR1:;#gamma_R9;")
c.Print(sys.argv[2]+".pdf")
#gPad.SetLogy()
#gPad.Update()
#c.print("SR1_SinglePhoR9.pdf","pdf")

c.Clear()
SinglePhoSigmaIEtaIEta.Draw()
SinglePhoSigmaIEtaIEta.SetTitle("SR1:;#gamma_i#etai#eta;")
c.Print(sys.argv[2]+".pdf")
#gPad.SetLogy()
#gPad.Update()
#c.print("SR1_SinglePhoSigmaIEtaIEta.pdf","pdf")

c.Clear()
SinglePhoSigmaIPhiIPhi.Draw()
SinglePhoSigmaIPhiIPhi.SetTitle("SR1:;#gamma_i#phii#phi;")
c.Print(sys.argv[2]+".pdf")
#gPad.SetLogy()
#gPad.Update()
#c.print("SR1_SinglePhoSigmaIPhiIPhi.pdf","pdf")

c.Clear()
SinglePhoEt.Scale(1,"width")
SinglePhoEt.Draw()
SinglePhoEt.SetTitle("SR1: #gamma;#gamma_{Et} (GeV);N_events/GeV")
c.Print(sys.argv[2]+".pdf")
#gPad.SetLogy()
#gPad.Update()
#c.print("SR1_SinglePhoEt.pdf","pdf")

c.Clear()
SinglePhoEta.Draw()
SinglePhoEta.SetTitle("SR1: #gamma;#gamma_#eta;")
c.Print(sys.argv[2]+".pdf")
#gPad.SetLogy()
#gPad.Update()
#c.print("SR1_SinglePhoEta.pdf","pdf")


c.Clear()
SR1_LeadBjetPt.Scale(1,"width")
SR1_LeadBjetPt.Draw()
SR1_LeadBjetPt.SetTitle("SR1;Lead bjet_Pt (GeV/c);N_events/GeV")
c.Print(sys.argv[2]+".pdf")
#c.print("SR1_LeadBjetPt.pdf","pdf")


c.Clear()
SR1invmupho.Scale(1,"width")
SR1invmupho.SetTitle("SR1;invmass_e#gamma;N_events/GeV")
SR1invmupho.Draw()
c.Print(sys.argv[2]+".pdf")
#c.print("SR1invmupho.pdf","pdf")

c.Clear()
SR1_jetHt.Scale(1,"width")
SR1_jetHt.Draw()
c.Print(sys.argv[2]+".pdf")
SR1_jetHt.SetTitle("MuChannel SR1; HT_jets;N_events/GeV")


#checkpoint
c.Clear()
SR2phodR.Draw()
c.Print(sys.argv[2]+".pdf")
#c.print("SR2phodR.pdf","pdf")



c.Clear()
SR2_SingleMuPt.Scale(1,"width")
SR2_SingleMuPt.Draw()
SR2_SingleMuPt.SetTitle("MuChannel SR2;mu_Pt (GeV/c);N_events/GeV")
c.Print(sys.argv[2]+".pdf")
#gPad.SetLogy()
#gPad.Update()
#c.print("SR2_SingleMuPt.pdf","pdf")

c.Clear()
SR2MET.Scale(1,"width")
SR2MET.Draw("e")
SR2MET.SetTitle("MuChannel SR2:MET;MET (GeV);N_events/GeV")
gPad.SetLogy()
gPad.Update()
c.Print(sys.argv[2]+".pdf")
#c.print("SR2MET.pdf","pdf")

c.Clear()
diPhotonM.Scale(1,"width")
diPhotonM.Draw("e")
diPhotonM.SetTitle("SR2: #gamma#gamma;m_{#gamma#gamma} (GeV);N_events/GeV")
c.Print(sys.argv[2]+".pdf")
#gPad.SetLogy()
#gPad.Update()
#c.print("SR2_diPhotonM.pdf","pdf")

c.Clear()
SR2nPho.Draw()
SR2nPho.SetTitle("SR2;n_Photon;")
c.Print(sys.argv[2]+".pdf")
#c.print("SR2nPho.pdf","pdf")

c.Clear()
LeadPhoEt.Scale(1,"width")
LeadPhoEt.Draw()
LeadPhoEt.SetTitle("SR2:Lead #gamma;Lead #gamma_Et(GeV);N_events/GeV")
c.Print(sys.argv[2]+".pdf")
#gPad.SetLogy()
#gPad.Update()
#c.print("SR2_LeadPhoEt.pdf","pdf")

c.Clear()
TrailPhoEt.Scale(1,"width")
TrailPhoEt.Draw()
TrailPhoEt.SetTitle("SR2:Trail #gamma;Trail #gamma_Et(GeV);N_events/GeV")
c.Print(sys.argv[2]+".pdf")
#gPad.SetLogy()
#gPad.Update()
#c.print("SR2_TrailPhoEt.pdf","pdf")


c.Clear()
SR2_LeadBjetPt.Scale(1,"width")
SR2_LeadBjetPt.Draw()
SR2_LeadBjetPt.SetTitle("SR2;Lead bjet_Pt (GeV/c);N_events/GeV")
c.Print(sys.argv[2]+".pdf")
#c.print("SR2_LeadBjetPt.pdf","pdf")

c.Clear()
SR2_jetHt.Scale(1,"width")
SR2_jetHt.Draw()
SR2_jetHt.SetTitle("MuChannel SR2; HT_jets;N_events/GeV")
c.Print(sys.argv[2]+".pdf")

c.Clear()
CR1MET.Scale(1,"width")
CR1MET.Draw("e")
CR1MET.SetTitle("MuChannel CR1:MET;MET (GeV);N_events/GeV")
gPad.SetLogy()
gPad.Update()
c.Print(sys.argv[2]+".pdf")
#c.print("CR1MET.pdf","pdf")


c.Clear()
CR1dR_fake_mu.Draw()
CR1dR_fake_mu.SetTitle("MuChannel CR1: dR(fake-mu);;")
c.Print(sys.argv[2]+".pdf")
#c.print("CR1dR_fake_mu.pdf","pdf")

c.Clear()
CR1_SingleMuPt.Scale(1,"width")
CR1_SingleMuPt.Draw()
CR1_SingleMuPt.SetTitle("MuChannel CR1;mu_Pt (GeV/c);N_events/GeV")
c.Print(sys.argv[2]+".pdf")
#c.print("CR1_SingleMu.pdf","pdf")


c.Clear()
SingleFakeR9.Draw()
SingleFakeR9.SetTitle("CR1:;fake_R9;")
c.Print(sys.argv[2]+".pdf")
#c.print("CR1_SingleFakeR9.pdf","pdf")

c.Clear()
SingleFakeSigmaIEtaIEta.Draw()
SingleFakeSigmaIEtaIEta.SetTitle("CR1:;fake_i#etai#eta;")
c.Print(sys.argv[2]+".pdf")
#c.print("CR1_SingleFakeSigmaIEtaIEta.pdf","pdf")

c.Clear()
SingleFakeSigmaIPhiIPhi.Draw()
SingleFakeSigmaIPhiIPhi.SetTitle("CR1:;fake_i#phii#phi;")
#c.print("CR1_SingleFakeSigmaIPhiIPhi.pdf","pdf")

c.Clear()
SingleFakeEt.Scale(1,"width")
SingleFakeEt.Draw()
SingleFakeEt.SetTitle("CR1: fake;fake_{Et} (GeV);N_events/GeV")
c.Print(sys.argv[2]+".pdf")
#c.print("CR1_SingleFakeEt.pdf","pdf")

c.Clear()
SingleFakeEta.Draw()
SingleFakeEta.SetTitle("CR1: fake;fake_#eta;")
c.Print(sys.argv[2]+".pdf")
#c.print("CR1_SingleFakeEta.pdf","pdf")


c.Clear()
CR1_LeadBjetPt.Scale(1,"width")
CR1_LeadBjetPt.Draw()
CR1_LeadBjetPt.SetTitle("CR1;Lead bjet_Pt (GeV/c);N_events/GeV")
c.Print(sys.argv[2]+".pdf")
#c.print("CR1_LeadBjetPt.pdf","pdf")


c.Clear()
CR1invmufake.Scale(1,"width")
CR1invmufake.SetTitle("CR1;invmass_e-fake;N_events/GeV")
CR1invmufake.Draw()
c.Print(sys.argv[2]+".pdf")
#c.print("CR1invmufake.pdf","pdf")

c.Clear()
CR1_jetHt.Scale(1,"width")
CR1_jetHt.Draw()
CR1_jetHt.SetTitle("MuChannel CR1; HT_jets;N_events/GeV")


c.Clear()
CR2_SingleMuPt.Scale(1,"width")
CR2_SingleMuPt.Draw()
CR2_SingleMuPt.SetTitle("MuChannel CR2;mu_Pt (GeV/c);N_events/GeV")
c.Print(sys.argv[2]+".pdf")
#c.print("CR2_SingleMuPt.pdf","pdf")

c.Clear()
CR2MET.Scale(1,"width")
CR2MET.Draw("e")
CR2MET.SetTitle("MuChannel CR2:MET;MET (GeV);N_events/GeV")
gPad.SetLogy()
gPad.Update()
c.Print(sys.argv[2]+".pdf")
#c.print("CR2MET.pdf","pdf")

c.Clear()
diFakeM.Scale(1,"width")
diFakeM.Draw("e")
diFakeM.SetTitle("CR2: ff;m_{ff} (GeV);N_events/GeV")
c.Print(sys.argv[2]+".pdf")
#c.print("CR2_diFakeM.pdf","pdf")

c.Clear()
CR2nFake.Draw()
CR2nFake.SetTitle("CR2;n_Fake;")
c.Print(sys.argv[2]+".pdf")
#c.print("CR2nFake.pdf","pdf")

c.Clear()
LeadFakeEt.Scale(1,"width")
LeadFakeEt.Draw()
LeadFakeEt.SetTitle("CR2:Lead fake;Lead fake_Et(GeV);N_events/GeV")
c.Print(sys.argv[2]+".pdf")
#c.print("CR2_LeadFakeEt.pdf","pdf")

c.Clear()
TrailFakeEt.Scale(1,"width")
TrailFakeEt.Draw()
TrailFakeEt.SetTitle("CR2:Trail fake;Trail fake_Et(GeV);N_events/GeV")
c.Print(sys.argv[2]+".pdf")
#c.print("CR2_TrailFakeEt.pdf","pdf")


c.Clear()
CR2_LeadBjetPt.Scale(1,"width")
CR2_LeadBjetPt.Draw()
CR2_LeadBjetPt.SetTitle("CR2;Lead bjet_Pt (GeV/c);N_events/GeV")
c.Print(sys.argv[2]+".pdf")
#c.print("CR2_LeadBjetPt.pdf","pdf")

c.Clear()
CR2_jetHt.Scale(1,"width")
CR2_jetHt.Draw()
CR2_jetHt.SetTitle("MuChannel CR2; HT_jets;N_events/GeV")
c.Print(sys.argv[2]+".pdf")




c.Clear()
c.SetRightMargin(0.14)
pre_nJet_nbJet.Draw("colz")
pre_nJet_nbJet.SetTitle("pre;n_Jet;nbJet")
gStyle.SetOptStat(0)
c.Print(sys.argv[2]+".pdf")
#gPad.SetLogy(0)
#gPad.SetLogz()                                                
#gPad.Update()
#c.print("pre_nJet_nbJet.pdf","pdf")

c.Clear()
c.SetRightMargin(0.14)
SR1_nJet_nbJet.Draw("colz")
SR1_nJet_nbJet.SetTitle("SR1;n_Jet;nbJet")
gStyle.SetOptStat(0)
gPad.SetLogy(0)
gPad.SetLogz()                                                            
gPad.Update()
c.Print(sys.argv[2]+".pdf")
#c.print("SR1_nJet_nbJet.pdf","pdf")


c.Clear()
c.SetRightMargin(0.14)
SR2_nJet_nbJet.Draw("colz")
SR2_nJet_nbJet.SetTitle("SR2;n_Jet;nbJet")
gStyle.SetOptStat(0)
c.Print(sys.argv[2]+".pdf")
#gPad.SetLogy(0)
#gPad.SetLogz()                                                
#gPad.Update()
#c.print("SR2_nJet_nbJet.pdf","pdf")

c.Clear()
c.SetRightMargin(0.14)
c.SetLeftMargin(0.12)
diPhotonM_MET.Draw("colz")
diPhotonM_MET.SetTitle("SR2: diPhotonMass vs MET;m_{#gamma#gamma} (GeV); MET")
diPhotonM_MET.GetYaxis().SetTitleOffset(1.5)
gStyle.SetOptStat(0)
c.Print(sys.argv[2]+".pdf")
#gPad.SetLogy(0)
#gPad.SetLogz()
#gPad.Update()
#c.print("SR2_diPhotonM_MET.pdf","pdf")


c.Clear()
c.SetRightMargin(0.14)
CR1_nJet_nbJet.Draw("colz")
CR1_nJet_nbJet.SetTitle("CR1;n_Jet;nbJet")
gStyle.SetOptStat(0)
gPad.SetLogy(0)
gPad.SetLogz()                                                            
gPad.Update()
c.Print(sys.argv[2]+".pdf")
#c.print("CR1_nJet_nbJet.pdf","pdf")


c.Clear()
c.SetRightMargin(0.14)
CR2_nJet_nbJet.Draw("colz")
CR2_nJet_nbJet.SetTitle("CR2;n_Jet;nbJet")
gStyle.SetOptStat(0)
c.Print(sys.argv[2]+".pdf")
#gPad.SetLogy(0)
#gPad.SetLogz()                                                
#gPad.Update()
#c.print("CR2_nJet_nbJet.pdf","pdf")

c.Clear()
c.SetRightMargin(0.14)
c.SetLeftMargin(0.12)
diFakeM_MET.Draw("colz")
diFakeM_MET.SetTitle("CR2: diFakeMass vs MET;m_{ff} (GeV); MET")
diFakeM_MET.GetYaxis().SetTitleOffset(1.5)
gStyle.SetOptStat(0)
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


