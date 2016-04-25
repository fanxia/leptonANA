#!/bin/python
# 3.17.2016 by Fan Xia
# This template uses the reduced EventTree_pre from dir:preselected as input, make SR and CR selection and store the new tree to dir:selected 
# For any change of the selection cuts, should do this ana again
# This script for mc bkg

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
chain_in.SetBranchStatus("AK8*",0)
n_events = chain_in.GetEntries()
print"Total events for processing: ",n_events

dd=datetime.datetime.now().strftime("%b%d")
log = open("skimlogANA.txt","a")
os.system('mkdir -p ../selected/skim_'+sys.argv[2]+dd)
os.chdir('../selected/skim_'+sys.argv[2]+dd)
file_out = ROOT.TFile("skim_"+sys.argv[2]+".root","recreate")
#------------define hists' bin size
#nxbin_pt=18
xbin_pt=array('d',[0,20,40,60,80,100,120,140,160,180,200,250,300,400,500,600,800,1000,1250])
#nxbin_met=11
xbin_met=array('d',[0,20,40,60,80,100,150,200,250,300,500,1000])

#------------

#--------------------define hists
pre_SingleElePt = ROOT.TH1F("pre_SingleElePt","pre_SingleElePt",17,xbin_pt)
pre_SingleEleEta = ROOT.TH1F("pre_SingleEleEta","pre_SingleEleEta",60,-3,3)
pre_nPho = ROOT.TH1F("pre_nPho","pre_nPho",5,0,5)
pre_nFake = ROOT.TH1F("pre_nFake","pre_nFake",5,0,5)
pre_nJet = ROOT.TH1F("pre_nJet","pre_nJet",20,0,20)
preMET = ROOT.TH1F("preMET","preMET",11,xbin_met)
pre_LeadBjetPt = ROOT.TH1F("pre_LeadBjetPt","pre_LeadBjetPt",17,xbin_pt)
pre_nJet_nbJet = ROOT.TH2F("pre_nJet_nbJet","pre_nJet_nbJet",20,0,20,10,0,10)
pre_jetHt = ROOT.TH1F("pre_jetHt","pre_jetHt",18,xbin_pt)

SR1_SingleElePt = ROOT.TH1F("SR1_SingleElePt","SR1_SingleElePt",16,xbin_pt)
SR1dR_pho_ele = ROOT.TH1F("SR1dR_pho_ele","SR1dR_pho_ele",100,0,10)
SinglePhoEt = ROOT.TH1F("SinglePhoEt","SinglePhoEt",17,xbin_pt)
SinglePhoEta = ROOT.TH1F("SinglePhoEta","SinglePhoEta",60,-3,3)
SinglePhoR9 = ROOT.TH1F("SinglePhoR9","SinglePhoR9",60,0,1.2)
SinglePhoSigmaIEtaIEta = ROOT.TH1F("SinglePhoSigmaIEtaIEta","SinglePhoSigmaIEtaIEta",100,0,0.05)
SinglePhoSigmaIPhiIPhi = ROOT.TH1F("SinglePhoSigmaIPhiIPhi","SinglePhoSigmaIPhiIPhi",100,0,0.1)
SR1MET = ROOT.TH1F("SR1MET","SR1MET",11,xbin_met)
SR1_LeadBjetPt = ROOT.TH1F("SR1_LeadBjetPt","SR1_LeadBjetPt",17,xbin_pt)
SR1_nJet_nbJet = ROOT.TH2F("SR1_nJet_nbJet","SR1_nJet_nbJet",15,0,15,10,0,10)
SR1invelepho = ROOT.TH1F("SR1invelepho","SR1invelepho",11,xbin_met)
SR1_jetHt = ROOT.TH1F("SR1_jetHt","SR1_jetHt",18,xbin_pt)
#SR1_nJet_nbJet_ratio = ROOT.TH2F("SR1_nJet_nbJet_ratio","SR1_nJet_nbJet_ratio",15,0,15,10,0,10)


SR2phodR = ROOT.TH1F("SR2phodR","SR2phodR",100,0,10)
SR2_SingleElePt = ROOT.TH1F("SR2_SingleElePt","SR2_SingleElePt",16,xbin_pt)
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


