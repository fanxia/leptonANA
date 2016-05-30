#Readme file:
#2016-4-7 fanxia
#update:2016-5-30



/scriptPre         script for pre selection, output store at /preselected

/scriptANA         
      mc_ana.py    original ana selection,get trees of pre, sr1,sr2,cr1,cr2. and lots plots 
                   use /preselected/* as input, output store at /selected
      dataSingleMu_ana.py        same as mc_ana.py now
      run_mc_ana.sh     shell script used to run all the bkgs mc 


      skim_ana_data.py   make ana selection,get a root file with EventTree store only selected events with user defined branches,and lot of histograms(used for plot directly)
      skim_ana_mc.py     diff from data: need to contain the weight branch, now only has the puweight factor inside. make ana selection,get a root file with EventTree store only selected events with user defined branches,and lot of histograms(used for plot directly)
      run_skim_ana.sh    shell script used to run all the bkgs and data by skim_ana_data/mc.py

/selected
       *skim_ana_rootDD     dir contains the skimmed root files for all datasets, ls inside to look at the datasets
       *April08    dirs get by skim_ana.py
       *Mar31 and ttgApril01       dirs get by mc_ana.py
       *data_Apr12  skimmed root get by skim_ana_data.py
       *mcxx_Apr15 skimmed root get by skim_ana_mc.py with the pu weight applied

/scriptPlot
       nVtxplot.py        a small script to plot nVtx pdf, normalized independently, now use mc_ana.py output as input, can modify for skimmed tree
       sumtable4skim.py   to get the summary table, now using the skimmed as input, pu weight has been applied
       combplot.py        to process the output of mc_ana.py(trees for different regions), complete branches, but too much.

       (deleted, changed algorithm)skim_combplot.py   to process the output tree of skim_ana.py, using branch info and fill. Can work for scale event by event. Might be the best method for future.

       plotskim.py        to process the output of skim_ana_*.py, produce the historgrams and stored in outplotDD, using run_plotskim.sh to run it for every datasets
       combskim.py        to process the outplotDD using their histograms directly, only works for lumi kind scale, not for scale event by event

/muonscalefac
	add scale factor information for muon, include tight id, tight iso, and trigger, for 7_4_X



# WORK FLOW

1 using scriptPre to produce preselected, ggntuples as input, output in preselected

2 using scriptANA/run_skim_ana.sh which calls the skim_ana_mc/data.py to produce selected, take 1 results as input,output in selected/skim_ana_rootDD

3 using scriptPlot/run_plotskim.sh which calls the plotskim.py to Fill histograms for all datasets, 2results as input, output in outplot_DD

4 run scriptPlot/combskim.py to combine all the datasets and make plots 