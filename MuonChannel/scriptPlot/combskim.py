#!/bin/python
# 4.7.2016 by Fan Xia
# To stack bkgs mc and combine data, bkgs and signal
# using the outplot_DD as inputs
# This script only good for exsisting histograms and scale combine them
# python combskim.py DD 

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

def stack(region,histname,data,dataname,bkglist,sig,signame,frac_sig):


    c=ROOT.TCanvas("c","Plots",1000,1100)
#    c.cd()
    Header=ROOT.TPaveText(0.06,0.901,0.38,0.94,"NDC")
    Header.SetFillColor(0)
    Header.SetFillStyle(0)
    Header.SetLineColor(0)
    Header.SetBorderSize(0)
    Header.AddText("2015 pp #sqrt{s} = 13 TeV")
    regionComment=ROOT.TPaveText(0.55,0.55,0.85,0.65,"NDC")
    regionComment.SetFillColor(0)
    regionComment.SetFillStyle(0)
    regionComment.SetLineColor(0)
    regionComment.SetBorderSize(0)
    regionComment.AddText(region+" muon")
#    regionComment.SetTextColor(601)


    gStyle.SetOptStat(0)
    leg=ROOT.TLegend(0.6,0.65,0.9,0.9)    
    leg1=ROOT.TLegend(0.6,0.8,0.9,0.9)    
    hs=ROOT.THStack("hs","hs")
#    hdiff=ROOT.TH1F()
    hssum=ROOT.TH1F()
    histdata=ROOT.TH1F()

#---------------data
    histdata=data.Get(histname)
    histdata.Sumw2()
    histdata.Draw()
    histdata.SetLineColor(kBlack)
    histdata.SetLineWidth(2)
    histdata.SetMarkerStyle(7)
#    histdata.SetLineStyle(2)
    leg.AddEntry(histdata,dataname,"l")
    leg1.AddEntry(histdata,"Data: "+dataname,"l")
#######################################
#--------------sig
    histsig=sig.Get(histname)
    histsig.Sumw2()
    histsig.Scale(frac_sig)
    histsig.Draw("HIST")
    histsig.SetLineColor(kBlue)
    histsig.SetLineWidth(2)
#    histsig.SetMarkerStyle(7)
#    histsig.SetLineStyle(2)
#    leg.AddEntry(histsig,signame,"l")
#    leg1.AddEntry(histsig,"Signal: "+signame,"l")

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
    hssum=hs.GetStack().Last().Clone()
    
#---------------draw stacked bkgs with data and (sig)--------

#    hs.SetTitle("MuonChannel: "++";"+branchname+";")
    c.Clear()
    pad1=TPad("pad1","pad1",0,0.27,1,1)
    pad2=TPad("pad2","pad2",0,0.03,1,0.27)
#    pad1.SetBottomMargin(0.0001)
#    pad1.SetBorderMode(0)
    pad2.SetTopMargin(0.05)
    pad1.Draw()
    pad2.Draw()

    pad1.cd()
    hs.Draw()
    histdata.Draw("e same")
    hs.SetTitle("")
    hs.GetXaxis().SetTitle(histdata.GetXaxis().GetTitle())
    hs.GetXaxis().SetTitleOffset(1.1)
    hs.GetYaxis().SetTitle(histdata.GetYaxis().GetTitle())
    hs.GetYaxis().SetTitleOffset(1.2)
    gPad.SetLogy()

#    hs.Draw("nostack")
    hs.SetMaximum(max(hs.GetMaximum(),histdata.GetMaximum())*1.1)
    hs.SetMinimum(hs.GetMinimum("nostack")*5.)
    
    histdata.Draw("e same")
    histdata.SetStats(0)
    leg.Draw()
    Header.Draw("same")
    regionComment.Draw("same")

    pad2.cd()
    # for gbin in range(1,hssum.GetNbinsX()):
    #     if hssum.GetBinContent(gbin)==0:continue
    #     diff=histdata.GetBinContent(gbin)/(hssum.GetBinContent(gbin)+0.0)
    #     hdiff.SetBinContent(gbin,diff)
    #     hdiff.GetYaxis().SetRange
    #     hdiff.GetYaxis().SetTitle("Data/MC")
    #     hdiff.Draw("e")
    #     line=TLine(0,1,hssum.GetXaxis().GetXmax(),1)
    #     line.SetLineStyle(2)
    #     line.Draw("same")
    hdiff=histdata.Clone("hdiff")
    hdiff.Divide(hssum)
    hdiff.SetLineWidth(1)
    hdiff.GetYaxis().SetTitle("Data/MC           ")
    hdiff.GetYaxis().SetTitleSize(0.07)
    hdiff.GetYaxis().SetTitleOffset(0.5)
    hdiff.GetYaxis().SetLabelSize(0.05)
    hdiff.GetXaxis().SetTitle("")
    hdiff.GetXaxis().SetLabelSize(0.07)
    hdiff.SetMaximum(2.0)
    hdiff.SetMinimum(0.0)
    hdiff.Draw("e")
    line=TLine(0,1,hssum.GetXaxis().GetXmax(),1)
    line.SetLineStyle(2)
    line.Draw("same")


    c.Print(histname+".pdf","pdf")
    c.Print("WWWoutcombplot_"+dd+"/"+histname+".png")
    c.Clear()
#--------and stack

#----------------draw sketch plot online with lines

    pad1=TPad("pad1","pad1",0,0.25,1,1)
    pad2=TPad("pad2","pad2",0,0.03,1,0.25)
