# this script is used to plot the scanned result
# the function defined below is used to read the output of tglf linear run, the 2 most unstable mode
def readfile(filename):
    count=0
    w=zeros([2,2])
    f=open(filename,'Ur')
    for line in f:
        if line.find('(wr,wi)')!=-1:
            temp=line.split()
            w[count][0]=temp[1]
            w[count][1]=temp[2]
            count=count+1
    return w
    f.close()
# define a function to calcualte the relative change of an array
def rltvchg(farr):
    farrmax=max(farr)
    farrmin=min(farr)
    chg=(farrmax-farrmin)/mean(farr)
    return int(100*chg)
Para=root['SETTINGS']['PLOTS']['Para']
mode=root['SETTINGS']['PLOTS']['mode']
Scalefactor=root['OUTPUTScan'][Para][mode].keys()
Scalefactor=[float(item) for item in Scalefactor]
nscale=len(Scalefactor)
paraextend=['RLNS','VPAR','VPAR_SHEAR','VTS_SHEAR']
if Para in paraextend:
    Para=Para+'_1'
para_orig=root['INPUTS']['input.tglf'][Para]
Para_rang=para_orig*array(Scalefactor)
#print(Para_rang)
#print(para_orig*Scalefactor)
# nonlinear properties
pfluxe=zeros(nscale)           # electron particle flux
Eflux_elec_lowk=zeros(nscale)  # lowk electron energy flux
Eflux_elec_highk=zeros(nscale) # highk electron energy flux
Eflux_elec_total=zeros(nscale) # total electron energy flux
Eflux_ion_lowk=zeros(nscale)   # lowk ion energy flux
Eflux_ion_highk=zeros(nscale)  # highk ion energy flux
Eflux_ion_total=zeros(nscale)  # total ion energy flux
mflux=zeros(nscale)  # momentum flux
# linear properties
wr=zeros([nscale,2])
wi=zeros([nscale,2])
count=0
n_null=[]
mode = root['SETTINGS']['PLOTS']['mode']
for item in Scalefactor:
    item=str(item)[0:4]
    try:
        if mode=='nonlin':
            data=root['OUTPUTScan'][Para][mode][item]['out.tglf.run']['data']
            pfluxe[count]=data['Gam/Gam_GB'][0]
            Eflux_elec_total[count]=data['Q/Q_GB'][0]
            Eflux_elec_lowk[count]=data['Q_low/Q_GB'][0]
            Eflux_elec_highk[count]=Eflux_elec_total[count]-Eflux_elec_lowk[count]
#            Eflux_ion_total=data['Q/Q_GB'][1]+data['Q/Q_GB'][2]+data['Q/Q_GB'][3]
            Eflux_ion_total[count]=sum(data['Q/Q_GB'][1:])
            Eflux_ion_lowk[count]=sum(data['Q_low/Q_GB'][1:])
            Eflux_ion_highk[count]=Eflux_ion_total[count]-Eflux_ion_lowk[count]
            mflux[count]=data['Pi/Pi_GB'][0]+ data['Pi/Pi_GB'][1]+data['Pi/Pi_GB'][2]+data['Pi/Pi_GB'][3]
        else:
            fn=root['OUTPUTScan'][Para][mode][item]['out.tglf.run'].filename
            w=readfile(fn)
            wr[count]=w.T[0]
            wi[count]=w.T[1]
#            print(wr[count])
            if wr[count][0]==0:
                n_null=n_null+[count]
    except:
        if count not in n_null:
            n_null=n_null+[count]
    finally:
        count=count+1
def delarr(X,num):
    X=list(X)
    for m in range(0,len(num)):
        del X[num[m]-m]
    X=array(X)
    return X
def delarr2D(X,num):
    col=size(X,1)
    row=size(X,0)
    XX=[]
    for k in range(0,col):
        Xk=list(X.T[k])
        for m in range(0,len(num)):
            del Xk[num[m]-m]
        XX.append(Xk)
    XX=array(XX)
    XX=reshape(XX,(col,row-len(num)))
    XX=XX.T
    return XX
