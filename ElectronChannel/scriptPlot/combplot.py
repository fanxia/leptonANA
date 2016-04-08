#!/bin/python
# 3.21.2016 by Fan Xia
# To stack bkgs mc and combine data, bkgs and signal

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

def stack(plotname,branchname,xname,yname,data,dataname,bkg1,bkg1name,frac1,bkg2,bkg2name,frac2,bkg3,bkg3name,frac3,bkg4,bkg4name,frac4,bkg5,bkg5name,frac5):

    c=ROOT.TCanvas("c","Plots",1000,800)
    gStyle.SetOptStat(0)
    gPad.SetLogy()
    c.cd()


#---------------bkg stack-------
    hs=ROOT.THStack("hs","plotname")
    histmc1=ROOT.TH1F("histmc1","histmc1",100,0,1000)
    histmc2=ROOT.TH1F("histmc2","histmc2",100,0,1000)
    histmc3=ROOT.TH1F("histmc3","histmc3",100,0,1000)
    histmc4=ROOT.TH1F("histmc4","histmc4",100,0,1000)
    histmc5=ROOT.TH1F("histmc5","histmc5",100,0,1000)

    bkg1.Draw(branchname+">>histmc1")
    histmc1.SetFillColor(kGreen+1)
    histmc1.Scale(frac1)
    hs.Add(histmc1)

    bkg2.Draw(branchname+">>histmc2")
    histmc2.SetFillColor(kOrange)
    histmc2.Scale(frac2)
    hs.Add(histmc2)

    bkg3.Draw(branchname+">>histmc3")
    histmc3.SetFillColor(kAzure-3)
    histmc3.Scale(frac3)
    hs.Add(histmc3)

    if bkg4.GetEntries() != 0:
        bkg4.Draw(branchname+">>histmc4")
        histmc4.SetFillColor(kCyan)
        histmc4.Scale(frac4)
        hs.Add(histmc4)


    bkg5.Draw(branchname+">>histmc5")
    histmc5.SetFillColor(kPink+1)
    histmc5.Scale(frac5)
    hs.Add(histmc5)






#--------------data--------------
    histdata=ROOT.TH1F("histdata","histdata",100,0,1000)
    data.Draw(branchname+">>histdata")
    print "datan",data.GetEntries()
    histdata.SetLineColor(kBlack)
    histdata.SetLineWidth(2)
    
#--------------signal----------
    
#---------------draw--------
#    hs.SetMinimum(hs.GetMinimum())
    hs.SetMaximum(hs.GetMaximum()*1.2)
#    hs.SetMinimum(hs.GetMinimum("nostack"))
    hs.SetMinimum(0.01)

    hs.Draw()
    hs.GetXaxis().SetLimits(0,1000)
    histdata.Draw("e same")
    hs.SetTitle("Electron Channel: "+plotname+";"+xname+";"+yname)


    leg=ROOT.TLegend(0.6,0.8,0.9,0.9)
#    leg->SetHeader();
    leg.AddEntry(histdata,dataname,"le");
    leg.AddEntry(histmc1,bkg1name,"f");
    leg.AddEntry(histmc2,bkg2name,"f");
    leg.AddEntry(histmc3,bkg3name,"f");
    if bkg4.GetEntries()!=0:
        leg.AddEntry(histmc4,bkg4name,"f");

    leg.AddEntry(histmc5,bkg5name,"f");

    leg.Draw();

#    gPad.Update()

    c.Print(plotname+".png","png")
    c.Clear()
# end stack plot module


def stackEle(plotname,branchname,data,dataname,bkglist):
    print "start stackele"

    c=ROOT.TCanvas("c","Plots",1000,1000)
    gStyle.SetOptStat(0)
#    gPad.SetLogy()
    c.cd()

#---------------bkg stack-------
    hs=ROOT.THStack("hs","plotname")
    leg=ROOT.TLegend(0.6,0.8,0.9,0.9)    
    for bkg in bkglist:
        print "get bkg input"
#        histmc=ROOT.TH1F("","",60,-3,3)
        histmc=ROOT.TH1F("","",80,0,800)
#        if bkg[0].GetEntries()==0:
#            continue

        for i in range(bkg[0].GetEntries()):
            bkg[0].GetEntry(i)
            ele_ind=bkg[0].ele_index
            histmc.Fill(getattr(bkg[0],branchname)[ele_ind])
        print "drawhistmc"
