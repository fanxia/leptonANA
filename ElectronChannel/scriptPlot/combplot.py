#!/bin/python
# 3.21.2016 by Fan Xia
# To stack bkgs mc and combine data, bkgs and signal

import os
import sys
from ROOT import *
from array import array
from leptonANA.ElectronChannel.ana_muon import *
from leptonANA.ElectronChannel.Utilfunc import *

# stack plot module
def stack(data,dataname,bkg1,bkg1name,bkg2,bkg2name,plotname,branchname):

    c=ROOT.TCanvas("c","Plots",800,800)
    gStyle.SetOptStat(0)
    c.cd()

    


#--------------data--------------
    data.Draw(branchname+">>histdata(100,0,1000)")
    histdata.Draw()


#---------------bkg stack-------
    hs=ROOT.THStack("hs","plotname")
    histmc1=ROOT.TH1F("histmc1","histmc1",100,0,1000)
    histmc2=ROOT.TH1F("histmc2","histmc2",100,0,1000)
    bkg1.Draw(branchname+">>histmc1")
    histmc1.SetFillColor(kRed-7)
    hs.Add(histmc1)
    bkg2.Draw(branchname+">>histmc2")
    histmc2.SetFillColor(kBlue-10)
    hs.Add(histmc2)
    hs.SetTitle(plotname+";;")
    hs.Draw()

#--------------signal----------




    leg=ROOT.TLegend(0.6,0.8,0.9,0.9)
#    leg->SetHeader();
    leg.AddEntry(histdata,dataname,"l");
    leg.AddEntry(histmc1,bkg1name,"f");
    leg.AddEntry(histmc2,bkg2name,"f");

    leg.Draw();
    gPad.SetLogy()
    gPad.Update()

    c.Print(plotname+".pdf","pdf")
    c.Clear()
# end stack plot module


sw = ROOT.TStopwatch()
sw.Start()
print "start"
data=ROOT.TFile("../selected/selected_dataSingleEle/selected_datasingleEle.root")
mcttjets=ROOT.TFile("../selected/selected_mcttjets/selected_mcttjets.root")
mcttwjets=ROOT.TFile("../selected/selected_mcttwjets/selected_mcttwjets.root")

sr1data=data.Get("ggNtuplizer/EventTree_SR1")
sr1mcttjets=mcttjets.Get("ggNtuplizer/EventTree_SR1")
sr1mcttwjets=mcttwjets.Get("ggNtuplizer/EventTree_SR1")

stack(data,"SingleEle",sr1mcttwjets,"bkg_ttwjets",sr1mcttjets,"bkg_ttjets","SR1pfMET","pfMET")


sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"
