# this script is used to plot the eigenfrequency and growth rate for all the scanning cases, 
# the parameters and the value is specified in root['SETTINGS']['PLOTS']['Para'] and root['SETTINGS']['PLOTS']['Range']
# note the stability analyis should be performed by TGLF before running this plot scrip
# first we should define a function to read the date of out.tglf.run, which contains the frequency and growth rate
#plt.close()
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
# find the nmodes
# we note that scaning of nmodes is not sensible for linear run
inputtglf=root['INPUTS']['input.tglf']
if inputtglf.has_key('NMODES'):
    nmodes=inputtglf['NMODES']
else:
    nmodes=2
# then read all the data
#iview=root['SETTINGS']['PLOTS']['iview']
kyarr=root['SETTINGS']['PLOTS']['kyarr']
para=root['SETTINGS']['PLOTS']['Para']
Range=root['SETTINGS']['PLOTS']['Range']
num_ky=len(kyarr)
nRange=len(Range)
omega=zeros([nmodes,nRange,num_ky])     # mode frequency,including dominate and nondominate modes
gamma=zeros([nmodes,nRange,num_ky]) # mode growth rate, including dominate and nondominate modes
ExBShear=zeros(nRange)         # ExB shearing rate, defined as a/cs*r/q*d(omega)/dr
Kappa=zeros(nRange)            # Elongation
Dlowk_arr=zeros(nRange)
Dhighk_arr=zeros(nRange)
S_arr=zeros(nRange)
# all the information about frequency and growth rate can be get
for k in range(0,nRange):
    count2=0
#    print(str(Range[k]))
    for item in kyarr:
        filename=root['OUTPUTS'][para][str(Range[k])]['lin'][str(item)[0:4]]['out.tglf.run'].filename
        w=readfile(filename,nmodes)
        for n in range(nmodes):
            omega[n][k][count2]=w[n][0]
            gamma[n][k][count2]=w[n][1]
        count2=count2+1
#######################################
isat1=0
if isat1==1:
    # here we try to get the gamma_model of the Sat1 model
    Gamma_Model=zeros([nRange,num_ky]) # Gamma_Model , used in Sat1
    Gamma_Stage=zeros([nRange,num_ky]) # Gamma_Model , used in Sat1
    # first define a function of the lorentzian weight function
    def WW(kyp,ky,kyarr,kymax):
    # the weight function between kyp and ky
        cky=3.0
        gkypky=1./(ky**2+cky*(ky-kyp)**2)
        nume=gkypky
        denom=0.
        num_ky=len(kyarr)
        for m in range(0,num_ky):
            if kyarr[m]>kymax:
                dkyp=kyarr[m]-kyarr[m-1]
                denom=denom+dkyp*1./(ky**2+cky*(ky-kyarr[m])**2)
        return nume/denom
    # then let's compute the gamma_stage1
    indlowk=find(kyarr<0.8)[-1]
    C1_ZF=0.92
    C2_ZF=0.48
    Alpha_ZF=1.0
    for k in range(0,nRange):
    #    gammadky=gamma_1[k]/kyarr
        gammadky=gamma[0][k]/kyarr
        gamma_temp=list(gamma[0][k]/kyarr)[0:indlowk]
        indkymax=gamma_temp.index(max(gamma_temp))
        kymax=kyarr[indkymax]
        gammadkymax=gammadky[indkymax]
        V_ZF=gammadkymax
        for m in range(indkymax,num_ky):
            Gamma_Stage[k][m]=C1_ZF*kymax*V_ZF+max([gamma[0][k][m]-C1_ZF*kyarr[m]*V_ZF,0])
        for n in range(indkymax,num_ky):
            if indkymax!=0:
                dkyparr=kyarr[indkymax:num_ky]-kyarr[indkymax-1:num_ky-1]
            else:
                dkyparr=kyarr[0:num_ky]-concatenate((array([0]),kyarr[0:num_ky-1]))
            Warr=[WW(kyarr[p],kyarr[n],kyarr,kymax) for p in range(indkymax,num_ky)]
            Gamma_Model[k][n]=sum(dkyparr*Warr*Gamma_Stage[k][indkymax:num_ky])
        for n in range(0,indkymax):
            Gamma_Model[k][n]=max([gamma[0][k][n]-C2_ZF*V_ZF*(kymax-kyarr[n]),0])
########################################
# all the ExB shearing information is get
for k in range(0,nRange):
#    ExBShear[k]=abs(root['OUTPUTSRec']['TGLFOutput'][iview][str(k+1)]['lin']['input.tglf']['VEXB_SHEAR'])
    if root['OUTPUTS'][para][str(Range[k])]['lin'][str(kyarr[0])[0:4]]['input.tglf'].has_key('VEXB_SHEAR'):
        ExBShear[k]=abs(root['OUTPUTS'][para][str(Range[k])]['lin'][str(kyarr[0])[0:4]]['input.tglf']['VEXB_SHEAR'])
    else:
        ExBShear[k] = 0.
    if root['OUTPUTS'][para][str(Range[k])]['lin'][str(kyarr[0])[0:4]]['input.tglf'].has_key('KAPPA_LOC'):
        Kappa[k] = abs(root['OUTPUTS'][para][str(Range[k])]['lin'][str(kyarr[0])[0:4]]['input.tglf']['KAPPA_LOC'])
    else:
        Kappa[k] = 1.
