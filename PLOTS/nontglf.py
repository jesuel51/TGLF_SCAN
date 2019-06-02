#  this script is used to plot the flux of each species and each modes
#  the parameter and its value is specified by root['SETTINGS']['PHYSICS']['Para'] and root['SETTINGS']['PHYSICS']['nRange'],respectively
#  let's define a function to read the out.tglf.flux_spectrum typefile
def readspectrum(filename):
    f=open(filename,'Ur')
    l=[]
    count=0
    for line in f:
        try:
            case=float(line[0:6])
            l.append(line)
        except:
            count=count+1
    #        print(count)
    col=len(l[0].split())
    row=len(l)
    ll=zeros([row,col])
    count=0
    for item in l:
        ll[count]=[float(item2) for item2 in item.split()]
        count=count+1
    return ll
    f.close()
def readflux(filename):
    f=open(filename,'Ur')
    for line in f:
        flux=[float(item) for item in line.split()]
    return flux
    f.close()
    
para=root['SETTINGS']['PHYSICS']['Para']
Range= root['SETTINGS']['PLOTS']['Range']
ifield=root['SETTINGS']['PLOTS']['ifield']
inputtglf=root['INPUTS']['input.tglf']
# number of species
if inputtglf.has_key('NS'):
    ns = inputtglf['NS']
else:
    ns = 2

nfield=1
if inputtglf['USE_BPER']==True:
    nfield=nfield+1
if inputtglf['USE_BPAR']==True:
    nfield=nfield+1
nRange=len(Range)
fn=root['OUTPUTS'][para][str(Range[0])]['nonlin']['out.tglf.flux_spectrum'].filename
lltemp=readspectrum(fn)
nky=size(lltemp.T[0])/nfield/ns
#nky=len(root['SETTINGS']['SETUP']['kyarr'])
specdata=zeros([nRange,nky*nfield*ns,6])
fluxdata=zeros([nRange,ns*4])
#count=0
for count in range(0,nRange):
    try:
        ll=readspectrum(root['OUTPUTS'][para][str(Range[count])]['nonlin']['out.tglf.flux_spectrum'].filename)
        specdata[count]=ll
        flux=readflux(root['OUTPUTS'][para][str(Range[count])]['nonlin']['out.tglf.gbflux'].filename)
        fluxdata[count]=flux
    except:
        specdata[count]=zeros([nky*nfield*ns,6])
        fluxdata[count]=zeros([ns*4])
#    count=count+1
# plot
#lab=['-kd','-ko','-k*','-ks','-md','-mo','-m*','-ms','-bd','-bo','-b*','-bs','-rd','-ro','-r*','-rs']
lab=['-kd','-md','-bd','-rd','-ko','-mo','-bo','-ro','-k*','-m*','-b*','-r*','-ks','-ms','-bs','-rs',\
     '--k','--m','--b','--r','-k', '-m', '-b', '-r' ]
#ion=['Elec','DT','He','Ar']
ion=['Elec','Ion','He','Ar']
fs1=24
fs2=20
fs3=20
lw=2
#figure('flux for each ky,left(phi contribution),right(B_para contribution)')
# first, let's get the all the flux first
pflux=zeros([nRange,ns,nky*nfield])
Eflux=zeros([nRange,ns,nky*nfield])
TorStrflux=zeros([nRange,ns,nky*nfield])
ParStrflux=zeros([nRange,ns,nky*nfield])
Exchflux=zeros([nRange,ns,nky*nfield])
ra=zeros(nRange)
for k in range(0,nRange):
    ll=specdata[k]
    ky=ll.T[0].reshape(ns,nky*nfield)
    pflux[k]=ll.T[1].reshape(ns,nky*nfield)
    Eflux[k]=ll.T[2].reshape(ns,nky*nfield)
    TorStrflux[k]=ll.T[3].reshape(ns,nky*nfield)
    ParStrflux[k]=ll.T[4].reshape(ns,nky*nfield)
    Exchflux[k]=ll.T[5].reshape(ns,nky*nfield)
