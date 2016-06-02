#!/bin/python
# 3.31.2016 by Fan Xia
# This template uses the reduced EventTree_pre from dir:preselected as input, make SR and CR selection and store the new tree to dir:selected 
# For any change of the selection cuts, should do this ana again
# This script is used to build a skimmed tree with only the useful branches, 
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


sw = ROOT.TStopwatch()
sw.Start()
print "start"
print "input: "+sys.argv[1]
print "output: "+sys.argv[2]
chain_in = ROOT.TChain("ggNtuplizer/EventTree_pre")
#chain_in.Add("../preselected/reduced_Muchannel_dataSingleMu.root")
chain_in.Add(sys.argv[1])
chain_in.SetBranchStatus("AK8*",0)
n_events = chain_in.GetEntries()
print"Total events for processing: ",n_events

musffile = TFile.Open("../muonscalefac/muonsf.root")
muidsf=musffile.Get("tightidsf")
muisosf=musffile.Get("tightisosf")
mutrigsf=musffile.Get("trigsf")

dd=datetime.datetime.now().strftime("%b%d")
log = open("skim_logANA.txt","a")
os.system('mkdir -p ../selected/skim_ana_root'+dd)
os.chdir('../selected/skim_ana_root'+dd)
file_out = ROOT.TFile("skim_"+sys.argv[2]+".root","recreate")


#--------------define branches to record seleted obj------------

region=array('i',[-1])
nVtx=array('i',[-1])
rho=array('d',[-1.])
pfMET=array('d',[-1.])
puweight=array('d',[-1.])

totalweight=array('d',[-1.])
muPt=array('d',[-1.])
muEta=array('d',[-1.])
muPhi=array('d',[-1.])
muSF=array('d',[-1.])
muPFChIso=array('d',[-1.])
muPFPhoIso=array('d',[-1.])
muNeuIso=array('d',[-1.])
muPFPUIso=array('d',[-1.])
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
phoHoverE=vector(float)(0)
phoR9=vector(float)(0)
phoSigmaIEtaIEta=vector(float)(0)
phoSigmaIPhiIPhi=vector(float)(0)
nFake=array('i',[-1])
fakeEt=vector(float)(0)
fakeEta=vector(float)(0)
fakePhi=vector(float)(0)
fakeR9=vector(float)(0)
fakeSigmaIEtaIEta=vector(float)(0)
fakeSigmaIPhiIPhi=vector(float)(0)

#-----------------------------------------------

tree_out=TTree("EventTree","EventTree")
tree_out.Branch("region",region,"region/I")
tree_out.Branch("nVtx",nVtx,"nVtx/I")
tree_out.Branch("rho",rho,"rho/D")
tree_out.Branch("puweight",puweight,"puweight/D")
tree_out.Branch("totalweight",totalweight,"totalweight/D")
tree_out.Branch("pfMET",pfMET,"pfMET/D")
tree_out.Branch("muPt",muPt,"muPt/D")
tree_out.Branch("muEta",muEta,"muEta/D")
tree_out.Branch("muPhi",muPhi,"muPhi/D")
tree_out.Branch("muSF",muSF,"muSF/D")


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
tree_out.Branch("phoR9",phoR9)
tree_out.Branch("phoHoverE",phoHoverE)
tree_out.Branch("phoSigmaIEtaIEta",phoSigmaIEtaIEta)
tree_out.Branch("phoSigmaIPhiIPhi",phoSigmaIPhiIPhi)



tree_out.Branch("nFake",nFake,"nFake/I")
tree_out.Branch("fakeEt",fakeEt)
tree_out.Branch("fakeEta",fakeEta)
tree_out.Branch("fakePhi",fakePhi)
tree_out.Branch("fakeR9",fakeR9)
tree_out.Branch("fakeSigmaIEtaIEta",fakeSigmaIEtaIEta)
tree_out.Branch("fakeSigmaIPhiIPhi",fakeSigmaIPhiIPhi)


n_singleMu=0
n_pre=0
n_SR1=0
n_SR2=0
n_CR1=0
n_CR2=0
nweight_pre=0
nweight_SR1=0
nweight_SR2=0
nweight_CR1=0
nweight_CR2=0

#for i in range(1000):
for i in range(n_events):
    chain_in.GetEntry(i)
    
    if i%10000 ==0:
        print "Processing entry ", i
##----------------0.5Vertex clean

#    if abs(chain_in.vtz)>24 or abs(chain_in.rho)>2: continue     //error here since the rho is not the "rho"
#    if not chain_in.hasGoodVtx:
#        continue
#    n_goodvtx+=1
# -----------------1.HLT selection 31,32

#    hltmu1 = chain_in.HLTEleMuX>>31&1
#    hltmu2 = chain_in.HLTEleMuX>>32&1
#    if hltmu1!=1 and hltmu2!=1:
#        continue
#    n_hlt+=1