CR1_SingleElePt = ROOT.TH1F("CR1_SingleElePt","CR1_SingleElePt",16,xbin_pt)
CR1dR_fake_ele = ROOT.TH1F("CR1dR_fake_ele","CR1dR_fake_ele",100,0,10)
SingleFakeEt = ROOT.TH1F("SingleFakeEt","SingleFakeEt",17,xbin_pt)
SingleFakeEta = ROOT.TH1F("SingleFakeEta","SingleFakeEta",60,-3,3)
SingleFakeR9 = ROOT.TH1F("SingleFakeR9","SingleFakeR9",60,0,1.2)
SingleFakeSigmaIEtaIEta = ROOT.TH1F("SingleFakeSigmaIEtaIEta","SingleFakeSigmaIEtaIEta",100,0,0.05)
SingleFakeSigmaIPhiIPhi = ROOT.TH1F("SingleFakeSigmaIPhiIPhi","SingleFakeSigmaIPhiIPhi",100,0,0.1)
CR1MET = ROOT.TH1F("CR1MET","CR1MET",11,xbin_met)
CR1_LeadBjetPt = ROOT.TH1F("CR1_LeadBjetPt","CR1_LeadBjetPt",17,xbin_pt)
CR1_nJet_nbJet = ROOT.TH2F("CR1_nJet_nbJet","CR1_nJet_nbJet",15,0,15,10,0,10)
CR1invelefake = ROOT.TH1F("CR1invelefake","CR1invelefake",11,xbin_met)
CR1_jetHt = ROOT.TH1F("CR1_jetHt","CR1_jetHt",18,xbin_pt)
#CR1_nJet_nbJet_ratio = ROOT.TH2F("CR1_nJet_nbJet_ratio","CR1_nJet_nbJet_ratio",15,0,15,10,0,10)



CR2_SingleElePt = ROOT.TH1F("CR2_SingleElePt","CR2_SingleElePt",16,xbin_pt)
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





#--------------define extra branches to record seleted obj------------

region=array('i',[-1])
nVtx=array('i',[-1])
rho=array('d',[-1.])
pfMET=array('d',[-1.])
elePt=array('d',[-1.])
eleEta=array('d',[-1.])
elePhi=array('d',[-1.])
elePFChIso=array('d',[-1.])
elePFPhoIso=array('d',[-1.])
eleNeuIso=array('d',[-1.])
elePFPUIso=array('d',[-1.])
njet=array('i',[-1])
jetPt=vector(float)(0)
jetEta=vector(float)(0)
jetPhi=vector(float)(0)
nbjet=array('i',[-1])
bjetPt=vector(float)(0)
bjetEta=vector(float)(0)
bjetPhi=vector(float)(0)
nPho=array('i',[-1])
phoEt=vector(float)(0)
phoEta=vector(float)(0)
phoPhi=vector(float)(0)
nFake=array('i',[-1])
fakeEt=vector(float)(0)
fakeEta=vector(float)(0)
fakePhi=vector(float)(0)


#-----------------------------------------------
tree_out=TTree("EventTree","EventTree")
tree_out.Branch("region",region,"region/I")
tree_out.Branch("nVtx",nVtx,"nVtx/I")
tree_out.Branch("rho",rho,"rho/D")
tree_out.Branch("pfMET",pfMET,"pfMET/D")
tree_out.Branch("elePt",elePt,"elePt/D")
tree_out.Branch("eleEta",eleEta,"eleEta/D")
tree_out.Branch("elePhi",elePhi,"elePhi/D")


tree_out.Branch("njet",njet,"njet/I")
tree_out.Branch("nbjet",nbjet,"nbjet/I")
tree_out.Branch("bjetPt",bjetPt)
tree_out.Branch("bjetEta",bjetEta)
tree_out.Branch("bjetPhi",bjetPhi)
tree_out.Branch("jetPt",jetPt)
tree_out.Branch("jetEta",jetEta)
tree_out.Branch("jetPhi",jetPhi)

tree_out.Branch("nPho",nPho,"nPho/I")
tree_out.Branch("phoEt",phoEt)
tree_out.Branch("phoEta",phoEta)
tree_out.Branch("phoPhi",phoPhi)

