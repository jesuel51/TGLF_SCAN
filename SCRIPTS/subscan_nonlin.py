##########
# this is a script used for quickly run tglf transport model
# note before running this script, the caseName set in root['SETTINGS']['PHYSICS']['case_tag'] should be modified , eg, nonlin
print "============== scan_tglf ==========="
# specify the caseroot and casetag, note usually caseroot needs to have the key caseName
caseRoot=root['Cases'] # the root of the tag, defines where to store the scanning data
caseName=root['SETTINGS']['PHYSICS']['case_tag'] # the name of the tag, which indicates the name of the scanning
# backup the input.tglf
root['INPUTS']['input.tglf_bak']=root['INPUTS']['input.tglf'].duplicate()
if not caseRoot.has_key(caseName):
    caseRoot[caseName]=OMFITtree()
else:
    for item in caseRoot[caseName].keys():     #cover the previous calculation
        del caseRoot[caseName][item]
wkdir=root['SETTINGS']['SETUP']['workDir'] # the local directory(not the remote one)
dir_list=[]
inputs_node_names={'input.tglf':OMFITnamelist} # input node names (not file name), in a format of dictionary
inputs_node=root['INPUTS']             # the father node of input_nodes_names
#inputs_series_nodes=root['OUTPUTS']['TGYROOutput']  # the input.tglf for all the radial grids are stored here
inputs=[]

base_loadOutputs={'out.tglf.run':OMFITgaCode,'out.tglf.flux_spectrum':OMFITgaCode,'out.tglf.gbflux':OMFITgaCode,'run_log':OMFITgaCode,\
                  'out.tglf.potential_spectrum':OMFITgaCode,'out.tglf.density_spectrum':OMFITgaCode,'out.tglf.temperature_spectrum':OMFITgaCode,\
                  'out.tglf.nete_crossphase_spectrum':OMFITgaCode,'out.tglf.eigenvalue_spectrum':OMFITgaCode}
# the inputfiles will not be load as output anymore 
#for item in inputs_node_names.keys():
#    base_loadOutputs[os.path.basename(root['INPUTS'][item].filename)]=inputs_node_names[item] #the input is recorded to output, os.path,basename is the name of the file but picked out the path
# kyarr=root['SETTINGS']['SETUP']['kyarr'] #you do not need this for nonlinear simulation
loadOutputs={} 
#for ra_ind in inputs_series_nodes.keys():
#p_tgyro=len(root['INPUTS']['TGYRO']['input.tgyro']['DIR'])
para_name=root['SETTINGS']['PHYSICS']['Para']
para_rang=root['SETTINGS']['PHYSICS']['Range']
ncount=-1
for para_val in para_rang:
    ncount=ncount+1
    printi('running the calculation on '+para_name+ '='+str(para_val))
    # set list
    inputs_node['input.tglf'][para_name]=para_val
    nPara=2
    while root['SETTINGS']['PHYSICS'].has_key('Para'+str(nPara)) and root['SETTINGS']['PHYSICS'].has_key('Range'+str(nPara)):
        inputs_node['input.tglf'][root['SETTINGS']['PHYSICS']['Para'+str(nPara)]]=root['SETTINGS']['PHYSICS']['Range'+str(nPara)][ncount]
        nPara=nPara+1
        # determine whether to use the self-consistent alpha 
    if root['SETTINGS']['PHYSICS']['ialpha']==1:
        const=-0.0397887779569
        inputk=inputs_node['input.tglf']
        ns=inputk['NS']
        padd=sum([inputk['AS_'+str(m)]*inputk['TAUS_'+str(m)]*(inputk['RLNS_'+str(m)]+inputk['RLTS_'+str(m)]) for m in arange(1,ns+1)])
        p_prime=const*padd*inputk['BETAE']*inputk['Q_LOC']/inputk['RMIN_LOC']
#        inputk['P_PRIME_LOC']=p_prime
        inputs_node['input.tglf']['P_PRIME_LOC']=p_prime
        print(inputk['P_PRIME_LOC'])
    inputs_node['input.tglf']['USE_TRANSPORT_MODEL']=True
    new_dir=para_name+'~'+str(para_val)
    dir_list.append(new_dir)
    # transfer the value to the inputs and prepare for running
    caseRoot[caseName][new_dir]=OMFITtree()
    if os.path.isfile(new_dir+r'.zip'):
        os.remove(new_dir+r'.zip')
    tmp_zip=zipfile.ZipFile(new_dir+r'.zip', mode='w') # construct a new zip file, and waiting for files to be written in 
#    for item  in inputs_node_names.keys():
#        if inputs_node.has_key(item):
#            inputs_node[item].save()
#            caseRoot[caseName][new_dir][item]=copy.deepcopy(inputs_node[item])
    item='input.tglf'
    inputs_node['input.tglf'].save()
    caseRoot[caseName][new_dir][item]=copy.deepcopy(inputs_node['input.tglf'])
    tmp_zip.write(caseRoot[caseName][new_dir][item].filename, caseRoot[caseName][new_dir][item].filename.split(os.sep)[-1]) # os.sep is / for linux and \ for windows
    tmp_zip.close()
    caseRoot[caseName][new_dir]['zip']=OMFITgaCode(tmp_zip.filename) # the inputs are compressed as an zip file and loaded in the output directory
    inputs.append(caseRoot[caseName][new_dir]['zip'])              # then the zipfile are import as input
   # set OUTPUTS( a lot of dir ) for loadOutputs, all the parameters ranges are covered
    for item in base_loadOutputs:
        loadOutputs[new_dir+os.sep+item]=base_loadOutputs[item]
        # so till now, a lot of zip files ,covering all the paraters set , are constructed. In addition, all the output file forms, are also constructed.
        # next issues is to run with the inputfiles prepared in zip file format
