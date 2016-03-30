# include functions for muon selection
import os
import sys
import ROOT


def muPFRelCombIso(pt,chIso,neuIso,phoIso,puIso):

    result= (chIso+max(0.,neuIso+phoIso-0.5*puIso))/pt

    return result

def good_LooseMu(pt,eta,loosid,iso):
    
    if pt>10 and abs(eta)<2.5 and loosid and iso<0.25:

        return True

def goog_TightMu(pt,eta,tightid,iso):
    if pt>30 and abs(eta)<2.1 and tightid and iso<0.15:
        return True
