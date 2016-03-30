# include functions for photon selection
import os
import sys
import ROOT


def good_LoosePho(et,eta,eleveto):

    if et>20 and abs(eta)<1.4442 and eleveto==1:
        return True

