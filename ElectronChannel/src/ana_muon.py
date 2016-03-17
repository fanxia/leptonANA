# include functions for muon selection
import os
import sys
import ROOT


def muPFRelCombIso(pt,chIso,neuIso,phoIso,puIso):

    result= (chIso+max(0.,neuIso+phoIso-0.5*puIso))/pt

    return result
