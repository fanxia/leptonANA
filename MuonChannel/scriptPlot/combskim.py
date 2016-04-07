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
lumi_data=1.73
#lumi_data=1.61

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
    histdata.SetLineWidth(2)
#    histdata.SetLineStyle(2)
    leg.AddEntry(histdata,dataname,"l")


#---------------bkg stack-("nostack"mode)------

    for bkg in bkglist:
        histmc=bkg[0].Get(histname)
        print "get bkg input"
        histmc.SetFillColor(bkg[3])
#        histmc.SetFillWidth(2)
        histmc.Scale(bkg[2])
        hs.Add(histmc)
        leg.AddEntry(histmc,bkg[1],"f")
    print "get bkg done"

    
#---------------draw--------

#    hs.SetTitle("MuonChannel: "++";"+branchname+";")
    hs.SetTitle(histdata.GetTitle())
    gPad.SetLogy()
    hs.Draw()
#    hs.Draw("nostack")
#    hs.SetMaximum(ymax)
#    hs.SetMinimum(ymin)
    leg.Draw()
    histdata.Draw("e same")
    c.Print(plotname+".png","png")
    c.Clear()
#--------and stack


sw = ROOT.TStopwatch()
sw.Start()
print "start"

#------------input file and input tree----------
data=TFile.Open("../selected/skim_dataSingleMuApr07/skim_dataSingleMu.root")
mcttg=TFile.Open("../selected/skim_mcttgApr07/skim_mcttg.root")
mcttw=TFile.Open("../selected/skim_mcttwApr07/skim_mcttw.root")
mctt=TFile.Open("../selected/skim_mcttApr07/skim_mctt.root")
mcdyjets=TFile.Open("../selected/skim_mcdyjetsApr07/skim_mcdyjets.root")
mcwjets=TFile.Open("../selected/skim_mcwjetsApr07/skim_mcwjets.root")



#-----------------output dir and files

dd=datetime.datetime.now().strftime("%b%d")
os.system('mkdir -p plot_'+dd)
os.chdir('plot_'+dd)
#f = open("summarytable.txt","w")


