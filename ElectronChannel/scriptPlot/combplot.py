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

xsec_ttw=0.2043
lumi_ttw=1238
frac_ttw=lumi_data/lumi_ttw

xsec_dyjets=6025.2
lumi_dyjets=4.77
frac_dyjets=lumi_data/lumi_dyjets

xsec_wjets=61526.7
lumi_wjets=0.393
frac_wjets=lumi_data/lumi_wjets

xsec_tt=831.76
lumi_tt=22.16
frac_tt=lumi_data/lumi_tt

xsec_ttg=3.697
lumi_ttg=1307.1
frac_ttg=lumi_data/lumi_ttg





# stack plot module

def stack(plotname,branchname,data,dataname,bkg1,bkg1name,frac1,bkg2,bkg2name,frac2,bkg3,bkg3name,frac3,bkg4,bkg4name,frac4,bkg5,bkg5name,frac5):

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

    bkg3.Draw(branchname+">>histmc3")
    histmc3.SetFillColor(kOrange)
    histmc3.Scale(frac3)
    hs.Add(histmc3)

    bkg4.Draw(branchname+">>histmc4")
    histmc4.SetFillColor(kViolet-1)
    histmc4.Scale(frac4)
    hs.Add(histmc4)

    bkg5.Draw(branchname+">>histmc5")
    histmc5.SetFillColor(kGreen+1)
    histmc5.Scale(frac5)
    hs.Add(histmc5)



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




def stackele(plotname,branchname,data,dataname,bkg1,bkg1name,frac1,bkg2,bkg2name,frac2):

    c=ROOT.TCanvas("c","Plots",800,800)
    gStyle.SetOptStat(0)
#    gPad.SetLogy()
    c.cd()

#---------------bkg stack-------
    bkg1ele_ind=bkg1.ele_index
    bkg2ele_ind=bkg2.ele_index
    hs=ROOT.THStack("hs","plotname")

    bkg1.Draw(branchname+"[bkg1ele_ind]>>histmc1")
    histmc1.SetFillColor(kRed-7)
    histmc1.Scale(frac1)
    hs.Add(histmc1)

    bkg2.Draw(branchname+"[bkg2ele_ind]>>histmc2")
    histmc2.SetFillColor(kBlue-10)
    histmc2.Scale(frac2)
    hs.Add(histmc2)

    hs.SetTitle(plotname+branchname+";;")

#--------------data--------------
    dataele_ind=data.ele_index
    data.Draw(branchname+"[dataele_ind]>>histdata")
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
# end stackele plot module


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
# end stackele plot module


sw = ROOT.TStopwatch()
sw.Start()
print "start"
data=TFile.Open("../selected/selected_dataSingleEle_321/selected_dataSingleEle_321.root")
#mcttjets=TFile.Open("../selected/selected_mcttjets_321/selected_mcttjets_321.root")
#mcttwjets=TFile.Open("../selected/selected_mcttwjets_321/selected_mcttwjets_321.root")
mcttg=TFile.Open("../selected/mcttgMar30/mcttg.root")
mcttw=TFile.Open("../selected/mcttwMar30/mcttw.root")
mctt=TFile.Open("../selected/mcttMar30/mctt.root")
mcdyjets=TFile.Open("../selected/mcdyjetstollMar30/mcdyjetstoll.root")
mcwjets=TFile.Open("../selected/mcwjetsMar30/mcwjets.root")

# predata=data.Get("ggNtuplizer/EventTree_pre")
# premcttjets=mcttjets.Get("ggNtuplizer/EventTree_pre")
# premcttwjets=mcttwjets.Get("ggNtuplizer/EventTree_pre")

# sr1data=data.Get("ggNtuplizer/EventTree_SR1")
# sr1mcttjets=mcttjets.Get("ggNtuplizer/EventTree_SR1")
# sr1mcttwjets=mcttwjets.Get("ggNtuplizer/EventTree_SR1")

# sr2data=data.Get("ggNtuplizer/EventTree_SR2")
# sr2mcttjets=mcttjets.Get("ggNtuplizer/EventTree_SR2")
# sr2mcttwjets=mcttwjets.Get("ggNtuplizer/EventTree_SR2")


predata=data.Get("EventTree_pre")
sr1data=data.Get("EventTree_SR1")
sr2data=data.Get("EventTree_SR2")
cr1data=data.Get("EventTree_CR1")
cr2data=data.Get("EventTree_CR2")

premctt=mctt.Get("EventTree_pre")
sr1mctt=mctt.Get("EventTree_SR1")
sr2mctt=mctt.Get("EventTree_SR2")
cr1mctt=mctt.Get("EventTree_CR1")
cr2mctt=mctt.Get("EventTree_CR2")

premcttw=mcttw.Get("EventTree_pre")
sr1mcttw=mcttw.Get("EventTree_SR1")
sr2mcttw=mcttw.Get("EventTree_SR2")
cr1mcttw=mcttw.Get("EventTree_CR1")
cr2mcttw=mcttw.Get("EventTree_CR2")


premcttg=mcttg.Get("EventTree_pre")
sr1mcttg=mcttg.Get("EventTree_SR1")
sr2mcttg=mcttg.Get("EventTree_SR2")
cr1mcttg=mcttg.Get("EventTree_CR1")
cr2mcttg=mcttg.Get("EventTree_CR2")


