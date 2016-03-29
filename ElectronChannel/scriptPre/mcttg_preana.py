#!/bin/python
# 3.17.2016 by Fan Xia
# This template uses the ggntuples as input, make the preselection and get reduced root file which should be saved in dir:preselected. It can be very time consuming and need to move output manually. This one is only for reducing event number purpose and get the first look of pre region. 
# If tighter cuts apply to the preselect, only need to run script in dir:scriptANA again. 
## This script pre select the mcttgamma

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
chain_in.Add
chain_in.Add("root://eoscms.cern.ch//eos/cms/store/group/phys_smp/ggNtuples/13TeV/mc/V07_04_16_03/job_spring15_TTG_miniAOD.root")
chain_in.SetBranchStatus("tau*",0)
n_events = chain_in.GetEntries()
print"Total events for processing: ",n_events

log = open("logpre.txt","a")
log.write("############################################################\n")
log.write("INPUT root://eoscms.cern.ch//eos/cms/store/group/phys_smp/ggNtuples/13TeV/mc/V07_04_16_03/job_spring15_TTG_miniAOD.root")


dd=datetime.datetime.now().strftime("%b%d")
os.system('mkdir -p ../preselected/Output_mcttg_'+dd)
os.chdir("../preselected/Output_mcttg_"+dd)

file_out = ROOT.TFile("reduced_mcttg.root","recreate")
dir_out = file_out.mkdir("ggNtuplizer")
dir_out.cd()
tree_out = chain_in.CloneTree(0)
tree_out.SetName("EventTree_pre")

n_goodvtx=0
n_hlt=0
n_singleEle=0
n_pre=0


for i in range(n_events):
    chain_in.GetEntry(i)
    
    if i%100000 ==0:
        print "Processing entry ", i

##----------------0.5Vertex clean

    if not chain_in.hasGoodVtx:
        continue
    n_goodvtx+=1
# -----------------1.HLT selection(HLT_Ele23_WP75_Gsf_v)

#    hltele = chain_in.HLTEleMuX>>10&1
#    if hltele!=1:
#        continue
#    n_hlt+=1


#-------------------1+2. only one tight ele
    n_tightEle=0
    n_looseEle=0
    for e in range(chain_in.nEle):
        if good_TightEle(chain_in.elePt[e],chain_in.eleEta[e],chain_in.eleIDbit[e]):
            n_tightEle+=1
#            ele_ind=e
        if good_LooseEle(chain_in.elePt[e],chain_in.eleEta[e],chain_in.eleIDbit[e]):
            n_looseEle+=1
    if n_tightEle !=1 or n_looseEle !=1:
        continue

    n_looseMu=0
    for m in range(chain_in.nMu):
        muPFIso=muPFRelCombIso(chain_in.muPt[m],chain_in.muPFChIso[m],chain_in.muPFNeuIso[m],chain_in.muPFPhoIso[m],chain_in.muPFPUIso[m])
#        print "iso",i,"---",muPFIso
#        if chain_in.muPt[m]>10 and abs(chain_in.muEta[m])<2.5 and chain_in.muIsLooseID[m] and muPFIso<0.25:

        if good_LooseMu(chain_in.muPt[m],chain_in.muEta[m],chain_in.muIsLooseID[m],muPFIso):
            n_looseMu+=1
    if n_looseMu !=0:
        continue

    n_singleEle+=1     


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

#-----------------------below for pre plots                                                                                                                                                                                     

#    pre_SingleElePt.Fill(chain_in.elePt[ele_ind])
#    pre_SingleEleEta.Fill(chain_in.eleEta[ele_ind])
#    pre_nJet_nbJet.Fill(n_jet,n_bjet)
#    pre_LeadBjetPt.Fill(chain_in.jetPt[leadbjet_ind])
#    preMET.Fill(chain_in.pfMET)
#    pre_nJet.Fill(n_jet)


file_out.Write()
file_out.Close()

print "----------------------"
print "TotalEventNumber = ", n_events
print "n_goodvtx pass = ",n_goodvtx
#print "n_hlt pass = ", n_hlt
print "n_singleEle pass = ", n_singleEle
print "n_pre selection = ",n_pre
print "----------------------"


#### to write in logpre.txt

log.write("%s"%datetime.datetime.now())
log.write("\nTotalEventNumber = %s"%n_events)
log.write("\nn_goodvtx pass = %s"%n_goodvtx)
#log.write ("\n n_hlt pass = %s"% n_hlt)
log.write( "\nn_singleEle pass =%s "%n_singleEle)
log.write("\nn_pre selection = %s"%n_pre)
log.write( "\n----------------------\n\n")
log.close()


sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"


