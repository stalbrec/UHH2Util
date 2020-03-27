import sys,csv,time


# datasets_csv = "102X_v1_2017_Bkg.csv"
# datasets_url = "https://docs.google.com/spreadsheets/d/19LSGDYDcXwhwowhub_-dIHpalkSmkYABOnRDSRnj38U/export?format=csv&id=19LSGDYDcXwhwowhub_-dIHpalkSmkYABOnRDSRnj38U&gid=1396292818"

datasets_csv = "102X_v2_2017_Bkg.csv"
datasets_url = "https://docs.google.com/spreadsheets/d/1wqwhKtALjZcejfTXgWE5dPE3bpEo0VQmq52SGE4oab4/export?format=csv&id=1wqwhKtALjZcejfTXgWE5dPE3bpEo0VQmq52SGE4oab4&gid=1396292818"

UHH2_DatasetsPath = "/afs/desy.de/user/a/albrechs/xxl/af-cms/UHH2/10_2/CMSSW_10_2_10/src/UHH2/common/UHH2-datasets/RunII_102X_v2/2017/QCD/"

unwanted_strings = ["_TuneCP5_13TeV_pythia8_Fall17","_v1","_v2"]

def modify_name(name):
    modified_name = name
    for string in unwanted_strings:
        modified_name = modified_name.replace(string,"")
    return modified_name

def print_header(short_name):
    xml_path = UHH2_DatasetsPath+short_name+'.xml'
    print('<!ENTITY %s SYSTEM "%s">'%(modify_name(short_name),xml_path))

def print_xml_elem(sample):
    print('<InputData Version="MC_%s_2017v2" Lumi="%s" Type="MC" NEventsMax="-1" Cacheable="False">'%(modify_name(sample['name'])+('_buggyPU' if sample['buggyPU'] else ''),sample['lumi']))
    print('&%s;'%modify_name(sample['name']))
    print('<InputTree Name="AnalysisTree"/>')
    print('<OutputTree Name="AnalysisTree"/>')
    print('</InputData>')
          
das_strings = [
    '/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    '/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM',
    '/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    '/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v3/MINIAODSIM',
    '/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    '/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v3/MINIAODSIM',
    '/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    '/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM',
    '/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    '/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM',
    '/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    '/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM',
    '/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    '/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v3/MINIAODSIM',
    '/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    '/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    '/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    '/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM'
]

import requests as rs
res=rs.get(url=datasets_url)
open(datasets_csv, 'wb').write(res.content)

sample_info = {}

with open(datasets_csv,'rb') as csvfile:
    setreader=csv.DictReader(csvfile)
    for row in setreader:
        if(len(sample_info) == len(das_strings)):
            break
        das = row['Sample Name'] 
        if(das in das_strings):
            sample_info.update({das:{'lumi':row["Lumi [pb^-1]"],'name':row["Short name"],'buggyPU':'buggy' in row['FurtherInfo'].lower()}})
print('HEADER')


for sample in das_strings:
    print_header(sample_info[sample]['name'])
print('BODY')
for sample in das_strings:
    print_xml_elem(sample_info[sample])

