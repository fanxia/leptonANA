# include functions for fake photon selection
import os
import sys
import ROOT


def good_fake(rho,et,eta,eleveto,HoverE,sigmaieie,chhadIso,NeuIso,PhoIso):

    if et<20 or abs(eta)>1.4442 or eleveto==0 or HoverE>0.05:
        return False


    if abs(eta)<1.0:
        eaNeu=0.0599
        eaPho=0.1271
    elif abs(eta)<1.479:
        eaNeu=0.0819
        eaPho=0.1101

    NeuIso_corrected=max(NeuIso-rho*eaNeu,0.0)
    PhoIso_corrected=max(PhoIso-rho*eaPho,0.0)

    if (1.92+0.014*et+0.000019*et**2)<NeuIso_corrected or (0.81+0.0053*et)<PhoIso_corrected:
        return False

    if sigmaieie>1.0102 or chhadIso>3.32:
        return True
    else:
        return False