# for test, this test shows the total flux is the sum of the flux over the ky
#print(sum(pflux[0][0]))
#print(sum(Eflux[0][0]))
#print(sum(TorStrflux[0][0]))
#print(sum(ParStrflux[0][0]))
# basically, it has been tested that the output flux is the sum over ky
# next ,we should give a summary on the flux, named particle&ion energy&electron energy flux * low-k&high-k&total
ky=ky[0][0:nky]
low_k_bdry = root['SETTINGS']['PHYSICS']['ky_bdry']  # the boundary of index for low-k
ind_low_k_bdry=max(find(ky<low_k_bdry))+0
print('ky_bdry=%5.2f'%ky[ind_low_k_bdry])
P_lowk_arr=zeros(nRange)
P_highk_arr=zeros(nRange)
P_total_arr=zeros(nRange)
Elec_lowk_arr=zeros(nRange)
Elec_highk_arr=zeros(nRange)
Elec_total_arr=zeros(nRange)
Ion_lowk_arr=zeros(nRange)
Ion_highk_arr=zeros(nRange)
Ion_total_arr=zeros(nRange)
TorM_lowk_arr=zeros(nRange)
TorM_highk_arr=zeros(nRange)
TorM_total_arr=zeros(nRange)
# if ifield < 3, only the flux induced by particular field is shown,
# when ifieid>-3, then the total flux(namely, flux induced by phi, A_para, B_para) will be plotted
for k in range(0,nRange):
    print(para+'='+str(Range[k]))
    if ifield<2:
        ifnky=ifield*nky
        p_lowk = sum(pflux[k][0][ifnky:ifnky+ind_low_k_bdry])    # low-k particle contribution
        p_highk = sum(pflux[k][0][ifnky+ind_low_k_bdry:ifnky+nky])    # high-k particle contribution
    #    p_total = sum(pflux[k][0])                     # total particle contribution
        p_total = p_lowk+p_highk                     # total particle contribution
        Elec_lowk = sum(Eflux[k][0][ifnky:ifnky+ind_low_k_bdry]) # low-k electron energy contribution
        Elec_highk = sum(Eflux[k][0][ifnky+ind_low_k_bdry:ifnky+nky]) # high-k electron energy contribution
        Elec_total = Elec_lowk+Elec_highk                  # total electron energy contribution
        Ion_lowk = sum([sum(Eflux[k][m][ifnky:ifnky+ind_low_k_bdry]) for m in range(1,ns)])  # low-k ion energy contribution
        Ion_highk = sum([sum(Eflux[k][m][ifnky+ind_low_k_bdry:ifnky+nky]) for m in range(1,ns)])  # high-k ion energy contribution
        Ion_total = Ion_lowk+Ion_highk     # total ion energy contribution
        TorM_lowk = sum([sum(TorStrflux[k][m][ifnky:ifnky+ind_low_k_bdry]) for m in range(1,ns)])  # low-k Toroidal momentum contribution
        TorM_highk = sum([sum(TorStrflux[k][m][ifnky+ind_low_k_bdry:ifnky+nky]) for m in range(1,ns)])  # high-k Toroidal momentum contribution
    #    TorM_total = sum([sum(TorStrflux[k][m]) for m in range(1,ns)])  # high-k Toroidal momentum contribution
        TorM_total = TorM_lowk+TorM_highk  # total momentum flux
