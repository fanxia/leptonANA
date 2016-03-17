#!/bin/python
# 3.17.2016 by Fan Xia
# This template uses the ggntuples as input, make the preselection and get reduced root file which should be saved in dir:preselected. It can be very time consuming and need to move output manually. This one is only for reducing event number purpose and get the first look of pre region. 
# If tighter cuts apply to the preselect, only need to run script in dir:scriptANA again. 


import os
import sys
import ROOT
from ROOT import *
from array import array
from ana_mu import muPFRelCombIso

sw = ROOT.TStopwatch()
sw.Start()
print "start"
chain_in = ROOT.TChain("ggNtuplizer/EventTree")
chain_in.Add("root://xrootd-cms.infn.it//store/group/phys_smp/ggNtuples/13TeV/data/V07_04_14_00/SilverJSON/job_data_ggNtuple_SingleElectron_Run2015D_PromptReco-v4_25ns_JSON_Silver_1915pb_miniAOD.root")
#chain_in.Add("data/SingleElectron_Run2015D_PromptReco-v4_25ns_JSON_Silver_1915pb_miniAOD__data_example.root")
chain_in.SetBranchStatus("tau*",0)
n_events = chain_in.GetEntries()
print"Total events for processing: ",n_events

#os.mkdir("Output_SingleEle_v315",0755)
os.system('mkdir -p Output_Elechannel_dataSingleEle_vDate')
os.chdir("Output_Elechannel_dataSingleEle_vDate")


#------------

pre_SingleElePt = ROOT.TH1F("pre_SingleElePt","pre_SingleElePt",100,0,1000)
pre_SingleEleEta = ROOT.TH1F("pre_SingleEleEta","pre_SingleEleEta",60,-3,3)
pre_nPho = ROOT.TH1F("pre_nPho","pre_nPho",5,0,5)
pre_nJet = ROOT.TH1F("pre_nJet","pre_nJet",15,0,15)
preMET = ROOT.TH1F("preMET","preMET",100,0,1000)
pre_LeadBjetPt = ROOT.TH1F("pre_LeadBjetPt","pre_LeadBjetPt",100,0,1000)
pre_nJet_nbJet = ROOT.TH2F("pre_nJet_nbJet","pre_nJet_nbJet",20,0,20,10,0,10)

file_out = ROOT.TFile("reduced_singleEle.root","recreate")
dir_out = file_out.mkdir("ggNtuplizer")
dir_out.cd()
tree_out = chain_in.CloneTree(0)
tree_out.SetName("EventTree_pre")

n_hlt=0
n_singleEle=0
n_pre=0

#for i in range(1000):
for i in range(n_events):
    chain_in.GetEntry(i)
    
    if i%100000 ==0:
        print "Processing entry ", i

##----------------0.5Vertex clean

#    if abs(chain_in.vtz)>24 or abs(chain_in.rho)>2: continue     //error here since the rho is not the "rho"


# -----------------1.HLT selection(HLT_Ele23_WPLoose_Gsf_v)

    hltele = chain_in.HLTEleMuX>>6&1
    if hltele!=1:
        continue
    n_hlt+=1


#-------------------1+2. only one tight ele
    n_tightEle=0
    n_looseEle=0
    for e in range(chain_in.nEle):
        if chain_in.elePt[e]>30 and (chain_in.eleIDbit[e]>>3&1)==1 and abs(chain_in.eleEta[e])<2.5:
            n_tightEle+=1
            ele_ind=e
        if chain_in.elePt[e]>10 and (chain_in.eleIDbit[e]>>1&1)==1 and abs(chain_in.eleEta[e])<2.5:
            n_looseEle+=1
    if n_tightEle !=1 or n_looseEle !=1:
        continue

    n_looseMu=0
    for m in range(chain_in.nMu):
        muPFIso=muPFRelCombIso(chain_in.muPt[m],chain_in.muPFChIso[m],chain_in.muPFNeuIso[m],chain_in.muPFPhoIso[m],chain_in.muPFPUIso[m])
#        print "iso",i,"---",muPFIso
        if chain_in.muPt[m]>10 and abs(chain_in.muEta[m])<2.5 and chain_in.muIsLooseID[m] and muPFIso<0.25:
            n_looseMu+=1
    if n_looseMu !=0:
        continue

    n_singleEle+=1     


#--------------------1+2+3.at least 3 jets and 1 bjet
    n_jet=0
    n_bjet=0
    jetlist =[]
    bjetlist=[]
    for j in range(chain_in.nJet):
        if chain_in.jetPt[j]>30 and abs(chain_in.jetEta[j])<2.4 and chain_in.jetPFLooseId[j]:
            n_jet+=1
            jetlist.append(j)
            if chain_in.jetpfCombinedInclusiveSecondaryVertexV2BJetTags[j]>0.89:
                n_bjet+=1
                bjetlist.append(j)
    if n_jet<3 or n_bjet<1:
        continue
    n_pre+=1
    leadbjet_ind=max(bjetlist,key=lambda x: chain_in.jetPt[x])
    tree_out.Fill()
#---------------------above for pre-selection---------------------


file_out.Write()
file_out.Close()

print "----------------------"
print "TotalEventNumber = ", n_events
print "n_hlt pass = ", n_hlt
print "n_singleEle pass = ", n_singleEle
print "n_pre selection = ",n_pre
print "----------------------"

c=ROOT.TCanvas("c","Plots",800,800)
c.cd()
pre_nPho.Draw()
gPad.SetLogy()
gPad.Update()
c.Print("pre_nPho.pdf","pdf")

c.Clear()
pre_nJet.Draw()
c.Print("pre_nJet.pdf","pdf")


c.Clear()
preMET.Draw("e")
preMET.SetTitle("Elehannel pre:MET;MET (GeV);")
c.Print("preMET.pdf","pdf")


c.Clear()
pre_SingleElePt.Draw()
pre_SingleElePt.SetTitle("EleChannel pre;ele_Pt (GeV/c);")
c.Print("pre_SingleEle.pdf","pdf")

c.Clear()
pre_SingleEleEta.Draw()
pre_SingleEleEta.SetTitle("EleChannel pre;ele_Eta;")
c.Print("pre_SingleEleEta.pdf","pdf")


c.Clear()
pre_LeadBjetPt.Draw()
pre_LeadBjetPt.SetTitle("pre;Lead bjet_Pt (GeV/c);")
c.Print("pre_LeadBjetPt.pdf","pdf")

c.Clear()
c.SetRightMargin(0.14)
pre_nJet_nbJet.Draw("colz")
pre_nJet_nbJet.SetTitle("pre;n_Jet;nbJet")
gStyle.SetOptStat(0)
gPad.SetLogy(0)
gPad.SetLogz()                                                
gPad.Update()
c.Print("pre_nJet_nbJet.pdf","pdf")

sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"

