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

def stack(plotname,branchname,xname,yname,data,dataname,bkg1,bkg1name,frac1,bkg2,bkg2name,frac2,bkg3,bkg3name,frac3,bkg4,bkg4name,frac4,bkg5,bkg5name,frac5):

    c=ROOT.TCanvas("c","Plots",1000,800)
    c.Clear
    gStyle.SetOptStat(0)
    gPad.SetLogy()
    c.cd()


#---------------bkg stack-------
    hs=ROOT.THStack("hs","plotname")
#    histmc1=ROOT.TH1F("histmc1","histmc1",100,0,1000)
#    histmc2=ROOT.TH1F("histmc2","histmc2",100,0,1000)

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
    data.Draw(branchname+">>histdata")
    histdata.SetLineColor(kBlack)
    histdata.SetLineWidth(2)
    
#--------------signal----------
    
#---------------draw--------
#    hs.SetMinimum(hs.GetMinimum())
#    hs.SetMaximum(hs.GetMaximum()*1.2)
    hs.SetMaximum(3.0)
    hs.SetMinimum(hs.GetMinimum("nostack"))
    hs.SetMinimum(0.01)
    hs.Draw()
    histdata.Draw("e same")
    hs.SetTitle("Muon Channel: "+plotname+";"+xname+";"+yname)


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
regionlist=["EventTree_pre","EventTree_SR1","EventTree_SR2","EventTree_CR1","EventTree_CR2"]
data=TFile.Open("../selected/dataSingleMu3Mar31/dataSingleMu3.root")
#mcttjets=TFile.Open("../selected/selected_mcttjets_321/selected_mcttjets_321.root")
#mcttwjets=TFile.Open("../selected/selected_mcttwjets_321/selected_mcttwjets_321.root")
mcttg=TFile.Open("../selected/mcttgApr03/mcttg.root")
mcttw=TFile.Open("../selected/mcttwMar31/mcttw.root")
mctt=TFile.Open("../selected/mcttMar31/mctt.root")
mcdyjets=TFile.Open("../selected/mcdyjetstollApr01/mcdyjetstoll.root")
mcwjets=TFile.Open("../selected/mcwjetsApr03/mcwjets.root")



dataTree=[data.Get(region) for region in regionlist]

mcttTree=[mctt.Get(region) for region in regionlist]
mcttwTree=[mcttw.Get(region) for region in regionlist]
mcttgTree=[mcttg.Get(region) for region in regionlist]
mcdyjetsTree=[mcdyjets.Get(region) for region in regionlist]
mcwjetsTree=[mcwjets.Get(region) for region in regionlist]


#-----------------output dir and files

dd=datetime.datetime.now().strftime("%b%d")
os.system('mkdir -p plot_'+dd)
os.chdir('plot_'+dd)
f = open("summarytable.txt","w")





#--------------------summary table----------------------------------

sumt=PrettyTable()
sumtt=PrettyTable()

Ndata=[tree.GetEntries() for tree in dataTree]
Nmctt=[tree.GetEntries()*frac_tt for tree in mcttTree]
Nmcttw=[tree.GetEntries()*frac_ttw for tree in mcttwTree]
Nmcttg=[tree.GetEntries()*frac_ttg for tree in mcttgTree]
Nmcdyjets=[tree.GetEntries()*frac_dyjets for tree in mcdyjetsTree]
Nmcwjets=[tree.GetEntries()*frac_wjets for tree in mcwjetsTree]

Nbkgsum=[Nmctt[i]+Nmcttw[i]+Nmcttg[i]+Nmcdyjets[i]+Nmcwjets[i] for i in range(5)]
sumt.field_names = ["Channel","Pre_selection","SR1","SR2"]
sumt.add_row(["tt",Nmctt[0],Nmctt[1],Nmctt[2]])
sumt.add_row(["ttw",Nmcttw[0],Nmcttw[1],Nmcttw[2]])
sumt.add_row(["ttg",Nmcttg[0],Nmcttg[1],Nmcttg[2]])
sumt.add_row(["zjets",Nmcdyjets[0],Nmcdyjets[1],Nmcdyjets[2]])
sumt.add_row(["wjets",Nmcwjets[0],Nmcwjets[1],Nmcwjets[2]])
sumt.add_row(["bkgsum",Nbkgsum[0],Nbkgsum[1],Nbkgsum[2]])
sumt.add_row(["-","-","-","-"])
sumt.add_row(["data",Ndata[0],Ndata[1],Ndata[2]])

sumtt.field_names = ["Channel","Pre_selection","CR1","CR2"]
sumtt.add_row(["tt",Nmctt[0],Nmctt[3],Nmctt[4]])
sumtt.add_row(["ttw",Nmcttw[0],Nmcttw[3],Nmcttw[4]])
sumtt.add_row(["ttg",Nmcttg[0],Nmcttg[3],Nmcttg[4]])
sumtt.add_row(["zjets",Nmcdyjets[0],Nmcdyjets[3],Nmcdyjets[4]])
sumtt.add_row(["wjets",Nmcwjets[0],Nmcwjets[3],Nmcwjets[4]])
sumtt.add_row(["bkgsum",Nbkgsum[0],Nbkgsum[3],Nbkgsum[4]])
sumtt.add_row(["-","-","-","-"])
sumtt.add_row(["data",Ndata[0],Ndata[3],Ndata[4]])

f.write("%s\n"%sumt)
f.write("%s"%sumtt)
f.close()




#------------pre plot
#--pfMET
#stack("Pre-selection_pfMET","pfMET","MET(GeV)","number of events",dataTree[0],"DataSingleMu",mcttwTree[0],"bkg_ttw",frac_ttw,mcttgTree[0],"bkg_ttg",frac_ttg,mcdyjetsTree[0],"bkg_zjets",frac_dyjets,mcwjetsTree[0],"bkg_wjets",frac_wjets,mcttTree[0],"bkg_tt",frac_tt)
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