premcdyjets=mcdyjets.Get("EventTree_pre")
sr1mcdyjets=mcdyjets.Get("EventTree_SR1")
sr2mcdyjets=mcdyjets.Get("EventTree_SR2")
cr1mcdyjets=mcdyjets.Get("EventTree_CR1")
cr2mcdyjets=mcdyjets.Get("EventTree_CR2")


premcwjets=mcwjets.Get("EventTree_pre")
sr1mcwjets=mcwjets.Get("EventTree_SR1")
sr2mcwjets=mcwjets.Get("EventTree_SR2")
cr1mcwjets=mcwjets.Get("EventTree_CR1")
cr2mcwjets=mcwjets.Get("EventTree_CR2")


dd=datetime.datetime.now().strftime("%b%d")
os.system('mkdir -p plot_'+dd)
os.chdir('plot_'+dd)

#------------pre plot
#--pfMET
stack("Pre_pfMET","pfMET",predata,"DataSingleEle",premctt,"bkg_tt",frac_tt,premcttg,"bkg_ttg",frac_ttg,premcttw,"bkg_ttw",frac_ttw,premcwjets,"bkg_wjets",frac_wjets,premcdyjets,"bkg_zjets",frac_dyjets)
#--elePt and eleEta
stackEle("pre_","elePt",predata,"SingleEle",premcttwjets,"bkg_ttwjets",frac_ttwjets,premcttjets,"bkg_ttjets",frac_ttjets)
stackEle("pre_","eleEta",predata,"SingleEle",premcttwjets,"bkg_ttwjets",frac_ttwjets,premcttjets,"bkg_ttjets",frac_ttjets)


#------------sr1 plot
#--pfMET
#stack("SR1pfMET","pfMET",sr1data,"SingleEle",sr1mcttwjets,"bkg_ttwjets",frac_ttwjets,sr1mcttjets,"bkg_ttjets",frac_ttjets)
stack("SR1_pfMET","pfMET",sr1data,"DataSingleEle",sr1mctt,"bkg_tt",frac_tt,sr1mcttg,"bkg_ttg",frac_ttg,sr1mcttw,"bkg_ttw",frac_ttw,sr1mcwjets,"bkg_wjets",frac_wjets,sr1mcdyjets,"bkg_zjets",frac_dyjets)
#--elePt and eleEta
stackEle("SR1_","elePt",sr1data,"SingleEle",sr1mcttwjets,"bkg_ttwjets",frac_ttwjets,sr1mcttjets,"bkg_ttjets",frac_ttjets)
stackEle("SR1_","eleEta",sr1data,"SingleEle",sr1mcttwjets,"bkg_ttwjets",frac_ttwjets,sr1mcttjets,"bkg_ttjets",frac_ttjets)
#--phoEt and Eta
stackpho("SR1_","phoEt",11,sr1data,"SingleEle",sr1mcttwjets,"bkg_ttwjets",frac_ttwjets,sr1mcttjets,"bkg_ttjets",frac_ttjets)
stackpho("SR1_","phoEta",11,sr1data,"SingleEle",sr1mcttwjets,"bkg_ttwjets",frac_ttwjets,sr1mcttjets,"bkg_ttjets",frac_ttjets)



#------------sr2 plot
#--pfMET
#stack("SR2pfMET","pfMET",sr2data,"SingleEle",sr2mcttwjets,"bkg_ttwjets",frac_ttwjets,sr2mcttjets,"bkg_ttjets",frac_ttjets)
stack("SR2_pfMET","pfMET",sr2data,"DataSingleEle",sr2mctt,"bkg_tt",frac_tt,sr2mcttg,"bkg_ttg",frac_ttg,sr2mcttw,"bkg_ttw",frac_ttw,sr2mcwjets,"bkg_wjets",frac_wjets,sr2mcdyjets,"bkg_zjets",frac_dyjets)
#--elePt and eleEta
stackEle("SR2_","elePt",predata,"SingleEle",premcttwjets,"bkg_ttwjets",frac_ttwjets,premcttjets,"bkg_ttjets",frac_ttjets)
stackEle("SR2_","eleEta",predata,"SingleEle",premcttwjets,"bkg_ttwjets",frac_ttwjets,premcttjets,"bkg_ttjets",frac_ttjets)
#--Leading phoEt and Eta
stackpho("SR2_Leading","phoEt",21,sr2data,"SingleEle",sr2mcttwjets,"bkg_ttwjets",frac_ttwjets,sr2mcttjets,"bkg_ttjets",frac_ttjets)
stackpho("SR2_Leading","phoEta",21,sr2data,"SingleEle",sr2mcttwjets,"bkg_ttwjets",frac_ttwjets,sr2mcttjets,"bkg_ttjets",frac_ttjets)
#--Trailing phoEt and Eta
stackpho("SR2_Trailing","phoEt",22,sr2data,"SingleEle",sr2mcttwjets,"bkg_ttwjets",frac_ttwjets,sr2mcttjets,"bkg_ttjets",frac_ttjets)
stackpho("SR2_Trailing","phoEta",22,sr2data,"SingleEle",sr2mcttwjets,"bkg_ttwjets",frac_ttwjets,sr2mcttjets,"bkg_ttjets",frac_ttjets)




sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"
