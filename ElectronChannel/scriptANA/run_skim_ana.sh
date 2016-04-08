#!/bin/bash
# To run all the ana, first as input, second as output name in selected/

python skim_ana_data.py ../preselected/Output_dataSingleEleMar29/reduced_dataSingleEle.root dataSingleEle


python skim_ana_mc.py ../preselected/Output_mcdyjets_Mar29/reduced_mcdyjetstoll.root mcdyjets
python skim_ana_mc.py ../preselected/Output_mcwjets_Mar29/reduced_mcwjets.root mcwjets

python skim_ana_mc.py ../preselected/Output_mctt_Mar29/reduced_mctt.root mctt
python skim_ana_mc.py ../preselected/Output_mcttg_Mar29/reduced_mcttg.root mcttg
python skim_ana_mc.py ../preselected/Output_mcttw_Mar29/reduced_mcttw.root mcttw


