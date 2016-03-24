# include functions for jet selection
import os
import sys
import ROOT


def good_LooseJet(pt,eta,loosid):
    
    if pt>30 and abs(eta)<2.4 and loosid:

        return True
