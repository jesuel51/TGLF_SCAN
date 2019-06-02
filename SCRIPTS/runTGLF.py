##===================================
### input
##==================================
inputs=[(root['INPUTS']['input.tglf'],'input.tglf'),
        (root['INPUTS']['jobtglf.pbs'],'jobtglf.pbs'),
        (root['INPUTS']['monitePBStglf.sh'],'monitePBStglf.sh')
	]
if root['SETTINGS']['PHYSICS']['mode']=='nonlin':
    root['INPUTS']['input.tglf']['USE_TRANSPORT_MODEL']=True
else:
    root['INPUTS']['input.tglf']['USE_TRANSPORT_MODEL']=False
##----------------------
### output
##----------------------
outputs=['out.tglf.run']
#executable ='chmod 777 monitePBStglf.sh ; ./monitePBStglf.sh';
executable ='pbsMonitor -cn 1 -exe tglf -e . -n 1'
ret_code=OMFITx.executable(root, inputs=inputs, outputs=outputs, executable=executable)
#-----------------------
# load the results
#-----------------------
for item in outputs:
    root['OUTPUTS'][item]=OMFITasciitable(item)
