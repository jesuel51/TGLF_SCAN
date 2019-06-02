#  this script focus on the particle flux of each species and each modes
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
lab=['-kd','-md','-bd','-rd','-ko','-mo','-bo','-ro','-k*','-m*','-b*','-r*','-ks','-ms','-bs','-rs']
#ion=['Elec','DT','He','Ar']
species=['e','D','T','He','Ar']
fs1=24
fs2=20
fs3=20
lw=2
#figure('flux for each ky,left(phi contribution),right(B_para contribution)')
# let's get the all the particle flux first
pflux=zeros([nRange,ns,nky*nfield])
ra=zeros(nRange)
for k in range(0,nRange):
    ll=specdata[k]
    ky=ll.T[0].reshape(ns,nky*nfield)
    pflux[k]=ll.T[1].reshape(ns,nky*nfield)
# basically, it has been tested that the output flux is the sum over ky
ky=ky[0][0:nky]
# note the electromagnetic effect can effect the electrostatic flux while the electromagnetic contribution can be quite small;
for k in range(0,nRange):
    p_total = sum(pflux[k][0])                     

print('Range = ',Range)
for isp in range(ns):
    print('$\Gamma_'+species[isp]+'$ = ',[int(1000*sum(pflux[k][isp]))/1.e3 for k in range(0,nRange)])
# plot the Cases
figure(figsize=[12,10])
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
subplot(121)
for isp in range(0,ns):
    plot(Range,[sum(pflux[k][isp]) for k in range(0,nRange)],lab[isp],linewidth=lw,markersize=ms,label=species[isp])
legend(loc=0,fontsize=fs2).draggable(True)
plot(array([Range[0],Range[-1]]),array([0,0]),'--r',linewidth=lw/2.)
title('$particle flux$',fontsize=fs1)
ylabel('$\Gamma/\Gamma_{GB}$',fontsize=fs1,family='serif')
#xticks(Range,fontsize=fs2,family='serif')
xticks(fontsize=fs2,family='serif')
yticks(fontsize=fs2,family='serif')
#xlim([0.1,1.2*max(kyarr)])
#ylim([1.e-3,1.e0])
xlabel(para,fontsize=fs1,family='serif')
subplot(122)
for isp in range(0,ns):
    plot(Range,array([sum(pflux[k][isp]) for k in range(0,nRange)])/inputtglf['AS_'+str(isp+1)],lab[isp],linewidth=lw,markersize=ms,label=species[isp])
plot(array([Range[0],Range[-1]]),array([0,0]),'--r',linewidth=lw/2.)
legend(loc=0,fontsize=fs2).draggable(True)
title('$particle flux/concentration$',fontsize=fs1)
ylabel('$\Gamma/\Gamma_{GB}$',fontsize=fs1,family='serif')
#xticks(Range,fontsize=fs2,family='serif')
xticks(fontsize=fs2,family='serif')
yticks(fontsize=fs2,family='serif')
#xlim([0.1,1.2*max(kyarr)])
#ylim([1.e-3,1.e0])
xlabel(para,fontsize=fs1,family='serif')


# plot spectrum,note only electronstatic part is plot
ipltEM=0
EMFluxScale=1.e3
figure(figsize=[12,8])
subplot(231)
for k in range(0,nRange):
#    semilogx(ky,Eflux[k][0][0:nky],'-bo',linewidth=lw,markersize=ms)
    semilogx(ky,pflux[k][0][0:nky],lab[k],linewidth=lw,markersize=ms)
    # temporaly use for plot the EM contribution
    if ipltEM==1:
        semilogx(ky,EMFluxScale*pflux[k][0][nky:],lab[k+1],linewidth=lw,markersize=ms)
title('$\Gamma_'+species[0]+'$',fontsize=fs1)
xticks(fontsize=fs2,family='serif')
yticks(fontsize=fs2,family='serif')
xlim([0.8*ky[0],1.2*ky[-1]])
#ylim([1.e-3,1.e0])
#xlabel(para,fontsize=fs1,family='serif')
xlabel('$k_y\\rho_s$',fontsize=fs1,family='serif')
subplot(232)
for k in range(0,nRange):
#    semilogx(ky,Eflux[k][1][0:nky],'-bo',linewidth=lw,markersize=ms)
    semilogx(ky,pflux[k][1][0:nky],lab[k],linewidth=lw,markersize=ms,label=str(Range[k]))
    if ipltEM==1:
        semilogx(ky,EMFluxScale*pflux[k][1][nky:],lab[k+1],linewidth=lw,markersize=ms,label='EM contribution')
title('$\Gamma_'+species[1]+'$',fontsize=fs1)
xticks(fontsize=fs2,family='serif')
yticks(fontsize=fs2,family='serif')
#xlim([0.1,1.2*ky[-1]])
xlim([0.8*ky[0],1.2*ky[-1]])
legend(loc=0,fontsize=fs2).draggable(True)
#xlim([0.1,1.2*max(kyarr)])
#ylim([1.e-3,1.e0])
xlabel('$k_y\\rho_s$',fontsize=fs1,family='serif')
subplot(233)
for k in range(0,nRange):
#    semilogx(ky,pflux[k][0][0:nky],'-bo',linewidth=lw,markersize=ms)
    semilogx(ky,pflux[k][2][0:nky],lab[k],linewidth=lw,markersize=ms)
    if ipltEM==1:
        semilogx(ky,EMFluxScale*pflux[k][2][nky:],lab[k+1],linewidth=lw,markersize=ms)
title('$\Gamma_'+species[2]+'$',fontsize=fs1)
xticks(fontsize=fs2,family='serif')
yticks(fontsize=fs2,family='serif')
#xlim([0.1,1.2*ky[-1]])
xlim([0.8*ky[0],1.2*ky[-1]])
#xlim([0.1,1.2*max(kyarr)])
#ylim([1.e-3,1.e0])
#xlabel('ky',fontsize=fs1,family='serif')
subplot(234)
for k in range(0,nRange):
#    semilogx(ky,TorStrflux[k][1][0:nky],'-bo',linewidth=lw,markersize=ms)
    semilogx(ky,pflux[k][3][0:nky],lab[k],linewidth=lw,markersize=ms)
    if ipltEM==1:
        semilogx(ky,EMFluxScale*pflux[k][3][nky:],lab[k+1],linewidth=lw,markersize=ms)
title('$\Gamma_{'+species[3]+'}$',fontsize=fs1)
xticks(fontsize=fs2,family='serif')
yticks(fontsize=fs2,family='serif')
#xlim([0.1,1.2*ky[-1]])
xlim([0.8*ky[0],1.2*ky[-1]])
#xlim([0.1,1.2*max(kyarr)])
#ylim([1.e-3,1.e0])
#xlabel('ky',fontsize=fs1,family='serif')
subplot(235)
for k in range(0,nRange):
#    semilogx(ky,TorStrflux[k][1][0:nky],'-bo',linewidth=lw,markersize=ms)
    semilogx(ky,pflux[k][4][0:nky],lab[k],linewidth=lw,markersize=ms)
    if ipltEM==1:
        semilogx(ky,EMFluxScale*pflux[k][4][nky:],lab[k+1],linewidth=lw,markersize=ms)
title('$\Gamma_{'+species[4]+'}$',fontsize=fs1)
xticks(fontsize=fs2,family='serif')
yticks(fontsize=fs2,family='serif')
#xlim([0.1,1.2*ky[-1]])
xlim([0.8*ky[0],1.2*ky[-1]])


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

