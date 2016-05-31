#!/bin/python
# 4.15.2016 by Fan Xia
# using the ../selected/skim...root as inputs
# count the sum, for weighted mc
# python sumtable4skim.py DD

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


sw = ROOT.TStopwatch()
sw.Start()
print "start"

#------------input file and input tree----------
data=TFile.Open("../selected/skim_ana_root"+sys.argv[1]+"/skim_dataSingleMu.root")
mcttg=TFile.Open("../selected/skim_ana_root"+sys.argv[1]+"/skim_mcttg.root")
mcttw=TFile.Open("../selected/skim_ana_root"+sys.argv[1]+"/skim_mcttw.root")
mctt=TFile.Open("../selected/skim_ana_root"+sys.argv[1]+"/skim_mctt.root")
mcdyjets=TFile.Open("../selected/skim_ana_root"+sys.argv[1]+"/skim_mcdyjets.root")
mcwjets=TFile.Open("../selected/skim_ana_root"+sys.argv[1]+"/skim_mcwjets.root")
signal=TFile.Open("../selected/skim_ana_root"+sys.argv[1]+"/skim_sig600_375.root")

dataTree=data.Get("EventTree")
mcttTree=mctt.Get("EventTree")
mcttgTree=mcttg.Get("EventTree")
mcttwTree=mcttw.Get("EventTree")
mcdyjetsTree=mcdyjets.Get("EventTree")
mcwjetsTree=mcwjets.Get("EventTree")
sigTree=signal.Get("EventTree")

dd=datetime.datetime.now().strftime("%b%d")
f=open(dd+"summarytable.txt","w")

#--------------------summary table before weight----------------------------------

sumt=PrettyTable()
sumtt=PrettyTable()

Ndata=[dataTree.Draw("","",""),dataTree.Draw("","region==1",""),dataTree.Draw("","region==2",""),dataTree.Draw("","region==3",""),dataTree.Draw("","region==4","")]
Nmctt=[mcttTree.Draw("","",""),mcttTree.Draw("","region==1",""),mcttTree.Draw("","region==2",""),mcttTree.Draw("","region==3",""),mcttTree.Draw("","region==4","")]
Nmctt=[x*frac_tt for x in Nmctt]

Nmcttg=[mcttgTree.Draw("","",""),mcttgTree.Draw("","region==1",""),mcttgTree.Draw("","region==2",""),mcttgTree.Draw("","region==3",""),mcttgTree.Draw("","region==4","")]
Nmcttg=[x*frac_ttg for x in Nmcttg]

Nmcttw=[mcttwTree.Draw("","",""),mcttwTree.Draw("","region==1",""),mcttwTree.Draw("","region==2",""),mcttwTree.Draw("","region==3",""),mcttwTree.Draw("","region==4","")]
Nmcttw=[x*frac_ttw for x in Nmcttw]

Nmcdyjets=[mcdyjetsTree.Draw("","",""),mcdyjetsTree.Draw("","region==1",""),mcdyjetsTree.Draw("","region==2",""),mcdyjetsTree.Draw("","region==3",""),mcdyjetsTree.Draw("","region==4","")]
Nmcdyjets=[x*frac_dyjets for x in Nmcdyjets]

Nmcwjets=[mcwjetsTree.Draw("","",""),mcwjetsTree.Draw("","region==1",""),mcwjetsTree.Draw("","region==2",""),mcwjetsTree.Draw("","region==3",""),mcwjetsTree.Draw("","region==4","")]
Nmcwjets=[x*frac_wjets for x in Nmcwjets]


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
#sumt.add_row(["diff",Nbkgsum[0]/Ndata[0]-1,Nbkgsum[1]/Ndata[1]-1,Nbkgsum[2]/Ndata[2]-1])



sumtt.field_names = ["Channel","Pre_selection","CR1","CR2"]
sumtt.add_row(["tt",Nmctt[0],Nmctt[3],Nmctt[4]])
sumtt.add_row(["ttw",Nmcttw[0],Nmcttw[3],Nmcttw[4]])
sumtt.add_row(["ttg",Nmcttg[0],Nmcttg[3],Nmcttg[4]])
sumtt.add_row(["zjets",Nmcdyjets[0],Nmcdyjets[3],Nmcdyjets[4]])
sumtt.add_row(["wjets",Nmcwjets[0],Nmcwjets[3],Nmcwjets[4]])
sumtt.add_row(["bkgsum",Nbkgsum[0],Nbkgsum[3],Nbkgsum[4]])
sumtt.add_row(["-","-","-","-"])
sumtt.add_row(["data",Ndata[0],Ndata[3],Ndata[4]])
#sumtt.add_row(["diff",Nbkgsum[0]/Ndata[0]-1,Nbkgsum[3]/Ndata[3]-1,Nbkgsum[4]/Ndata[4]-1])