print(n_null)
if mode=='nonlin':
    pfluxe=delarr(pfluxe,n_null)
    Eflux_elec_total=delarr(Eflux_elec_total,n_null)
    Eflux_elec_lowk=delarr(Eflux_elec_lowk,n_null)
    Eflux_elec_highk=delarr(Eflux_elec_highk,n_null)
    Eflux_ion_total=delarr(Eflux_ion_total,n_null)
    Eflux_ion_lowk=delarr(Eflux_ion_lowk,n_null)
    Eflux_ion_highk=delarr(Eflux_ion_highk,n_null)
    mflux=delarr(mflux,n_null)
else:
    wr=delarr2D(wr,n_null)
    wi=delarr2D(wi,n_null)
Para_rang=delarr(Para_rang,n_null)
#print(wr)
Scalefactor=delarr(Scalefactor,n_null)
figure('scan '+Para,figsize=[14,12])
fs1=32
fs2=24
lw=6
ms=12
ilogxplt=root['SETTINGS']['PLOTS']['ilogxplt']
ilogyplt=root['SETTINGS']['PLOTS']['ilogyplt']
if mode=='nonlin':
    subplot(2,2,1)
    if ilogxplt==1:
        if ilogyplt==1:
            loglog(Para_rang,pfluxe,'-ro',linewidth=lw,markersize=ms,label='$\delta$='+str(rltvchg(pfluxe)/100.))
        else:
            semilogx(Para_rang,pfluxe,'-ro',linewidth=lw,markersize=ms,label='$\delta$='+str(rltvchg(pfluxe)/100.))
    else: 
        if ilogyplt==1:
            semilogy(Para_rang,pfluxe,'-ro',linewidth=lw,markersize=ms,label='$\delta$='+str(rltvchg(pfluxe)/100.))
        else:
            plot(Para_rang,pfluxe,'-ro',linewidth=lw,markersize=ms,label='$\delta$='+str(rltvchg(pfluxe)/100.))
    #semilogx(Scalefactor,pfluxe,'-ro',linewidth=lw,markersize=ms)
#    xlabel(Para,fontsize=fs1,family='serif')
    #xlabel('ScaleFactor',fontsize=fs1)
#    title('Electron particle flux-GB',fontsize=fs1,family='serif')
    title('(a)$\Gamma_e$',fontsize=fs1,family='serif')
    xticks(fontsize=fs2,family='serif')
    yticks(fontsize=fs2,family='serif')
    legend(loc=0,fontsize=fs2).draggable(True)
    subplot(2,2,2)
    if ilogxplt==1:
        if ilogyplt==1:
            loglog(Para_rang,Eflux_elec_total,'-ro',linewidth=lw,markersize=ms,label='total $\delta$='+str(rltvchg(Eflux_elec_total)/100.))
            loglog(Para_rang,Eflux_elec_lowk,'-bo',linewidth=lw,markersize=ms,label='low-k $\delta$='+str(rltvchg(Eflux_elec_lowk)/100.))
            loglog(Para_rang,10.*Eflux_elec_highk,'-ko',linewidth=lw,markersize=ms,label='high-k $\delta$='+str(rltvchg(Eflux_elec_lowk)/100.))
        else:
            semilogx(Para_rang,Eflux_elec_total,'-ro',linewidth=lw,markersize=ms,label='total $\delta$='+str(rltvchg(Eflux_elec_total)/100.))
            semilogx(Para_rang,Eflux_elec_lowk,'-bo',linewidth=lw,markersize=ms,label='low-k $\delta$='+str(rltvchg(Eflux_elec_lowk)/100.))
            semilogx(Para_rang,10*Eflux_elec_highk,'-ko',linewidth=lw,markersize=ms,label='high-k $\delta$='+str(rltvchg(Eflux_elec_highk)/100.))
    else:
        if ilogyplt==1:
            semilogy(Para_rang,Eflux_elec_total,'-ro',linewidth=lw,markersize=ms,label='total $\delta$='+str(rltvchg(Eflux_elec_total)/100.))
            semilogy(Para_rang,Eflux_elec_lowk,'-bo',linewidth=lw,markersize=ms,label='lowk $\delta$='+str(rltvchg(Eflux_elec_lowk)/100.))
            semilogy(Para_rang,10*Eflux_elec_highk,'-ko',linewidth=lw,markersize=ms,label='highk $\delta$='+str(rltvchg(Eflux_elec_highk)/100.))
        else:
            plot(Para_rang,Eflux_elec_total,'-ro',linewidth=lw,markersize=ms,label='total $\delta$='+str(rltvchg(Eflux_elec_total)/100.))
            plot(Para_rang,Eflux_elec_lowk,'-bo',linewidth=lw,markersize=ms,label='lowk $\delta$='+str(rltvchg(Eflux_elec_lowk)/100.))
            plot(Para_rang,10*Eflux_elec_highk,'-ko',linewidth=lw,markersize=ms,label='10*highk $\delta$='+str(rltvchg(Eflux_elec_highk)/100.))
    legend(loc=0,fontsize=fs2).draggable(True)
    #semilogx(Scalefactor,eflux,'-bo',linewidth=lw,markersize=ms)