tree_out.Branch("nFake",nFake,"nFake/I")
tree_out.Branch("fakeEt",fakeEt)
tree_out.Branch("fakeEta",fakeEta)
tree_out.Branch("fakePhi",fakePhi)



TRVSR2pho1=ROOT.TLorentzVector()
TRVSR2pho2=ROOT.TLorentzVector()
TRVSR1pho=ROOT.TLorentzVector()
TRVCR2fake1=ROOT.TLorentzVector()
TRVCR2fake2=ROOT.TLorentzVector()
TRVCR1fake=ROOT.TLorentzVector()
TRVele=ROOT.TLorentzVector()

n_hlt=0
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


# -----------------1.HLT selection(HLT_Ele23_WP75_Gsf_v)

    hltele = chain_in.HLTEleMuX>>6&1
    if hltele!=1:
        continue
    n_hlt+=1


#-------------------1+2. only one tight ele
    n_tightEle=0
    n_looseEle=0
    for e in range(chain_in.nEle):
        if good_TightEle(chain_in.elePt[e],chain_in.eleEta[e],chain_in.eleIDbit[e]):
            n_tightEle+=1
            ele_ind=e
        if good_LooseEle(chain_in.elePt[e],chain_in.eleEta[e],chain_in.eleIDbit[e]):
            n_looseEle+=1
    if n_tightEle !=1 or n_looseEle !=1:
        continue

    n_looseMu=0
    for m in range(chain_in.nMu):
        muPFIso=muPFRelCombIso(chain_in.muPt[m],chain_in.muPFChIso[m],chain_in.muPFNeuIso[m],chain_in.muPFPhoIso[m],chain_in.muPFPUIso[m])
#        print "iso",i,"---",muPFIso
        if good_LooseMu(chain_in.muPt[m],chain_in.muEta[m],chain_in.muIsLooseID[m],muPFIso):
            n_looseMu+=1
    if n_looseMu !=0:
        continue

    n_singleEle+=1     

    elePt[0]=chain_in.elePt[ele_ind]
    eleEta[0]=chain_in.eleEta[ele_ind]
    elePhi[0]=chain_in.elePhi[ele_ind]

#--------------------1+2+3.at least 3 jets and 1 bjet
    n_jet=0
    n_bjet=0
    jetlist =[]
    bjetlist=[]
    jetht=0
    for j in range(chain_in.nJet):
        if good_LooseJet(chain_in.jetPt[j],chain_in.jetEta[j], chain_in.jetPFLooseId[j]):
            n_jet+=1
            jetlist.append(j)
            jetht=jetht+chain_in.jetPt[j]
            if chain_in.jetpfCombinedInclusiveSecondaryVertexV2BJetTags[j]>0.89:
                n_bjet+=1
                bjetlist.append(j)
    if n_jet<3 or n_bjet<1:
        continue
    n_pre+=1
    leadbjet_ind=max(bjetlist,key=lambda x: chain_in.jetPt[x])

    region[0]=0
    pfMET[0]=chain_in.pfMET
    nVtx[0]=chain_in.nVtx
    rho[0]=chain_in.rho
    njet[0]=len(jetlist)
    nbjet[0]=len(bjetlist)
    for bind in bjetlist: 
        bjetPt.push_back(chain_in.jetPt[bind])
        bjetEta.push_back(chain_in.jetEta[bind])
        bjetPhi.push_back(chain_in.jetPhi[bind])
    for ind in jetlist: 
        jetPt.push_back(chain_in.jetPt[ind])
        jetEta.push_back(chain_in.jetEta[ind])
        jetPhi.push_back(chain_in.jetPhi[ind])



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

    nPho[0]=len(pholist)
    for pind in pholist: 
        phoEt.push_back(chain_in.phoEt[pind])
        phoEta.push_back(chain_in.phoEta[pind])
        phoPhi.push_back(chain_in.phoPhi[pind])
    nFake[0]=len(fakelist)
    for pind in fakelist: 
        fakeEt.push_back(chain_in.phoEt[pind])
        fakeEta.push_back(chain_in.phoEta[pind])
        fakePhi.push_back(chain_in.phoPhi[pind])


