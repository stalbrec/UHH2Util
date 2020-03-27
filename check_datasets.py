from __future__ import print_function
import sys,csv,time

# sys.path.append("/afs/desy.de/user/a/albrechs/xxl/af-cms/UHH2/10_2/CMSSW_10_2_10/src/UHH2/scripts/crab")
sys.path.append("/afs/desy.de/user/a/albrechs/xxl/af-cms/UHH2/10_2_v2/CMSSW_10_2_16/src/UHH2/scripts/crab")

from DasQuery import autocomplete_Datasets
from Utilities.General.cmssw_das_client import get_data

def check_datasets_for_buggyPU(inputDatasets=[]):
    inputDatasets = autocomplete_Datasets(inputDatasets)
    datasets = []
    print('checking these datasets for buggy PU (look up "PU2017" in parents DAS string)')
    for dataset in inputDatasets:
        print(dataset)
        json_dict = get_data(host = 'https://cmsweb.cern.ch',query="parent dataset="+dataset,idx=0,limit=0,threshold=300)
        try:
            parent = json_dict['data'][0]['parent'][0]['name']

            datasets.append((dataset,parent))
        except:
            print('Did not find parent for %s'%dataset)

    print('The following datasets have buggy PU:')
    buggy_datasets=[]
    for dataset,parent in datasets:        
        if('PU2017' not in parent):
            print(dataset)
            buggy_datasets.append(dataset)
    return buggy_datasets

def get_n_events(inputDatasets=[]):
    inputDatasets = autocomplete_Datasets(inputDatasets)
    DatasetsNevents = []
    
    for dataset in inputDatasets:
        # json_dict = get_data(host = 'https://cmsweb.cern.ch',query="parent dataset="+dataset,idx=0,limit=0,threshold=300)
        json_dict = get_data(host = 'https://cmsweb.cern.ch',query="file dataset=%s"%dataset,idx=0,limit=0,threshold=300)
        nevents = 0.
        try:
            files = json_dict['data'][0]['file']
            for f in json_dict['data']:
                nevents += float(f['file'][0]['nevents'])
        except:
            print('Did not find files for %s'%dataset)
        print(dataset,'\t\t',nevents)
        DatasetsNevents.append(nevents)
    return DatasetsNevents

if(__name__ == "__main__"):
    inputDatasets =[
        #'/QCD_Pt_15to30_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14*/MINIAODSIM',
        # '/QCD_Pt_30to50_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14*/MINIAODSIM',
        # '/QCD_Pt_50to80_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14*/MINIAODSIM',
        # '/QCD_Pt_80to120_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14*/MINIAODSIM',
         # '/QCD_Pt_120to170_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
        # '/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14*/MINIAODSIM',
        # '/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14*/MINIAODSIM',
        # '/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14*/MINIAODSIM',
        # '/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14*/MINIAODSIM',
        # '/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14*/MINIAODSIM',
        # '/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14*/MINIAODSIM',
        # '/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14*/MINIAODSIM',
        # '/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
        # '/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
        # '/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14*/MINIAODSIM'

        
    '/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14*/MINIAODSIM',
    '/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14*/MINIAODSIM',
    '/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14*/MINIAODSIM',
    '/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14*/MINIAODSIM',
    '/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14*/MINIAODSIM',
    '/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14*/MINIAODSIM',
    '/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14*/MINIAODSIM',
    '/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    '/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    '/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14*/MINIAODSIM'
    ]
    # print(check_datasets_for_buggyPU(input_datasets))
    get_n_events(inputDatasets)
    exit(0)
    datasets_csv = "102X_v1_2017_Bkg.csv"
    datasets_url = "https://docs.google.com/spreadsheets/d/19LSGDYDcXwhwowhub_-dIHpalkSmkYABOnRDSRnj38U/export?format=csv&id=19LSGDYDcXwhwowhub_-dIHpalkSmkYABOnRDSRnj38U&gid=1396292818"

    # datasets_csv = "102X_v2_2017_Bkg.csv"
    # datasets_url = "https://docs.google.com/spreadsheets/d/1wqwhKtALjZcejfTXgWE5dPE3bpEo0VQmq52SGE4oab4/export?format=csv&id=1wqwhKtALjZcejfTXgWE5dPE3bpEo0VQmq52SGE4oab4&gid=1396292818"
    
    
    import requests as rs
    res=rs.get(url=datasets_url)
    open(datasets_csv, 'wb').write(res.content)
    
    n_samples = 0
    n_buggy_samples = 0
    with open(datasets_csv,'rb') as csvfile:
        setreader=csv.DictReader(csvfile)

        csv_outfile =  open(datasets_csv.split('.')[0]+'_buggyPU.csv','wb')
        csvwriter=csv.DictWriter(csv_outfile,fieldnames=['DAS','short_name'])
        csvwriter.writeheader()
        datasets_outfile =  open(datasets_csv.split('.')[0]+'_buggyPU_das.txt','wb')
        shortnames_outfile = open(datasets_csv.split('.')[0]+'_buggyPU_short_name.txt','wb')

        for row in setreader:
            sample_name = row['Sample Name'] if 'Sample Name' in row else ''            
            short_name = row['Short name'] if 'Short name' in row else ''
            if(row['Sample Name'] is ''):
                continue
            print('checking',sample_name)
            n_samples += 1
            buggy_samples = check_datasets_for_buggyPU([sample_name])
            for sample in buggy_samples:
                print('found buggy PU:',sample)
                n_buggy_samples += 1
                csvwriter.writerow({'DAS':sample,'short_name':short_name})
                datasets_outfile.write(sample+'\n')
                shortnames_outfile.write(short_name+'\n')
            time.sleep(5)
    print('in %s there are %i samples'%(datasets_csv.split('.')[0],n_samples))
    
#/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14*/MINIAODSIM -> base + ext (base buggy)
#/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v3/MINIAODSIM -> ok
#/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v3/MINIAODSIM ->
