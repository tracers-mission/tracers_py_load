import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from ..general.misc_functions import time_res_f

# -----------------------------------------------------------

def plot_mag_B(mag_dict, ax=None, component_colors=['red','blue','green','black'], b_total=False, time_res=None, title=None):
    """
    Plots each axis of calibrated magnetic field data in a time series.
    
    Required input
    --
    Dictionary output from MAG_L2 loading routine.

    Optional inputs
    --
    ax: Axis object from matplotlib.
    component_colors: List of three colors for each MAG axis to be plotted. If user wishes to plot total
    magnetic field strength, a fourth color code can be added in this list.
    b_total: True or False; indicates if user wants to overplot |B| on magnetic field components.
    time_res:  Resolution of time ticks. Example input would be time_res='60s'.
    title: Title string for plot
    
    """
    coords = mag_dict['B Coordinates'].upper()
    time = mag_dict['DT']

    if ax is None:
        fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(10,3))

    ax.plot(time, mag_dict['Bx'], c=component_colors[0], label='B$_x$')
    ax.plot(time, mag_dict['By'], c=component_colors[1], label='B$_y$')
    ax.plot(time, mag_dict['Bz'], c=component_colors[2], label='B$_z$')
    if b_total is True:
        ax.plot(time, mag_dict['|B|'], c='k', label='|B|')
        
    ax.legend(frameon=False)
    if title is None:
        title = f'TS{mag_dict['spacecraft']} Magnetic Field Data ({coords} Coords.)'
    ax.set_title(title)
    if time_res is not None:
        ax = time_res_f(ax, time, time_res)
    ax.set_ylabel('Magnetic Field [nT]')
    ax.set_xlim([mag_dict['start_time'], mag_dict['end_time']])

    return ax

# -----------------------------------------------------------

def plot_mag_deltaB(mag_dict, ax=None, component_colors=['red','blue','green'], db_total=False, time_res=None, title=None):
    """
    Plots each axis of delta B data in a time series.
    
    Required input
    --
    Dictionary output from MAG_L2 loading routine.

    Optional inputs
    --
    ax: Axis object from matplotlib.
    component_colors: List of three colors for each MAG axis to be plotted. If user wishes to plot total
    deltaB field strength, a fourth color code can be added in this list.
    db_total: True or False; indicates if user wants to overplot |deltaB| on deltaB components.
    time_res:  Resolution of time ticks. Example input would be time_res='60s'.
    title: Title string for plot
    """
    coords = mag_dict['delta_B Coordinates'].upper()
    time = mag_dict['DT']

    if ax is None:
        fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(10,3))

    ax.plot(time, mag_dict['deltaBx'], c=component_colors[0], label=r'$\delta$B$_x$')
    ax.plot(time, mag_dict['deltaBy'], c=component_colors[1], label=r'$\delta$B$_y$')
    ax.plot(time, mag_dict['deltaBz'], c=component_colors[2], label=r'$\delta$B$_z$')
    if db_total is True:
        deltab_total = np.sqrt(mag_dict['deltaBx']**2 + mag_dict['deltaBy']**2 + mag_dict['deltaBz']**2)
        ax.plot(time, deltab_total, c='k', label=r'|$\delta$B|')
        
    ax.legend(frameon=False)
    if title is None:
        title = f'TS{mag_dict['spacecraft']} Magnetic Field Perturbation Data ({coords} Coords.)'
    ax.set_title(title)
    if time_res is not None:
        ax = time_res_f(ax, time, time_res)
    ax.set_ylabel(r'$\delta$B [nT]')
    ax.set_xlim([mag_dict['start_time'], mag_dict['end_time']])    

    return ax

# -----------------------------------------------------------