#    xlabel(Para,fontsize=fs1,family='serif')
    xticks(fontsize=fs2,family='serif')
    yticks(fontsize=fs2,family='serif')
#    title('Energy energy flux',fontsize=fs1,family='serif')
    title('(b)$Q_e$',fontsize=fs1,family='serif')
    subplot(2,2,4)
    if ilogxplt==1:
        if ilogyplt==1:
            loglog(Para_rang,Eflux_ion_total,'-ro',linewidth=lw,markersize=ms,label='total $\delta$='+str(rltvchg(Eflux_ion_total)/100.))
            loglog(Para_rang,Eflux_ion_lowk,'-bo',linewidth=lw,markersize=ms,label='low-k $\delta$='+str(rltvchg(Eflux_ion_lowk)/100.))
 #           loglog(Para_rang,Eflux_ion_highk,'-ko',linewidth=lw,markersize=ms,label='high-k')
        else:
            semilogx(Para_rang,Eflux_ion_total,'-ro',linewidth=lw,markersize=ms,label='total $\delta$='+str(rltvchg(Eflux_ion_total)/100.))
            semilogx(Para_rang,Eflux_ion_lowk,'-bo',linewidth=lw,markersize=ms,label='low-k $\delta$='+str(rltvchg(Eflux_ion_lowk)/100.))
 #           semilogx(Para_rang,Eflux_ion_total,'-ko',linewidth=lw,markersize=ms,label='high-k')
    else:
        if ilogyplt==1:
            semilogy(Para_rang,Eflux_ion_total,'-ro',linewidth=lw,markersize=ms,label='total $\delta$='+str(rltvchg(Eflux_ion_total)/100.))
            semilogy(Para_rang,Eflux_ion_lowk,'-bo',linewidth=lw,markersize=ms,label='lowk $\delta$='+str(rltvchg(Eflux_ion_lowk)/100.))
 #           semilogy(Para_rang,Eflux_ion_highk,'-ko',linewidth=lw,markersize=ms,label='highk')
        else:
            plot(Para_rang,Eflux_ion_total,'-ro',linewidth=lw,markersize=ms,label='total $\delta$='+str(rltvchg(Eflux_ion_total)/100.))
            plot(Para_rang,Eflux_ion_lowk,'-bo',linewidth=lw,markersize=ms,label='lowk $\delta$='+str(rltvchg(Eflux_ion_lowk)/100.))
 #           plot(Para_rang,Eflux_ion_highk,'-ko',linewidth=lw,markersize=ms,label='highk')
    legend(loc=0,fontsize=fs2).draggable(True)
    #semilogx(Scalefactor,eflux,'-bo',linewidth=lw,markersize=ms)
    xlabel(Para,fontsize=fs1,family='serif')
    xticks(fontsize=fs2,family='serif')
    yticks(fontsize=fs2,family='serif')
#    title('Ion energy flux',fontsize=fs1,family='serif')
    title('(d)$Q_i$',fontsize=fs1,family='serif')
    subplot(2,2,3)
    if ilogxplt==1:
        if ilogyplt==1:
            loglog(Para_rang,mflux,'-ro',linewidth=lw,markersize=ms,label='$\delta$='+str(rltvchg(mflux)/100.))
        else:
            semilogx(Para_rang,mflux,'-ro',linewidth=lw,markersize=ms,label='$\delta$='+str(rltvchg(mflux)/100.))
    else:
        if ilogyplt==1:
            semilogy(Para_rang,mflux,'-ro',linewidth=lw,markersize=ms,label='$\delta$='+str(rltvchg(mflux)/100.))
        else:
            plot(Para_rang,mflux,'-ro',linewidth=lw,markersize=ms,label='$\delta$='+str(rltvchg(mflux)/100.))
    #semilogx(Scalefactor,mflux,'-mo',linewidth=lw,markersize=ms)