#    Kappa[k]=abs(root['OUTPUTSRec']['TGYROOutput'][iview][k+1]['KAPPA_LOC'])
#    Kappa[k]=abs(root['OUTPUTSRec']['TGLFOutput'][iview][str(k+1)]['lin']['input.tglf']['KAPPA_LOC'])
ExBShear=ExBShear*0.3*sqrt(Kappa)
# based on the profiles we get, then all the linear information can be plotted
figure('micro-turbulence linear stability property',figsize=[12,9])
#lab=['-kd','-ko','-k*','-md','-mo','-m*','-bd','-bo','-b*','-rd','-ro','-r*','-gd','go','-g*']
lab=['-kd','-md','-bd','-rd','-gd','-ko','-mo','-bo','-ro','-go','-k*','-m*','-b*','-r*','-g*'];#       '-ko','-k*','-md','-mo','-m*','-bd','-bo','-b*','-rd','-ro','-r*','-gd','go','-g*']
lw=2
fs1=20
fs2=16
fs3=24
ms=12
pow_kyarr=root['SETTINGS']['PLOTS']['pow_kyarr']
ilogx=root['SETTINGS']['PLOTS']['ilogx']
idimplt=root['SETTINGS']['PLOTS']['idimplt']
ilogplt = 0# decide whether to use logrithm coordinate
ipltExB = 1 
ipltSat1 = 0
imnsExB = root['SETTINGS']['PLOTS']['imnsExB'] # 1:minus ExB; 0: not minus ExB
ipltsx=0  # determine whether plot the Sx value
if ipltsx==1:
    ky_bdry=root['SETTINGS']['PHYSICS']['ky_bdry']
    ind_bdry=find(kyarr>ky_bdry)[0]
    print('ky_bdry=%6.2f'%kyarr[ind_bdry])
indmode=root['SETTINGS']['PLOTS']['indmode']  # index of mode, 0: dominate mode, 1: subdominate mode, 2: subsubdominate mode, etc
subplot(221)
if idimplt==1:
    for k in range(0,nRange):
        if ilogx==1:
            semilogx(kyarr,omega[indmode][k]/kyarr**pow_kyarr,lab[k],linewidth=lw+1)
        else:
            plot(kyarr,omega[indmode][k]/kyarr**pow_kyarr,lab[k],linewidth=lw+1)
#    legend(loc=1,fontsize=fs2).draggable(True)
    xlim([0.8*min(kyarr),1.2*max(kyarr)])
else:
    for k in range(0,num_ky):
        if ilogx==0:
            plot(Range,omega[indmode].T[k]/kyarr[k]**pow_kyarr,lab[k],linewidth=lw+1)
        else:
            semilogx(Range,omega[indmode].T[k]/kyarr[k]**pow_kyarr,lab[k],linewidth=lw+1)
    xlim([0.8*min(Range),1.2*max(Range)])
xticks(fontsize=fs2)
yticks(fontsize=fs2)
if pow_kyarr==1:
    ylabel('$\omega/k_y$',fontsize=fs1)
else:
    ylabel('$\omega$',fontsize=fs1)
subplot(223)
if idimplt==1:
    if ipltExB==1:
        if ilogx==1:
            semilogx(kyarr,ExBShear[k]/kyarr**pow_kyarr,'--r',linewidth=lw,label='$\gamma_{e-eff}$/$k_y$**'+str(pow_kyarr))
        else:
            plot(kyarr,ExBShear[k]/kyarr**pow_kyarr,'--r',linewidth=lw,label='$\gamma_{e-eff}$/$k_y$**'+str(pow_kyarr))
    for k in range(0,nRange):
        if imnsExB == 1:   # the ExB shear is minused
            if ilogx==1:
                semilogx(kyarr,(gamma[indmode][k]-ExBShear[k])/kyarr**pow_kyarr,lab[k],linewidth=lw+1,label=Range[k])
            else:
                plot(kyarr,(gamma[indmode][k]-ExBShear[k])/kyarr**pow_kyarr,lab[k],linewidth=lw+1,label=Range[k])
        else:                 # the ExB shear is not minused
            if ilogx==1:
                semilogx(kyarr,gamma[indmode][k]/kyarr**pow_kyarr,lab[k],linewidth=lw,label=Range[k])
            else:
                plot(kyarr,gamma[indmode][k]/kyarr**pow_kyarr,lab[k],linewidth=lw,label=Range[k])
        if ipltSat1==1:
            if ilogx==1:
                semilogx(kyarr,Gamma_Stage[k]/kyarr**pow_kyarr,lab[k-1],linewidth=lw+1,label='Gamma_Stage/ky^'+str(pow_kyarr))
                semilogx(kyarr,Gamma_Model[k]/kyarr**pow_kyarr,lab[k+1],linewidth=lw+1,label='Gamma_Model/ky^'+str(pow_kyarr))
            else:
                plot(kyarr,Gamma_Stage[k]/kyarr**pow_kyarr,lab[k-1],linewidth=lw+1,label='Gamma_Stage/ky^'+str(pow_kyarr))
                plot(kyarr,Gamma_Model[k]/kyarr**pow_kyarr,lab[k+1],linewidth=lw+1,label='Gamma_Model/ky^'+str(pow_kyarr))
    xlim([0.8*min(kyarr),1.2*max(kyarr)])
    xlabel('$k_y$*$\\rho_s$',fontsize=fs1)