#---------------------fake dR loop----
    # fakelist2=[]
    # for f1 in fakelist1:
    #      dRfake_ele = dR(chain_in.phoEta[f1],chain_in.eleEta[ele_ind],chain_in.phoPhi[f1],chain_in.elePhi[ele_ind])
    #      if dRfake_ele<=0.3:
    #          continue
    #      fakelist2.append(f1)
        
    # fakelist3=[]
    # for f2 in fakelist2:
    #     w = 1
    #     for j in jetlist:
    #          dRfaket_jet = dR(chain_in.phoEta[f2],chain_in.jetEta[j],chain_in.phoPhi[f2],chain_in.jetPhi[j])
    #          if dRfaket_jet<=0.3:
    #              w=0
    #              break
    #     if w==1:
    #          fakelist3.append(f2)

    # fakelist=[]
    # for f3 in fakelist3:
    #      w = 1
    #      for f4 in fakelist3:
    #          dRfake_fake = dR(chain_in.phoEta[f3],chain_in.phoEta[f4],chain_in.phoPhi[f3],chain_in.phoPhi[f4])
    #          if dRfake_fake<=0.3 and f4!=f3:
    #              w=0
    #              break
    #      if w==1:
    #          fakelist.append(f3)


#-----------------------below for pre plots

#    pholist=pholist1
#    fakelist=fakelist1

    pre_nPho.Fill(len(pholist))
    pre_nFake.Fill(len(fakelist))
    pre_SingleElePt.Fill(chain_in.elePt[ele_ind])
    pre_SingleEleEta.Fill(chain_in.eleEta[ele_ind])
    pre_nJet_nbJet.Fill(n_jet,n_bjet)
    pre_LeadBjetPt.Fill(chain_in.jetPt[leadbjet_ind])
    preMET.Fill(chain_in.pfMET)
    pre_nJet.Fill(n_jet)
    pre_jetHt.Fill(jetht)

#-------------------------below for signal region1 &2
    if len(pholist)==1:
        region[0]=1
        singlepho_ind=pholist[0]

        (n_SR1)+=1
        TRVSR1pho.SetPtEtaPhiM(chain_in.phoEt[singlepho_ind],chain_in.phoEta[singlepho_ind],chain_in.phoPhi[singlepho_ind],0.0)

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
        SR1_jetHt.Fill(jetht)
    elif len(pholist)>=2:
        region[0]=2
        leadpho_ind=max(pholist,key=lambda x: chain_in.phoEt[x])
        trailpho_ind=max([pp for pp in pholist if pp!=leadpho_ind],key=lambda x: chain_in.phoEt[x])
        TRVSR2pho1.SetPtEtaPhiM(chain_in.phoEt[leadpho_ind],chain_in.phoEta[leadpho_ind],chain_in.phoPhi[leadpho_ind],0.0)
        TRVSR2pho2.SetPtEtaPhiM(chain_in.phoEt[trailpho_ind],chain_in.phoEta[trailpho_ind],chain_in.phoPhi[trailpho_ind],0.0)
#        phodR=pho1.DeltaR(pho2)
#        if phodR<0.5:
#            continue
        (n_SR2)+=1

        
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
        SR2_jetHt.Fill(jetht)
#------------------------------below for control region 1&2 depends on fake numbers
    if len(fakelist)==1 and len(pholist)==0:
        region[0]=3
        singlefake_ind=fakelist[0]
        (n_CR1)+=1
        TRVCR1fake.SetPtEtaPhiM(chain_in.phoEt[singlefake_ind],chain_in.phoEta[singlefake_ind],chain_in.phoPhi[singlefake_ind],0.0)

        CR1MET.Fill(chain_in.pfMET)
        dRfake_ele = dR(chain_in.phoEta[singlefake_ind],chain_in.eleEta[ele_ind],chain_in.phoPhi[singlefake_ind],chain_in.elePhi[ele_ind])
        CR1dR_fake_ele.Fill(dRfake_ele)
        SingleFakeEt.Fill(chain_in.phoEt[singlefake_ind])
        SingleFakeEta.Fill(chain_in.phoEta[singlefake_ind])
        SingleFakeR9.Fill(chain_in.phoR9[singlefake_ind])
        SingleFakeSigmaIPhiIPhi.Fill(chain_in.phoSigmaIPhiIPhi[singlefake_ind])
        SingleFakeSigmaIEtaIEta.Fill(chain_in.phoSigmaIEtaIEta[singlefake_ind])
        CR1invelefake.Fill((TRVele+TRVCR1fake).M())
        CR1_jetHt.Fill(jetht)
        CR1_nJet_nbJet.Fill(n_jet,n_bjet)