#    print('           low-k        high-k      total      high-k/total(%)')
#    print("particle %-12.2e %-12.2e %-12.2e %-12.2d"%(p_lowk,p_highk,p_total,100*p_highk/p_total))
#    print('electron %-12.2e %-12.2e %-12.2e %-12.2d'%(Elec_lowk,Elec_highk,Elec_total,100*Elec_highk/Elec_total))
#    print('ion      %-12.2e %-12.2e %-12.2e %-12.2d'%(Ion_lowk,Ion_highk,Ion_total,100*Ion_highk/Ion_total))
#    print('TorM     %-12.2e %-12.2e %-12.2e %-12.2d'%(TorM_lowk,TorM_highk,TorM_total,100*TorM_highk/TorM_total))
    else:
        ifnky=ifield*nky
        p_lowk = sum(sum([pflux[k][0][ifnky:ifnky+ind_low_k_bdry] for ifnky in nky*arange(nfield)]))    # low-k particle contribution
        p_highk = sum(sum([pflux[k][0][ifnky+ind_low_k_bdry:ifnky+nky] for ifnky in nky*arange(nfield)]))    # high-k particle contribution
    #    p_total = sum(pflux[k][0])                     # total particle contribution
        p_total = p_lowk+p_highk                     # total particle contribution
        Elec_lowk = sum(sum([Eflux[k][0][ifnky:ifnky+ind_low_k_bdry] for ifnky in nky*arange(nfield)])) 
        Elec_highk = sum(sum([Eflux[k][0][ifnky+ind_low_k_bdry:ifnky+nky] for ifnky in nky*arange(nfield)]))
        Elec_total = Elec_lowk+Elec_highk                  # total electron energy contribution
        Ion_lowk = sum(sum([[sum(Eflux[k][m][ifnky:ifnky+ind_low_k_bdry]) for m in range(1,ns)] for ifnky in nky*arange(nfield)]))  
        Ion_highk = sum(sum([[sum(Eflux[k][m][ifnky+ind_low_k_bdry:ifnky+nky]) for m in range(1,ns)] for ifnky in nky*arange(nfield)]))
        Ion_total = Ion_lowk+Ion_highk     # total ion energy contribution
        TorM_lowk = sum(sum([[sum(TorStrflux[k][m][ifnky:ifnky+ind_low_k_bdry]) for m in range(1,ns)] for ifnky in nky*arange(nfield)]))  # low-k Toroidal momentum contribution
        TorM_highk = sum(sum([[sum(TorStrflux[k][m][ifnky+ind_low_k_bdry:ifnky+nky]) for m in range(1,ns)] for ifnky in nky*arange(nfield)]))  # high-k Toroidal momentum contribution
    #    TorM_total = sum([sum(TorStrflux[k][m]) for m in range(1,ns)])  # high-k Toroidal momentum contribution
        TorM_total = TorM_lowk+TorM_highk  # total momentum flux
    P_lowk_arr[k]=p_lowk
    P_highk_arr[k]=p_highk
    P_total_arr[k]=p_total
    Elec_lowk_arr[k]=Elec_lowk
    Elec_highk_arr[k]=Elec_highk
    Elec_total_arr[k]=Elec_total
    Ion_lowk_arr[k]=Ion_lowk
    Ion_highk_arr[k]=Ion_highk
    Ion_total_arr[k]=Ion_total
    TorM_lowk_arr[k]=TorM_lowk
    TorM_highk_arr[k]=TorM_highk
    TorM_total_arr[k]=TorM_total
# plot the Cases
if ifield == 0:
    figname='$\phi$'
elif ifield ==1 :
    figname='$A_{\para}$'
elif ifield == 2:
    figname='$B_{\para}$'
else:
    figname='sum of all fields'
fig=figure(figsize=[10,10])
fig.canvas.set_window_title(figname)
ms=12
lw=2
fs1=24
fs2=20
ipltlhk=root['SETTINGS']['PLOTS']['ipltlhk']
# when the value of the scanned parameter is bool ,used 0 and 1 to represent false and true
for k in range(0,nRange):
    if Range[k] == True:
        Range[k]=1
    elif Range[k] == False:
        Range[k]=0

subplot(223)
if ipltlhk==1:
    plot(Range,Elec_lowk_arr,'-bo',linewidth=lw,markersize=ms,label='lowk')
    plot(Range,Elec_highk_arr,'-ko',linewidth=lw,markersize=ms,label='highk')
plot(Range,Elec_total_arr,'-ro',linewidth=lw,markersize=ms,label='total')
legend(loc=0,fontsize=fs2).draggable(True)
title('$Q_e$',fontsize=fs1)
#xticks(Range,fontsize=fs2,family='serif')
xticks(fontsize=fs2,family='serif')
yticks(fontsize=fs2,family='serif')
#xlim([0.1,1.2*max(kyarr)])
#ylim([1.e-3,1.e0])
xlabel(para,fontsize=fs1,family='serif')
subplot(224)
if ipltlhk==1:
    plot(Range,Ion_lowk_arr,'-bo',linewidth=lw,markersize=ms,label='lowk')
    plot(Range,Ion_highk_arr,'-ko',linewidth=lw,markersize=ms,label='highk')