else:  #note at present,if idimplt==0, for converience, ExB shear will not be minused and only gamma (instead of gamma_net) will be plotted
    for k in range(0,num_ky):
        if ilogx==0:
            plot(Range,gamma[indmode].T[k]/kyarr[k]**pow_kyarr,lab[k],linewidth=lw+1,label=kyarr[k])
        else:
            semilogx(Range,gamma[indmode].T[k]/kyarr[k]**pow_kyarr,lab[k],linewidth=lw+1,label=kyarr[k])
    xlim([0.8*min(Range),1.2*max(Range)])
    xlabel(para,fontsize=fs1)
legend(loc=1,fontsize=fs2).draggable(True)
xticks(fontsize=fs2)
yticks(fontsize=fs2)
ylabel('($\gamma$-'+str(imnsExB)+'$\gamma_E$)/ky**'+str(pow_kyarr),fontsize=fs1)
#plot the Sx variation with the parameter scanned
if ipltsx==1:
# calculate the Sx value
    for k in range(0,nRange):
        gammatemp=gamma[indmode][k]-ExBShear[k]
        D_lowk=max(gammatemp[0:ind_bdry]/kyarr[0:ind_bdry])
        D_lowk=max([D_lowk,0])
        D_highk=max(gammatemp[ind_bdry:]/kyarr[ind_bdry:])
        D_highk=max([D_highk,0])
        try:
            S=D_lowk/(D_lowk+D_highk)
        except:
            S=1.
        print(para+':%-6.2e,D_lowk:%-6.2e,D_highk:%-6.2e,S:%-6.2e'%(Range[k],D_lowk,D_highk,S))
        Dlowk_arr[k]=D_lowk
        Dhighk_arr[k]=D_highk
        S_arr[k]=S
    subplot(222)
    plot(Range,Dlowk_arr,'-bo',linewidth=lw+1,markersize=ms,label='lowk')
    plot(Range,Dhighk_arr,'-ro',linewidth=lw+1,markersize=ms,label='highk')
    legend(loc=0,fontsize=fs2).draggable(True)
    xticks(Range,fontsize=fs2)
    yticks(fontsize=fs2)
    ylabel('$\gamma_{net}$',fontsize=fs1)
    #xlabel('$k_y$*$\\rho_s$',fontsize=fs1)
    subplot(224)
    plot(Range,S_arr,'-bo',linewidth=lw,markersize=ms,label='lowk')
    #legend(loc=1,fontsize=fs2).draggable(True)
    xticks(Range,fontsize=fs2)
    yticks(fontsize=fs2)
    ylabel('$Sx$',fontsize=fs1)
    xlabel(para,fontsize=fs1)
    # determine whether to write the omega and gamma_out to a file
    # eigenout is the name of file which to write the eigenfunction
iwritelin=root['SETTINGS']['PLOTS']['iwritelin']
if iwritelin==1 and root['SETTINGS']['DEPENDENCIES'].has_key('linout'):
# recommendation name of linout:tglflin_paraname_otheroption.txt
    eigenout=root['SETTINGS']['DEPENDENCIES']['linout']
    numky=len(kyarr)
    fid = open(eigenout,'w')
# first write the scanned parameter name into the file
    fid.write(para) 
    fid.write('\n')
# write the nRange and the para_val into the file
    fid.write(str(nRange))
    fid.write('\n')
    line=''
    for m in range(nRange):
        line=line+str(Range[m])+'    '
    fid.write(line)
    fid.write('\n')
# write nmodes into the file    
    fid.write(str(nmodes)+'    '+str(numky))
    fid.write('\n')
# write the eigenmodes into the file
# format : row number :numky
# column : ky, ((omega,gamma)*nmodes)*nRange
    for k in range(numky):
        line=str(kyarr[k])
        for p in range(nRange):
            for n in range(nmodes):
#                line=line+'    '+str(w_1[p][k])+'    '+str(gamma_1[p][k])+'    '+str(w_2[p][k])+'    '+str(gamma_2[p][k])
                line=line+'    '+str(omega[n][p][k])+'    '+str(gamma[n][p][k])
        fid.write(line)
        fid.write('\n')
    fid.close()
