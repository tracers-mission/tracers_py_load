import copy
import matplotlib.pyplot as plt
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