#    title('Total momentum flux',fontsize=fs1,family='serif')
    title('(c)$\Pi$',fontsize=fs1,family='serif')
    xlabel(Para,fontsize=fs1,family='serif')
    xticks(fontsize=fs2,family='serif')
    yticks(fontsize=fs2,family='serif')
    legend(loc=0,fontsize=fs2).draggable(True)
else:
    subplot(1,2,1)
    if ilogxplt==1:
        if ilogyplt==1:
	    loglog(Para_rang,wr.T[0],'-ro',linewidth=lw,markersize=ms,label='$\omega-\delta$='+str(rltvchg(wr.T[0])/100.))
#	    loglog(Para_rang,wr.T[1],'-bo',linewidth=lw,markersize=ms,label='wr-second most unstable')
        else:
            semilogx(Para_rang,wr.T[0],'-ro',linewidth=lw,markersize=ms,label='$\omega-\delta$='+str(rltvchg(wr.T[0])/100.))
#            semilogx(Para_rang,wr.T[1],'-bo',linewidth=lw,markersize=ms,label='wr-second most unstable')
    else:
        if ilogyplt==1:
            semilogy(Para_rang,wr.T[0],'-ro',linewidth=lw,markersize=ms,label='$\omega-\delta$='+str(rltvchg(wr.T[0])/100.))
#            semilogy(Para_rang,wr.T[1],'-bo',linewidth=lw,markersize=ms,label='wr-second most unstable')
        else:
            plot(Para_rang,wr.T[0],'-ro',linewidth=lw,markersize=ms,label='$\omega\delta$='+str(rltvchg(wr.T[0])/100.))
#            plot(Para_rang,wr.T[1],'-bo',linewidth=lw,markersize=ms,label='wr-second most unstable')
    legend(loc=0,fontsize=fs2).draggable(True)
    xlabel(Para,fontsize=fs2,family='serif')
    xticks(fontsize=fs2,family='serif')
    yticks(fontsize=fs2,family='serif')
    subplot(1,2,2)
    if ilogxplt==1:
        if ilogyplt==1:
            loglog(Para_rang,wi.T[0],'-ro',linewidth=lw,markersize=ms,label='wi-most unstable $\delta$='+str(rltvchg(wi.T[0])/100.))
#            loglog(Para_rang,wi.T[1],'-bo',linewidth=lw,markersize=ms,label='wi-second most unstable')
        else:
            semilogx(Para_rang,wi.T[0],'-ro',linewidth=lw,markersize=ms,label='wi-most unstable $\delta$='+str(rltvchg(wi.T[0])/100.))
#            semilogx(Para_rang,wi.T[1],'-bo',linewidth=lw,markersize=ms,label='wi-second most unstable')
    else:
        if ilogyplt==1:
            semilogy(Para_rang,wi.T[0],'-ro',linewidth=lw,markersize=ms,label='wi-most unstable $\delta$='+str(rltvchg(wi.T[0])/100.))
#            semilogy(Para_rang,wi.T[1],'-bo',linewidth=lw,markersize=ms,label='wi-second most unstable')
        else:
#            plot(Para_rang,wi.T[0],'-ro',linewidth=lw,markersize=ms,label='wi-most unstable $\delta$='+str(rltvchg(pfluxe)/100.))
            plot(Para_rang,wi.T[0],'-ro',linewidth=lw,markersize=ms,label='$\gamma \delta$='+str(rltvchg(wi.T[0])/100.))
#            plot(Para_rang,wi.T[1],'-bo',linewidth=lw,markersize=ms,label='wi-second most unstable')
    legend(loc=0,fontsize=fs2).draggable(True)
    xlabel(Para,fontsize=fs2,family='serif')
    xticks(fontsize=fs2,family='serif')
    yticks(fontsize=fs2,family='serif')