stack("preMET","preMET",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("pre-seletion_muPt","pre_SingleMuPt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("pre-seletion_muEta","pre_SingleMuEta",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("pre-npho","pre_nPho",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("pre-nfake","pre_nFake",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("pre-nJet","pre_nJet",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])






stack("SR1MET","SR1MET",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("SR1-seletion_muPt","SR1_SingleMuPt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("SR1dR_pho_mu","SR1dR_pho_mu",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("SinglePhoEt","SinglePhoEt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("SR1invmupho","SR1invmupho",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])


stack("SR2MET","SR2MET",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("SR2-seletion_muPt","SR2_SingleMuPt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("SR2phodR","SR2phodR",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("diPhotonM","diPhotonM",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("LeadPhoEt","LeadPhoEt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
stack("TrailPhoEt","TrailPhoEt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])


#--muPt and muEta
#stackMu("Pre-seletion_muPt","muPt",predata,"SingleMu",[[premcttw,"bkg_ttw",frac_ttw,417],[premcttg,"bkg_ttg",frac_ttg,800],[premcdyjets,"bkg_zjets",frac_dyjets,857],[premcwjets,"bkg_wjets",frac_wjets,432],[premctt,"bkg_tt",frac_tt,901]])
#stackMu("Pre-seletion_muEta","muEta",predata,"SingleMu",[[premcttw,"bkg_ttw",frac_ttw,417],[premcttg,"bkg_ttg",frac_ttg,800],[premcdyjets,"bkg_zjets",frac_dyjets,857],[premcwjets,"bkg_wjets",frac_wjets,432],[premctt,"bkg_tt",frac_tt,901]])


#------------sr1 plot
#--pfMET
#stack("SR1pfMET","pfMET",sr1data,"SingleMu",sr1mcttwjets,"bkg_ttwjets",frac_ttwjets,sr1mcttjets,"bkg_ttjets",frac_ttjets)
#stack("SR1_pfMET","pfMET","MET(GeV)","number of events",sr1data,"DataSingleMu",sr1mcttw,"bkg_ttw",frac_ttw,sr1mcttg,"bkg_ttg",frac_ttg,sr1mcdyjets,"bkg_zjets",frac_dyjets,sr1mcwjets,"bkg_wjets",frac_wjets,sr1mctt,"bkg_tt",frac_tt)
#--muPt and muEta
#stackMu("SR1_muPt","muPt",sr1data,"SingleMu",[[sr1mcttw,"bkg_ttw",frac_ttw,417],[sr1mcttg,"bkg_ttg",frac_ttg,800],[sr1mcdyjets,"bkg_zjets",frac_dyjets,857],[sr1mcwjets,"bkg_wjets",frac_wjets,432],[sr1mctt,"bkg_tt",frac_tt,901]])
#stackMu("SR1_muEta","muEta",sr1data,"SingleMu",[[sr1mcttw,"bkg_ttw",frac_ttw,417],[sr1mcttg,"bkg_ttg",frac_ttg,800],[sr1mcdyjets,"bkg_zjets",frac_dyjets,857],[sr1mcwjets,"bkg_wjets",frac_wjets,432],[sr1mctt,"bkg_tt",frac_tt,901]])
#--phoEt and Eta
#stackpho("SR1_","phoEt",11,sr1data,"SingleMu",sr1mcttwjets,"bkg_ttwjets",frac_ttwjets,sr1mcttjets,"bkg_ttjets",frac_ttjets)
#stackpho("SR1_","phoEta",11,sr1data,"SingleMu",sr1mcttwjets,"bkg_ttwjets",frac_ttwjets,sr1mcttjets,"bkg_ttjets",frac_ttjets)



#------------sr2 plot
#--pfMET
#stack("SR2pfMET","pfMET",sr2data,"SingleMu",sr2mcttwjets,"bkg_ttwjets",frac_ttwjets,sr2mcttjets,"bkg_ttjets",frac_ttjets)
#stack("SR2_pfMET","pfMET","MET(GeV)","number of events",sr2data,"DataSingleMu",sr2mcttw,"bkg_ttw",frac_ttw,sr2mcttg,"bkg_ttg",frac_ttg,sr2mcdyjets,"bkg_zjets",frac_dyjets,sr2mcwjets,"bkg_wjets",frac_wjets,sr2mctt,"bkg_tt",frac_tt)

#--muPt and muEta
#stackMu("SR2_muPt","muPt",sr2data,"SingleMu",[[sr2mcttw,"bkg_ttw",frac_ttw,417],[sr2mcttg,"bkg_ttg",frac_ttg,800],[sr2mcdyjets,"bkg_zjets",frac_dyjets,857],[sr2mcwjets,"bkg_wjets",frac_wjets,432],[sr2mctt,"bkg_tt",frac_tt,901]])
#stackMu("SR2_muEta","muEta",sr2data,"SingleMu",[[sr2mcttw,"bkg_ttw",frac_ttw,417],[sr2mcttg,"bkg_ttg",frac_ttg,800],[sr2mcdyjets,"bkg_zjets",frac_dyjets,857],[sr2mcwjets,"bkg_wjets",frac_wjets,432],[sr2mctt,"bkg_tt",frac_tt,901]])
#stackMu("SR2_","muEta",predata,"SingleMu",premcttwjets,"bkg_ttwjets",frac_ttwjets,premcttjets,"bkg_ttjets",frac_ttjets)
#--Leading phoEt and Eta
#stackpho("SR2_Leading","phoEt",21,sr2data,"SingleMu",sr2mcttwjets,"bkg_ttwjets",frac_ttwjets,sr2mcttjets,"bkg_ttjets",frac_ttjets)
#stackpho("SR2_Leading","phoEta",21,sr2data,"SingleMu",sr2mcttwjets,"bkg_ttwjets",frac_ttwjets,sr2mcttjets,"bkg_ttjets",frac_ttjets)
#--Trailing phoEt and Eta
#stackpho("SR2_Trailing","phoEt",22,sr2data,"SingleMu",sr2mcttwjets,"bkg_ttwjets",frac_ttwjets,sr2mcttjets,"bkg_ttjets",frac_ttjets)
#stackpho("SR2_Trailing","phoEta",22,sr2data,"SingleMu",sr2mcttwjets,"bkg_ttwjets",frac_ttwjets,sr2mcttjets,"bkg_ttjets",frac_ttjets)








sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"