plot(Range,Ion_total_arr,'-ro',linewidth=lw,markersize=ms,label='total')
# temporately used
#Qi_exp=root['SETTINGS']['PLOTS']['Qi_exp']
#plot(array([Range[0],Range[-1]]),array([Qi_exp,Qi_exp]),'--r')
legend(loc=0,fontsize=fs2).draggable(True)
title('$Q_i$',fontsize=fs1)
#xticks(Range,fontsize=fs2,family='serif')
xticks(fontsize=fs2,family='serif')
yticks(fontsize=fs2,family='serif')
#xlim([0.1,1.2*max(kyarr)])
#ylim([1.e-3,1.e0])
xlabel(para,fontsize=fs1,family='serif')
subplot(221)
if ipltlhk==1:
    plot(Range,P_lowk_arr,'-bo',linewidth=lw,markersize=ms,label='lowk')
    plot(Range,P_highk_arr,'-ko',linewidth=lw,markersize=ms,label='highk')
plot(Range,P_total_arr,'-ro',linewidth=lw,markersize=ms,label='total')
legend(loc=0,fontsize=fs2).draggable(True)
title('$\Gamma$',fontsize=fs1)
#xticks(Range,fontsize=fs2,family='serif')
xticks(fontsize=fs2,family='serif')
yticks(fontsize=fs2,family='serif')
#xlim([0.1,1.2*max(kyarr)])
#ylim([1.e-3,1.e0])
#xlabel(para,fontsize=fs1,family='serif')
subplot(222)
if ipltlhk==1:
    plot(Range,TorM_lowk_arr,'-bo',linewidth=lw,markersize=ms,label='lowk')
    plot(Range,TorM_highk_arr,'-ko',linewidth=lw,markersize=ms,label='highk')
plot(Range,TorM_total_arr,'-ro',linewidth=lw,markersize=ms,label='total')
legend(loc=0,fontsize=fs2).draggable(True)
title('$\Pi$',fontsize=fs1)
#xticks(Range,fontsize=fs2,family='serif')
xticks(fontsize=fs2,family='serif')
yticks(fontsize=fs2,family='serif')
#xlim([0.1,1.2*max(kyarr)])
#ylim([1.e-3,1.e0])
#xlabel(para,fontsize=fs1,family='serif')
# give a summary print of the total and low-k fluxes
# total flux
print('Range = ',Range)
print('Qe = ',Elec_total_arr)
print('Qi = ',Ion_total_arr)
print('Gamma = ',P_total_arr)
print('Pi = ',TorM_total_arr)
# low-k flux
print('Qe_lowk = ',Elec_lowk_arr)
print('Qi_lowk = ',Ion_lowk_arr)
print('Gamma_lowk = ',P_lowk_arr)
print('Pi_lowk = ',TorM_lowk_arr)

# plot spectrum,note only electronstatic part is plot
ipltEM=0
EMFluxScale=1.e3
# ifield =0: ES, ifield =1, A_para, ifeidl =2 , B_para
#ifield=root['SETTINGS']['PLOTS']['ifield']
fig=figure(figsize=[10,10])
fig.canvas.set_window_title(figname)
subplot(223)
for k in range(0,nRange):
    if ifield<nfield:
        semilogx(ky,Eflux[k][0][ifield*nky:(ifield+1)*nky],lab[k],linewidth=lw,markersize=ms)
    else:
        semilogx(ky,sum([Eflux[k][0][ifield*nky:(ifield+1)*nky] for ifield in arange(nfield)],0),lab[k],linewidth=lw,markersize=ms)
title('$Q_e$',fontsize=fs1)
xticks(fontsize=fs2,family='serif')
yticks(fontsize=fs2,family='serif')
xlim([0.8*ky[0],1.2*ky[-1]])
#ylim([1.e-3,1.e0])
#xlabel(para,fontsize=fs1,family='serif')
xlabel('$k_y\\rho_s$',fontsize=fs1,family='serif')
subplot(224)
for k in range(0,nRange):
    if ifield<nfield:
        semilogx(ky,Eflux[k][1][ifield*nky:(ifield+1)*nky],lab[k],linewidth=lw,markersize=ms,label=str(Range[k]))
    else:
        semilogx(ky,sum([Eflux[k][1][ifield*nky:(ifield+1)*nky] for ifield in arange(nfield)],0),lab[k],linewidth=lw,markersize=ms,label=str(Range[k]))
