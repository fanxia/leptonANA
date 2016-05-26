#!/bin/bash
# To run all the ana, first as input from selected, second as output name in 
#./run_plotskim.sh DD

if [ $# -eq 0 ]
    then
    echo "Please put the inputfiledata, for example: May 25, which use the ../selected/skim_ana_rootMay25/* as input"
    exit 1
fi

if [ $# -eq 1 ]
    then


#python skim_ana_data.py ../preselected/Output_dataSingleMu3Mar31/reduced_dataSingleMu.root dataSingleMu

#python skim_ana_mc.py ../preselected/Output_sig600_375_May10/reduced_sig600_375.root sig600_375
    if [ -d "../selected/skim_ana_root$1" ]
    then
	echo "INPUT: ../selected/skim_ana_root$1"

	python plotskim.py ../selected/skim_ana_root$1/skim_dataSingleMu.root dataSingleMu
	python plotskim.py ../selected/skim_ana_root$1/skim_sig600_375.root sig600_375


	python plotskim.py ../selected/skim_ana_root$1/skim_mcdyjets.root mcdyjets
	python plotskim.py ../selected/skim_ana_root$1/skim_mcwjets.root mcwjets
	python plotskim.py ../selected/skim_ana_root$1/skim_mctt.root mctt
	python plotskim.py ../selected/skim_ana_root$1/skim_mcttg.root mcttg
	python plotskim.py ../selected/skim_ana_root$1/skim_mcttw.root mcttw
    else
	echo "INPUT doesn't exist!"
	exit
    fi

fi

