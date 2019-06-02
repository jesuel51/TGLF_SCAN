# this script is used to plot the eigenfrequency and growth rate for all the scanning cases, 
# the parameters and the value is specified in root['SETTINGS']['PLOTS']['2d']['Para_x'] and root['SETTINGS']['PLOTS']['Range_x'] as well as 
# root['SETTINGS']['PLOTS']['2d']['Para_y'] and root['SETTINGS']['PLOTS']['Range_y']
# note the stability analyis should be performed by TGLF before running this plot scrip
# at present version, only the dominate mode plot is available
# first we should define a function to read the date of out.tglf.run, which contains the frequency and growth rate
#plt.close()
import numpy as np
import numpy as np
def readfile(filename,nmodes):
# nmodes is the number of the modes
    count=0
    w=zeros([nmodes,2])
    f=open(filename,'Ur')
    for line in f:
        if line.find('(wr,wi)')!=-1:
            temp=line.split()
            w[count][0]=temp[1]
            w[count][1]=temp[2]
            count=count+1
    return w
inputtglf=root['INPUTS']['input.tglf']
# then read all the data
effnum=root['SETTINGS']['PLOTS']['effnum']
if inputtglf.has_key('NMODES'):
    nmodes=inputtglf['NMODES']
else:
    nmodes=2
input_tglf=root['INPUTS']['input.tglf']
# note that it make no sense that scale the gamma_e in the linear run
plots=root['SETTINGS']['PLOTS']['2d']
physics=root['SETTINGS']['PLOTS']['2d']
if root['SETTINGS']['PLOTS']['iflwphy']==1:
    plots['Para_x']=physics['Para_x']
    plots['Para_y']=physics['Para_y']
    plots['Range_x']=physics['Range_x']
    plots['Range_x']=physics['Range_x']
    plots['kyarr']=physics['kyarr']
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
w_arr=zeros([nRange_x,nRange_y,num_ky])     # dominate mode frequency
#err_w_arr=zeros([nRange_x,nRange_y,num_ky])     # error in dominate mode frequency
gamma_arr=zeros([nRange_x,nRange_y,num_ky]) # dominate mode growth rate
#err_gamma_arr=zeros([nRange_x,nRange_y,num_ky]) # error in dominate mode growth rate
# all the information about frequency and growth rate can be get
for k in range(0,nRange_x):
    for p in range(0,nRange_y):
        count2=0
    #    print(str(Range[k]))
        for ky in kyarr:
            try:
                filename=root['OUTPUTS'][Para_x][str(Range_x[k])[0:effnum]][Para_y][str(Range_y[p])[0:effnum]]['lin'][str(ky)[0:effnum]]['out.tglf.run'].filename
#                print(filename)
                w=readfile(filename,nmodes)
#            w,err_w=readfile(filename)
            except:
                w=zeros([nmodes,2])
   # only the domiante mode is read at the present version
            w_arr[k][p][count2]=w[0][0]
            gamma_arr[k][p][count2]=w[0][1]
#            err_w_arr[k][p][count2]=err_w[0]
#            err_gamma_arr[k][p][count2]=err_w[1]
            count2=count2+1
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
    plots['kyarr']=physics['kyarr']
ilogx=plots['ilogx']
ilogy=plots['ilogy']
# do the contourf plot
idimplt=root['SETTINGS']['PLOTS']['idimplt']
nky=len(plots['kyarr'])
if idimplt==0:
    Range_x_grid,Range_y_grid=meshgrid(Range_x,Range_y)
else:
    Range_x_grid,Range_y_grid=meshgrid(Range_y,Range_x)
for k in range(nky):
    fig=figure(str(kyarr[k]),figsize=[12,12])
    ax = fig.gca(projection='3d')
    subplot(1,2,1)
    if idimplt==0:
        count=0
        for val_y in Range_y:
            plot(Range_x,w_arr.T[k][count],lab[count],label=str(val_y),linewidth=lw)
            count=count+1
        xlabel(Para_x,fontsize=fs2,family='serif')
        legend(loc=0,fontsize=fs2).draggable(True)
        if ilogx==1:
            ax1.set_xscale('log')
        if ilogy==1:
            ax1.set_yscale('log')
    else:
        count=0
        for val_x in Range_x:
            plot(Range_y,w_arr.T[k].T[count],lab[count],label=str(val_x),linewidth=lw)
            count=count+1
        xlabel(Para_y,fontsize=fs2,family='serif')
        legend(loc=0,fontsize=fs2).draggable(True)
        if ilogx==1:
            ax1.set_yscale('log')
        if ilogy==1:
            ax1.set_xscale('log')
    ylabel('$c_s/a$',fontsize=fs2,family='serif')
    xticks(fontsize=fs2,family='serif')
    yticks(fontsize=fs2,family='serif')
    title('$\omega$',fontsize=fs1,family='serif')
    subplot(1,2,2)
    if idimplt==0:
        count=0
        for val_y in Range_y:
            plot(Range_x,gamma_arr.T[k][count],lab[count],label=str(val_y),linewidth=lw)
            count=count+1
        xlabel(Para_x,fontsize=fs2,family='serif')
        legend(loc=0,fontsize=fs2).draggable(True)
        if ilogx==1:
            ax1.set_xscale('log')
        if ilogy==1:
            ax1.set_yscale('log')
    else:
        count=0
        for val_x in Range_x:
            plot(Range_y,gamma_arr.T[k].T[count],lab[count],label=str(val_x),linewidth=lw)
            count=count+1
        xlabel(Para_y,fontsize=fs2,family='serif')
        legend(loc=0,fontsize=fs2).draggable(True)
        if ilogx==1:
            ax1.set_yscale('log')
        if ilogy==1:
            ax1.set_xscale('log')
    ylabel('$c_s/a$',fontsize=fs2,family='serif')
    xticks(fontsize=fs2,family='serif')
    yticks(fontsize=fs2,family='serif')
    title('$\gamma$',fontsize=fs1,family='serif')
# # ===================================
iwritelin=root['SETTINGS']['PLOTS']['iwritelin']  # determine whether to write out to a file
numky=len(kyarr) 
nmodes=1
if iwritelin==1 and root['SETTINGS']['DEPENDENCIES'].has_key('linout'):
    eigenout=root['SETTINGS']['DEPENDENCIES']['linout']
    fid=open(eigenout,'w')
# first write the scanned parameter name into the file
    fid.write(Para_x+'    '+Para_y)
    fid.write('\n')
# write the nRange and the para_val into the file
    fid.write(str(len(Range_x))+'    '+str(len(Range_y)))
    fid.write('\n')
    line=''
    for m in range(len(Range_x)):
        line=line+str(Range_x[m])+'    '
    fid.write(line)
    fid.write('\n')
    line=''
    for m in range(len(Range_y)):
        line=line+str(Range_y[m])+'    '
    fid.write(line)
    fid.write('\n')
# write nmodes into the file    
    fid.write(str(nmodes)+'    '+str(numky))
    fid.write('\n')
    for k in range(numky):
        line=str(kyarr[k])
        for p in range(len(Range_x)):
            for q in range(len(Range_y)):
# w_arr=zeros([nRange_x,nRange_y,num_ky])
#            line=line+'    '+str(w_arr[p][k])+'    '+str(gamma_arr[p][k])+'    '+str(err_w_arr[p][k])+'    '+str(err_gamma_arr[p][k])
                line=line+'    '+str(w_arr[p][q][k])+'    '+str(gamma_arr[p][q][k])
        fid.write(line)
        fid.write('\n')
    fid.close()