title('$Q_i$',fontsize=fs1)
xticks(fontsize=fs2,family='serif')
yticks(fontsize=fs2,family='serif')
#xlim([0.1,1.2*ky[-1]])
xlim([0.8*ky[0],1.2*ky[-1]])
legend(loc=0,fontsize=fs2).draggable(True)
#xlim([0.1,1.2*max(kyarr)])
#ylim([1.e-3,1.e0])
xlabel('$k_y\\rho_s$',fontsize=fs1,family='serif')
subplot(221)
for k in range(0,nRange):
    if ifield<nfield:
        semilogx(ky,pflux[k][0][ifield*nky:(ifield+1)*nky],lab[k],linewidth=lw,markersize=ms)
    else:
        semilogx(ky,sum([pflux[k][0][ifield*nky:(ifield+1)*nky] for ifield in arange(nfield)],0),lab[k],linewidth=lw,markersize=ms)
title('$\Gamma$',fontsize=fs1)
xticks(fontsize=fs2,family='serif')
yticks(fontsize=fs2,family='serif')
#xlim([0.1,1.2*ky[-1]])
xlim([0.8*ky[0],1.2*ky[-1]])
#xlim([0.1,1.2*max(kyarr)])
#ylim([1.e-3,1.e0])
#xlabel('ky',fontsize=fs1,family='serif')
subplot(222)
for k in range(0,nRange):
    if ifield<nfield:
        semilogx(ky,TorStrflux[k][1][ifield*nky:(ifield+1)*nky],lab[k],linewidth=lw,markersize=ms)
    else:
        semilogx(ky,sum([TorStrflux[k][1][ifield*nky:(ifield+1)*nky] for ifield in arange(nfield)],0),lab[k],linewidth=lw,markersize=ms)
title('$\Pi_i$',fontsize=fs1)
xticks(fontsize=fs2,family='serif')
yticks(fontsize=fs2,family='serif')
#xlim([0.1,1.2*ky[-1]])
xlim([0.8*ky[0],1.2*ky[-1]])
#xlim([0.1,1.2*max(kyarr)])
#ylim([1.e-3,1.e0])
#xlabel('ky',fontsize=fs1,family='serif')

#================================================================================
# plot the particle flux spectrum



# the format for one line is Gamma_lowk,Gamma_highk,Qe_lowk,Qe_highk,Qi_lowk,Qi_highk,Pi_lowk,Pi_highk
iwriteflux=root['SETTINGS']['PLOTS']['iwriteflux']
if iwriteflux==1:
    fluxout=root['SETTINGS']['DEPENDENCIES']['fluxout']
    fid=open(fluxout,'w')
# firstly write the scanned parameter name into the file
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
# write the number of poloidal modes into the file for flux summation
    fid.write(str(nfield)+'    '+str(nky))
    fid.write('\n')
# both the electrostatic and electromagnetic contribution will be writen
#    for k in range(0,nRange):
#        line=str(root['SETTINGS']['PLOTS']['Range'][k])+'    '+\
#             str(sum(pflux[k][0][0:ind_low_k_bdry]))+'    '+\
#             str(sum(pflux[k][0][ind_low_k_bdry:]))+'    '+\
#             str(sum(Eflux[k][0][0:ind_low_k_bdry]))+'    '+\
#             str(sum(Eflux[k][0][ind_low_k_bdry:]))+'    '+\
#             str(sum([sum(Eflux[k][m][0:ind_low_k_bdry]) for m in range(1,ns)]))+'    '+\
#             str(sum([sum(Eflux[k][m][ind_low_k_bdry:]) for m in range(1,ns)]))+'    '+\
#             str(sum([sum(TorStrflux[k][m][0:ind_low_k_bdry]) for m in range(1,ns)]))+'    '+\
#             str(sum([sum(TorStrflux[k][m][ind_low_k_bdry:]) for m in range(1,ns)]))
# write the flux spectrum into the file
# fromation: row number, nky
# colum: ky, ((pflux,Qe, Qi, Pi)*nmodes)*nRange)
    for k in range(nky):
        line=str(ky[k])
        for p in range(nRange):
            for n in range(nfield):
                line=line+'    '+str(pflux[p][0][k+n*nky])+'    '+\
                                 str(Eflux[p][0][k+n*nky])+'    '+\
                                 str(sum([Eflux[p][m][k+n*nky] for m in range(1,ns)]))+'    '+\
                                 str(sum([TorStrflux[p][m][k+n*nky] for m in range(1,ns)]))
        fid.write(line)
        fid.write('\n')
    fid.close()

