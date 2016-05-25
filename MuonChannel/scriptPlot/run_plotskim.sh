#!/bin/bash
# To run all the ana, first as input from selected, second as output name in 

#python skim_ana_data.py ../preselected/Output_dataSingleMu3Mar31/reduced_dataSingleMu.root dataSingleMu

#python skim_ana_mc.py ../preselected/Output_sig600_375_May10/reduced_sig600_375.root sig600_375

python plotskim.py ../selected/skim_ana_rootDD/skim_dataSingleMu.root dataSingleMu

python plotskim.py ../selected/skim_ana_rootDD/skim_sig600_375.root sig600_375


python plotskim.py ../selected/skim_ana_rootDD/skim_mcdyjets.root mcdyjets
python plotskim.py ../selected/skim_ana_rootDD/skim_mcwjets.root mcwjets
python plotskim.py ../selected/skim_ana_rootDD/skim_mctt.root mctt
python plotskim.py ../selected/skim_ana_rootDD/skim_mcttg.root mcttg
python plotskim.py ../selected/skim_ana_rootDD/skim_mcttw.root mcttw

