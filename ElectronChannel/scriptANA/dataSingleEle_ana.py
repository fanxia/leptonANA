#!/bin/python
# 3.17.2016 by Fan Xia
# This template uses the reduced EventTree_pre from dir:preselected as input, make SR and CR selection and store the new tree to dir:selected 
# For any change of the selection cuts, should do this ana again
# This script for data

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


sw = ROOT.TStopwatch()
sw.Start()
print "start"
print "input: "+sys.argv[1]
print "output: "+sys.argv[2]
chain_in = ROOT.TChain("ggNtuplizer/EventTree_pre")
#chain_in.Add("../preselected/reduced_Elechannel_dataSingleEle.root")
chain_in.Add(sys.argv[1])
n_events = chain_in.GetEntries()
print"Total events for processing: ",n_events

dd=datetime.datetime.now().strftime("%b%d")
log = open("logANA.txt","a")
os.system('mkdir -p ../selected/'+sys.argv[2]+dd)
os.chdir('../selected/'+sys.argv[2]+dd)


#------------

pre_SingleElePt = ROOT.TH1F("pre_SingleElePt","pre_SingleElePt",100,0,1000)
pre_SingleEleEta = ROOT.TH1F("pre_SingleEleEta","pre_SingleEleEta",60,-3,3)
pre_nPho = ROOT.TH1F("pre_nPho","pre_nPho",5,0,5)
pre_nFake = ROOT.TH1F("pre_nFake","pre_nFake",5,0,5)
pre_nJet = ROOT.TH1F("pre_nJet","pre_nJet",15,0,15)
preMET = ROOT.TH1F("preMET","preMET",100,0,1000)
pre_LeadBjetPt = ROOT.TH1F("pre_LeadBjetPt","pre_LeadBjetPt",100,0,1000)
pre_nJet_nbJet = ROOT.TH2F("pre_nJet_nbJet","pre_nJet_nbJet",20,0,20,10,0,10)


SR1_SingleElePt = ROOT.TH1F("SR1_SingleElePt","SR1_SingleElePt",100,0,1000)
SR1dR_pho_ele = ROOT.TH1F("SR1dR_pho_ele","SR1dR_pho_ele",100,0,10)
SinglePhoEt = ROOT.TH1F("SinglePhoEt","SinglePhoEt",100,0,1000)
SinglePhoEta = ROOT.TH1F("SinglePhoEta","SinglePhoEta",60,-3,3)
SinglePhoR9 = ROOT.TH1F("SinglePhoR9","SinglePhoR9",60,0,1.2)
SinglePhoSigmaIEtaIEta = ROOT.TH1F("SinglePhoSigmaIEtaIEta","SinglePhoSigmaIEtaIEta",100,0,0.05)
SinglePhoSigmaIPhiIPhi = ROOT.TH1F("SinglePhoSigmaIPhiIPhi","SinglePhoSigmaIPhiIPhi",100,0,0.1)
SR1MET = ROOT.TH1F("SR1MET","SR1MET",100,0,1000)
SR1_LeadBjetPt = ROOT.TH1F("SR1_LeadBjetPt","SR1_LeadBjetPt",100,0,1000)
SR1_nJet_nbJet = ROOT.TH2F("SR1_nJet_nbJet","SR1_nJet_nbJet",15,0,15,10,0,10)
SR1invelepho = ROOT.TH1F("SR1invelepho","SR1invelepho",100,0,1000)
#SR1_nJet_nbJet_ratio = ROOT.TH2F("SR1_nJet_nbJet_ratio","SR1_nJet_nbJet_ratio",15,0,15,10,0,10)


SR2phodR = ROOT.TH1F("SR2phodR","SR2phodR",100,0,10)
SR2_SingleElePt = ROOT.TH1F("SR2_SingleElePt","SR2_SingleElePt",100,0,1000)
diPhotonM = ROOT.TH1F("diPhotonM","diPhotonM",100,0,1000)
SR2MET = ROOT.TH1F("SR2MET","SR2MET",100,0,1000)
SR2nPho = ROOT.TH1F("SR2nPho","SR2nPho",5,0,5)
diPhotonM_MET = ROOT.TH2F("diPhotonM_MET","diPhotonM_MET",100,0,1000,100,0,1000)
SR2_LeadBjetPt = ROOT.TH1F("SR2_LeadBjetPt","SR2_LeadBjetPt",100,0,1000)
LeadPhoEt = ROOT.TH1F("LeadPhoEt","LeadPhoEt",100,0,1000)
TrailPhoEt = ROOT.TH1F("TrailPhoEt","TrailPhoEt",100,0,1000)
SR2_nJet_nbJet = ROOT.TH2F("SR2_nJet_nbJet","SR2_nJet_nbJet",15,0,15,10,0,10)
#SR2_nJet_nbJet_ratio = ROOT.TH2F("SR2_nJet_nbJet_ratio","SR2_nJet_nbJet_ratio",15,0,15,10,0,10)


