#!/bin/python
# 4.14.2016 by Fan Xia
# To compare mc  nvtx distribution before and after pu with data in pre region

import os
import sys
import time
import datetime
from ROOT import *
from array import array
from prettytable import PrettyTable
from leptonANA.ElectronChannel.ana_muon import *
from leptonANA.ElectronChannel.Utilfunc import *


def testPU(plotname,branchname,data,dataname,bkg):
    print "start stackmu"

    c=ROOT.TCanvas("c","Plots",1000,1000)
    c.cd()
#   gStyle.SetOptStat(0)
    leg=ROOT.TLegend(0.6,0.8,0.9,0.9)    
    hs=ROOT.THStack("hs","hs")
#---------------data
    histdata=ROOT.TH1F("histdata","histdata",50,0,50)
    for j in range(data.GetEntries()):
        data.GetEntry(j)
        histdata.Fill(getattr(data,branchname))
    histdata.Draw()
    histdata.Scale(1.0/data.GetEntries())
    histdata.SetLineColor(kBlack)
    histdata.SetLineWidth(2)
#    histdata.SetLineStyle(2)
    hs.Add(histdata)
    leg.AddEntry(histdata,dataname,"l")


#---------------bkg stack-("nostack"mode)------

    histmc=ROOT.TH1F("histmc","histmc",50,0,50)
    histmcpu=ROOT.TH1F("histmcpu","histmcpu",50,0,50)
    hdiff=ROOT.TH1F("","",50,0,50)
    p=ROOT.TH1F("p","mcweightdist",100,0,5)
    
    print "get bkg input"
    nevents=bkg[0].GetEntries()
    print nevents
    
    for i in range(nevents):
        bkg[0].GetEntry(i)
        histmc.Fill(getattr(bkg[0],branchname))
    histmc.SetLineColor(bkg[2])
    histmc.SetLineWidth(2)
    histmc.Scale(1.0/nevents)
    hs.Add(histmc)
    leg.AddEntry(histmc,bkg[1],"l")

    for j in range(nevents):
        bkg[0].GetEntry(j)
        putrue=int(bkg[0].puTrue[12])
        puR=puweightlist[putrue]
        p.Fill(puR)
        histmcpu.Fill(getattr(bkg[0],branchname),puR)
    histmcpu.Draw()
    histmcpu.SetLineColor(kRed)
    histmcpu.SetLineWidth(2)
    histmcpu.Scale(1.0/nevents)

    hs.Add(histmcpu)
    leg.AddEntry(histmcpu,"mc after PU","le")

    p.Draw()
    c.Print("puweightTest.png","png")
    c.Clear()

#    histmcpu.Draw("hist")
        
#---------------draw--------
    c.Clear()
    gStyle.SetOptStat(0)
    pad1=TPad("pad1","pad1",0,0.33,1,1)
    pad2=TPad("pad2","pad2",0,0,1,0.33)
    pad1.SetBottomMargin(0.00001)
    pad1.SetBorderMode(0)
    pad2.SetTopMargin(0.00001)
    pad2.SetBottomMargin(0.15)
    pad2.SetBorderMode(0)
    pad1.Draw()
    pad2.Draw()
    pad1.cd()
#    histdata.Draw()
#    histmc.Draw("same")
#    histmcpu.Draw("same hist")

    hs.SetTitle("MuonChannel: "+plotname+";"+branchname+";")
    hs.Draw("nostack")
#    hs.SetMaximum(0.5)
    leg.Draw()

    pad2.cd()
    for g in range(1,51):
        if histdata.GetBinContent(g)==0: continue
        diff=histmcpu.GetBinContent(g)/histdata.GetBinContent(g)
        hdiff.SetBinContent(g,diff)
    hdiff.GetYaxis().SetTitle("mc_after_PU/data")
    hdiff.GetXaxis().SetTitle("nVtx")
#    hdiff.GetYaxis().SetLabelSize(18)
    hdiff.Draw("e")
    hdiff.SetMarkerStyle(7)
#    hdiff.Draw("hist p")
    line = TLine(0,1,50,1)
    line.SetLineStyle(2)
    line.Draw("same")


    c.Print("vtxpu.png","png")
#    c.Clear()
# end stackmu plot module

sw = ROOT.TStopwatch()
sw.Start()
print "start"

data=TFile.Open("../selected/dataSingleMu3Mar31/dataSingleMu3.root")
mcttg=TFile.Open("../selected/mcttgApr03/mcttg.root")
mcttw=TFile.Open("../selected/mcttwMar31/mcttw.root")
mctt=TFile.Open("../selected/mcttMar31/mctt.root")
mcdyjets=TFile.Open("../selected/mcdyjetstollApr01/mcdyjetstoll.root")
mcwjets=TFile.Open("../selected/mcwjetsApr03/mcwjets.root")

regionlist=["EventTree_pre","EventTree_SR1","EventTree_SR2","EventTree_CR1","EventTree_CR2"]
dataTree=[data.Get(region) for region in regionlist]

mcttTree=[mctt.Get(region) for region in regionlist]
mcttwTree=[mcttw.Get(region) for region in regionlist]
mcttgTree=[mcttg.Get(region) for region in regionlist]
mcdyjetsTree=[mcdyjets.Get(region) for region in regionlist]
mcwjetsTree=[mcwjets.Get(region) for region in regionlist]


#nvtxmcploter("pre_nvtx","nVtx",dataTree[0],"dataSingleMu",[[mcttwTree[0],"bkg_ttw",417],[mcttgTree[0],"bkg_ttg",800],[mcdyjetsTree[0],"bkg_zjets",857],[mcwjetsTree[0],"bkg_wjets",432],[mcttTree[0],"bkg_tt",901]])
testPU("pre_nvtx","nVtx",dataTree[0],"dataSingleMu",[mcttwTree[0],"mc(bkg_ttw)",417])



sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"
