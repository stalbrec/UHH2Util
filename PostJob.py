#!/usr/bin/env python
import os,glob
def handle_command(command,debug=False):
    print(command)
    if not debug:
        os.system(command)


macroDir='/afs/desy.de/user/a/albrechs/xxl/af-cms/UHH2/10_2/CMSSW_10_2_10/src/UHH2/JetMass/macros'

INdir='/nfs/dust/cms/user/albrechs/UHH2/JetMassOutput/WMass/'
OUTdir='/afs/desy.de/user/a/albrechs/xxl/af-cms/UHH2/10_2/CMSSW_10_2_10/src/UHH2/JetMass/Histograms/W/'

#2016
# SIGNALS={
#   'WMatched':'uhh2.AnalysisModuleRunner.MC.MC_WJetsToQQ_WMatched_2016v3.root'
# }
# BACKGROUNDS={
#   'QCD':'uhh2.AnalysisModuleRunner.MC.MC_QCD_HT*',
#   'WUnmatched':'uhh2.AnalysisModuleRunner.MC.MC_WJetsToQQ_WUnmatched_2016v3.root'
# }
# DATA={
#     'Data':'uhh2.AnalysisModuleRunner.DATA.DATA_JetHTRun2016v3*'
# }

#2017
SIGNALS={
  'WMatched':'uhh2.AnalysisModuleRunner.MC.MC_WJetsToQQ_*_WMatched_2017v2.root'
}


BACKGROUNDS={
  'QCD':'uhh2.AnalysisModuleRunner.MC.MC_QCD_Pt*',
  'WUnmatched':'uhh2.AnalysisModuleRunner.MC.MC_WJetsToQQ_*_WUnmatched_2017v2.root'
}
DATA={
    'Data':'uhh2.AnalysisModuleRunner.DATA.DATA_JetHTRun2017v2*'
}


ALL_MC=SIGNALS.copy()
ALL_MC.update(BACKGROUNDS)

#merge binned background samples and rename others
for sampleName,name in ALL_MC.items():
    if(len(glob.glob(INdir+name))>1):
        handle_command('hadd -f -T %s.root %s'%(OUTdir+sampleName,INdir+name))
    else:
        handle_command('cp %s %s.root'%(INdir+name,OUTdir+sampleName))

#create PseudoData from all MC
pseudoData_command='hadd -f -T %sPseudo.root'%OUTdir
for sampleName in ALL_MC.keys():
    pseudoData_command+=' %s.root'%(OUTdir+sampleName)
handle_command(pseudoData_command)

#merge Data Samples
for sampleName,name in DATA.items():
    handle_command('hadd -f -T %s.root %s'%(OUTdir+sampleName,INdir+name))