#        SR1_nJet_nbJet_ratio.Fill(n_jet,n_bjet)
        CR1_SingleElePt.Fill(chain_in.elePt[ele_ind])
        CR1_LeadBjetPt.Fill(chain_in.jetPt[leadbjet_ind])

    elif len(fakelist)>=2 and len(pholist)==0:    
        region[0]=4
        leadfake_ind=max(fakelist,key=lambda x: chain_in.phoEt[x])
        trailfake_ind=max([pp for pp in fakelist if pp!=leadfake_ind],key=lambda x: chain_in.phoEt[x])
        TRVCR2fake1.SetPtEtaPhiM(chain_in.phoEt[leadfake_ind],chain_in.phoEta[leadfake_ind],chain_in.phoPhi[leadfake_ind],0.0)
        TRVCR2fake2.SetPtEtaPhiM(chain_in.phoEt[trailfake_ind],chain_in.phoEta[trailfake_ind],chain_in.phoPhi[trailfake_ind],0.0)
#        fakedR=fake1.DeltaR(fake2)
#        if fakedR<0.5:
#            continue
        (n_CR2)+=1
        CR2_jetHt.Fill(jetht)
        CR2nFake.Fill(len(fakelist))
        diFakeM.Fill((TRVCR2fake1+TRVCR2fake2).M())
        CR2MET.Fill(chain_in.pfMET)
        CR2_SingleElePt.Fill(chain_in.elePt[ele_ind])
        diFakeM_MET.Fill((TRVCR2fake1+TRVCR2fake2).M(),chain_in.pfMET)
        LeadFakeEt.Fill(chain_in.phoEt[leadfake_ind])
        TrailFakeEt.Fill(chain_in.phoEt[trailfake_ind])
        CR2_LeadBjetPt.Fill(chain_in.jetPt[leadbjet_ind])
        CR2_nJet_nbJet.Fill(n_jet,n_bjet)

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





#file_out.Write()
#file_out.Close()

print "----------------------"
print "TotalEventNumber = ", n_events
print "n_hlt pass = ",n_hlt
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
#c.Print("pre_nPho.pdf","pdf")

c.Clear()
pre_nFake.Draw()
gPad.SetLogy()
gPad.Update()
#c.Print("pre_nFake.pdf","pdf")


c.Clear()
pre_nJet.Draw()
#c.Print("pre_nJet.pdf","pdf")


c.Clear()
preMET.Sumw2()
preMET.Scale(1,"width")
preMET.Draw("e")
#preMET.SetBins()
preMET.SetTitle("EleChannel pre:MET;MET (GeV);N_events/GeV")
#c.print("preMET.pdf","pdf")


c.Clear()
pre_SingleElePt.Scale(1,"width")
pre_SingleElePt.Draw()
pre_SingleElePt.SetTitle("EleChannel pre;ele_Pt (GeV/c);N_events/GeV")
#c.print("pre_SingleEle.pdf","pdf")

c.Clear()
pre_SingleEleEta.Draw()
pre_SingleEleEta.SetTitle("EleChannel pre;ele_Eta;")
#c.print("pre_SingleEleEta.pdf","pdf")


c.Clear()
pre_LeadBjetPt.Scale(1,"width")
pre_LeadBjetPt.Draw()
pre_LeadBjetPt.SetTitle("pre;Lead bjet_Pt (GeV/c);N_events/GeV")
#c.print("pre_LeadBjetPt.pdf","pdf")

c.Clear()
pre_jetHt.Scale(1,"width")
pre_jetHt.Draw()
pre_jetHt.SetTitle("EleChannel pre-selection; HT_jets;N_events/GeV")


c.Clear()
SR1MET.Sumw2()
SR1MET.Scale(1,"width")
SR1MET.Draw("e")
SR1MET.SetTitle("EleChannel SR1:MET;MET (GeV);N_events/GeV")
gPad.SetLogy()
gPad.Update()
#c.print("SR1MET.pdf","pdf")


