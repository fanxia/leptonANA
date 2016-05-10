#!/bin/bash
# To run all the ana, first as input, second as output name in selected/

#python skim_ana_data.py ../preselected/Output_dataSingleMu3Mar31/reduced_dataSingleMu.root dataSingleMu

#python skim_ana_mc.py ../preselected/Output_sig600_375_May10/reduced_sig600_375.root sig600_375


python skim_ana_mc.py ../preselected/Output_mcdyjets_Mar31/reduced_mcdyjets.root mcdyjets
python skim_ana_mc.py ../preselected/Output_mcwjets_Mar31/reduced_mcwjets.root mcwjets

python skim_ana_mc.py ../preselected/Output_mctt_Mar31/reduced_mctt.root mctt
python skim_ana_mc.py ../preselected/Output_mcttg_Apr01/reduced_mcttg.root mcttg
python skim_ana_mc.py ../preselected/Output_mcttw_Mar31/reduced_mcttw.root mcttw