CR1_SingleElePt = ROOT.TH1F("CR1_SingleElePt","CR1_SingleElePt",100,0,1000)
CR1dR_fake_ele = ROOT.TH1F("CR1dR_fake_ele","CR1dR_fake_ele",100,0,10)
SingleFakeEt = ROOT.TH1F("SingleFakeEt","SingleFakeEt",100,0,1000)
SingleFakeEta = ROOT.TH1F("SingleFakeEta","SingleFakeEta",60,-3,3)
SingleFakeR9 = ROOT.TH1F("SingleFakeR9","SingleFakeR9",60,0,1.2)
SingleFakeSigmaIEtaIEta = ROOT.TH1F("SingleFakeSigmaIEtaIEta","SingleFakeSigmaIEtaIEta",100,0,0.05)
SingleFakeSigmaIPhiIPhi = ROOT.TH1F("SingleFakeSigmaIPhiIPhi","SingleFakeSigmaIPhiIPhi",100,0,0.1)
CR1MET = ROOT.TH1F("CR1MET","CR1MET",100,0,1000)
CR1_LeadBjetPt = ROOT.TH1F("CR1_LeadBjetPt","CR1_LeadBjetPt",100,0,1000)
CR1_nJet_nbJet = ROOT.TH2F("CR1_nJet_nbJet","CR1_nJet_nbJet",15,0,15,10,0,10)
CR1invelefake = ROOT.TH1F("CR1invelefake","CR1invelefake",100,0,1000)
#CR1_nJet_nbJet_ratio = ROOT.TH2F("CR1_nJet_nbJet_ratio","CR1_nJet_nbJet_ratio",15,0,15,10,0,10)



CR2_SingleElePt = ROOT.TH1F("CR2_SingleElePt","CR2_SingleElePt",100,0,1000)
diFakeM = ROOT.TH1F("diFakeM","diFakeM",100,0,1000)
CR2MET = ROOT.TH1F("CR2MET","CR2MET",100,0,1000)
CR2nFake = ROOT.TH1F("CR2nFake","CR2nFake",5,0,5)
diFakeM_MET = ROOT.TH2F("diFakeM_MET","diFakeM_MET",100,0,1000,100,0,1000)
CR2_LeadBjetPt = ROOT.TH1F("CR2_LeadBjetPt","CR2_LeadBjetPt",100,0,1000)
LeadFakeEt = ROOT.TH1F("LeadFakeEt","LeadFakeEt",100,0,1000)
TrailFakeEt = ROOT.TH1F("TrailFakeEt","TrailFakeEt",100,0,1000)
CR2_nJet_nbJet = ROOT.TH2F("CR2_nJet_nbJet","CR2_nJet_nbJet",15,0,15,10,0,10)
#CR2_nJet_nbJet_ratio = ROOT.TH2F("CR2_nJet_nbJet_ratio","CR2_nJet_nbJet_ratio",15,0,15,10,0,10)
#------------

file_out = ROOT.TFile(sys.argv[2]+".root","recreate")
#dir_out = file_out.mkdir("ggNtuplizer")
#dir_out.cd()

#--------------define extra branches to record seleted obj------------
ele_index=array('i',[-1])
leadbjet_index=array('i',[-1])
sr1pho_index=array('i',[-1])
sr2pho_index=array('i',[-1,-1])
cr1fake_index=array('i',[-1])
cr2fake_index=array('i',[-1,-1])

#-----------------------------------------------
tree_out = chain_in.CloneTree(0)
tree_out.SetName("EventTree_pre")
tree_out.Branch("ele_index",ele_index,"ele_index/I")
tree_out.Branch("leadbjet_index",leadbjet_index,"leadbjet_index/I")

