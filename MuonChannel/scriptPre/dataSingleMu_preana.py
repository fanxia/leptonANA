#!/bin/python
# 3.17.2016 by Fan Xia
# This template uses the ggntuples as input, make the preselection and get reduced root file which should be saved in dir:preselected. It can be very time consuming and need to move output manually. This one is only for reducing event number purpose and get the first look of pre region. 
# If tighter cuts apply to the preselect, only need to run script in dir:scriptANA again. 
## This script pre select the dataSingeMu

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

sw = ROOT.TStopwatch()
sw.Start()
print "start"
chain_in = ROOT.TChain("ggNtuplizer/EventTree")
chain_in.Add("root://eoscms.cern.ch//store/group/phys_smp/ggNtuples/13TeV/data/V07_04_16_03/job_SingleMu_Run2015D_PR_v4_miniAOD.root")
#chain_in.Add("root://eoscms.cern.ch//store/group/phys_smp/ggNtuples/13TeV/data/V07_04_16_03/data3/ggNtuples/V07_04_16_03/job_SingleEle_Run2015D_PR_v4_miniAOD.root")
#chain_in.Add("root://eoscms.cern.ch//store/group/phys_smp/ggNtuples/13TeV/data/V07_04_16_03/data3/ggNtuples/V07_04_16_03/job_SingleEle_Run2015D_Oct05_miniAOD.root")

chain_in.SetBranchStatus("tau*",0)
n_events = chain_in.GetEntries()
print"Total events for processing: ",n_events

dd=datetime.datetime.now().strftime("%b%d")
log = open("logpre.txt","a")
#os.mkdir("Output_SingleEle_v315",0755)
os.system('mkdir -p ../preselected/Output_dataSingleMu'+dd)
os.chdir("../preselected/Output_dataSingleMu"+dd)


file_out = ROOT.TFile("reduced_dataSingleMu.root","recreate")
dir_out = file_out.mkdir("ggNtuplizer")
dir_out.cd()
tree_out = chain_in.CloneTree(0)
tree_out.SetName("EventTree_pre")

n_goodvtx=0
n_hlt=0
n_singleMu=0
n_pre=0

for i in range(10000):
#for i in range(n_events):
    chain_in.GetEntry(i)
    
    if i%100000 ==0:
        print "Processing entry ", i

##----------------0.5Vertex clean

#    if abs(chain_in.vtz)>24 or abs(chain_in.rho)>2: continue     //error here since the rho is not the "rho"
    if not chain_in.hasGoodVtx:
        continue
    n_goodvtx+=1
# -----------------1.HLT selection 31,32

    hltmu1 = chain_in.HLTEleMuX>>31&1
    hltmu2 = chain_in.HLTEleMuX>>32&1
    if hltmu1!=1 and hltmu2!=1:
        continue
    n_hlt+=1


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
#        print "iso",i,"---",muPFIso
#        if chain_in.muPt[m]>10 and abs(chain_in.muEta[m])<2.5 and chain_in.muIsLooseID[m] and muPFIso<0.25:
        if good_TightMu(chain_in.muPt[m],chain_in.muEta[m],chain_in.muIsTightID[m],muPFIso):
            n_tightMu+=1
        if good_LooseMu(chain_in.muPt[m],chain_in.muEta[m],chain_in.muIsLooseID[m],muPFIso):
            n_looseMu+=1
    if n_looseMu!=1 or n_tightMu!=1 :
        continue

    n_singleMu+=1     


#--------------------1+2+3.at least 3 jets and 1 bjet
    n_jet=0
    n_bjet=0
 #   jetlist =[]
 #   bjetlist=[]
    for j in range(chain_in.nJet):
        if good_LooseJet(chain_in.jetPt[j],chain_in.jetEta[j], chain_in.jetPFLooseId[j]):
            n_jet+=1
 #           jetlist.append(j)
            if chain_in.jetpfCombinedInclusiveSecondaryVertexV2BJetTags[j]>0.89:
                n_bjet+=1
 #               bjetlist.append(j)
    if n_jet<3 or n_bjet<1:
        continue
    n_pre+=1
#    leadbjet_ind=max(bjetlist,key=lambda x: chain_in.jetPt[x])
    tree_out.Fill()
#---------------------above for pre-selection---------------------



file_out.Write()
file_out.Close()

print "----------------------"
print "TotalEventNumber = ", n_events
print "n_goodvtx pass =", n_goodvtx
print "n_hlt pass = ", n_hlt
print "n_singleMu pass = ", n_singleMu
print "n_pre selection = ",n_pre
print "----------------------"


#### to write in logpre.txt

log.write("############################################################\n")
log.write("%s"%datetime.datetime.now())
log.write("\n-----dataSingleElectron----------\n")
log.write("TotalEventNumber = %s"%n_events)
log.write("\n n_goodvtx pass = %s"%n_goodvtx)
log.write ("\n n_hlt pass = %s"% n_hlt)
log.write( "\nn_singleMu pass =%s "%n_singleMu)
log.write("\nn_pre selection = %s"%n_pre)
log.write( "\n----------------------\n\n")
log.close()

sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"