#        histmc.Draw()
        histmc.SetFillColor(bkg[3])
        histmc.Scale(bkg[2])
        hs.Add(histmc)
        leg.AddEntry(histmc,bkg[1],"f")
    print "get bkg done"


#--------------data--------------
#    histdata=ROOT.TH1F("","",60,-3,3)
    histdata=ROOT.TH1F("","",80,0,800)
    for j in range(data.GetEntries()):
        data.GetEntry(j)
        dataele_ind=data.ele_index
        histdata.Fill(getattr(data,branchname)[dataele_ind])
    histdata.Draw()
    histdata.SetLineColor(kBlack)
    histdata.SetLineWidth(2)
    print "maxdata",histdata.GetMaximum()
    leg.AddEntry(histdata,dataname,"le");    
#--------------signal----------
    
#---------------draw--------
    hs.SetMaximum(histdata.GetMaximum()*1.1)
    hs.SetTitle("EleChannel:"+plotname+";"+branchname)
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



sw = ROOT.TStopwatch()
sw.Start()
print "start"
data=TFile.Open("../selected/dataSingleEleApr01/dataSingleEle.root")
#mcttjets=TFile.Open("../selected/selected_mcttjets_321/selected_mcttjets_321.root")
#mcttwjets=TFile.Open("../selected/selected_mcttwjets_321/selected_mcttwjets_321.root")
mcttg=TFile.Open("../selected/mcttgApr01/mcttg.root")
mcttw=TFile.Open("../selected/mcttwApr01/mcttw.root")
mctt=TFile.Open("../selected/mcttApr01/mctt.root")
mcdyjets=TFile.Open("../selected/mcdyjetstollApr01/mcdyjetstoll.root")
mcwjets=TFile.Open("../selected/mcwjetsApr01/mcwjets.root")

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


#-----------------output dir and files

dd=datetime.datetime.now().strftime("%b%d")
os.system('mkdir -p plot_'+dd)
os.chdir('plot_'+dd)
f = open("summarytable.txt","w")





#--------------------summary table----------------------------------

sumt=PrettyTable()
sumtt=PrettyTable()
dataNpre=predata.GetEntries()
dataNsr1=sr1data.GetEntries()
dataNsr2=sr2data.GetEntries()
dataNcr1=cr1data.GetEntries()
dataNcr2=cr2data.GetEntries()

mcttNpre=premctt.GetEntries()*frac_tt
mcttNsr1=sr1mctt.GetEntries()*frac_tt
mcttNsr2=sr2mctt.GetEntries()*frac_tt
mcttNcr1=cr1mctt.GetEntries()*frac_tt
mcttNcr2=cr2mctt.GetEntries()*frac_tt


mcttwNpre=premcttw.GetEntries()*frac_ttw
mcttwNsr1=sr1mcttw.GetEntries()*frac_ttw
mcttwNsr2=sr2mcttw.GetEntries()*frac_ttw
mcttwNcr1=cr1mcttw.GetEntries()*frac_ttw
mcttwNcr2=cr2mcttw.GetEntries()*frac_ttw


mcttgNpre=premcttg.GetEntries()*frac_ttg
mcttgNsr1=sr1mcttg.GetEntries()*frac_ttg
mcttgNsr2=sr2mcttg.GetEntries()*frac_ttg
mcttgNcr1=cr1mcttg.GetEntries()*frac_ttg
mcttgNcr2=cr2mcttg.GetEntries()*frac_ttg


mcdyjetsNpre=premcdyjets.GetEntries()*frac_dyjets
mcdyjetsNsr1=sr1mcdyjets.GetEntries()*frac_dyjets
mcdyjetsNsr2=sr2mcdyjets.GetEntries()*frac_dyjets
mcdyjetsNcr1=cr1mcdyjets.GetEntries()*frac_dyjets
mcdyjetsNcr2=cr2mcdyjets.GetEntries()*frac_dyjets


mcwjetsNpre=premcwjets.GetEntries()*frac_wjets
mcwjetsNsr1=sr1mcwjets.GetEntries()*frac_wjets
mcwjetsNsr2=sr2mcwjets.GetEntries()*frac_wjets
mcwjetsNcr1=cr1mcwjets.GetEntries()*frac_wjets
mcwjetsNcr2=cr2mcwjets.GetEntries()*frac_wjets