tree1_out = chain_in.CloneTree(0)
tree1_out.SetName("EventTree_SR1")
tree1_out.Branch("ele_index",ele_index,"ele_index/I")
tree1_out.Branch("leadbjet_index",leadbjet_index,"leadbjet_index/I")
tree1_out.Branch("sr1pho_index",sr1pho_index,"sr1pho_index/I")

tree2_out = chain_in.CloneTree(0)
tree2_out.SetName("EventTree_SR2")
tree2_out.Branch("ele_index",ele_index,"ele_index/I")
tree2_out.Branch("leadbjet_index",leadbjet_index,"leadbjet_index/I")
tree2_out.Branch("sr2pho_index",sr2pho_index,"sr2pho_index[2]/I")

tree3_out = chain_in.CloneTree(0)
tree3_out.SetName("EventTree_CR1")
tree3_out.Branch("ele_index",ele_index,"ele_index/I")
tree3_out.Branch("leadbjet_index",leadbjet_index,"leadbjet_index/I")
tree3_out.Branch("cr1fake_index",cr1fake_index,"cr1fake_index/I")

tree4_out = chain_in.CloneTree(0)
tree4_out.SetName("EventTree_CR2")
tree4_out.Branch("ele_index",ele_index,"ele_index/I")
tree4_out.Branch("leadbjet_index",leadbjet_index,"leadbjet_index/I")
tree4_out.Branch("cr2fake_index",cr2fake_index,"cr2fake_index[2]/I")

TRVSR2pho1=ROOT.TLorentzVector()
TRVSR2pho2=ROOT.TLorentzVector()
TRVSR1pho=ROOT.TLorentzVector()
TRVCR2fake1=ROOT.TLorentzVector()
TRVCR2fake2=ROOT.TLorentzVector()
TRVCR1fake=ROOT.TLorentzVector()
TRVele=ROOT.TLorentzVector()

#n_hlt=0
n_singleEle=0
n_pre=0
n_SR1=0
n_SR2=0
n_CR1=0
n_CR2=0

#for i in range(1000):
for i in range(n_events):
    chain_in.GetEntry(i)
    
    if i%10000 ==0:
        print "Processing entry ", i

##----------------0.5Vertex clean

#    if abs(chain_in.vtz)>24 or abs(chain_in.rho)>2: continue     //error here since the rho is not the "rho"


# -----------------1.HLT selection

#    hltele = chain_in.HLTEleMuX>>6&1
#    if hltele!=1:
#        continue
#    n_hlt+=1


#-------------------1+2. only one tight ele
    n_tightEle=0
    n_looseEle=0
    for e in range(chain_in.nEle):
        if good_TightEle(chain_in.elePt[e],chain_in.eleEta[e],chain_in.eleIDbit[e]):
            n_tightEle+=1
            ele_ind=e
            ele_index[0]=e
        if good_LooseEle(chain_in.elePt[e],chain_in.eleEta[e],chain_in.eleIDbit[e]):
            n_looseEle+=1
    if n_tightEle !=1 or n_looseEle !=1:
        continue

    n_looseMu=0
    for m in range(chain_in.nMu):
        muPFIso=muPFRelCombIso(chain_in.muPt[m],chain_in.muPFChIso[m],chain_in.muPFNeuIso[m],chain_in.muPFPhoIso[m],chain_in.muPFPUIso[m])
        if good_LooseMu(chain_in.muPt[m],chain_in.muEta[m],chain_in.muIsLooseID[m],muPFIso):
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
        if good_LooseJet(chain_in.jetPt[j],chain_in.jetEta[j], chain_in.jetPFLooseId[j]):
            n_jet+=1
            jetlist.append(j)
            if chain_in.jetpfCombinedInclusiveSecondaryVertexV2BJetTags[j]>0.89:
                n_bjet+=1
                bjetlist.append(j)
    if n_jet<3 or n_bjet<1:
        continue
    n_pre+=1
    leadbjet_ind=max(bjetlist,key=lambda x: chain_in.jetPt[x])
    leadbjet_index[0]=leadbjet_ind
    tree_out.Fill()

    TRVele.SetPtEtaPhiM(chain_in.elePt[ele_ind],chain_in.eleEta[ele_ind],chain_in.elePhi[ele_ind],0.000511)
#---------------------above for pre-selection---------------------


#---------------------photon dR loop----
    pholist1=[]
    for p0 in range(chain_in.nPho):
         dRphoton_ele = dR(chain_in.phoEta[p0],chain_in.eleEta[ele_ind],chain_in.phoPhi[p0],chain_in.elePhi[ele_ind])
         if dRphoton_ele<=0.3:
             continue
         pholist1.append(p0)
        