c.Clear()
SR1dR_pho_ele.Draw()
SR1dR_pho_ele.SetTitle("EleChannel SR1: dR(#gammaele);;")
#c.print("SR1dR_pho_ele.pdf","pdf")

c.Clear()
SR1_SingleElePt.Scale(1,"width")
SR1_SingleElePt.Draw()
SR1_SingleElePt.SetTitle("EleChannel SR1;ele_Pt (GeV/c);N_events/GeV")
#gPad.SetLogy()
#gPad.Update()
#c.print("SR1_SingleEle.pdf","pdf")


c.Clear()
SinglePhoR9.Draw()
SinglePhoR9.SetTitle("SR1:;#gamma_R9;")
#gPad.SetLogy()
#gPad.Update()
#c.print("SR1_SinglePhoR9.pdf","pdf")

c.Clear()
SinglePhoSigmaIEtaIEta.Draw()
SinglePhoSigmaIEtaIEta.SetTitle("SR1:;#gamma_i#etai#eta;")
#gPad.SetLogy()
#gPad.Update()
#c.print("SR1_SinglePhoSigmaIEtaIEta.pdf","pdf")

c.Clear()
SinglePhoSigmaIPhiIPhi.Draw()
SinglePhoSigmaIPhiIPhi.SetTitle("SR1:;#gamma_i#phii#phi;")
#gPad.SetLogy()
#gPad.Update()
#c.print("SR1_SinglePhoSigmaIPhiIPhi.pdf","pdf")

c.Clear()
SinglePhoEt.Scale(1,"width")
SinglePhoEt.Draw()
SinglePhoEt.SetTitle("SR1: #gamma;#gamma_{Et} (GeV);N_events/GeV")
#gPad.SetLogy()
#gPad.Update()
#c.print("SR1_SinglePhoEt.pdf","pdf")

c.Clear()
SinglePhoEta.Draw()
SinglePhoEta.SetTitle("SR1: #gamma;#gamma_#eta;")
#gPad.SetLogy()
#gPad.Update()
#c.print("SR1_SinglePhoEta.pdf","pdf")


c.Clear()
SR1_LeadBjetPt.Scale(1,"width")
SR1_LeadBjetPt.Draw()
SR1_LeadBjetPt.SetTitle("SR1;Lead bjet_Pt (GeV/c);N_events/GeV")
#c.print("SR1_LeadBjetPt.pdf","pdf")


c.Clear()
SR1invelepho.Scale(1,"width")
SR1invelepho.SetTitle("SR1;invmass_e#gamma;N_events/GeV")
SR1invelepho.Draw()
#c.print("SR1invelepho.pdf","pdf")

c.Clear()
SR1_jetHt.Scale(1,"width")
SR1_jetHt.Draw()
SR1_jetHt.SetTitle("EleChannel SR1; HT_jets;N_events/GeV")


#checkpoint
c.Clear()
SR2phodR.Draw()
#c.print("SR2phodR.pdf","pdf")



c.Clear()
SR2_SingleElePt.Scale(1,"width")
SR2_SingleElePt.Draw()
SR2_SingleElePt.SetTitle("EleChannel SR2;ele_Pt (GeV/c);N_events/GeV")
#gPad.SetLogy()
#gPad.Update()
#c.print("SR2_SingleElePt.pdf","pdf")

c.Clear()
SR2MET.Sumw2()
SR2MET.Scale(1,"width")
SR2MET.Draw("e")
SR2MET.SetTitle("EleChannel SR2:MET;MET (GeV);N_events/GeV")
gPad.SetLogy()
gPad.Update()
#c.print("SR2MET.pdf","pdf")

c.Clear()
diPhotonM.Scale(1,"width")
diPhotonM.Draw("e")
diPhotonM.SetTitle("SR2: #gamma#gamma;m_{#gamma#gamma} (GeV);N_events/GeV")
#gPad.SetLogy()
#gPad.Update()
#c.print("SR2_diPhotonM.pdf","pdf")

