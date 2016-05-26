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


xsec_sig600=0.175
lumi_sig600=21.14
frac_sig600=lumi_data/lumi_sig600



# stack plot module

def stack(plotname,histname,data,dataname,bkglist,sig,signame,frac_sig):


    c=ROOT.TCanvas("c","Plots",1100,900)
    c.cd()
    gStyle.SetOptStat(0)
    leg=ROOT.TLegend(0.6,0.65,0.9,0.9)    
    leg1=ROOT.TLegend(0.6,0.8,0.9,0.9)    
    hs=ROOT.THStack("hs","hs")


#---------------data
    histdata=data.Get(histname)
    histdata.Draw()
    histdata.SetLineColor(kBlack)
    histdata.SetLineWidth(2)
    histdata.SetMarkerStyle(7)
#    histdata.SetLineStyle(2)
    leg.AddEntry(histdata,dataname,"l")
    leg1.AddEntry(histdata,"Data: "+dataname,"l")
#######################################
#sig
    histsig=sig.Get(histname)
    histsig.Sumw2()
    histsig.Scale(frac_sig)
    histsig.Draw("HIST")
    histsig.SetLineColor(kBlue)
    histsig.SetLineWidth(2)
#    histsig.SetMarkerStyle(7)
#    histsig.SetLineStyle(2)
#    leg.AddEntry(histsig,signame,"l")
    leg1.AddEntry(histsig,"Signal: "+signame,"l")

#######################################


#---------------bkg stack-("nostack"mode)------

    for bkg in bkglist:
        histmc=bkg[0].Get(histname)
        print "get bkg input"
        histmc.SetFillColor(bkg[3])
#        histmc.SetFillWidth(2)
        histmc.Scale(bkg[2])
        histmc.SetStats(0)

        hs.Add(histmc,"HIST")
        leg.AddEntry(histmc,bkg[1],"f")
    print "get bkg done"

    
#---------------draw--------

#    hs.SetTitle("MuonChannel: "++";"+branchname+";")
    hs.Draw()
    hs.SetTitle(histdata.GetTitle())
    hs.GetXaxis().SetTitle(histdata.GetXaxis().GetTitle())
    hs.GetYaxis().SetTitle(histdata.GetYaxis().GetTitle())
    gPad.SetLogy()

#    hs.Draw("nostack")
    hs.SetMaximum(max(hs.GetMaximum(),histdata.GetMaximum())*1.1)
    hs.SetMinimum(hs.GetMinimum("nostack")*5.)
    
    histdata.Draw("e same")
    histdata.SetStats(0)
    leg.Draw()
    c.Print(plotname+".pdf","pdf")
    c.Clear()
#--------and stack


    hssum=hs.GetStack().Last().Clone()
    hssum.SetLineColor(kRed)
    hssum.SetLineWidth(2)
    hssum.SetFillColor(0)
    leg1.AddEntry(hssum,"Bkgs sum","l")
    hssum.Draw("HIST")
    hssum.SetTitle(histdata.GetTitle())
    hssum.GetXaxis().SetTitle(histdata.GetXaxis().GetTitle())
    hssum.GetYaxis().SetTitle(histdata.GetYaxis().GetTitle())
    gPad.SetLogy()

#    hs.Draw("nostack")
    hssum.SetMaximum(max(hs.GetMaximum(),histdata.GetMaximum())*1.1)
    hssum.SetMinimum(hs.GetMinimum("nostack")*5.)
    histdata.Draw("e same")
    histdata.SetStats(0)
#    histsig.Draw("hist same")
    leg1.Draw()
    c.Print(plotname+"sketch.pdf","pdf")
    c.Clear()



sw = ROOT.TStopwatch()
sw.Start()
print "start"

#------------input file and input tree----------
data=TFile.Open("../selected/skim_dataSingleMuApr25/skim_dataSingleMu.root")
mcttg=TFile.Open("../selected/skim_mcttgApr15/skim_mcttg.root")
mcttw=TFile.Open("../selected/skim_mcttwApr15/skim_mcttw.root")
mctt=TFile.Open("../selected/skim_mcttApr15/skim_mctt.root")
mcdyjets=TFile.Open("../selected/skim_mcdyjetsApr15/skim_mcdyjets.root")
mcwjets=TFile.Open("../selected/skim_mcwjetsApr15/skim_mcwjets.root")
sig=TFile.Open("../selected/skim_sig600_375May10/skim_sig600_375.root")


#-----------------output dir and files

dd=datetime.datetime.now().strftime("%b%d")
os.system('mkdir -p plot_'+dd)
os.chdir('plot_'+dd)
#f = open("summarytable.txt","w")


stack("preMET","preMET",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
# stack("pre-seletion_muPt","pre_SingleMuPt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("pre-seletion_muEta","pre_SingleMuEta",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("pre-npho","pre_nPho",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("pre-nfake","pre_nFake",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("pre-nJet","pre_nJet",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("pre-jetHt","pre_jetHt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])





stack("SR1MET","SR1MET",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
# stack("SR1-seletion_muPt","SR1_SingleMuPt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("SR1dR_pho_mu","SR1dR_pho_mu",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("SinglePhoEt","SinglePhoEt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("SR1invmupho","SR1invmupho",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("SR1_jetHt","SR1_jetHt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])


stack("SR2MET","SR2MET",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
# stack("SR2-seletion_muPt","SR2_SingleMuPt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("SR2phodR","SR2phodR",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("diPhotonM","diPhotonM",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("LeadPhoEt","LeadPhoEt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("TrailPhoEt","TrailPhoEt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("SR2_jetHt","SR2_jetHt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])


# stack("CR1MET","CR1MET",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("CR1-seletion_muPt","CR1_SingleMuPt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("CR1dR_fake_mu","CR1dR_fake_mu",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("SingleFakeEt","SingleFakeEt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("CR1invmufake","CR1invmufake",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("CR1_jetHt","CR1_jetHt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])

# stack("CR2MET","CR2MET",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("CR2-seletion_muPt","CR2_SingleMuPt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("diFakeM","diFakeM",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("LeadFakeEt","LeadFakeEt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("TrailFakeEt","TrailFakeEt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])
# stack("CR2_jetHt","CR2_jetHt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]])

# #--muPt and muEta
# #stackMu("Pre-seletion_muPt","muPt",predata,"SingleMu",[[premcttw,"bkg_ttw",frac_ttw,417],[premcttg,"bkg_ttg",frac_ttg,800],[premcdyjets,"bkg_zjets",frac_dyjets,857],[premcwjets,"bkg_wjets",frac_wjets,432],[premctt,"bkg_tt",frac_tt,901]])
# #stackMu("Pre-seletion_muEta","muEta",predata,"SingleMu",[[premcttw,"bkg_ttw",frac_ttw,417],[premcttg,"bkg_ttg",frac_ttg,800],[premcdyjets,"bkg_zjets",frac_dyjets,857],[premcwjets,"bkg_wjets",frac_wjets,432],[premctt,"bkg_tt",frac_tt,901]])


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
