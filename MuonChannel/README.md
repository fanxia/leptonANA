#Readme file:
#2016-4-7 fanxia
#update:2016-4-15



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
       *April08    dirs get by skim_ana.py
       *Mar31 and ttgApril01       dirs get by mc_ana.py
       *data_Apr12  skimmed root get by skim_ana_data.py
       *mcxx_Apr15 skimmed root get by skim_ana_mc.py with the pu weight applied
/scriptPlot
       nVtxplot.py        a small script to plot nVtx pdf, normalized independently, now use mc_ana.py output as input, can modify for skimmed tree
       sumtable4skim.py   to get the summary table, now using the skimmed as input, pu weight has been applied
       combplot.py        to process the output of mc_ana.py(trees for different regions), complete branches, but too much.
       combskim.py        to process the output ot skim_ana.py using the histograms directly, only works for lumi kind scale, not for scale event by event
       skim_combplot.py   to process the output tree of skim_ana.py, using branch info and fill. Can work for scale event by event. Might be the best method for future.