c.Clear()
SR2nPho.Draw()
SR2nPho.SetTitle("SR2;n_Photon;")
#c.print("SR2nPho.pdf","pdf")

c.Clear()
LeadPhoEt.Scale(1,"width")
LeadPhoEt.Draw()
LeadPhoEt.SetTitle("SR2:Lead #gamma;Lead #gamma_Et(GeV);N_events/GeV")
#gPad.SetLogy()
#gPad.Update()
#c.print("SR2_LeadPhoEt.pdf","pdf")

c.Clear()
TrailPhoEt.Scale(1,"width")
TrailPhoEt.Draw()
TrailPhoEt.SetTitle("SR2:Trail #gamma;Trail #gamma_Et(GeV);N_events/GeV")
#gPad.SetLogy()
#gPad.Update()
#c.print("SR2_TrailPhoEt.pdf","pdf")


c.Clear()
SR2_LeadBjetPt.Scale(1,"width")
SR2_LeadBjetPt.Draw()
SR2_LeadBjetPt.SetTitle("SR2;Lead bjet_Pt (GeV/c);N_events/GeV")
#c.print("SR2_LeadBjetPt.pdf","pdf")

c.Clear()
SR2_jetHt.Scale(1,"width")
SR2_jetHt.Draw()
SR2_jetHt.SetTitle("EleChannel SR2; HT_jets;N_events/GeV")


c.Clear()
CR1MET.Sumw2()
CR1MET.Scale(1,"width")
CR1MET.Draw("e")
CR1MET.SetTitle("EleChannel CR1:MET;MET (GeV);N_events/GeV")
gPad.SetLogy()
gPad.Update()
#c.print("CR1MET.pdf","pdf")


c.Clear()
CR1dR_fake_ele.Draw()
CR1dR_fake_ele.SetTitle("EleChannel CR1: dR(fake-ele);;")
#c.print("CR1dR_fake_ele.pdf","pdf")

c.Clear()
CR1_SingleElePt.Scale(1,"width")
CR1_SingleElePt.Draw()
CR1_SingleElePt.SetTitle("EleChannel CR1;ele_Pt (GeV/c);N_events/GeV")
#c.print("CR1_SingleEle.pdf","pdf")


c.Clear()
SingleFakeR9.Draw()
SingleFakeR9.SetTitle("CR1:;fake_R9;")
#c.print("CR1_SingleFakeR9.pdf","pdf")

c.Clear()
SingleFakeSigmaIEtaIEta.Draw()
SingleFakeSigmaIEtaIEta.SetTitle("CR1:;fake_i#etai#eta;")
#c.print("CR1_SingleFakeSigmaIEtaIEta.pdf","pdf")

c.Clear()
SingleFakeSigmaIPhiIPhi.Draw()
SingleFakeSigmaIPhiIPhi.SetTitle("CR1:;fake_i#phii#phi;")
#c.print("CR1_SingleFakeSigmaIPhiIPhi.pdf","pdf")

c.Clear()
SingleFakeEt.Scale(1,"width")
SingleFakeEt.Draw()
SingleFakeEt.SetTitle("CR1: fake;fake_{Et} (GeV);N_events/GeV")
#c.print("CR1_SingleFakeEt.pdf","pdf")

c.Clear()
SingleFakeEta.Draw()
SingleFakeEta.SetTitle("CR1: fake;fake_#eta;")
#c.print("CR1_SingleFakeEta.pdf","pdf")


c.Clear()
CR1_LeadBjetPt.Scale(1,"width")
CR1_LeadBjetPt.Draw()
CR1_LeadBjetPt.SetTitle("CR1;Lead bjet_Pt (GeV/c);N_events/GeV")
#c.print("CR1_LeadBjetPt.pdf","pdf")


c.Clear()
CR1invelefake.Scale(1,"width")
CR1invelefake.SetTitle("CR1;invmass_e-fake;N_events/GeV")
CR1invelefake.Draw()
#c.print("CR1invelefake.pdf","pdf")

c.Clear()
CR1_jetHt.Scale(1,"width")
CR1_jetHt.Draw()
CR1_jetHt.SetTitle("EleChannel CR1; HT_jets;N_events/GeV")


