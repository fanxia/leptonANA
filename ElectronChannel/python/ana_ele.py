# include functions for ele selection
import os
import sys
import ROOT



def good_TightEle(pt,eta,eleid):
    
    if pt>30 and abs(eta)<2.5 and (eleid>>3&1)==1:

        return True

def good_LooseEle(pt,eta,eleid):
    
    if pt>10 and abs(eta)<2.5 and (eleid>>1&1)==1:

        return True
