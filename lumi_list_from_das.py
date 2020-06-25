from __future__ import print_function
import sys,csv,time
import FWCore.PythonUtilities.LumiList as LumiList
import requests,re,os

sys.path.append("/afs/desy.de/user/a/albrechs/xxl/af-cms/UHH2/10_2_v2/CMSSW_10_2_16/src/UHH2/scripts/crab")

from DasQuery import autocomplete_Datasets
from Utilities.General.cmssw_das_client import get_data

def get_lumi_lists(inputDataset="/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic*/MINIAODSIM"):
    inputDatasets = autocomplete_Datasets([inputDataset])
    result={}
    for dataset in inputDatasets:
        print(dataset)
        json_dict = get_data(host = 'https://cmsweb.cern.ch',query="lumi file dataset="+dataset,idx=0,limit=0,threshold=300)
        lumi_list = LumiList.LumiList()
        try:
            n_files = len(json_dict['data'])
            for i,file_info in enumerate(json_dict['data']):
                if(i>n_files):
                    break
                lumi_list += LumiList.LumiList(runsAndLumis={'1':file_info['lumi'][0]['number']})
        except:
            print('Did not find lumis for %s'%dataset)
        result.update({dataset:lumi_list})    
    return result

def get_ntuple_info(branch,year,name):
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/{doc_id}/export?format=csv&id=%s{doc_id}&gid={sheet_id}"

    doc_ids = {
        "RunII_102X_v2":"1wqwhKtALjZcejfTXgWE5dPE3bpEo0VQmq52SGE4oab4",
        "RunII_102X_v1":"19LSGDYDcXwhwowhub_-dIHpalkSmkYABOnRDSRnj38U"
    }
    sheet_ids = {
        "bkg":{
            "2016":"1477167626",
            "2017":"1396292818",
            "2018":"0"
        },
        "sig":{
            "2016":"822571647",
            "2017":"571605227",
            "2018":"1537748452"
        },
        "data":{
            "2016":"2053028482",
            "2017":"637267164",
            "2018":"712721274"
        }
    }
    year_match = re.search(r'201[678][A-Z]*', year)
    year = "2017" if not year_match else year_match.group()
    ntuple_info=[]
    for sample_type in ['bkg','sig']:
        csv_filename = branch+'_'+year+'_'+sample_type+'.csv'
        if(not os.path.isfile(csv_filename)):            
            print('trying to find sample in',sample_type,'spreadsheet')
            url = spreadsheet_url.format(doc_id=doc_ids[branch],sheet_id=sheet_ids[sample_type][year])
            print('downloading spreadsheet:',url)
            r = requests.get(url=url)
            open(csv_filename, 'wb').write(r.content)

        with open(csv_filename,'rb') as csvfile:
            setreader=csv.DictReader(csvfile)
            for row in setreader:
                das = row['Sample Name']
                if(das is None or das == ""):
                    continue
                if(name in das):
                    return {'lumi':row["Lumi [pb^-1]"],'name':row["Short name"],'das':das}

if(__name__=="__main__"):
    affected_dirs={}
    for i in open("affected_dirs.txt","r"):
        info = i.replace("\n","").split("/")
        branch = info[0]
        year = info[1]
        name = info[2]
        #skip these branches and handle manually
        if branch == 'RunII_80X_v3' or '106X' in branch:
            continue
        if branch not in affected_dirs:
            affected_dirs.update({branch:{}})
        if year not in affected_dirs[branch]:
            affected_dirs[branch].update({year:[]})
        affected_dirs[branch][year].append(name)

    for branch in affected_dirs.keys():
        print(branch)
        for year in affected_dirs[branch]:
            print(year)
            for name in affected_dirs[branch][year]:
                print(name)
                ntuple_info = get_ntuple_info(branch,year,name)
                outdir = 'LumiLists/'+branch+'/'+year+'/'
                if(not os.path.exists(outdir)):
                    os.makedirs(outdir)
                if(ntuple_info is None):
                    print("Did not find entry in spreadsheet for",name,'. Skipping it')
                    continue
                das_string = ntuple_info["das"]
                if(das_string[0] != "/"):
                    das_string = "/"+das_string
                lumi_lists = get_lumi_lists(das_string)
                for das,ll in lumi_lists.items():
                    file_name = name + ("_ext" if (len(lumi_lists.keys())>1 and "_ext" in das) else "")+'.json'
                    ll.writeJSON(fileName=outdir+file_name)