#    pholist2=[]
#    for p1 in pholist1:
#        w = 1
#        for j in jetlist:
#             dRphoton_jet = dR(chain_in.phoEta[p1],chain_in.jetEta[j],chain_in.phoPhi[p1],chain_in.jetPhi[j])
#             if dRphoton_jet<=0.3:
#                 w=0
#                 break
#        if w==1:
#             pholist2.append(p1)

#    pholist3=[]
#    for p2 in pholist2:
#         w = 1
#         for p3 in pholist2:
#             dRphoton_photon = dR(chain_in.phoEta[p3],chain_in.phoEta[p2],chain_in.phoPhi[p3],chain_in.phoPhi[p2])
#             if dRphoton_photon<=0.3 and p2!=p3:
#                 w=0
#                 break
#         if w==1:
#             pholist3.append(p2)



#---------------------1+2+3+4.loose photon: singlepho  or diphoton and fake photon: single fake or more fakes
    pholist = [] 
    fakelist= []
    for p in pholist1:
        if (chain_in.phoIDbit[p]>>0&1)==0:
            if good_fake(chain_in.rho,chain_in.phoEt[p],chain_in.phoEta[p],chain_in.phoEleVeto[p],chain_in.phoHoverE[p],chain_in.phoSigmaIEtaIEta[p],chain_in.phoPFChIso[p],chain_in.phoPFNeuIso[p],chain_in.phoPFPhoIso[p]):
                fakelist.append(p)
        elif (chain_in.phoIDbit[p]>>0&1)==1:
            if good_LoosePho(chain_in.phoEt[p],chain_in.phoEta[p],chain_in.phoEleVeto[p]):
                pholist.append(p)


#-----------------------below for pre plots

#    pholist=pholist2
#    fakelist=fakelist2

    pre_nPho.Fill(len(pholist))
    pre_nFake.Fill(len(fakelist))
    pre_SingleElePt.Fill(chain_in.elePt[ele_ind])
    pre_SingleEleEta.Fill(chain_in.eleEta[ele_ind])
    pre_nJet_nbJet.Fill(n_jet,n_bjet)
    pre_LeadBjetPt.Fill(chain_in.jetPt[leadbjet_ind])
    preMET.Fill(chain_in.pfMET)
    pre_nJet.Fill(n_jet)


#-------------------------below for signal region1 &2
    if len(pholist)==1:
        singlepho_ind=pholist[0]
        sr1pho_index[0]=singlepho_ind
        (n_SR1)+=1
        TRVSR1pho.SetPtEtaPhiM(chain_in.phoEt[singlepho_ind],chain_in.phoEta[singlepho_ind],chain_in.phoPhi[singlepho_ind],0.0)
        tree1_out.Fill()
        SR1MET.Fill(chain_in.pfMET)
        dRphoton_ele = dR(chain_in.phoEta[singlepho_ind],chain_in.eleEta[ele_ind],chain_in.phoPhi[singlepho_ind],chain_in.elePhi[ele_ind])
        SR1dR_pho_ele.Fill(dRphoton_ele)
        SinglePhoEt.Fill(chain_in.phoEt[singlepho_ind])
        SinglePhoEta.Fill(chain_in.phoEta[singlepho_ind])
        SinglePhoR9.Fill(chain_in.phoR9[singlepho_ind])
        SinglePhoSigmaIPhiIPhi.Fill(chain_in.phoSigmaIPhiIPhi[singlepho_ind])
        SinglePhoSigmaIEtaIEta.Fill(chain_in.phoSigmaIEtaIEta[singlepho_ind])
        SR1invelepho.Fill((TRVele+TRVSR1pho).M())

        SR1_nJet_nbJet.Fill(n_jet,n_bjet)
