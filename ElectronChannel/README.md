Electron channel
-----------------------------
--Logfile //for running record
--*python //all source functions 
--*Datasamples //10000events cloned from ggntuples, testing purpose
--*preselected //reduced file that has passed the preselection, offer input to scriptANA, file named as reduced_Elechannel_dataname/mcname/signal_vDate.root
--*selected //store the events have passed tighter cuts and SR, CR informations

--*scriptPre // script used to produce reduced file, only pre_cuts
--*scriptANA // script used the preselected as input to produce selected

--*reweight // store events that have been reweighted and ready for final plot

--*scriptPlot // using the reweighted as input to plot

--*mcjob.sh // run bkgs' script_ana command