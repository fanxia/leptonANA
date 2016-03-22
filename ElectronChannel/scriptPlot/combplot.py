#!/bin/python
# 3.21.2016 by Fan Xia
# To stack bkgs mc and combine data, bkgs and signal

import os
import sys
import time
import datetime
from ROOT import *
from array import array
from leptonANA.ElectronChannel.ana_muon import *
from leptonANA.ElectronChannel.Utilfunc import *

#-----------xsec and lumi and fraction---------
lumi_data=1.0

xsec_ttjets=831.76
lumi_ttjets=51.44
frac_ttjets=lumi_data/lumi_ttjets

xsec_ttwjets=0.2043
lumi_ttwjets=1238
frac_ttwjets=lumi_data/lumi_ttwjets


# stack plot module

def stack(data,dataname,bkg1,bkg1name,frac1,bkg2,bkg2name,frac2,plotname,branchname):

    c=ROOT.TCanvas("c","Plots",800,800)
    gStyle.SetOptStat(0)
    gPad.SetLogy()
    c.cd()


#---------------bkg stack-------
    hs=ROOT.THStack("hs","plotname")
#    histmc1=ROOT.TH1F("histmc1","histmc1",100,0,1000)
#    histmc2=ROOT.TH1F("histmc2","histmc2",100,0,1000)

    bkg1.Draw(branchname+">>histmc1")
    histmc1.SetFillColor(kRed-7)
    histmc1.Scale(frac1)
    hs.Add(histmc1)

    bkg2.Draw(branchname+">>histmc2")
    histmc2.SetFillColor(kBlue-10)
    histmc2.Scale(frac2)
    hs.Add(histmc2)

    hs.SetTitle(plotname+";;")


#--------------data--------------
    data.Draw(branchname+">>histdata")
    histdata.SetLineColor(kBlack)
    histdata.SetLineWidth(2)
    
#--------------signal----------
    
#---------------draw--------
#    hs.SetMinimum(hs.GetMinimum())
    hs.SetMaximum(hs.GetMaximum()*1.2)
    hs.SetMinimum(hs.GetMinimum("nostack"))
    hs.Draw()
    histdata.Draw("e same")



    leg=ROOT.TLegend(0.6,0.8,0.9,0.9)
#    leg->SetHeader();
    leg.AddEntry(histdata,dataname,"le");
    leg.AddEntry(histmc1,bkg1name,"f");
    leg.AddEntry(histmc2,bkg2name,"f");

    leg.Draw();

#    gPad.Update()

    c.Print(plotname+".png","png")
    c.Clear()
# end stack plot module




def stackele(data,dataname,bkg1,bkg1name,frac1,bkg2,bkg2name,frac2,plotname):

    c=ROOT.TCanvas("c","Plots",800,800)
    gStyle.SetOptStat(0)
#    gPad.SetLogy()
    c.cd()


#---------------bkg stack-------
    bkg1ele_ind=bkg1.ele_index
    bkg2ele_ind=bkg2.ele_index
    hs=ROOT.THStack("hs","plotname")


    bkg1.Draw("elePt[bkg1ele_ind]>>histmc1")
    histmc1.SetFillColor(kRed-7)
    histmc1.Scale(frac1)
    hs.Add(histmc1)

    bkg2.Draw(branchname+">>histmc2")
    histmc2.SetFillColor(kBlue-10)
    histmc2.Scale(frac2)
    hs.Add(histmc2)

    hs.SetTitle(plotname+"ele_Pt;;")

#--------------data--------------
#    data.Draw(">>histdata")
#    histdata.SetLineColor(kBlack)
#    histdata.SetLineWidth(2)
    
#--------------signal----------
    
#---------------draw--------
    hs.SetMaximum(hs.GetMaximum()*1.2)
    hs.SetMinimum(hs.GetMinimum("nostack"))
    hs.Draw()
#    histdata.Draw("e same")

    leg=ROOT.TLegend(0.6,0.8,0.9,0.9)
#    leg->SetHeader();
#    leg.AddEntry(histdata,dataname,"le");
    leg.AddEntry(histmc1,bkg1name,"f");
    leg.AddEntry(histmc2,bkg2name,"f");

    leg.Draw();

#    gPad.Update()

    c.Print(plotname+"ele_Pt.png","png")
    c.Clear()
# end stackele plot module


sw = ROOT.TStopwatch()
sw.Start()
print "start"
data=ROOT.TFile("../selected/selected_dataSingleEle/selected_datasingleEle.root")
mcttjets=ROOT.TFile("../selected/selected_mcttjets_321/selected_mcttjets_321.root")
mcttwjets=ROOT.TFile("../selected/selected_mcttwjets_321/selected_mcttwjets_321.root")

# predata=data.Get("ggNtuplizer/EventTree_pre")
# premcttjets=mcttjets.Get("ggNtuplizer/EventTree_pre")
# premcttwjets=mcttwjets.Get("ggNtuplizer/EventTree_pre")

# sr1data=data.Get("ggNtuplizer/EventTree_SR1")
# sr1mcttjets=mcttjets.Get("ggNtuplizer/EventTree_SR1")
# sr1mcttwjets=mcttwjets.Get("ggNtuplizer/EventTree_SR1")

# sr2data=data.Get("ggNtuplizer/EventTree_SR2")
# sr2mcttjets=mcttjets.Get("ggNtuplizer/EventTree_SR2")
# sr2mcttwjets=mcttwjets.Get("ggNtuplizer/EventTree_SR2")


predata=data.Get("ggNtuplizer/EventTree_pre")
premcttjets=mcttjets.Get("EventTree_pre")
premcttwjets=mcttwjets.Get("EventTree_pre")

sr1data=data.Get("ggNtuplizer/EventTree_SR1")
sr1mcttjets=mcttjets.Get("EventTree_SR1")
sr1mcttwjets=mcttwjets.Get("EventTree_SR1")

sr2data=data.Get("ggNtuplizer/EventTree_SR2")
sr2mcttjets=mcttjets.Get("EventTree_SR2")
sr2mcttwjets=mcttwjets.Get("EventTree_SR2")


dd=datetime.datetime.now().strftime("%b%d")
os.system('mkdir -p plot_'+dd)
os.chdir('plot_'+dd)

#------------pre plot
stack(predata,"SingleEle",premcttwjets,"bkg_ttwjets",frac_ttwjets,premcttjets,"bkg_ttjets",frac_ttjets,"Pre_pfMET","pfMET")
stackEle(predata,"SingleEle",premcttwjets,"bkg_ttwjets",frac_ttwjets,premcttjets,"bkg_ttjets",frac_ttjets,"SR1_")


#------------sr1 plot
stack(sr1data,"SingleEle",sr1mcttwjets,"bkg_ttwjets",frac_ttwjets,sr1mcttjets,"bkg_ttjets",frac_ttjets,"SR1pfMET","pfMET")

#------------sr2 plot
stack(sr2data,"SingleEle",sr2mcttwjets,"bkg_ttwjets",frac_ttwjets,sr2mcttjets,"bkg_ttjets",frac_ttjets,"SR2pfMET","pfMET")




sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"
