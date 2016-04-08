#!/bin/python
# 4.7.2016 by Fan Xia
# To stack bkgs mc and combine data, bkgs and signal
# using the ../selected/skim...root as inputs
# This script only good for exsisting histograms and scale combine them

import os
import sys
import time
import datetime
from ROOT import *
from array import array
from prettytable import PrettyTable
from leptonANA.ElectronChannel.ana_muon import *
from leptonANA.ElectronChannel.Utilfunc import *

#-----------xsec and lumi and fraction---------
lumi_data=2.69


xsec_ttjets=831.76
lumi_ttjets=51.44
frac_ttjets=lumi_data/lumi_ttjets

xsec_ttw=0.2043
lumi_ttw=1238
frac_ttw=lumi_data/lumi_ttw

xsec_dyjets=6025.2
lumi_dyjets=4.77
frac_dyjets=lumi_data/lumi_dyjets

xsec_wjets=61526.7
lumi_wjets=0.4
frac_wjets=lumi_data/lumi_wjets

xsec_tt=831.76
lumi_tt=23.75
frac_tt=lumi_data/lumi_tt

xsec_ttg=3.697
lumi_ttg=1307.1
frac_ttg=lumi_data/lumi_ttg





# stack plot module

def stack(plotname,histname,data,dataname,bkglist):


    c=ROOT.TCanvas("c","Plots",1000,1000)
    c.cd()
    gStyle.SetOptStat(0)
    leg=ROOT.TLegend(0.6,0.8,0.9,0.9)    
    hs=ROOT.THStack("hs","hs")


#---------------data
    histdata=data.Get(histname)
    histdata.Draw()
    histdata.SetLineColor(kBlack)
    histdata.SetLineWidth(1)
#    histdata.SetLineStyle(2)
    leg.AddEntry(histdata,dataname,"l")


#---------------bkg stack-("nostack"mode)------

    for bkg in bkglist:
        histmc=bkg[0].Get(histname)
        print "get bkg input"
        histmc.SetFillColor(bkg[3])
#        histmc.SetFillWidth(2)
        histmc.Scale(bkg[2])
        histmc.SetStats(0)
        hs.Add(histmc)
        leg.AddEntry(histmc,bkg[1],"f")
    print "get bkg done"

    
#---------------draw--------


    hs.Draw()
    hs.SetTitle(histdata.GetTitle())
    hs.GetXaxis().SetTitle(histdata.GetXaxis().GetTitle())
    gPad.SetLogy()

#    hs.Draw("nostack")
#    hs.SetMaximum(ymax)
    hs.SetMinimum(hs.GetMinimum("nostack")*5.)
    histdata.Draw("e same")
    histdata.SetStats(0)
    leg.Draw()
    c.Print(plotname+".pdf","pdf")
    c.Clear()
#--------and stack


sw = ROOT.TStopwatch()
sw.Start()
print "start"

#------------input file and input tree----------
data=TFile.Open("../selected/skim_dataSingleEleApr08/skim_dataSingleEle.root")
mcttg=TFile.Open("../selected/skim_mcttgApr08/skim_mcttg.root")
mcttw=TFile.Open("../selected/skim_mcttwApr08/skim_mcttw.root")
mctt=TFile.Open("../selected/skim_mcttApr08/skim_mctt.root")
mcdyjets=TFile.Open("../selected/skim_mcdyjetsApr08/skim_mcdyjets.root")
mcwjets=TFile.Open("../selected/skim_mcwjetsApr08/skim_mcwjets.root")



#-----------------output dir and files

dd=datetime.datetime.now().strftime("%b%d")
os.system('mkdir -p plot_'+dd)
os.chdir('plot_'+dd)
#f = open("summarytable.txt","w")


stack("preMET","preMET",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("pre-seletion_elePt","pre_SingleElePt",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("pre-seletion_eleEta","pre_SingleEleEta",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("pre-npho","pre_nPho",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("pre-nfake","pre_nFake",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("pre-nJet","pre_nJet",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])






stack("SR1MET","SR1MET",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("SR1-seletion_elePt","SR1_SingleElePt",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("SR1dR_pho_ele","SR1dR_pho_ele",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("SinglePhoEt","SinglePhoEt",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("SR1invelepho","SR1invelepho",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])


stack("SR2MET","SR2MET",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("SR2-seletion_elePt","SR2_SingleElePt",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("SR2phodR","SR2phodR",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("diPhotonM","diPhotonM",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("LeadPhoEt","LeadPhoEt",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("TrailPhoEt","TrailPhoEt",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])



stack("CR1MET","CR1MET",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("CR1-seletion_elePt","CR1_SingleElePt",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("CR1dR_fake_ele","CR1dR_fake_ele",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("SingleFakeEt","SingleFakeEt",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("CR1invelefake","CR1invelefake",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])


stack("CR2MET","CR2MET",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("CR2-seletion_elePt","CR2_SingleElePt",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("diFakeM","diFakeM",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("LeadFakeEt","LeadFakeEt",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("TrailFakeEt","TrailFakeEt",data,"SingleEle",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])




sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"
