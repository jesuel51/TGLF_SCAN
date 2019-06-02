# this script is used to plot the eigenfunction of a specified mode 
# the ky to be plotted is determined by 
# root['SETTINGS']['PLOTS']['Para'] 
# root['SETTINGS']['PLOTS']['ParaVal'] 
# root['SETTINGS']['PLOTS']['kyballoon'] 
###################################################################
# the first line stores the number of modes, fields and thetas
# first,let's define a function to read all the important values
def readfile(filename):
    count=-1
    w=zeros([2,2])
    f=open(filename,'Ur')
    for line in f:
        count=count+1
        if count==0:
            numbers=[int(item) for item in line.split()]
            nmode=numbers[0]
            nfield=numbers[1]
            ntheta=numbers[2]
#            print(ntheta)
            Theta=zeros([ntheta,1])
            RePhi=zeros([ntheta,nmode])
            ImPhi=zeros([ntheta,nmode])
            ReBPer=zeros([ntheta,nmode])
            ImBPer=zeros([ntheta,nmode])
#            count=count+1
        elif count==1:
            continue;
        elif count>1:
#            print(line)
            temp=[float(item) for item in line.split()]
            Theta[count-2]=temp[0]
            temp2=array(temp[1:]).reshape(nmode,nfield,2)
#            print(temp2)
            RePhi[count-2]=[temp2[k,0,0] for k in arange(nmode)]
            ImPhi[count-2]=[temp2[k,0,1] for k in arange(nmode)]
            if nfield>1:
                ReBPer[count-2]=[temp2[k,1,0] for k in arange(nmode)]
                ImBPer[count-2]=[temp2[k,1,1] for k in arange(nmode)]
    return nmode,Theta,RePhi,ImPhi,ReBPer,ImBPer

# read the data and plot
PLOTS=root['SETTINGS']['PLOTS']
Para=PLOTS['Para']
ParaVal=PLOTS['ParaVal']
kyballoon=PLOTS['kyballoon']
filename=root['OUTPUTS'][Para][str(ParaVal)]['lin'][str(kyballoon)[0:4]]['out.tglf.wavefunction'].filename
[nmode,Theta,RePhi,ImPhi,ReBPer,ImBPer]=readfile(filename)
# plot
figure(figsize=[8,12])
fs1=24
fs2=20
lw=2
Theta=Theta/pi
for k in arange(1,nmode+1):
    subplot(2,nmode,k)
    plot(Theta,RePhi.T[k-1],'-bo',linewidth=lw,label='RePhi')
    plot(Theta,ImPhi.T[k-1],'-ro',linewidth=lw,label='ImPhi')
    title('mode'+str(k),fontsize=fs1,family='serif')
    xticks(fontsize=fs2,family='serif')
    yticks(fontsize=fs2,family='serif')
    if k==1:
        legend(loc=0,fontsize=fs2).draggable(True)
    subplot(2,nmode,nmode+k)
    plot(Theta,ReBPer.T[k-1],'-b',linewidth=lw,label='ReBPer')
    plot(Theta,ImBPer.T[k-1],'-r',linewidth=lw,label='ImBPer')
    xticks(fontsize=fs2,family='serif')
    yticks(fontsize=fs2,family='serif')
    xlabel('$\\theta\\pi$',fontsize=fs2,family='serif')
    if k==1:
        legend(loc=0,fontsize=fs2).draggable(True)
