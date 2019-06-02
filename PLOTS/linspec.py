# this script is used to read the ouputfile of nonlinear run out.tglf.eigenvalue_spectrum
# this file stores the linear result, including of frequency and growth rate of each mode
# define a function a read the file out.tglf.eigenvalue_spectrum
def readspectrum(filename):
# nmode means the number of modes for each ky
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

# have the parameter
para=root['SETTINGS']['PHYSICS']['Para']
Range= root['SETTINGS']['PLOTS']['Range']
inputtglf=root['INPUTS']['input.tglf']
# read the file
nrange=len(Range)
fn_temp=root['OUTPUTS'][para][str(Range[0])]['nonlin']['out.tglf.eigenvalue_spectrum'].filename
data_temp=readspectrum(fn_temp)
kyarr=data_temp.T[0]
numky=len(kyarr)
omega_1=zeros([nrange,numky])
omega_2=zeros([nrange,numky])
gamma_1=zeros([nrange,numky])
gamma_2=zeros([nrange,numky])
for count in range(0,nrange):
    ll=readspectrum(root['OUTPUTS'][para][str(Range[count])]['nonlin']['out.tglf.eigenvalue_spectrum'].filename)
    omega_1[count]=ll.T[2]
    gamma_1[count]=ll.T[1]
    omega_2[count]=ll.T[4]
    gamma_2[count]=ll.T[3]

# let's plot, we will plot the frequency&growth rate dominate and subdominate mode 
lab=['-kd','-md','-bd','-rd','-ko','-mo','-bo','-ro','-k*','-m*','-b*','-r*','-ks','-ms','-bs','-rs']
fs1=24
fs2=20
fs3=20
lw=2
ms=6
figure(figsize=[10,10])
subplot(221)
for k in range(0,nrange):
    semilogx(kyarr,omega_1[k]/kyarr,lab[k],linewidth=lw,markersize=ms,label=str(Range[k]))
title('dominate mode',fontsize=fs1,family='serif')
ylabel('$\omega/ky$',fontsize=fs2,family='serif')
xticks(fontsize=fs2,family='serif')
yticks(fontsize=fs2,family='serif')
legend(loc=0,fontsize=fs2).draggable(True)
subplot(223)
for k in range(0,nrange):
    semilogx(kyarr,gamma_1[k]/kyarr,lab[k],linewidth=lw,markersize=ms)
#title('dominate mode',fontsize=fs1,family='serif')
ylabel('$\gamma/ky$',fontsize=fs2,family='serif')
xticks(fontsize=fs2,family='serif')
yticks(fontsize=fs2,family='serif')
xlabel('$k_y\\rho_s$',fontsize=fs2,family='serif')
subplot(222)
for k in range(0,nrange):
    semilogx(kyarr,omega_2[k]/kyarr,lab[k],linewidth=lw,markersize=ms)
title('subdominate mode',fontsize=fs1,family='serif')
#ylabel('$\omega$',fontsize=fs2,family='serif')
xticks(fontsize=fs2,family='serif')
yticks(fontsize=fs2,family='serif')
subplot(224)
for k in range(0,nrange):
    semilogx(kyarr,gamma_2[k]/kyarr,lab[k],linewidth=lw,markersize=ms)
#title('dominate mode',fontsize=fs1,family='serif')
#ylabel('$\gamma$',fontsize=fs2,family='serif')
xticks(fontsize=fs2,family='serif')
yticks(fontsize=fs2,family='serif')
xlabel('$k_y\\rho_s$',fontsize=fs2,family='serif')
