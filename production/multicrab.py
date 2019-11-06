import sys
from multiprocessing import Pool

#inputDataset = "/Cosmics/Commissioning2019-v1/RAW"
inputDataset = "/MiniDaq/Commissioning2019-v1/RAW"

# These are the cfg parameters used to configure the
# dtDpgNtuples_slicetest_cfg.py configuration file
configParams = ["ntupleName=DTDPGNtuple.root","nEvents=5000"]
# E.g. use dedicated tTrigs
# configParams = ['ntupleName=DTDPGNtuple.root', \
#                 'tTrigFile=calib/TTrigDB_cosmics_ttrig.db']

# These are the additional input files (e.g. sqlite .db)
# needed by dtDpgNtuples_slicetest_cfg.py to run
inputFiles = []
# E.g. use dedicated tTrigs
# inputFiles = ['./calib/TTrigDB_cosmics_ttrig.db']


def SendCrabJob(runno):
    from CRABAPI.RawCommand       import crabCommand
    from multiprocessing          import Process
    from CRABClient.UserUtilities import config
    print "\n> Sending CRAB job for run number:", runno
    config = config()

    def submit(config):
        res = crabCommand('submit', config = config)

    config.General.workArea        = 'crab_jobs'
    config.General.requestName     = 'DTDPGNtuples_SliceTest_run' + str(runno)
    config.General.transferOutputs = True

    config.JobType.pluginName  = 'Analysis'
    config.JobType.psetName    = 'dtDpgNtuples_slicetest_cfg.py'

    config.JobType.pyCfgParams = configParams
    config.JobType.inputFiles  = inputFiles
    config.JobType.maxMemoryMB = 4000

    config.Data.inputDataset   = inputDataset
    config.Data.splitting      = 'Automatic'
    #config.Data.splitting      = 'LumiBased'
    #config.Data.unitsPerJob    = 10
    config.Data.runRange       = str(runno)
    config.Data.inputDBS       = 'https://cmsweb.cern.ch/dbs/prod/global/DBSReader/'
    config.Data.outLFNDirBase  = '/store/group/dpg_dt/comm_dt/commissioning_2019_data/crab/'

    config.Site.storageSite = 'T2_CH_CERN'
    config.Site.blacklist   = ['T2_BR_SPRACE', 'T2_US_Wisconsin', 'T1_RU_JINR', 'T2_RU_JINR', 'T2_EE_Estonia']

    #p = Process(target=submit, args=(config,))
    #p.start()
    #p.join()
    submit(config)
    return



if __name__ == '__main__':

    if len(sys.argv) == 1: raise RuntimeError("FATAL: no runs nor cores provided.")

    ncores = int(sys.argv[1])

    if ncores <= 99999:
        print "\n> Parallelisation of CRAB job sending with", ncores
        pool = Pool(ncores)
        pool.map(SendCrabJob, [int(sys.argv[rl]) for rl in range(2, len(sys.argv))])
        pool.close()
        pool.join()
        del pool
    else:
        for rn in sys.argv:
            if rn == sys.argv[0]: continue
            else:                 SendCrabJob(int(rn))

