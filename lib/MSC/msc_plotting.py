import copy
import datetime as dt 
from matplotlib import colors
import matplotlib.pyplot as plt
import numpy as np
import warnings

from ..general.misc_functions import time_res_f

warnings.filterwarnings("ignore", category=UserWarning, message="no explicit representation of timezones available for np.datetime64")


def plot_msc_l2(msc_dict, ax=None, coords=None, time_res=None, title=None):
    """
    This plots MSC AC magnetic field data as a time series. Each componet of the magnetic field is plotted in the same subpanel. 
    
    Required inputs 
    ---------------------------------------------------------------
    MSC data dictionary generated from MSC_L2 class

    Optional inputs
    ---------------------------------------------------------------
    ax: axis object from matplotlib 
    coords: TSCS or FAC; default is TSCS. FAC often lacks data due to bad attitude solution.
    time_res: Resolution of time ticks. Example input would be time_res='60s'.
    title: Plot title. There is a default plot title, but this keyword allows you to change it.
    """
    spacecraft = msc_dict['spacecraft']
    dt_new = msc_dict['DT'].copy()
    
    if ax is None:
        fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(8,3))

    if coords is None:
        coords = 'tscs'

    if title is None:
        title = f'{spacecraft.upper()} MSC AC Magnetic Field @ 2048 Hz ({coords.upper()} Coords.)'

    var2plot = msc_dict[f'bac_{coords.lower()}']
    ax.plot(msc_dict['DT'], var2plot[:,0],label=r'B$_X$',c='#D81B60')
    ax.plot(msc_dict['DT'], var2plot[:,1], label=r'B$_Y$',c='#1E88E5')
    ax.plot(msc_dict['DT'], var2plot[:,2], label=r'B$_Z$',c='#FFC107')
        
    if time_res is not None:
        ax = time_res_f(ax, dt_new, time_res)
    
    ax.set_xlim([msc_dict['start_time'], msc_dict['end_time']])
    ax.set_ylabel('Magnetic Field [nT]')
    ax.set_title(title)
    ax.legend()


    return ax







def plot_msc_l2_psd(msc_dict, ax=None, cmap='jet', coords='tscs',  component='x', nfft=512, time_res=None, title=None,  stride=int(512/8)):
    """
    This plots MSC AC magnetic field data as power spectral density utilizing a Hanning window FFT.
    
    Required inputs 
    ---------------------------------------------------------------
    MSC data dictionary generated from MSC_L2 class

    Optional inputs
    ---------------------------------------------------------------
    ax: axis object from matplotlib 
    cmap: python colormap; default is jet
    coords: TSCS or FAC; default is TSCS. FAC often lacks data due to bad attitude solution.
    component: name of B field component you wish to plot ('x','y',or 'z'); default is x
    nfft: window size; default is 512 timestamps
    time_res: Resolution of time ticks. Example input would be time_res='60s'.
    title: Plot title. There is a default plot title, but this keyword allows you to change it.
    stride: overlap fraction; default is 7/8
    """


    spacecraft = msc_dict['spacecraft']

    times = msc_dict['UTC']
    win = np.hanning(nfft)
    win = win/(np.mean(win**2))
    ndata = len(times)

    # initializing output arrays for Fast Fourier Transform & new time stamps
    fft = np.zeros([int((ndata-nfft)/stride)+1,nfft,3],dtype=complex)
    t_new = np.zeros([int((ndata-nfft)/stride)+1])

    start = 0 
    end = int(len(times) - nfft)
    
    # -------------------- Fourier transform
    i = 0
    for j in range(start, end, stride):
        for k in range(0,3):
            # FFT of each MSC component
            fft[i,:,k] = np.fft.fft(msc_dict[f'bac_{coords}'][j:(j+nfft),k]*win, norm='forward')
        t_new[i] = (times[j] + times[j+nfft])/2.
        i = i+1
    
    fft = fft[:,0:int(nfft/2),:]

    # -------------------- Getting frequencies
    delta_t = np.median(times[1:len(times)] - times[0:len(times)-1])
    Fsamp = round(1/delta_t)
    freq = np.fft.fftfreq(nfft,d=1/Fsamp)
    freq = freq[0:int(nfft/2)]
    
    while t_new[-1] == 0.0:
        t_new=t_new[0:-1]
        fft = fft[0:-1]

    # ------------------- Computing power spectral density in nT**2/Hz for each component
    power_spectral_density = (np.abs(fft)**2)/(2*freq[1])
    
    # ------------------- Getting plot

    t_new_dt = [dt.datetime.fromtimestamp(x,dt.UTC) for x in t_new] 
    time_xx, frequency_yy = np.meshgrid(t_new_dt, freq)
    
    if ax is None:
        fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(8,3))

    if time_res is not None:
        ax = time_res_f(ax, t_new_dt, time_res)

    if component.lower() == 'x':
        bdata = power_spectral_density[:,:,0]
    if component.lower() == 'y':
        bdata = power_spectral_density[:,:,1]
    if component.lower() == 'z':
        bdata = power_spectral_density[:,:,2]

    cb = ax.pcolormesh(time_xx, frequency_yy, bdata.T, cmap=cmap, norm=colors.LogNorm(vmin=1e-10,vmax=1e-2))
    ax.set_ylabel('Frequency [Hz]')
    plt.colorbar(cb,ax=ax,label=r'Power Spectral Density [nT$^2$/Hz]')
    if title is None:
        ax.set_title(rf'{spacecraft.upper()} Power Spectral Density: B$_{component}$, {coords.upper()}')
    ax.set_xlim([msc_dict['start_time'], msc_dict['end_time']])
    ax.set_ylabel('Frequency [Hz]')


    return ax