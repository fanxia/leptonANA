#!/bin/bash
# To run all the mc_ana, first as input, second as output name in selected/

python mc_ana.py ../preselected/Output_mcdyjets_Mar29/reduced_mcdyjetstoll.root mcdyjetstoll
python mc_ana.py ../preselected/Output_mcwjets_Mar29/reduced_mcwjets.root mcwjets

python mc_ana.py ../preselected/Output_mctt_Mar29/reduced_mctt.root mctt
python mc_ana.py ../preselected/Output_mcttg_Mar29/reduced_mcttg.root mcttg
python mc_ana.py ../preselected/Output_mcttw_Mar29/reduced_mcttw.root mcttw