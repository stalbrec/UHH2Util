from __future__ import print_function
import ROOT,uproot

xml_files=[
     'MC_QCD_Pt_1000to1400_2017v2_46.xml',
     'MC_QCD_Pt_1000to1400_2017v2_48.xml',
     'MC_QCD_Pt_1000to1400_2017v2_51.xml',
     'MC_QCD_Pt_1000to1400_2017v2_52.xml',
     'MC_QCD_Pt_1000to1400_2017v2_54.xml',
     'MC_QCD_Pt_1000to1400_2017v2_57.xml',
     'MC_QCD_Pt_1000to1400_2017v2_59.xml'
]
path = '/nfs/dust/cms/user/albrechs/UHH2/10_2_afs_installation/DazsleWorkdir/workdir_WMassDDTMaps/'
for xml in xml_files:
    print('processing xml:', xml)
    root_files=[]
    with open(path+xml) as xml_file:
        for l in xml_file:
            if ".root" in l and 'pnfs' in l:
                root_files.append(l.split('"')[1])
        xml_file.close()
        for root_file in root_files:
            f = uproot.open(root_file)
            tree = f['AnalysisTree']
            try:
                branch = tree['PFParticles.m_pt']
                array = branch.array()
            except:
                print('root file',root_file,'is broken')