#        SR1_nJet_nbJet_ratio.Fill(n_jet,n_bjet)
        SR1_SingleElePt.Fill(chain_in.elePt[ele_ind])
        SR1_LeadBjetPt.Fill(chain_in.jetPt[leadbjet_ind])

    elif len(pholist)>=2:    
        leadpho_ind=max(pholist,key=lambda x: chain_in.phoEt[x])
        trailpho_ind=max([pp for pp in pholist if pp!=leadpho_ind],key=lambda x: chain_in.phoEt[x])
        sr2pho_index[0]=leadpho_ind
        sr2pho_index[1]=trailpho_ind
        TRVSR2pho1.SetPtEtaPhiM(chain_in.phoEt[leadpho_ind],chain_in.phoEta[leadpho_ind],chain_in.phoPhi[leadpho_ind],0.0)
        TRVSR2pho2.SetPtEtaPhiM(chain_in.phoEt[trailpho_ind],chain_in.phoEta[trailpho_ind],chain_in.phoPhi[trailpho_ind],0.0)
#        phodR=pho1.DeltaR(pho2)
#        if phodR<0.5:
#            continue
        (n_SR2)+=1
        tree2_out.Fill()
        
        phodR=TRVSR2pho1.DeltaR(TRVSR2pho2)
        SR2phodR.Fill(phodR)

        SR2nPho.Fill(len(pholist))
        diPhotonM.Fill((TRVSR2pho1+TRVSR2pho2).M())
        SR2MET.Fill(chain_in.pfMET)
        SR2_SingleElePt.Fill(chain_in.elePt[ele_ind])
        diPhotonM_MET.Fill((TRVSR2pho1+TRVSR2pho2).M(),chain_in.pfMET)
        LeadPhoEt.Fill(chain_in.phoEt[leadpho_ind])
        TrailPhoEt.Fill(chain_in.phoEt[trailpho_ind])
        SR2_LeadBjetPt.Fill(chain_in.jetPt[leadbjet_ind])
        SR2_nJet_nbJet.Fill(n_jet,n_bjet)

#------------------------------below for control region 1&2 depends on fake numbers
    if len(fakelist)==1 and len(pholist)==0:
        singlefake_ind=fakelist[0]
        cr1fake_index[0]=singlefake_ind
        (n_CR1)+=1
        TRVCR1fake.SetPtEtaPhiM(chain_in.phoEt[singlefake_ind],chain_in.phoEta[singlefake_ind],chain_in.phoPhi[singlefake_ind],0.0)
        tree3_out.Fill()
        CR1MET.Fill(chain_in.pfMET)
        dRfake_ele = dR(chain_in.phoEta[singlefake_ind],chain_in.eleEta[ele_ind],chain_in.phoPhi[singlefake_ind],chain_in.elePhi[ele_ind])
        CR1dR_fake_ele.Fill(dRfake_ele)
        SingleFakeEt.Fill(chain_in.phoEt[singlefake_ind])
        SingleFakeEta.Fill(chain_in.phoEta[singlefake_ind])
        SingleFakeR9.Fill(chain_in.phoR9[singlefake_ind])
        SingleFakeSigmaIPhiIPhi.Fill(chain_in.phoSigmaIPhiIPhi[singlefake_ind])
        SingleFakeSigmaIEtaIEta.Fill(chain_in.phoSigmaIEtaIEta[singlefake_ind])
        CR1invelefake.Fill((TRVele+TRVCR1fake).M())

        CR1_nJet_nbJet.Fill(n_jet,n_bjet)
#        SR1_nJet_nbJet_ratio.Fill(n_jet,n_bjet)
        CR1_SingleElePt.Fill(chain_in.elePt[ele_ind])
        CR1_LeadBjetPt.Fill(chain_in.jetPt[leadbjet_ind])

    elif len(fakelist)>=2 and len(pholist)==0:    
        leadfake_ind=max(fakelist,key=lambda x: chain_in.phoEt[x])
        trailfake_ind=max([pp for pp in fakelist if pp!=leadfake_ind],key=lambda x: chain_in.phoEt[x])
        cr2fake_index[0]=leadfake_ind
        cr2fake_index[1]=trailfake_ind
        TRVCR2fake1.SetPtEtaPhiM(chain_in.phoEt[leadfake_ind],chain_in.phoEta[leadfake_ind],chain_in.phoPhi[leadfake_ind],0.0)
        TRVCR2fake2.SetPtEtaPhiM(chain_in.phoEt[trailfake_ind],chain_in.phoEta[trailfake_ind],chain_in.phoPhi[trailfake_ind],0.0)
