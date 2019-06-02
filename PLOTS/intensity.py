# this script is used to plot the fluctuation intensity of 
#(1) electronstatic potential; (2) density ; (3) temperature; (4) crossphase of ne&Te
# for the density and potential fluctuation, only the electron part will be plotted;
# for the cross phase between ne&Te, only the 1st(dominate) mode will be plotted;
# define a function to read all the 4 files, including out.tglf.potential, out.tglf.density_spectrum, out.tglf.temperature_spectrum and out.tglf.nete_crossphase_spectrum
def readspectrum(filename):
# the returned value will be a matrix
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
# in this script, we will not store the data with a array, but read and plot simultaneously
# plot the Cases
lab=['-kd','-md','-bd','-rd','-ko','-mo','-bo','-ro','-k*','-m*','-b*','-r*','-ks','-ms','-bs','-rs']
para=root['SETTINGS']['PHYSICS']['Para']
Range= root['SETTINGS']['PLOTS']['Range']
ns=root['INPUTS']['input.tglf']['NS'] # number of species
figure(figsize=[10,10])
ms=12
lw=2
fs1=24
fs2=20
# plot the potential spectrum
subplot(221)
count=0
for item in Range:
    fn=root['OUTPUTS'][para][str(item)]['nonlin']['out.tglf.potential_spectrum'].filename
    ll=readspectrum(fn)
    semilogx(ll.T[0],ll.T[1],lab[count],linewidth=lw,markersize=ms,label=item)
    count=count+1
title('$\phi$',fontsize=fs1,family='serif')
xticks(fontsize=fs2,family='serif')
yticks(fontsize=fs2,family='serif')
xlim([0.8*ll.T[0][0],1.2*ll.T[0][-1]])
legend(loc=0,fontsize=fs2).draggable(True)
# plot the density spectrum spectrum
subplot(222)
count=0
for item in Range:
    fn=root['OUTPUTS'][para][str(item)]['nonlin']['out.tglf.density_spectrum'].filename
    ll=readspectrum(fn)
    semilogx(ll.T[0],ll.T[1],lab[count],linewidth=lw,markersize=ms,label=item)
    count=count+1
title('$ne$',fontsize=fs1,family='serif')
xticks(fontsize=fs2,family='serif')
yticks(fontsize=fs2,family='serif')
xlim([0.8*ll.T[0][0],1.2*ll.T[0][-1]])
# plot the Te spectrum
subplot(224)
count=0
for item in Range:
    fn=root['OUTPUTS'][para][str(item)]['nonlin']['out.tglf.temperature_spectrum'].filename
    ll=readspectrum(fn)
    semilogx(ll.T[0],ll.T[1],lab[count],linewidth=lw,markersize=ms,label=item)
    count=count+1
title('$Te$',fontsize=fs1,family='serif')
xticks(fontsize=fs2,family='serif')
yticks(fontsize=fs2,family='serif')
xlabel('$k_y$',fontsize=fs1,family='serif')
xlim([0.8*ll.T[0][0],1.2*ll.T[0][-1]])
# plot the crossphase between ne&Te
subplot(223)
count=0
for item in Range:
    fn=root['OUTPUTS'][para][str(item)]['nonlin']['out.tglf.nete_crossphase_spectrum'].filename
    ll=readspectrum(fn)
#    semilogx(ll.T[0],ll.T[1],lab[count],linewidth=lw,markersize=ms,label=item)
    semilogx(ll.T[0],cos(ll.T[1]),lab[count],linewidth=lw,markersize=ms,label=item)
    count=count+1
title('$cos(\delta(ne,Te))$',fontsize=fs1,family='serif')
xticks(fontsize=fs2,family='serif')
yticks(fontsize=fs2,family='serif')
xlabel('$k_y$',fontsize=fs1,family='serif')
xlim([0.8*ll.T[0][0],1.2*ll.T[0][-1]])