outputs=loadOutputs.keys()
#
executable='mv * input.tglf;\n'+root['SETTINGS']['SETUP']['executable']

#set job scipts
pbs_file=root['SETTINGS']['SETUP']['workDir']+os.sep+'scan.pbs'
username=root['SETTINGS']['REMOTE_SETUP']['server'].split('@')[0]
ps_name='tglf'
#print ps_name # You may need to check command name

## the bash_head below is used in running on shenma
if root['SETTINGS']['SETUP']['server']=='shenma':
    bash_head= \
    r'#!/bin/sh '+'\n'+ \
    r'#PBS -N '+ps_name +'\n'+ \
    r'#PBS -l nodes='+str(root['SETTINGS']['SETUP']['num_nodes'])+':ppn='+str(root['SETTINGS']['SETUP']['num_cores']) +'\n'+ \
    r'#PBS -j oe' +'\n'+ \
    r'#PBS -l walltime='+str(root['SETTINGS']['SETUP']['wall_time']) +'\n'+ \
    r'#PBS -q '+root['SETTINGS']['SETUP']['pbs_queue'] +'\n'+ \
    r'cd ${PBS_O_WORKDIR}' +'\n'+ \
    r'pwd'  +'\n'+ \
    r'NP=`cat ${PBS_NODEFILE}|wc -l`' +'\n'+ \
    '\n'+ \
    r'JOBID_FILE="JOBID_${PBS_JOBID}"' +'\n'+ \
    r'touch ${JOBID_FILE}' +'\n'
else:
    ## the bash_head below in used in running on kuafu
    num_nodes=root['SETTINGS']['SETUP']['num_nodes']
    num_cores=root['SETTINGS']['SETUP']['num_cores']
    bash_head= \
    r'#!/bin/sh '+'\n' + \
    r'#SBATCH -p '+root['SETTINGS']['SETUP']['pbs_queue'] +'\n' +\
    r'#SBATCH -J '+ps_name +'\n' +\
    r'#SBATCH -t '+str(root['SETTINGS']['SETUP']['wall_time']) +'\n' +\
    r'#SBATCH -o -o.out'+'\n' +\
    r'#SBATCH -e -e.out'+'\n' +\
    r'#SBATCH --workdir=./'+'\n' +\
    r'#SBATCH --ntasks '+str(num_nodes*num_cores) +'\n'

bash_content= \
'dir_list=('+' '.join(dir_list)+')' +'\n'+ \
r'for i in ${dir_list[@]}; ' +'\n'+  \
'do '  +'\n'+  \
r'  while [[ $( ps -u '+username+r' |grep '+ps_name+r' | wc -l ) -gt '+str(root['SETTINGS']['SETUP']['num_cores']-1)+' ]]; do ' +'\n' + \
r'    sleep 2s' +'\n' +\
r'  done ' +'\n'+ \
r'  unzip ${i}.zip -d $i ' +'\n'+ \
r' cd $i'  +'\n'+ \
executable+r' > run_log & ' +'\n'+ \
r"  cd .." +'\n'+ \
r'done' +'\n'

bash_tail= \
r'while [[ $( ps -u '+username+r' |grep '+ps_name+r' | wc -l ) -gt 0 ]]; do ' +'\n' + \
r'  sleep 5s' +'\n'+ \
r'done ' +'\n'+ \
r'rm ${JOBID_FILE}' +'\n'



##############################################
if not os.path.exists(str(root['SETTINGS']['SETUP']['workDir'])):
    os.makedirs(str(root['SETTINGS']['SETUP']['workDir']))
##############################################
with open(pbs_file,'w') as f1:
    f1.write(bash_head+'\n'+bash_content+'\n'+bash_tail)
caseRoot[caseName][pbs_file.split(os.sep)[-1]]=OMFITascii(pbs_file)

inputs.append(caseRoot[caseName][pbs_file.split(os.sep)[-1]])

# sub jobs
#executable='chmod u+x pbsMonitor; ./pbsMonitor '+'scan.pbs'
executable='pbsMonitor '+'scan.pbs'
#executable='chmod u+x '+pbs_file+'; '+pbs_file
ret_code=OMFITx.executable(root, inputs=inputs, outputs=[],  server=root['SETTINGS']['REMOTE_SETUP']['server'], tunnel=None, executable=executable,clean=True)

workDir='./'
workDir=str(root['SETTINGS']['REMOTE_SETUP']['workDir'])+os.sep
# load result
print 'listdir'
print os.listdir(workDir)
#print os.listdir(wkdir+os.sep)
#print outputs
for item in outputs:
    if os.path.exists(workDir+os.sep+item):
        print "Loading "+item
        if not caseRoot[caseName].has_key(item.split(os.sep)[0]):
            caseRoot[caseName][item.split(os.sep)[0]]=OMFITtree()
        caseRoot[caseName][item.split(os.sep)[0]][item.split(os.sep)[-1]]=loadOutputs[item](workDir+os.sep+item)
for item in caseRoot[caseName]:
    if isinstance(caseRoot[caseName][item],dict) and caseRoot[caseName][item].has_key('zip'):
        del caseRoot[caseName][item]['zip']
del caseRoot[caseName]['scan.pbs']
root['INPUTS']['input.tglf']=root['INPUTS']['input.tglf_bak'].duplicate()
del root['INPUTS']['input.tglf_bak']