#        fakedR=fake1.DeltaR(fake2)
#        if fakedR<0.5:
#            continue
        (n_CR2)+=1
        tree4_out.Fill()
        CR2nFake.Fill(len(fakelist))
        diFakeM.Fill((TRVCR2fake1+TRVCR2fake2).M())
        CR2MET.Fill(chain_in.pfMET)
        CR2_SingleElePt.Fill(chain_in.elePt[ele_ind])
        diFakeM_MET.Fill((TRVCR2fake1+TRVCR2fake2).M(),chain_in.pfMET)
        LeadFakeEt.Fill(chain_in.phoEt[leadfake_ind])
        TrailFakeEt.Fill(chain_in.phoEt[trailfake_ind])
        CR2_LeadBjetPt.Fill(chain_in.jetPt[leadbjet_ind])
        CR2_nJet_nbJet.Fill(n_jet,n_bjet)





#file_out.Write()
#file_out.Close()

print "----------------------"
print "TotalEventNumber = ", n_events
print "n_singleEle pass = ", n_singleEle
print "n_pre selection = ",n_pre
print "n_SR1 = ", n_SR1
print "n_SR2 = ", n_SR2
print "n_CR1 = ", n_CR1
print "n_CR2 = ", n_CR2
print "----------------------"


#### to write in logpre.txt
log.write("############################################################\n")
log.write("INPUT %s"%sys.argv[1])
log.write("\nOutPUT %s\n"%sys.argv[2])
log.write("%s"%datetime.datetime.now())
log.write("\nTotalEventNumber = %s"%n_events)
log.write( "\nn_singleEle pass =%s "%n_singleEle)
log.write("\nn_pre selection = %s"%n_pre)
log.write("\nn_SR1 =%s "%n_SR1)
log.write("\nn_SR2 =%s "%n_SR2)
log.write("\nn_CR1 =%s "%n_CR1)
log.write("\nn_CR2 =%s "%n_CR2)
log.write( "\n----------------------\n\n")
log.close()



c=ROOT.TCanvas("c","Plots",800,800)
c.cd()
pre_nPho.Draw()
gPad.SetLogy()
gPad.Update()
c.Print("pre_nPho.pdf","pdf")

c.Clear()
pre_nFake.Draw()
gPad.SetLogy()
gPad.Update()
c.Print("pre_nFake.pdf","pdf")


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
SR1MET.Draw("e")
SR1MET.SetTitle("EleChannel SR1:MET;MET (GeV);")
gPad.SetLogy()
gPad.Update()
c.Print("SR1MET.pdf","pdf")


c.Clear()
SR1dR_pho_ele.Draw()
SR1dR_pho_ele.SetTitle("EleChannel SR1: dR(#gammaele);;")
c.Print("SR1dR_pho_ele.pdf","pdf")

c.Clear()
SR1_SingleElePt.Draw()
SR1_SingleElePt.SetTitle("EleChannel SR1;ele_Pt (GeV/c);")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR1_SingleEle.pdf","pdf")


c.Clear()
SinglePhoR9.Draw()
SinglePhoR9.SetTitle("SR1:;#gamma_R9;")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR1_SinglePhoR9.pdf","pdf")

c.Clear()
SinglePhoSigmaIEtaIEta.Draw()
SinglePhoSigmaIEtaIEta.SetTitle("SR1:;#gamma_i#etai#eta;")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR1_SinglePhoSigmaIEtaIEta.pdf","pdf")

c.Clear()
SinglePhoSigmaIPhiIPhi.Draw()
SinglePhoSigmaIPhiIPhi.SetTitle("SR1:;#gamma_i#phii#phi;")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR1_SinglePhoSigmaIPhiIPhi.pdf","pdf")

c.Clear()
SinglePhoEt.Draw()
SinglePhoEt.SetTitle("SR1: #gamma;#gamma_{Et} (GeV);")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR1_SinglePhoEt.pdf","pdf")

c.Clear()
SinglePhoEta.Draw()
SinglePhoEta.SetTitle("SR1: #gamma;#gamma_#eta;")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR1_SinglePhoEta.pdf","pdf")


c.Clear()
SR1_LeadBjetPt.Draw()
SR1_LeadBjetPt.SetTitle("SR1;Lead bjet_Pt (GeV/c);")
c.Print("SR1_LeadBjetPt.pdf","pdf")


c.Clear()
SR1invelepho.SetTitle("SR1;invmass_e#gamma;")
SR1invelepho.Draw()
c.Print("SR1invelepho.pdf","pdf")

#checkpoint
c.Clear()
SR2phodR.Draw()
c.Print("SR2phodR.pdf","pdf")



