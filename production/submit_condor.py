import os, sys
from multiprocessing import Pool

isTP = True
ConfigPath = 'condor/CondorConfig_TP.sh' if isTP else 'condor/CondorConfig_Cosmics.sh'


def mkdir(directory) :
    if not os.path.exists(directory):
        os.makedirs(directory)


def LaunchCondorJob(runno):
    print "# Submitting job for run number", runno, "to lxplus\' HTCondor cluster."

    template = open(ConfigPath).read()
    exect    = template.format(directory = os.getcwd(), runno = runno)
    mkdir('exec')

    f = open('exec/exec_%s.sh'%runno,'w')
    f.write(exect)
    f.close()

    mkdir('submit')
    mkdir('logs')
    f = open('submit/submit_%s.sub'%runno, 'w')
    f.write( "executable         = exec/exec_%s.sh\n"%runno)
    f.write( "output             = logs/$(ClusterId).$(ProcId).out\n")
    f.write( "error              = logs/$(ClusterId).$(ProcId).error\n")
    f.write( "log                = logs/$(ClusterId).log\n")
    f.write( "use_x509userproxy  = true\n")
    f.write('+JobFlavour = "tomorrow"\n' )
    #f.write('+JobFlavour = "workday"\n' )
    f.write("queue \n")
    f.close()
    os.system('condor_submit submit/submit_%s.sub'%runno)
    return


if __name__ == '__main__':
    ncores = int(sys.argv[1])
    tsks = []
    if ncores <= 99999:
        print "\n> Parallelisation of run analysing with", ncores, "cores."

        for rn in [int(sys.argv[rl]) for rl in range(2, len(sys.argv))]:
            tsks.append( int(rn) )

        print "> Beginning submission..."
        pool = Pool(ncores)
        pool.map(LaunchCondorJob, tsks)
        pool.close()
        pool.join()
        del pool
    else:
        for rn in [int(sys.argv[rl]) for rl in range(1, len(sys.argv))]:
            tsks.append( int(rn) )

        print "\n> Beginning submission..."
        for tsk in tsks: LaunchCondorJob(tsk)
