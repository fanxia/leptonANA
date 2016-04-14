#!/bin/python
#this script to calculat the pileup weight
#data input is the data_true.root
#mc input is the pdf list

from ROOT import *
import ROOT
import sys

ddata=TFile.Open("DataPU_true.root")
data=ddata.Get("pileup")

mclist=[4.8551E-07,1.74806E-06,3.30868E-06,1.62972E-05,4.95667E-05,0.000606966,0.003307249,0.010340741,0.022852296,0.041948781,0.058609363,0.067475755,0.072817826,0.075931405,0.076782504,0.076202319,0.074502547,0.072355135,0.069642102,0.064920999,0.05725576,0.047289348,0.036528446,0.026376131,0.017806872,0.011249422,0.006643385,0.003662904,0.001899681,0.00095614,0.00050028,0.000297353,0.000208717,0.000165856,0.000139974,0.000120481,0.000103826,8.88868E-05,7.53323E-05,6.30863E-05,5.21356E-05,4.24754E-05,3.40876E-05,2.69282E-05,2.09267E-05,1.5989E-05,4.8551E-06,2.42755E-06,4.8551E-07,2.42755E-07,1.21378E-07,4.8551E-08]

log=open("puweight.txt","w")
f=TFile("pileup.root","recreate")
puweight=ROOT.TH1F("puweight","puweight",52,0,52)
pileupmc=ROOT.TH1F("pileupmc","pileupmc",52,0,52)
#pileupdata=ROOT.TH1F("pileupdata","pileupdata",50,0,50)
#pileupmc=ROOT.TH1F("pileupmc","pileupmc",50,0,50)

c=ROOT.TCanvas("c","Plots",1000,1000)
c.cd()
#gStyle.SetOptStat(0)
leg=ROOT.TLegend(0.6,0.8,0.9,0.9)


datalist=[]
Ndata=0
for m in range(1,53):
    Ndata=Ndata+data.GetBinContent(m)
pileupdata=data.Clone()
pileupdata.Scale(1.0/Ndata)
pileupdata.Draw()
for l in range(1,53):
    datalist.append(pileupdata.GetBinContent(l))
pileupdata.SetTitle("pileupdata")
pileupdata.Write()
log.write("INPUT data true pu %s\n"%datalist)


for i in range(1,53):
    pileupmc.SetBinContent(i,mclist[i-1])
pileupmc.Write()

puweightlist=[]
for j in range(0,52):
    puweightlist.append(datalist[j]/mclist[j])
    puweight.SetBinContent(j+1,datalist[j]/mclist[j])
puweight.Write()

log.write("pileweightlist: %s\n"%puweightlist)
log.close()

pileupdata.Draw()

pileupdata.SetLineColor(kBlack)
leg.AddEntry(pileupdata,"Data pu_true","l")
pileupmc.Draw("same")
pileupmc.SetLineColor(kRed)
leg.AddEntry(pileupmc,"MC pu_true","l")
leg.Draw()

c.Print("PUTrue-data_vs_mc.pdf","pdf")

f.Close()


