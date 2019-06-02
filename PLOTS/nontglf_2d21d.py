# this script is used to plot the flux of all channels in the 2D space
# the parameters and the value is specified in root['SETTINGS']['PLOTS']['2d']['Para_x'] and root['SETTINGS']['PLOTS']['Range_x'] as well as 
# root['SETTINGS']['PLOTS']['2d']['Para_y'] and root['SETTINGS']['PLOTS']['Range_y']
# note the stability analyis should be performed by TGLF before running this plot scrip
# first we should define a function to read the total
# at present, we only care about the flux , not the flux spectrum
#plt.close()
import numpy as np
def readflux(filename):
    f=open(filename,'Ur')
    for line in f:
        flux=[float(item) for item in line.split()]
    num=len(flux)
    ns=num/4
    flux=array(flux).reshape(4,ns)
    Gammae=flux[0][0]
    Qe=flux[1][0]
    Qi=sum([flux[1][k] for k in arange(1,ns)])
    Tor=sum([flux[2][k] for k in range(ns)])
    return Gammae,Qi,Qe,Tor
    f.close()
# then read all the data
effnum=root['SETTINGS']['PLOTS']['effnum']
input_tglf=root['INPUTS']['input.tglf']
ns=input_tglf['NS']
# note that it make no sense that scale the gamma_e in the linear run
plots=root['SETTINGS']['PLOTS']['2d']
physics=root['SETTINGS']['PLOTS']['2d']
if root['SETTINGS']['PLOTS']['iflwphy']==1:
    plots['Para_x']=physics['Para_x']
    plots['Para_y']=physics['Para_y']
    plots['Range_x']=physics['Range_x']
    plots['Range_x']=physics['Range_x']
#    plots['kyarr']=physics['kyarr']
#kyarr=root['SETTINGS']['SETUP']['kyarr']
kyarr=plots['kyarr']
Para_x=plots['Para_x']
Para_y=plots['Para_y']
Range_x=plots['Range_x']
Range_y=plots['Range_y']
# determine whether plot the ExB shearing rate, the capability of plotting ExB is unvailable at present
#ipltExB=root['SETTINGS']['PLOTS']['ipltExB']
#gammae_eff = 0.3*sqrt(kappa)*gamma_e
num_ky=len(kyarr)
#nRange=len(root['INPUTS']['TGYRO']['input.tgyro']['DIR'])
nRange_x=len(Range_x)
nRange_y=len(Range_y)
Qi_arr=zeros([nRange_y,nRange_x])
Qe_arr=zeros([nRange_y,nRange_x])
Gammae_arr=zeros([nRange_y,nRange_x])
Tor_arr=zeros([nRange_y,nRange_x])
# all the information about frequency and growth rate can be get
for k in range(0,nRange_x):
    for p in range(0,nRange_y):
        try:
            filename=root['OUTPUTS'][Para_x][str(Range_x[k])[0:effnum]][Para_y][str(Range_y[p])[0:effnum]]['nonlin']['out.tglf.gbflux'].filename
            Gammae,Qi,Qe,Tor=readflux(filename)
            Qi_arr[p][k]=Qi
            Qe_arr[p][k]=Qe
            Gammae_arr[p][k]=Gammae
            Tor_arr[p][k]=Tor
        except:
#            fluxdata[k][p]=zeros([ns*4])
            Qi_arr[p][k]=0
            Qe_arr[p][k]=0
            Gammae_arr[p][k]=0
            Tor_arr[p][k]=0
#        w_arr[k][p][count2]=w[0][0]
#        gamma_arr[k][p][count2]=w[0][1]
########################################
# based on the profiles we get, then all the linear information can be plotted
lab=['-kd','-md','-bd','-rd','-gd','-ko','-mo','-bo','-ro','-go','-k*','-m*','-b*','-r*','-g*'\
     '--k','--m','--b','--r','--g','-k', '-m', '-b', '-r' ];#       '-ko','-k*','-md','-mo','-m*','-bd','-bo','-b*','-rd','-ro','-r*','-gd','go','-g*']
lw=2
fs1=20
fs2=16
fs3=24
plots=root['SETTINGS']['PLOTS']['2d']
physics=root['SETTINGS']['PHYSICS']['2d']
if root['SETTINGS']['PLOTS']['iflwphy']==1:
    plots['Para_x']=physics['Para_x']
    plots['Para_y']=physics['Para_y']
    plots['Range_x']=physics['Range_x']
    plots['Range_y']=physics['Range_y']
#    plots['kyarr']=physics['kyarr']
# both the Range_x and Range_y will be scaled to a more meanful physical value
Range_x=Range_x*plots['Range_xscale']
Range_y=Range_y*plots['Range_yscale']
idimplt=root['SETTINGS']['PLOTS']['idimplt']
ilogx=plots['ilogx']
ilogy=plots['ilogy']
nky=len(plots['kyarr'])
if idimplt==0:
    Range_x_grid,Range_y_grid=meshgrid(Range_x,Range_y)
else:
    Range_x_grid,Range_y_grid=meshgrid(Range_y,Range_x)
