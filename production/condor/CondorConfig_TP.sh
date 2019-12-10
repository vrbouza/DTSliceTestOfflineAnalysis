#!/bin/sh
echo 'START---------------'

cd {directory}
cd ..
source configForSliceTestAnalysis.sh

cd {directory}

cmsRun dtDpgNtuples_slicetest_cfg.py runNumber={runno} nEvents=5000

size=0
if test -f "DTDPGNtuple_run{runno}.root"; then
    size=$(stat -c%s DTDPGNtuple_run{runno}.root)
fi

if ((size<1000)) ; then
  echo "Ntuple production failed, retrying with .dat files"
  cmsRun dtDpgNtuples_slicetest_cfg.py runNumber={runno} nEvents=5000 runOnDat=True inputFolderCentral=/eos/cms/store/t0streamer/Minidaq/A/
fi

# python condor/report.py {runno}
