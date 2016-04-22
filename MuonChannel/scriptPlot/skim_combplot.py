#!/bin/python
# 4.7.2016 by Fan Xia
# To stack bkgs mc and combine data, bkgs and signal
# using the ../selected/skim...root as inputs

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

def stack(region,plotname,branchname,xname,yname,xnbin,xmin,xmax,ymin,ymax,data,dataname,bkglist):


    c=ROOT.TCanvas("c","Plots",1000,1000)
    c.cd()
    gStyle.SetOptStat(0)
    leg=ROOT.TLegend(0.6,0.8,0.9,0.9)    
    hs=ROOT.THStack("hs","hs")


#---------------data
    histdata=ROOT.TH1F("histdata","histdata",xnbin,xmin,xmax)
    for j in range(data.GetEntries()):
        data.GetEntry(j)
        if data.region==region:
            histdata.Fill(getattr(data,branchname))
    histdata.Draw()
    histdata.SetLineColor(kBlack)
    histdata.SetLineWidth(2)
    histdata.SetLineStyle(2)
    leg.AddEntry(histdata,dataname,"l")


#---------------bkg stack-("nostack"mode)------

    for bkg in bkglist:
        histmc=ROOT.TH1F("","",xnbin,xmin,xmax)
        print "get bkg input"
        nevents=bkg[0].GetEntries()
        print nevents
        if nevents==0:
            continue
        for i in range(nevents):
            bkg[0].GetEntry(i)
            if bkg[0].region==region:
                histmc.Fill(getattr(bkg[0],branchname))
        if histmc.GetEntries()==0: continue
        histmc.SetLineColor(bkg[3])
        histmc.SetLineWidth(2)
        histmc.Scale(bkg[2])
        hs.Add(histmc)
        leg.AddEntry(histmc,bkg[1],"l")
    print "get bkg done"

    
#---------------draw--------

    hs.SetTitle("MuonChannel: "+plotname+";"+branchname+";")
    hs.Draw()
#    hs.Draw("nostack")
    hs.SetMaximum(ymax)
    hs.SetMinimum(ymin)
    leg.Draw()
    histdata.Draw("same")
    c.Print("xxx.png","png")
    hs.Write()
    histdata.Write()
    c.Clear()
#--------and stack



def stackMu(plotname,branchname,data,dataname,bkglist):
    print "start stackmu"

    c=ROOT.TCanvas("c","Plots",1000,1000)
    gStyle.SetOptStat(0)
#    gPad.SetLogy()
    c.cd()

#---------------bkg stack-------
    hs=ROOT.THStack("hs","plotname")
    leg=ROOT.TLegend(0.6,0.8,0.9,0.9)    
    for bkg in bkglist:
        print "get bkg input"
        histmc=ROOT.TH1F("","",60,-3,3)
#        histmc=ROOT.TH1F("","",80,0,800)
#        if bkg[0].GetEntries()==0:
#            continue

        for i in range(bkg[0].GetEntries()):
            bkg[0].GetEntry(i)
            mu_ind=bkg[0].mu_index
            histmc.Fill(getattr(bkg[0],branchname)[mu_ind])
        print "drawhistmc"
#        histmc.Draw()
        histmc.SetFillColor(bkg[3])
        histmc.Scale(bkg[2])
        hs.Add(histmc)
        leg.AddEntry(histmc,bkg[1],"f")
    print "get bkg done"


#--------------data--------------
    histdata=ROOT.TH1F("","",60,-3,3)
#    histdata=ROOT.TH1F("","",80,0,800)
    for j in range(data.GetEntries()):
        data.GetEntry(j)
        datamu_ind=data.mu_index
        histdata.Fill(getattr(data,branchname)[datamu_ind])
    histdata.Draw()
    histdata.SetLineColor(kBlack)
    histdata.SetLineWidth(2)
    print "maxdata",histdata.GetMaximum()
    leg.AddEntry(histdata,dataname,"le");    
#--------------signal----------
    
#---------------draw--------
    hs.SetMaximum(histdata.GetMaximum()*1.1)
    hs.SetTitle("MuonChannel:"+plotname+";"+branchname)
#    hs.SetMaximum(10000)
    hs.SetMinimum(0.01)
