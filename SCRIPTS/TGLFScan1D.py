# this script is used to scan the Para of TGLF
mode=root['SETTINGS']['PHYSICS']['mode']
if mode=='lin':
    root['SCRIPTS']['subscan_lin.py'].run()
    case_tag=root['SETTINGS']['PHYSICS']['case_tag']
    for item in root['Cases'][case_tag].keys():
        item_temp=item.split('~')
        if not  root['OUTPUTS'].has_key(item_temp[0]):
            root['OUTPUTS'][item_temp[0]]=OMFITtree()
        if not  root['OUTPUTS'][item_temp[0]].has_key(item_temp[1]):
            root['OUTPUTS'][item_temp[0]][item_temp[1]]=OMFITtree()
        if not root['OUTPUTS'][item_temp[0]][item_temp[1]].has_key('lin'):
            root['OUTPUTS'][item_temp[0]][item_temp[1]]['lin']=OMFITtree()
        root['OUTPUTS'][item_temp[0]][item_temp[1]]['lin'][item_temp[3]]=OMFITtree()
        for files in root['Cases'][case_tag][item]:
            root['OUTPUTS'][item_temp[0]][item_temp[1]]['lin'][item_temp[3]][files]=root['Cases'][case_tag][item][files] 
else:
    root['SCRIPTS']['subscan_nonlin.py'].run()
    case_tag=root['SETTINGS']['PHYSICS']['case_tag']
    for item in root['Cases'][case_tag].keys():
        item_temp=item.split('~')
        if not  root['OUTPUTS'].has_key(item_temp[0]):
            root['OUTPUTS'][item_temp[0]]=OMFITtree()
        if not  root['OUTPUTS'][item_temp[0]].has_key(item_temp[1]):
            root['OUTPUTS'][item_temp[0]][item_temp[1]]=OMFITtree()
        if not root['OUTPUTS'][item_temp[0]][item_temp[1]].has_key('nonlin'):
            root['OUTPUTS'][item_temp[0]][item_temp[1]]['nonlin']=OMFITtree()
        for files in root['Cases'][case_tag][item].keys():
            root['OUTPUTS'][item_temp[0]][item_temp[1]]['nonlin'][files]=root['Cases'][case_tag][item][files] 
    