#    pad1.SetBottomMargin(0.0001)
#    pad1.SetBorderMode(0)
    pad2.SetTopMargin(0.05)
    pad1.Draw()
    pad2.Draw()
    pad1.cd()
    hssum.SetLineColor(kRed)
    hssum.SetLineWidth(2)
    hssum.SetFillColor(0)
    leg1.AddEntry(hssum,"Bkgs sum","l")
    hssum.Draw("HIST")
    hssum.SetTitle(histdata.GetTitle())
    hssum.GetXaxis().SetTitle(histdata.GetXaxis().GetTitle())
    hssum.GetXaxis().SetTitleOffset(1.1)
    hssum.GetYaxis().SetTitle(histdata.GetYaxis().GetTitle())
    hssum.GetYaxis().SetTitleOffset(1.1)
    gPad.SetLogy()

#    hs.Draw("nostack")
    hssum.SetMaximum(max(hs.GetMaximum(),histdata.GetMaximum())*1.1)
    hssum.SetMinimum(hs.GetMinimum("nostack")*5.)
    histdata.Draw("e same")
    histdata.SetStats(0)
#    histsig.Draw("hist same")
    leg1.Draw()
    Header.Draw("same")
    regionComment.Draw("same")

    pad2.cd()
#    hdiff=histdata.Clone("hdiff")
#    hdiff.Divide(hssum)
#    hdiff.SetLineWidth(1)
#    hdiff.GetYaxis().SetTitle("Data/MC           ")
#    hdiff.GetYaxis().SetTitleSize(0.07)
#    hdiff.GetYaxis().SetTitleOffset(0.5)
#    hdiff.GetYaxis().SetLabelSize(0.05)
#    hdiff.GetXaxis().SetTitle("")
#    hdiff.GetXaxis().SetLabelSize(0.07)
#    hdiff.SetMaximum(2.0)
#    hdiff.SetMinimum(0.0)
    hdiff.Draw("e")
    line=TLine(0,1,hssum.GetXaxis().GetXmax(),1)
    line.SetLineStyle(2)
    line.Draw("same")


    c.Print(histname+"sketch.pdf","pdf")

    c.Print("WWWoutcombplot_"+dd+"/"+histname+"sketch.png")
    c.Clear()



sw = ROOT.TStopwatch()
sw.Start()
print "start"

#------------input file and input tree----------
data=TFile.Open("outplot_"+sys.argv[1]+"/skimplot_dataSingleMu.root")
mcttg=TFile.Open("outplot_"+sys.argv[1]+"/skimplot_mcttg.root")
mcttw=TFile.Open("outplot_"+sys.argv[1]+"/skimplot_mcttw.root")
mctt=TFile.Open("outplot_"+sys.argv[1]+"/skimplot_mctt.root")
mcdyjets=TFile.Open("outplot_"+sys.argv[1]+"/skimplot_mcdyjets.root")
mcwjets=TFile.Open("outplot_"+sys.argv[1]+"/skimplot_mcwjets.root")
sig=TFile.Open("outplot_"+sys.argv[1]+"/skimplot_sig600_375.root")


#-----------------output dir and files

dd=datetime.datetime.now().strftime("%b%d")
os.system('mkdir -p outcombplot_'+dd)
os.chdir('outcombplot_'+dd)
os.system('mkdir -p WWWoutcombplot_'+dd)

stack("Pre-selection","preMET",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("Pre-selection","pre_SingleMuPt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("Pre-selection","pre_nPho",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("Pre-selection","pre_nFake",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("Pre-selection","pre_nJet",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("Pre-selection","pre_SingleMuEta",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("Pre-selection","pre_LeadBjetPt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("Pre-selection","pre_jetHt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)



stack("SR1","SR1MET",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("SR1","SR1dR_pho_mu",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("SR1","SR1_SingleMuPt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("SR1","SinglePhoR9",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("SR1","SinglePhoHoE",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("SR1","SinglePhoSigmaIEtaIEta",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("SR1","SinglePhoSigmaIPhiIPhi",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("SR1","SinglePhoEt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("SR1","SinglePhoEta",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("SR1","SR1_LeadBjetPt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("SR1","SR1invmupho",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("SR1","SR1_jetHt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)

stack("SR2","SR2MET",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("SR2","SR2phodR",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("SR2","SR2_SingleMuPt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("SR2","diPhotonM",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("SR2","SR2nPho",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("SR2","LeadPhoEt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("SR2","TrailPhoEt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("SR2","SR2_LeadBjetPt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("SR2","SR2_jetHt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)



stack("CR1","CR1MET",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("CR1","CR1dR_fake_mu",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("CR1","CR1_SingleMuPt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("CR1","SingleFakeR9",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("CR1","SingleFakeSigmaIEtaIEta",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("CR1","SingleFakeEt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("CR1","SingleFakeEta",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("CR1","CR1_LeadBjetPt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("CR1","CR1invmufake",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("CR1","CR1_jetHt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)

stack("CR2","CR2MET",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
#stack("CR2","CR2fakedR",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("CR2","CR2_SingleMuPt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("CR2","diFakeM",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("CR2","CR2nFake",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("CR2","LeadFakeEt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("CR2","TrailFakeEt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("CR2","CR2_LeadBjetPt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)
stack("CR2","CR2_jetHt",data,"SingleMu",[[mcttw,"bkg_ttw",frac_ttw,417],[mcttg,"bkg_ttg",frac_ttg,800],[mcdyjets,"bkg_zjets",frac_dyjets,857],[mcwjets,"bkg_wjets",frac_wjets,432],[mctt,"bkg_tt",frac_tt,901]],sig,"stop600_bino375",frac_sig600)


os.system('cp -r WWWoutcombplot_'+dd+' ~/www/susyplots/')
os.system('rm -r WWWoutcombplot_'+dd)
print "the plots have also been saved to www"
sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"