#for k in range(nky):
Q_exp=root['SETTINGS']['PLOTS']['2d']['Q_Exp']
for k in range(1):
    fig=figure('Flux 2D',figsize=[12,12])
    ax = fig.gca(projection='3d')
    subplot(2,2,1)
    if idimplt==0:
        count=0
        for val_y in Range_y:
            plot(Range_x,Gammae_arr[count],lab[count],label=str(val_y),linewidth=lw)
            count=count+1
        if Q_exp[0]==1 and Q_exp[1]==0:
            plot(array([Range_x[0],Range_x[-1]]),array([Q_exp[2],Q_exp[2]]),'--r',linewidth=lw/2)
        if ilogx==1:
            ax1.set_xscale('log')
        if ilogy==1:
            ax1.set_yscale('log')
    else:
        count=0
        for val_x in Range_x:
            plot(Range_y,Gammae_arr.T[count],lab[count],label=str(val_x),linewidth=lw)
            count=count+1
        if Q_exp[0]==1 and Q_exp[1]==0:
            plot(array([Range_y[0],Range_y[-1]]),array([Q_exp[2],Q_exp[2]]),'--r',linewidth=lw/2)
        if ilogx==1:
            ax1.set_xscale('log')
        if ilogy==1:
            ax1.set_yscale('log')
    xticks(fontsize=fs2,family='serif')
    yticks(fontsize=fs2,family='serif')
    title('$\Gamma_e$',fontsize=fs1,family='serif')
    subplot(2,2,2)
    if idimplt==0:
        count=0
        for val_y in Range_y:
            plot(Range_x,Tor_arr[count],lab[count],label=str(val_y),linewidth=lw)
            count=count+1
        if Q_exp[0]==1 and Q_exp[1]==1:
            plot(array([Range_x[0],Range_x[-1]]),array([Q_exp[2],Q_exp[2]]),'--r',linewidth=lw/2)
        if ilogx==1:
            ax1.set_xscale('log')
        if ilogy==1:
            ax1.set_yscale('log')
    else:
        count=0
        for val_x in Range_x:
            plot(Range_y,Tor_arr.T[count],lab[count],label=str(val_x),linewidth=lw)
            count=count+1
        if Q_exp[0]==1 and Q_exp[1]==1:
            plot(array([Range_y[0],Range_y[-1]]),array([Q_exp[2],Q_exp[2]]),'--r',linewidth=lw/2)
        if ilogx==1:
            ax1.set_xscale('log')
        if ilogy==1:
            ax1.set_yscale('log')
    xticks(fontsize=fs2,family='serif')
    yticks(fontsize=fs2,family='serif')
    title('$\Pi$',fontsize=fs1,family='serif')
    subplot(2,2,3)
    if idimplt==0:
        count=0
        for val_y in Range_y:
            plot(Range_x,Qe_arr[count],lab[count],label=str(val_y),linewidth=lw)
            count=count+1
        xlabel(Para_x,fontsize=fs2,family='serif')
        if Q_exp[0]==1 and Q_exp[1]==2:
            plot(array([Range_x[0],Range_x[-1]]),array([Q_exp[2],Q_exp[2]]),'--r',linewidth=lw/2)
        if ilogx==1:
            ax1.set_xscale('log')
        if ilogy==1:
            ax1.set_yscale('log')
    else:
        count=0
        for val_x in Range_x:
            plot(Range_y,Qe_arr.T[count],lab[count],label=str(val_x),linewidth=lw)
            count=count+1
        if Q_exp[0]==1 and Q_exp[1]==2:
            plot(array([Range_y[0],Range_y[-1]]),array([Q_exp[2],Q_exp[2]]),'--r',linewidth=lw/2)
        xlabel(Para_y,fontsize=fs2,family='serif')
        if ilogx==1:
            ax1.set_xscale('log')
        if ilogy==1:
            ax1.set_yscale('log')
    xticks(fontsize=fs2,family='serif')
    yticks(fontsize=fs2,family='serif')
    title('$Q_e$',fontsize=fs1,family='serif')
    subplot(2,2,4)
    if idimplt==0:
        count=0
        for val_y in Range_y:
            plot(Range_x,Qi_arr[count],lab[count],label=str(val_y),linewidth=lw)
            count=count+1
        if Q_exp[0]==1 and Q_exp[1]==3:
            plot(array([Range_x[0],Range_x[-1]]),array([Q_exp[2],Q_exp[2]]),'--r',linewidth=lw/2)
        xlabel(Para_x,fontsize=fs2,family='serif')
        legend(loc=0,fontsize=fs2).draggable(True)
        if ilogx==1:
            ax1.set_xscale('log')
        if ilogy==1:
            ax1.set_yscale('log')
    else:
        count=0
        for val_x in Range_x:
            plot(Range_y,Qi_arr.T[count],lab[count],label=str(val_x),linewidth=lw)
            count=count+1
        if Q_exp[0]==1 and Q_exp[1]==3:
            plot(array([Range_y[0],Range_y[-1]]),array([Q_exp[2],Q_exp[2]]),'--r',linewidth=lw/2)
        xlabel(Para_y,fontsize=fs2,family='serif')
        legend(loc=0,fontsize=fs2).draggable(True)
        if ilogx==1:
            ax1.set_yscale('log')
        if ilogy==1:
            ax1.set_xscale('log')
    xticks(fontsize=fs2,family='serif')
    yticks(fontsize=fs2,family='serif')
    title('$Q_i$',fontsize=fs1,family='serif')
