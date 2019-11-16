import ROOT     as r
import sys, os
from multiprocessing import Pool

if len(sys.argv) == 1: raise RuntimeError("FATAL: no inputs given.")

r.gROOT.SetBatch(True)
r.gROOT.LoadMacro("./DTNtupleBaseAnalyzer.C+")
r.gROOT.LoadMacro("./DTNtupleDigiAnalyzer.C+")
r.gROOT.LoadMacro("./DTNtupleTriggerAnalyzer.C+")
r.gROOT.LoadMacro("./DTNtupleSegmentAnalyzer.C+")

def AnalyseDigiThings(runno):
    os.system("mkdir -p ./run" + str(runno) + "/digi/");
    inputFile = "../production/DTDPGNtuple_run{rn}.root".format(rn = runno)

    digiAnalysis = r.DTNtupleDigiAnalyzer(inputFile, "./run" + str(runno) + "/digi/results_digi.root");
    digiAnalysis.Loop();
    return


def AnalyseTriggerThings(runno):
    os.system("mkdir -p ./run" + str(runno) + "/trigger/");
    inputFile = "../production/DTDPGNtuple_run{rn}.root".format(rn = runno)

    triggerAnalysis = r.DTNtupleTriggerAnalyzer(inputFile, "./run" + str(runno) + "/trigger/results_trigger.root");
    triggerAnalysis.Loop();
    return


def AnalyseSegmentThings(runno):
    os.system("mkdir -p ./run" + str(runno) + "/segment/");
    inputFile = "../production/DTDPGNtuple_run{rn}.root".format(rn = runno)

    segmentAnalysis = r.DTNtupleSegmentAnalyzer(inputFile, "./run" + str(runno) + "/segment/results_segment.root");
    segmentAnalysis.PreLoop("Ph1");
    segmentAnalysis.PreLoop("Ph2");
    segmentAnalysis.Loop();
    return


def LazyOptimisation(tsk):
    runNumb, ty = tsk
    if   ty == "digi":    return AnalyseDigiThings(runNumb)
    elif ty == "trigger": return AnalyseTriggerThings(runNumb)
    elif ty == "segment": return AnalyseSegmentThings(runNumb)


if __name__ == '__main__':
    ncores = int(sys.argv[1])
    tsks = []
    if ncores <= 99999:
        print "\n> Parallelisation of run analysing with", ncores, "cores."

        for rn in [int(sys.argv[rl]) for rl in range(2, len(sys.argv))]:
            for ty in ["digi", "trigger", "segment"]:
                tsks.append( (rn, ty) )

        pool = Pool(ncores)
        pool.map(LazyOptimisation, tsks)
        pool.close()
        pool.join()
        del pool
    else:
        for rn in [int(sys.argv[rl]) for rl in range(1, len(sys.argv))]:
            for ty in ["digi", "trigger", "segment"]:
                tsks.append( (rn, ty) )

        for tsk in tsks: LazyOptimisation(tsk)