bkgsumNpre=mcttNpre+mcttwNpre+mcttgNpre+mcdyjetsNpre+mcwjetsNpre
bkgsumNsr1=mcttNsr1+mcttwNsr1+mcttgNsr1+mcdyjetsNsr1+mcwjetsNsr1
bkgsumNsr2=mcttNsr2+mcttwNsr2+mcttgNsr2+mcdyjetsNsr2+mcwjetsNsr2
bkgsumNcr1=mcttNcr1+mcttwNcr1+mcttgNcr1+mcdyjetsNcr1+mcwjetsNcr1
bkgsumNcr2=mcttNcr2+mcttwNcr2+mcttgNcr2+mcdyjetsNcr2+mcwjetsNcr2


sumt.field_names = ["Channel","Pre_selection","SR1","SR2"]
sumt.add_row(["tt",mcttNpre,mcttNsr1,mcttNsr2])
sumt.add_row(["ttw",mcttwNpre,mcttwNsr1,mcttwNsr2])
sumt.add_row(["ttg",mcttgNpre,mcttgNsr1,mcttgNsr2])
sumt.add_row(["zjets",mcdyjetsNpre,mcdyjetsNsr1,mcdyjetsNsr2])
sumt.add_row(["wjets",mcwjetsNpre,mcwjetsNsr1,mcwjetsNsr2])
sumt.add_row(["bkgs sum",bkgsumNpre,bkgsumNsr1,bkgsumNsr2])
sumt.add_row(["-","-","-","-"])
sumt.add_row(["data",dataNpre,dataNsr1,dataNsr2])


sumtt.field_names = ["Channel","Pre_selection","CR1","CR2"]
sumtt.add_row(["tt",mcttNpre,mcttNcr1,mcttNcr2])
sumtt.add_row(["ttw",mcttwNpre,mcttwNcr1,mcttwNcr2])
sumtt.add_row(["ttg",mcttgNpre,mcttgNcr1,mcttgNcr2])
sumtt.add_row(["zjets",mcdyjetsNpre,mcdyjetsNcr1,mcdyjetsNcr2])
sumtt.add_row(["wjets",mcwjetsNpre,mcwjetsNcr1,mcwjetsNcr2])
sumtt.add_row(["bkgs sum",bkgsumNpre,bkgsumNcr1,bkgsumNcr2])
sumtt.add_row(["-","-","-","-"])
sumtt.add_row(["data",dataNpre,dataNcr1,dataNcr2])


f.write("%s\n"%sumt)
f.write("%s"%sumtt)
f.close()


#------------pre plot
#--pfMET
#stack("Pre-selection_pfMET","pfMET","MET(GeV)","number of events",predata,"DataSingleEle",premcttw,"bkg_ttw",frac_ttw,premcttg,"bkg_ttg",frac_ttg,premcdyjets,"bkg_zjets",frac_dyjets,premcwjets,"bkg_wjets",frac_wjets,premctt,"bkg_tt",frac_tt)
#stack("Pre-selection_nVtx","nVtx","nVtx","number of events",predata,"DataSingleEle",premcttw,"bkg_ttw",frac_ttw,premcttg,"bkg_ttg",frac_ttg,premcdyjets,"bkg_zjets",frac_dyjets,premcwjets,"bkg_wjets",frac_wjets,premctt,"bkg_tt",frac_tt)
#--elePt and eleEta
#stackEle("Pre-seletion_elePt","elePt",predata,"SingleEle",[[premcttw,"bkg_ttw",frac_ttw,417],[premcttg,"bkg_ttg",frac_ttg,800],[premcdyjets,"bkg_zjets",frac_dyjets,857],[premcwjets,"bkg_wjets",frac_wjets,432],[premctt,"bkg_tt",frac_tt,901]])
#stackEle("Pre-seletion_eleEta","eleEta",predata,"SingleEle",[[premcttw,"bkg_ttw",frac_ttw,417],[premcttg,"bkg_ttg",frac_ttg,800],[premcdyjets,"bkg_zjets",frac_dyjets,857],[premcwjets,"bkg_wjets",frac_wjets,432],[premctt,"bkg_tt",frac_tt,901]])


