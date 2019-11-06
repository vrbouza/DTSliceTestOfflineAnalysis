#!/bin/sh
echo 'START---------------'

CMSSW_FOLDER=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DT/OfflineCode/SliceTest/v7/CMSSW_10_6_0/
CRAB_CONFIG_SCRIPT=/cvmfs/cms.cern.ch/crab3/crab.sh
source /afs/cern.ch/cms/cmsset_default.sh

cd {directory}

cd $CMSSW_FOLDER/src
echo "[$0]: Configuring CMSSW from directory $CMSSW_FOLDER/src"
cmsenv
cd -

echo "[$0]: Configuring CRAB using $CRAB_CONFIG_SCRIPT"
. $CRAB_CONFIG_SCRIPT

cmsRun dtDpgNtuples_slicetest_cfg.py runNumber={runno}  &> log1_{runno}

size=0
if test -f "DTDPGNtuple_run{runno}.root"; then
    size=$(stat -c%s DTDPGNtuple_run{runno}.root)
fi 

if ((size<1000)) ; then 
    echo "Ntuple production failed, retrying with .dat files"  &> log2_{runno}
    cmsRun dtDpgNtuples_slicetest_cfg.py runNumber={runno} nEvents=5000 runOnDat=True inputFolderCentral=/eos/cms/store/t0streamer/Minidaq/A/  &> log3_{runno}
fi


python condor/report.py {runno}
