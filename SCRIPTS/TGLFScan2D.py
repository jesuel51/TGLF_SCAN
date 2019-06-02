# this script is used to scan the Para of TGLF
mode=root['SETTINGS']['PHYSICS']['2d']['mode']
if mode=='lin':
    root['SCRIPTS']['subscan_lin_2d.py'].run()
    case_tag=root['SETTINGS']['PHYSICS']['case_tag']
    for item in root['Cases'][case_tag].keys():
        item_temp=item.split('~')
        if not  root['OUTPUTS'].has_key(item_temp[0]):
            root['OUTPUTS'][item_temp[0]]=OMFITtree()
        if not  root['OUTPUTS'][item_temp[0]].has_key(item_temp[1]):
            root['OUTPUTS'][item_temp[0]][item_temp[1]]=OMFITtree()
        if not  root['OUTPUTS'][item_temp[0]][item_temp[1]].has_key(item_temp[2]):
            root['OUTPUTS'][item_temp[0]][item_temp[1]][item_temp[2]]=OMFITtree()
        if not  root['OUTPUTS'][item_temp[0]][item_temp[1]][item_temp[2]].has_key(item_temp[3]):
            root['OUTPUTS'][item_temp[0]][item_temp[1]][item_temp[2]][item_temp[3]]=OMFITtree()
        if not root['OUTPUTS'][item_temp[0]][item_temp[1]][item_temp[2]][item_temp[3]].has_key('lin'):
            root['OUTPUTS'][item_temp[0]][item_temp[1]][item_temp[2]][item_temp[3]]['lin']=OMFITtree()
        if not root['OUTPUTS'][item_temp[0]][item_temp[1]][item_temp[2]][item_temp[3]]['lin'].has_key(item_temp[5]):
            root['OUTPUTS'][item_temp[0]][item_temp[1]][item_temp[2]][item_temp[3]]['lin'][item_temp[5]]=OMFITtree()
        for files in root['Cases'][case_tag][item]:
            root['OUTPUTS'][item_temp[0]][item_temp[1]][item_temp[2]][item_temp[3]]['lin'][item_temp[5]][files]=root['Cases'][case_tag][item][files] 
else:
    root['SCRIPTS']['subscan_nonlin_2d.py'].run()
    case_tag=root['SETTINGS']['PHYSICS']['case_tag']
    for item in root['Cases'][case_tag].keys():
        item_temp=item.split('~')
        if not  root['OUTPUTS'].has_key(item_temp[0]):
            root['OUTPUTS'][item_temp[0]]=OMFITtree()
        if not  root['OUTPUTS'][item_temp[0]].has_key(item_temp[1]):
            root['OUTPUTS'][item_temp[0]][item_temp[1]]=OMFITtree()
        if not  root['OUTPUTS'][item_temp[0]][item_temp[1]].has_key(item_temp[2]):
            root['OUTPUTS'][item_temp[0]][item_temp[1]][item_temp[2]]=OMFITtree()
        if not  root['OUTPUTS'][item_temp[0]][item_temp[1]][item_temp[2]].has_key(item_temp[3]):
            root['OUTPUTS'][item_temp[0]][item_temp[1]][item_temp[2]][item_temp[3]]=OMFITtree()
        if not root['OUTPUTS'][item_temp[0]][item_temp[1]][item_temp[2]][item_temp[3]].has_key('nonlin'):
            root['OUTPUTS'][item_temp[0]][item_temp[1]][item_temp[2]][item_temp[3]]['nonlin']=OMFITtree()
        for files in root['Cases'][case_tag][item]:
            root['OUTPUTS'][item_temp[0]][item_temp[1]][item_temp[2]][item_temp[3]]['nonlin'][files]=root['Cases'][case_tag][item][files]
    