#------------sr1 plot
#--pfMET
stack("SR1_pfMET","pfMET","MET(GeV)","number of events",sr1data,"DataSingleEle",sr1mcttw,"bkg_ttw",frac_ttw,sr1mcttg,"bkg_ttg",frac_ttg,sr1mcdyjets,"bkg_zjets",frac_dyjets,sr1mcwjets,"bkg_wjets",frac_wjets,sr1mctt,"bkg_tt",frac_tt)

#--elePt and eleEta
stackEle("SR1_elePt","elePt",sr1data,"SingleEle",[[sr1mcttw,"bkg_ttw",frac_ttw,417],[sr1mcttg,"bkg_ttg",frac_ttg,800],[sr1mcdyjets,"bkg_zjets",frac_dyjets,857],[sr1mcwjets,"bkg_wjets",frac_wjets,432],[sr1mctt,"bkg_tt",frac_tt,901]])
#stackEle("SR1_eleEta","eleEta",sr1data,"SingleEle",[[sr1mcttw,"bkg_ttw",frac_ttw,417],[sr1mcttg,"bkg_ttg",frac_ttg,800],[sr1mcdyjets,"bkg_zjets",frac_dyjets,857],[sr1mcwjets,"bkg_wjets",frac_wjets,432],[sr1mctt,"bkg_tt",frac_tt,901]])
#--phoEt and Eta
#stackpho("SR1_","phoEt",11,sr1data,"SingleEle",sr1mcttwjets,"bkg_ttwjets",frac_ttwjets,sr1mcttjets,"bkg_ttjets",frac_ttjets)
#stackpho("SR1_","phoEta",11,sr1data,"SingleEle",sr1mcttwjets,"bkg_ttwjets",frac_ttwjets,sr1mcttjets,"bkg_ttjets",frac_ttjets)



#------------sr2 plot
#--pfMET
stack("SR2_pfMET","pfMET","MET(GeV)","number of events",sr2data,"DataSingleEle",sr2mcttw,"bkg_ttw",frac_ttw,sr2mcttg,"bkg_ttg",frac_ttg,sr2mcdyjets,"bkg_zjets",frac_dyjets,sr2mcwjets,"bkg_wjets",frac_wjets,sr2mctt,"bkg_tt",frac_tt)


#--elePt and eleEta
stackEle("SR2_elePt","elePt",sr2data,"SingleEle",[[sr2mcttw,"bkg_ttw",frac_ttw,417],[sr2mcttg,"bkg_ttg",frac_ttg,800],[sr2mcdyjets,"bkg_zjets",frac_dyjets,857],[sr2mcwjets,"bkg_wjets",frac_wjets,432],[sr2mctt,"bkg_tt",frac_tt,901]])
#stackEle("SR2_eleEta","eleEta",sr2data,"SingleEle",[[sr2mcttw,"bkg_ttw",frac_ttw,417],[sr2mcttg,"bkg_ttg",frac_ttg,800],[sr2mcdyjets,"bkg_zjets",frac_dyjets,857],[sr2mcwjets,"bkg_wjets",frac_wjets,432],[sr2mctt,"bkg_tt",frac_tt,901]])


#--Leading phoEt and Eta
stackpho("SR2_Leading","phoEt",21,sr2data,"SingleEle",sr2mcttwjets,"bkg_ttwjets",frac_ttwjets,sr2mcttjets,"bkg_ttjets",frac_ttjets)
stackpho("SR2_Leading","phoEta",21,sr2data,"SingleEle",sr2mcttwjets,"bkg_ttwjets",frac_ttwjets,sr2mcttjets,"bkg_ttjets",frac_ttjets)
#--Trailing phoEt and Eta
stackpho("SR2_Trailing","phoEt",22,sr2data,"SingleEle",sr2mcttwjets,"bkg_ttwjets",frac_ttwjets,sr2mcttjets,"bkg_ttjets",frac_ttjets)
stackpho("SR2_Trailing","phoEta",22,sr2data,"SingleEle",sr2mcttwjets,"bkg_ttwjets",frac_ttwjets,sr2mcttjets,"bkg_ttjets",frac_ttjets)








sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"
