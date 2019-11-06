import os, sys

def mkdir (directory) :
    if not os.path.exists(directory):
        os.makedirs(directory)

def LaunchCondorJob(runno):
    print "\nSubmitting job for run number", runno, "to lxplus\' HTCondor cluster."
    template = open('condor/configForSliceTestAnalysis.sh').read()
    exect = template.format(directory=os.getcwd(),runno=runno)
    mkdir('exec')
    f = open('exec/exec_%s.sh'%runno ,'w')
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


for rn in sys.argv:
    if rn == sys.argv[0]: continue
    else:                 LaunchCondorJob(int(rn))