c.Clear()
CR2_SingleElePt.Scale(1,"width")
CR2_SingleElePt.Draw()
CR2_SingleElePt.SetTitle("EleChannel CR2;ele_Pt (GeV/c);N_events/GeV")
#c.print("CR2_SingleElePt.pdf","pdf")

c.Clear()
CR2MET.Sumw2()
CR2MET.Scale(1,"width")
CR2MET.Draw("e")
CR2MET.SetTitle("EleChannel CR2:MET;MET (GeV);N_events/GeV")
gPad.SetLogy()
gPad.Update()
#c.print("CR2MET.pdf","pdf")

c.Clear()
diFakeM.Scale(1,"width")
diFakeM.Draw("e")
diFakeM.SetTitle("CR2: ff;m_{ff} (GeV);N_events/GeV")
#c.print("CR2_diFakeM.pdf","pdf")

c.Clear()
CR2nFake.Draw()
CR2nFake.SetTitle("CR2;n_Fake;")
#c.print("CR2nFake.pdf","pdf")

c.Clear()
LeadFakeEt.Scale(1,"width")
LeadFakeEt.Draw()
LeadFakeEt.SetTitle("CR2:Lead fake;Lead fake_Et(GeV);N_events/GeV")
#c.print("CR2_LeadFakeEt.pdf","pdf")

c.Clear()
TrailFakeEt.Scale(1,"width")
TrailFakeEt.Draw()
TrailFakeEt.SetTitle("CR2:Trail fake;Trail fake_Et(GeV);N_events/GeV")
#c.print("CR2_TrailFakeEt.pdf","pdf")


c.Clear()
CR2_LeadBjetPt.Scale(1,"width")
CR2_LeadBjetPt.Draw()
CR2_LeadBjetPt.SetTitle("CR2;Lead bjet_Pt (GeV/c);N_events/GeV")
#c.print("CR2_LeadBjetPt.pdf","pdf")

c.Clear()
CR2_jetHt.Scale(1,"width")
CR2_jetHt.Draw()
CR2_jetHt.SetTitle("EleChannel CR2; HT_jets;N_events/GeV")


c.Clear()
c.SetRightMargin(0.14)
pre_nJet_nbJet.Draw("colz")
pre_nJet_nbJet.SetTitle("pre;n_Jet;nbJet")
gStyle.SetOptStat(0)
#gPad.SetLogy(0)
#gPad.SetLogz()                                                
#gPad.Update()
#c.Print("pre_nJet_nbJet.pdf","pdf")

c.Clear()
c.SetRightMargin(0.14)
SR1_nJet_nbJet.Draw("colz")
SR1_nJet_nbJet.SetTitle("SR1;n_Jet;nbJet")
gStyle.SetOptStat(0)
gPad.SetLogy(0)
gPad.SetLogz()                                                            
gPad.Update()
#c.Print("SR1_nJet_nbJet.pdf","pdf")


c.Clear()
c.SetRightMargin(0.14)
SR2_nJet_nbJet.Draw("colz")
SR2_nJet_nbJet.SetTitle("SR2;n_Jet;nbJet")
gStyle.SetOptStat(0)
#gPad.SetLogy(0)
#gPad.SetLogz()                                                
#gPad.Update()
#c.Print("SR2_nJet_nbJet.pdf","pdf")

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
#c.Print("SR2_diPhotonM_MET.pdf","pdf")


c.Clear()
c.SetRightMargin(0.14)
CR1_nJet_nbJet.Draw("colz")
CR1_nJet_nbJet.SetTitle("CR1;n_Jet;nbJet")
gStyle.SetOptStat(0)
gPad.SetLogy(0)
gPad.SetLogz()                                                            
gPad.Update()
#c.Print("CR1_nJet_nbJet.pdf","pdf")


c.Clear()
c.SetRightMargin(0.14)
CR2_nJet_nbJet.Draw("colz")
CR2_nJet_nbJet.SetTitle("CR2;n_Jet;nbJet")
gStyle.SetOptStat(0)
#gPad.SetLogy(0)
#gPad.SetLogz()                                                
#gPad.Update()
#c.Print("CR2_nJet_nbJet.pdf","pdf")

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
#c.Print("CR2_diFakeM_MET.pdf","pdf")


file_out.Write()
file_out.Close()


sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"


