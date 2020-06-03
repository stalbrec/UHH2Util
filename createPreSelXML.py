#!/usr/bin/env python
from __future__ import print_function
import os,glob,sys

#make sure script does not use deprecated version of readaMCatNloEntries.py from sframe_batch
for i,p in enumerate(sys.path):
    if('sframebatch' in p.lower()):
        sys.path.pop(i)

#instead add crab script path to python path in order to use its version of readaMCatNloEntries.py
sys.path.append(os.environ['CMSSW_BASE']+'/src/UHH2/scripts/crab')
from readaMCatNloEntries import *

snippet='<In FileName="%s" Lumi="0.0"/>\n'

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("inputXML",type=str, help="inputXML which will be parsed for possible root outputfiles")
args = parser.parse_args()

inXML_path=os.path.abspath(args.inputXML)
OutDir=inXML_path.replace(inXML_path.split('/')[-1],'PreSel/')
if(not os.path.exists(OutDir)):
    os.mkdir(OutDir)
inXML=open(inXML_path,'r+')
root_dir = ''
workdir = ''
datasets=[]
root_dir_var=None
for l in inXML:
    if('ENTITY' in l and 'OUTdir' in l):
        root_dir_var = l.split('"')[1]
    if('OutputDirectory' in l and '<!-' not in l):
        root_dir = l.split('"')[3]
    if('workdir' in l and 'ConfigSGE' in l):
        workdir = l.split('"')[9]
    if('<InputData Version=' in l and '<!--' not in l):
        datasets.append(l.split('"')[1])
print('root_dir_var',root_dir_var)
if(root_dir_var):
    root_dir = root_dir_var
root_dir+=workdir
print('root_dir',root_dir)
inXML.close()
for dataset in datasets:
    rule=root_dir+'/*'+dataset+'*'
    print(rule)
    files=glob.glob(rule)
    outXML=open(OutDir+dataset+'.xml','w')
    for file in files:
        outXML.write(snippet%file)
    outXML.close()
    readEntries(4,[OutDir+dataset+'.xml'],True)