#-------------------1+2. only one tight muon
    n_looseEle=0
    for e in range(chain_in.nEle):
        if good_LooseEle(chain_in.elePt[e],chain_in.eleEta[e],chain_in.eleIDbit[e]):
            n_looseEle+=1
    if n_looseEle!=0:
        continue

    n_tightMu=0
    n_looseMu=0
    for m in range(chain_in.nMu):
        muPFIso=muPFRelCombIso(chain_in.muPt[m],chain_in.muPFChIso[m],chain_in.muPFNeuIso[m],chain_in.muPFPhoIso[m],chain_in.muPFPUIso[m])

        if good_TightMu(chain_in.muPt[m],chain_in.muEta[m],chain_in.muIsTightID[m],muPFIso):
            n_tightMu+=1
            mu_ind=m
#            mu_index[0]=m
        if good_LooseMu(chain_in.muPt[m],chain_in.muEta[m],chain_in.muIsLooseID[m],muPFIso):
            n_looseMu+=1
    if n_looseMu!=1 or n_tightMu!=1 :
        continue

    n_singleMu+=1     

    muPt[0]=chain_in.muPt[mu_ind]
    muEta[0]=chain_in.muEta[mu_ind]
    muPhi[0]=chain_in.muPhi[mu_ind]

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

#-------get puweight--------------------
    putrue=int(chain_in.puTrue[12])
    pu=puweightlist[putrue]
    puweight[0]=pu
#-------end get puweight----------------

#-------get muon sf: id*iso*trig-------------------
    pt=chain_in.muPt[mu_ind]
    eta=abs(chain_in.muEta[mu_ind])
    if pt<120:
        musf=(muidsf.GetBinContent(muidsf.FindBin(pt,eta)))*(muisosf.GetBinContent(muisosf.FindBin(pt,eta)))*(mutrigsf.GetBinContent(mutrigsf.FindBin(pt,eta)))
    else: musf=1.0
    muSF[0]=musf
#--------end muonsf------------------------------
#---------------------photon dR loop----
    pholist1=[]
    for p0 in range(chain_in.nPho):
         dRphoton_mu = dR(chain_in.phoEta[p0],chain_in.muEta[mu_ind],chain_in.phoPhi[p0],chain_in.muPhi[mu_ind])
         if dRphoton_mu<=0.3:
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
        phoR9.push_back(chain_in.phoR9[pind])
        phoHoverE.push_back(chain_in.phoHoverE[pind])
        phoSigmaIEtaIEta.push_back(chain_in.phoSigmaIEtaIEta[pind])
        phoSigmaIPhiIPhi.push_back(chain_in.phoSigmaIPhiIPhi[pind])

    nFake[0]=len(fakelist)
    for pind in fakelist: 
        fakeEt.push_back(chain_in.phoEt[pind])
        fakeEta.push_back(chain_in.phoEta[pind])
        fakePhi.push_back(chain_in.phoPhi[pind])
        fakeR9.push_back(chain_in.phoR9[pind])
        fakeSigmaIEtaIEta.push_back(chain_in.phoSigmaIEtaIEta[pind])
        fakeSigmaIPhiIPhi.push_back(chain_in.phoSigmaIPhiIPhi[pind])



#---------------------fake dR loop----
    # fakelist2=[]
    # for f1 in fakelist1:
    #      dRfake_ele = dR(chain_in.phoEta[f1],chain_in.muEta[mu_ind],chain_in.phoPhi[f1],chain_in.muPhi[mu_ind])
    #      if dRfake_mu<=0.3:
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

#-----------------------define weight which used to calculated the weighted event numbers

    weight=pu*musf
    totalweight[0]=weight
    nweight_pre=nweight_pre+weight


#-------------------------below for signal region1 &2
    if len(pholist)==1:
        region[0]=1
        (n_SR1)+=1
        (nweight_SR1)+=weight

    elif len(pholist)>=2:    
        region[0]=2
        (n_SR2)+=1
        (nweight_SR2)+=weight

#------------------------------below for control region 1&2 depends on fake numbers
    if len(fakelist)==1 and len(pholist)==0:
        region[0]=3
        (n_CR1)+=1
        (nweight_CR1)+=weight
    elif len(fakelist)>=2 and len(pholist)==0:    
        region[0]=4
        (n_CR2)+=1
        (nweight_CR2)+=weight

    tree_out.Fill()
#----------------------clean branches for next event
    bjetPt.clear()
    bjetEta.clear()
    bjetPhi.clear()

    jetPt.clear()
    jetEta.clear()
    jetPhi.clear()

    phoEt.clear()
    phoEta.clear()
    phoPhi.clear()
    phoR9.clear()
    phoHoverE.clear()
    phoSigmaIEtaIEta.clear()
    phoSigmaIPhiIPhi.clear()

    fakeEt.clear()
    fakeEta.clear()
    fakePhi.clear()
    fakeR9.clear()
    fakeSigmaIEtaIEta.clear()
    fakeSigmaIPhiIPhi.clear()

file_out.Write()
file_out.Close()



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


sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"