def plot_TS_pos(mag_dict, ax=None, component_colors=['red','blue','green'], time_res=None, title=None):
    """
    Plots each component of TRACERS position.
    
    Required input
    --
    Dictionary output from MAG_L2 loading routine.

    Optional inputs
    --
    ax: Axis object from matplotlib.
    component_colors: List of three colors for each position component to be plotted.
    time_res:  Resolution of time ticks. Example input would be time_res='60s'.
    title: Title string for plot
    
    """
    coords = mag_dict['Attitude Coordinates'].upper()
    time = mag_dict['DT_1sps']

    if ax is None:
        fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(10,3))

    ax.plot(time, mag_dict['TSx'], c=component_colors[0], label='X')
    ax.plot(time, mag_dict['TSy'], c=component_colors[1], label='Y')
    ax.plot(time, mag_dict['TSz'], c=component_colors[2], label='Z')

        
    ax.legend(frameon=False)
    if title is None:
        title = f'TS{mag_dict['spacecraft']} Position Data ({coords} Coords.)'
    ax.set_title(title)
    if time_res is not None:
        ax = time_res_f(ax, time, time_res)
    ax.set_ylabel('Spacecraft Position [km]')
    ax.set_xlim([mag_dict['start_time'], mag_dict['end_time']])
    
    return ax

# -----------------------------------------------------------

def plot_TS_vel(mag_dict, ax=None, component_colors=['red','blue','green','k'], time_res=None, title=None, v_total=False):
    """
    Plots each component of TRACERS velocity in a time series.
    
    Required input
    --
    Dictionary output from MAG_L2 loading routine.

    Optional inputs
    --
    ax: Axis object from matplotlib.
    component_colors: List of three colors for each velocity component to be plotted. If user wants to overplot speed,
    a fourth color string can be added to this input.
    time_res:  Resolution of time ticks. Example input would be time_res='60s'.
    title: Title string for plot
    v_total: True or False; will overplot speed if user indicates True.
    
    """
    coords = mag_dict['Attitude Coordinates'].upper()
    time = mag_dict['DT_1sps']

    if ax is None:
        fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(10,3))

    ax.plot(time, mag_dict['TSvx'], c=component_colors[0], label='V$_x$')
    ax.plot(time, mag_dict['TSvy'], c=component_colors[1], label='V$_y$')
    ax.plot(time, mag_dict['TSvz'], c=component_colors[2], label='V$_z$')

    if v_total is True:
        speed = np.sqrt(mag_dict['TSvx']**2 + mag_dict['TSvy']**2 + mag_dict['TSvz']**2)
        ax.plot(time, speed, c=component_colors[3], label='|V|')
        
    ax.legend(frameon=False)
    if title is None:
        title = f'TS{mag_dict['spacecraft']} Position Data ({coords} Coords.)'
    ax.set_title(title)
    if time_res is not None:
        ax = time_res_f(ax, time, time_res)
    ax.set_ylabel('Spacecraft Velocity [km/s]')
    ax.set_xlim([mag_dict['start_time'], mag_dict['end_time']])
    
    return ax

# -----------------------------------------------------------

def plot_IGRF(mag_dict, ax=None, component_colors=['red','blue','green'], igrf_total=False, time_res=None, title=None):
    """
    Plots each component of model IGRF in a time series.
    
    Required input
    --
    Dictionary output from MAG_L2 loading routine.

    Optional inputs
    --
    ax: Axis object from matplotlib.
    component_colors: List of three colors for each IGRF component to be plotted. If user wants IGRF magnitude to be overplotted,
    user can add a fourth color string in this argument.
    igrf_total: True or False; will overplot magnitude of IGRF if True.
    time_res:  Resolution of time ticks. Example input would be time_res='60s'.
    title: Title string for plot
    
    """
    coords = mag_dict['Attitude Coordinates'].upper()
    time = mag_dict['DT_1sps']

    if ax is None:
        fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(10,3))

    ax.plot(time, mag_dict['IGRFx'], c=component_colors[0], label='IGRF$_x$')
    ax.plot(time, mag_dict['IGRFy'], c=component_colors[1], label='IGRF$_y$')
    ax.plot(time, mag_dict['IGRFz'], c=component_colors[2], label='IGRF$_z$')

    if igrf_total is True:
        igrft = np.sqrt(mag_dict['IGRFx']**2 + mag_dict['IGRFy']**2 + mag_dict['IGRFz']**2)
        ax.plot(time, igrft, c=component_colors[3], label='|IGRF|')
        
    ax.legend(frameon=False)
    if title is None:
        title = f'TS{mag_dict['spacecraft']} Model IGRF Data ({coords} Coords.)'
    ax.set_title(title)
    if time_res is not None:
        ax = time_res_f(ax, time, time_res)
    ax.set_ylabel('IGRF Magnetic Field [nT]')    
    ax.set_xlim([mag_dict['start_time'], mag_dict['end_time']])
    
    return ax
