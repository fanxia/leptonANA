#!/bin/python

# This script is used to calculate the btag weight on event based

from ROOT import *
import ROOT
import os
import sys
from leptonANA.ElectronChannel.ana_jet import *

#jet=[btagged,flavor,btageff,btagsf]

def BTAGweight(jets):
    Pmc1=1.0
    Pmc2=1.0
    Pdata1=1.0
    Pdata2=1.0
    

    for jet in jets:
        
        btagged=jet[0]
        flavor=jet[1]
        btageff=jet[2]
        btagsf=jet[3]

        if btageff==0.0 or btageff==1.0:continue

        Pmc2*=(1-btageff)
        Pdata2*=(1-btageff*btagsf)

        if btagged: 
            Pmc1*=btageff
            Pdata1*=btageff*btagsf
        else: 
            Pmc1*=(1-btageff)
            Pdata1*=(1-btageff*btagsf)

    weight1=Pdata1/Pmc1
#    print weight1

    if Pmc2==1.0: weight2=1
    else:
        weight2=(1.0-Pdata2)/(1.0-Pmc2)

    return weight2
