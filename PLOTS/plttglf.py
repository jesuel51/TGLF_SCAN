# this script is used to plot both the linear and nonlinear property of tglf results
plots=root['SETTINGS']['PLOTS']
if plots['mode']=='lin':
    root['PLOTS']['lintglf.py'].run()
else:
    root['PLOTS']['nontglf.py'].run()