c.Clear()
SR2_SingleElePt.Draw()
SR2_SingleElePt.SetTitle("EleChannel SR2;ele_Pt (GeV/c);")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR2_SingleElePt.pdf","pdf")

c.Clear()
SR2MET.Draw("e")
SR2MET.SetTitle("EleChannel SR2:MET;MET (GeV);")
gPad.SetLogy()
gPad.Update()
c.Print("SR2MET.pdf","pdf")

c.Clear()
diPhotonM.Draw("e")
diPhotonM.SetTitle("SR2: #gamma#gamma;m_{#gamma#gamma} (GeV);")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR2_diPhotonM.pdf","pdf")

c.Clear()
SR2nPho.Draw()
SR2nPho.SetTitle("SR2;n_Photon;")
c.Print("SR2nPho.pdf","pdf")

c.Clear()
LeadPhoEt.Draw()
LeadPhoEt.SetTitle("SR2:Lead #gamma;Lead #gamma_Et(GeV);")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR2_LeadPhoEt.pdf","pdf")

c.Clear()
TrailPhoEt.Draw()
TrailPhoEt.SetTitle("SR2:Trail #gamma;Trail #gamma_Et(GeV);")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR2_TrailPhoEt.pdf","pdf")


c.Clear()
SR2_LeadBjetPt.Draw()
SR2_LeadBjetPt.SetTitle("SR2;Lead bjet_Pt (GeV/c);")
c.Print("SR2_LeadBjetPt.pdf","pdf")


c.Clear()
CR1MET.Draw("e")
CR1MET.SetTitle("EleChannel CR1:MET;MET (GeV);")
gPad.SetLogy()
gPad.Update()
c.Print("CR1MET.pdf","pdf")


c.Clear()
CR1dR_fake_ele.Draw()
CR1dR_fake_ele.SetTitle("EleChannel CR1: dR(fake-ele);;")
c.Print("CR1dR_fake_ele.pdf","pdf")

c.Clear()
CR1_SingleElePt.Draw()
CR1_SingleElePt.SetTitle("EleChannel CR1;ele_Pt (GeV/c);")
#gPad.SetLogy()
#gPad.Update()
c.Print("CR1_SingleEle.pdf","pdf")


c.Clear()
SingleFakeR9.Draw()
SingleFakeR9.SetTitle("CR1:;fake_R9;")
#gPad.SetLogy()
#gPad.Update()
c.Print("CR1_SingleFakeR9.pdf","pdf")

c.Clear()
SingleFakeSigmaIEtaIEta.Draw()
SingleFakeSigmaIEtaIEta.SetTitle("CR1:;fake_i#etai#eta;")
#gPad.SetLogy()
#gPad.Update()
c.Print("CR1_SingleFakeSigmaIEtaIEta.pdf","pdf")

c.Clear()
SingleFakeSigmaIPhiIPhi.Draw()
SingleFakeSigmaIPhiIPhi.SetTitle("CR1:;fake_i#phii#phi;")
#gPad.SetLogy()
#gPad.Update()
c.Print("CR1_SingleFakeSigmaIPhiIPhi.pdf","pdf")

c.Clear()
SingleFakeEt.Draw()
SingleFakeEt.SetTitle("CR1: fake;fake_{Et} (GeV);")
#gPad.SetLogy()
#gPad.Update()
c.Print("CR1_SingleFakeEt.pdf","pdf")

c.Clear()
SingleFakeEta.Draw()
SingleFakeEta.SetTitle("CR1: fake;fake_#eta;")
#gPad.SetLogy()
#gPad.Update()
c.Print("CR1_SingleFakeEta.pdf","pdf")


c.Clear()
CR1_LeadBjetPt.Draw()
CR1_LeadBjetPt.SetTitle("CR1;Lead bjet_Pt (GeV/c);")
c.Print("CR1_LeadBjetPt.pdf","pdf")


c.Clear()
CR1invelefake.SetTitle("CR1;invmass_e-fake;")
CR1invelefake.Draw()
c.Print("CR1invelefake.pdf","pdf")

c.Clear()
CR2_SingleElePt.Draw()
CR2_SingleElePt.SetTitle("EleChannel CR2;ele_Pt (GeV/c);")
#gPad.SetLogy()
#gPad.Update()
c.Print("CR2_SingleElePt.pdf","pdf")

c.Clear()
CR2MET.Draw("e")
CR2MET.SetTitle("EleChannel CR2:MET;MET (GeV);")
gPad.SetLogy()
gPad.Update()
c.Print("CR2MET.pdf","pdf")