#    hs.SetMinimum(hs.GetMinimum("nostack"))
    gPad.SetLogy()
    hs.Draw()
    histdata.Draw("e same")

    leg.Draw();
    c.Print(plotname+".png","png")
    c.Clear()
# end stackmu plot module


def stackpho(plotname,branchname,region,data,dataname,bkg1,bkg1name,frac1,bkg2,bkg2name,frac2):

    c=ROOT.TCanvas("c","Plots",800,800)
    gStyle.SetOptStat(0)
#    gPad.SetLogy()
    c.cd()

#---------------bkg stack-------
 #sr1,only one photon
    if region==11:
        bkg1pho_ind=bkg1.pho_index
        bkg2pho_ind=bkg2.pho_index
        datapho_ind=data.pho_index
 #sr2,leading photon
    elif region==21:
        bkg1pho_ind=bkg1.pho_index[0]
        bkg2pho_ind=bkg2.pho_index[0]
        datapho_ind=data.pho_index[0]
 #sr2,trailing photon
    elif region==22:
        bkg1pho_ind=bkg1.pho_index[1]
        bkg2pho_ind=bkg2.pho_index[1]
        datapho_ind=data.pho_index[1]

    hs=ROOT.THStack("hs","plotname")

    bkg1.Draw(branchname+"[bkg1pho_ind]>>histmc1")
    histmc1.SetFillColor(kRed-7)
    histmc1.Scale(frac1)
    hs.Add(histmc1)

    bkg2.Draw(branchname+"[bkg2pho_ind]>>histmc2")
    histmc2.SetFillColor(kBlue-10)
    histmc2.Scale(frac2)
    hs.Add(histmc2)

    hs.SetTitle(plotname+branchname+";;")

#--------------data--------------
    data.Draw(branchname+"[datapho_ind]>>histdata")
    histdata.SetLineColor(kBlack)
    histdata.SetLineWidth(2)
    
#--------------signal----------
    
#---------------draw--------
    hs.SetMaximum(histdata.GetMaximum()*1.1)
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
    c.Print(plotname+branchname+".png","png")
    c.Clear()
# end stackmu plot module


sw = ROOT.TStopwatch()
sw.Start()
print "start"


#------------input file and input tree----------
data=TFile.Open("../selected/skim_dataSingleMuApr12/skim_dataSingleMu.root")
mcttg=TFile.Open("../selected/skim_mcttgApr15/skim_mcttg.root")
mcttw=TFile.Open("../selected/skim_mcttwApr15/skim_mcttw.root")
mctt=TFile.Open("../selected/skim_mcttApr15/skim_mctt.root")
mcdyjets=TFile.Open("../selected/skim_mcdyjetsApr15/skim_mcdyjets.root")
mcwjets=TFile.Open("../selected/skim_mcwjetsApr15/skim_mcwjets.root")


dataTree=data.Get("EventTree")
mcttTree=mctt.Get("EventTree")
mcttwTree=mcttw.Get("EventTree")
mcttgTree=mcttg.Get("EventTree")
mcdyjetsTree=mcdyjets.Get("EventTree")
mcwjetsTree=mcwjets.Get("EventTree")


#-----------------output dir and files

dd=datetime.datetime.now().strftime("%b%d")
os.system('mkdir -p plot_'+dd)
os.chdir('plot_'+dd)



#------------pre plot
#--pfMET
stack(0,"Pre-selection_pfMET","pfMET","MET(GeV)","number of events",100,0,1000,0.01,10000,dataTree,"DataSingleMu",[[mcttwTree,"bkg_ttw",frac_ttw,417],[mcttgTree,"bkg_ttg",frac_ttg,800],[mcdyjetsTree,"bkg_zjets",frac_dyjets,857],[mcwjetsTree,"bkg_wjets",frac_wjets,432],[mcttTree,"bkg_tt",frac_tt,901]])
#--nVtx
#stack("Pre-selection_nVtx","nVtx","nVtx","number of events",predata,"DataSingleMu",premcttw,"bkg_ttw",frac_ttw,premcttg,"bkg_ttg",frac_ttg,premcdyjets,"bkg_zjets",frac_dyjets,premcwjets,"bkg_wjets",frac_wjets,premctt,"bkg_tt",frac_tt)


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
