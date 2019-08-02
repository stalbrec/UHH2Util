#!/usr/bin/env python3
from __future__ import print_function
import os,glob,sys
snippet='<In FileName="%s" Lumi="0.0"/>\n'
if(len(sys.argv)<2):
    print('Please provide config XML!')
    exit(0)

print(sys.argv[1])
inXML=open(sys.argv[1],'r+', encoding="utf-8")
dir=''

for l in inXML:
    if('OUTdir' in l or 'OutputDirectory' in l):
        dir = l.split('"')[1]
        break
datasets=[]
for l in inXML:
    if('workdir' in l):
        dir+=l.split('"')[9]
    if('<InputData Version=' in l and '<!--' not in l):
        datasets.append(l.split('"')[1])
inXML.close()
print(dir)
print(datasets)

for dataset in datasets:
    rule=dir+'/*'+dataset+'*'
    print(rule)
    files=glob.glob(rule)
    outXML=open('PreSel/'+dataset+'.xml','w')
    for file in files:
        outXML.write(snippet%file)
    outXML.close()