c.Clear()
diFakeM.Draw("e")
diFakeM.SetTitle("CR2: ff;m_{ff} (GeV);")
#gPad.SetLogy()
#gPad.Update()
c.Print("CR2_diFakeM.pdf","pdf")

c.Clear()
CR2nFake.Draw()
CR2nFake.SetTitle("CR2;n_Fake;")
c.Print("CR2nFake.pdf","pdf")

c.Clear()
LeadFakeEt.Draw()
LeadFakeEt.SetTitle("CR2:Lead fake;Lead fake_Et(GeV);")
#gPad.SetLogy()
#gPad.Update()
c.Print("CR2_LeadFakeEt.pdf","pdf")

c.Clear()
TrailFakeEt.Draw()
TrailFakeEt.SetTitle("CR2:Trail fake;Trail fake_Et(GeV);")
#gPad.SetLogy()
#gPad.Update()
c.Print("CR2_TrailFakeEt.pdf","pdf")


c.Clear()
CR2_LeadBjetPt.Draw()
CR2_LeadBjetPt.SetTitle("CR2;Lead bjet_Pt (GeV/c);")
c.Print("CR2_LeadBjetPt.pdf","pdf")



c.Clear()
c.SetRightMargin(0.14)
pre_nJet_nbJet.Draw("colz")
pre_nJet_nbJet.SetTitle("pre;n_Jet;nbJet")
gStyle.SetOptStat(0)
#gPad.SetLogy(0)
#gPad.SetLogz()                                                
#gPad.Update()
c.Print("pre_nJet_nbJet.pdf","pdf")

c.Clear()
c.SetRightMargin(0.14)
SR1_nJet_nbJet.Draw("colz")
SR1_nJet_nbJet.SetTitle("SR1;n_Jet;nbJet")
gStyle.SetOptStat(0)
gPad.SetLogy(0)
gPad.SetLogz()                                                            
gPad.Update()
c.Print("SR1_nJet_nbJet.pdf","pdf")


c.Clear()
c.SetRightMargin(0.14)
SR2_nJet_nbJet.Draw("colz")
SR2_nJet_nbJet.SetTitle("SR2;n_Jet;nbJet")
gStyle.SetOptStat(0)
#gPad.SetLogy(0)
#gPad.SetLogz()                                                
#gPad.Update()
c.Print("SR2_nJet_nbJet.pdf","pdf")

c.Clear()
c.SetRightMargin(0.14)
c.SetLeftMargin(0.12)
diPhotonM_MET.Draw("colz")
diPhotonM_MET.SetTitle("SR2: diPhotonMass vs MET;m_{#gamma#gamma} (GeV); MET")
diPhotonM_MET.GetYaxis().SetTitleOffset(1.5)
gStyle.SetOptStat(0)
#gPad.SetLogy(0)
#gPad.SetLogz()
#gPad.Update()
c.Print("SR2_diPhotonM_MET.pdf","pdf")


c.Clear()
c.SetRightMargin(0.14)
CR1_nJet_nbJet.Draw("colz")
CR1_nJet_nbJet.SetTitle("CR1;n_Jet;nbJet")
gStyle.SetOptStat(0)
gPad.SetLogy(0)
gPad.SetLogz()                                                            
gPad.Update()
c.Print("CR1_nJet_nbJet.pdf","pdf")


c.Clear()
c.SetRightMargin(0.14)
CR2_nJet_nbJet.Draw("colz")
CR2_nJet_nbJet.SetTitle("CR2;n_Jet;nbJet")
gStyle.SetOptStat(0)
#gPad.SetLogy(0)
#gPad.SetLogz()                                                
#gPad.Update()
c.Print("CR2_nJet_nbJet.pdf","pdf")

c.Clear()
c.SetRightMargin(0.14)
c.SetLeftMargin(0.12)
diFakeM_MET.Draw("colz")
diFakeM_MET.SetTitle("CR2: diFakeMass vs MET;m_{ff} (GeV); MET")
diFakeM_MET.GetYaxis().SetTitleOffset(1.5)
gStyle.SetOptStat(0)
#gPad.SetLogy(0)
#gPad.SetLogz()
#gPad.Update()
c.Print("CR2_diFakeM_MET.pdf","pdf")


file_out.Write()
file_out.Close()


sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"


