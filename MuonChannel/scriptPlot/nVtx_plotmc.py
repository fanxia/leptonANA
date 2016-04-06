#!/bin/python
# 4.6.2016 by Fan Xia
# To compare mc nvtx distribution in pre region

import os
import sys
import time
import datetime
from ROOT import *
from array import array
from prettytable import PrettyTable
from leptonANA.ElectronChannel.ana_muon import *
from leptonANA.ElectronChannel.Utilfunc import *


def nvtxmcploter(plotname,branchname,data,dataname,bkglist):
    print "start stackmu"

    c=ROOT.TCanvas("c","Plots",1000,1000)
    c.cd()
    gStyle.SetOptStat(0)
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
    histdata.SetLineStyle(2)
    leg.AddEntry(histdata,dataname,"l")


#---------------bkg stack-("nostack"mode)------

    for bkg in bkglist:
        histmc=ROOT.TH1F("","",50,0,50)
        print "get bkg input"
        nevents=bkg[0].GetEntries()
        print nevents
        if nevents==0:
            continue
        for i in range(nevents):
            bkg[0].GetEntry(i)
            histmc.Fill(getattr(bkg[0],branchname))
        histmc.SetLineColor(bkg[2])
        histmc.SetLineWidth(2)
        histmc.Scale(1.0/nevents)
        hs.Add(histmc)
        leg.AddEntry(histmc,bkg[1],"l")
    print "get bkg done"

    
#---------------draw--------

    hs.SetTitle("MuonChannel: "+plotname+";"+branchname+";")
    hs.Draw("nostack")
    hs.SetMaximum(0.12)
    leg.Draw()
    histdata.Draw("same")
    c.Print("xxx.png","png")
    hs.Write()
    histdata.Write()
    c.Clear()
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


#--------Output-------------------------
dd=datetime.datetime.now().strftime("%b%d")
os.system('mkdir -p plot_'+dd)
os.chdir('plot_'+dd)
fout=TFile("fout.root","recreate")

#---------plot 5 bkgs nvtx pdf--------------

nvtxmcploter("pre_nvtx","nVtx",dataTree[0],"dataSingleMu",[[mcttwTree[0],"bkg_ttw",417],[mcttgTree[0],"bkg_ttg",800],[mcdyjetsTree[0],"bkg_zjets",857],[mcwjetsTree[0],"bkg_wjets",432],[mcttTree[0],"bkg_tt",901]])


fout.Close()
sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"
