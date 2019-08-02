#!/usr/bin/env python
import os,glob
def handle_command(command,debug=False):
    print(command)
    if not debug:
        os.system(command)

INdir='/nfs/dust/cms/user/albrechs/SingleJetTrees/WMassPreSel/'
OUTdir='/afs/desy.de/user/a/albrechs/xxl/af-cms/UHH2/10_2/CMSSW_10_2_10/src/UHH2/JetMass/Histograms/W/'
SIGNALS={
  'WMatched':'uhh2.AnalysisModuleRunner.MC.MC_WJetsToQQ_WMatched_2016v3.root'
}
BACKGROUNDS={
  'QCD':'uhh2.AnalysisModuleRunner.MC.MC_QCD_HT*',
  'WUnmatched':'uhh2.AnalysisModuleRunner.MC.MC_WJetsToQQ_WUnmatched_2016v3.root'
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

#add all Backgrounds for ddt TH3D Histograms
h3_command='hadd -f -T %s/N2_v_mSD_v_pT.root'%OUTdir
for bgName in BACKGROUNDS.keys():
    h3_command+=' %s.root'%(OUTdir+bgName)
handle_command(h3_command)