f.write("Before weight\n")
f.write("%s\n"%sumt)
f.write("%s\n"%sumtt)


#--------------------------summary table after weight--------------------------

wsumt=PrettyTable()
wsumtt=PrettyTable()

wNmctt=[0,0,0,0,0]
wNmcttw=[0,0,0,0,0]
wNmcttg=[0,0,0,0,0]
wNmcdyjets=[0,0,0,0,0]
wNmcwjets=[0,0,0,0,0]
for mc in [[mcttTree,wNmctt,frac_tt],[mcttgTree,wNmcttg,frac_ttg],[mcttwTree,wNmcttw,frac_ttw],[mcdyjetsTree,wNmcdyjets,frac_dyjets],[mcwjetsTree,wNmcwjets,frac_wjets]]:
    print "get bkg",mc[2]
    for i in range(mc[0].GetEntries()):
        mc[0].GetEntry(i)
        wei=mc[0].totalweight
        mc[1][0]+=wei
        for re in [1,2,3,4]:
            if mc[0].region==re:
                mc[1][re]+=wei
    for j in range(5):
        mc[1][j]=mc[1][j]*mc[2]

wNsig=[0,0,0,0,0]
for sig in [[sigTree,wNsig,frac_sig600]]:
    print "get sig"
    for i in range(sig[0].GetEntries()):
        sig[0].GetEntry(i)
        wei=sig[0].totalweight
        sig[1][0]+=wei
        for re in [1,2,3,4]:
            if sig[0].region==re:
                sig[1][re]+=wei
    for j in range(5):
        sig[1][j]=sig[1][j]*sig[2]


wNbkgsum=[wNmctt[i]+wNmcttw[i]+wNmcttg[i]+wNmcdyjets[i]+wNmcwjets[i] for i in range(5)]
wsumt.field_names = ["Channel","Pre_selection","SR1","SR2"]
wsumt.add_row(["tt",wNmctt[0],wNmctt[1],wNmctt[2]])
wsumt.add_row(["ttw",wNmcttw[0],wNmcttw[1],wNmcttw[2]])
wsumt.add_row(["ttg",wNmcttg[0],wNmcttg[1],wNmcttg[2]])
wsumt.add_row(["zjets",wNmcdyjets[0],wNmcdyjets[1],wNmcdyjets[2]])
wsumt.add_row(["wjets",wNmcwjets[0],wNmcwjets[1],wNmcwjets[2]])
wsumt.add_row(["-","-","-","-"])
wsumt.add_row(["bkgsum",wNbkgsum[0],wNbkgsum[1],wNbkgsum[2]])
wsumt.add_row(["-","-","-","-"])
#wsumt.add_row(["sig600_375",wNsig[0],wNsig[1],wNsig[2]])
#wsumt.add_row(["-","-","-","-"])
wsumt.add_row(["data",Ndata[0],Ndata[1],Ndata[2]])
#wsumt.add_row(["diff",wNbkgsum[0]/Ndata[0]-1,wNbkgsum[1]/Ndata[1]-1,wNbkgsum[2]/Ndata[2]-1])

wsumtt.field_names = ["Channel","Pre_selection","CR1","CR2"]
wsumtt.add_row(["tt",wNmctt[0],wNmctt[3],wNmctt[4]])
wsumtt.add_row(["ttw",wNmcttw[0],wNmcttw[3],wNmcttw[4]])
wsumtt.add_row(["ttg",wNmcttg[0],wNmcttg[3],wNmcttg[4]])
wsumtt.add_row(["zjets",wNmcdyjets[0],wNmcdyjets[3],wNmcdyjets[4]])
wsumtt.add_row(["wjets",wNmcwjets[0],wNmcwjets[3],wNmcwjets[4]])
wsumtt.add_row(["-","-","-","-"])
wsumtt.add_row(["bkgsum",wNbkgsum[0],wNbkgsum[3],wNbkgsum[4]])
#wsumtt.add_row(["-","-","-","-"])
#wsumtt.add_row(["sig600_375",wNsig[0],wNsig[3],wNsig[4]])
wsumtt.add_row(["-","-","-","-"])
wsumtt.add_row(["data",Ndata[0],Ndata[3],Ndata[4]])
#wsumtt.add_row(["diff",wNbkgsum[0]/Ndata[0]-1,wNbkgsum[3]/Ndata[3]-1,wNbkgsum[4]/Ndata[4]-1])

f.write("After weight\n")
f.write("%s\n"%wsumt)
f.write("%s\n"%wsumtt)








f.close()







sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"
