import colorcet as cc
import copy
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import pandas as pd
from ..general.misc_functions import time_res_f

def plot_aci_l2(aci_dict,anode=None,anode_sum=None,ax=None,cmap=None,echannel=None,\
                energy_avg=None,time_res=None,title=None,units=None,zlim=None):

    """
    Plots ACI L2 data. Required input is ACI data dictionary generated from ACI_L2 or read_aci_l2_files.

    Default is to plot anode-averaged energy spectrogram in units of differential energy flux.

    Optional arguments
    ---------------------------------------------------------------
    anode: index of specific anode to plot. results in energy x time spectrogram for specific ACI anode.
    anode_sum: True or False; will sum over all anodes. default is False.
    ax: axis object. can utilize pre-existing matplotlib.pylot axis object as input, or this routine will generate a new one.
    cmap: colormap name. default is custom soft rainbow.
    echannel: index of energy channel you wish to plot. will generate anode x time series for one energy channel.
    energy_avg: True or False; will average signal over all energy channels for each anode. will output plot
                with anode x time series averaged over all energies.
    time_res: resolution of time ticks (i.e., time_res='60s', time_res='10min')
    title: user input title of the axis object
    units: units to load ('counts' or 'def'; default is 'def' [eV/(eV cm2 s sr)])
    zlim: limit of colorbar on spectrograph. calculated by default but can be changed by user (e.g., zlim=[1e5,1e0])
    
    """
    spacecraft = aci_dict['spacecraft']
    if units is None:
        units = 'def'
    
    if units.lower() == 'def':
        particle_data = aci_dict['def']

    if cmap is None:
        cmap = cc.cm['CET_R3']
    else:
        cmap = plt.get_cmap(cmap)
    
    cmap = copy.copy(cmap)
    cmap.set_under('black')


    # +++++++++++++++++++++++++++++++++++++++++++++++
    # fills in periods when data aren't available so plotting looks normal
    total_times = len(aci_dict['UTC'])
    tdiff = pd.Series(aci_dict['UTC']).diff()

    time_jumps = np.where(tdiff > 40)[0] # greater than back orbit difference indicates missing data

    if len(time_jumps) > 0:
        new_utcs = []
        new_pd = []
        list_shapes = []
        for q in range(len(time_jumps)):
            jump_idx = time_jumps[q]
            prior_res = round(np.mean(tdiff[jump_idx-2:jump_idx]),2)
            bounding_times = [aci_dict['DT'][jump_idx - 1], aci_dict['DT'][jump_idx + 1]]            
            filler_times = pd.date_range(bounding_times[0], bounding_times[1], freq=f'{prior_res}s', tz='UTC')
            new_filler_times = pd.DataFrame({'date': filler_times[1:-1]})
            new_utc_fillers = new_filler_times['date'].sub(pd.Timestamp(0,tz='UTC')).dt.total_seconds()
            new_utcs.append(new_utc_fillers)
    
            if q == 0 :
                pd_sub = particle_data[0:jump_idx,:,:]
                new_pd.append(pd_sub)
                new_pd.append(np.zeros((len(new_utc_fillers),47,16)))
                list_shapes.append(np.shape(pd_sub)[0])
                list_shapes.append(len(new_utc_fillers))

                if len(time_jumps) == 1:
                    pd_sub = particle_data[jump_idx:,:,:]
                    new_pd.append(pd_sub)
                    list_shapes.append(np.shape(pd_sub)[0])

                
            elif q != 0 and q < len(time_jumps)-1:
                pd_sub = particle_data[time_jumps[q-1]:time_jumps[q],:,:]
                new_pd.append(pd_sub)
                new_pd.append(np.zeros((len(new_utc_fillers),47,16)))
                list_shapes.append(np.shape(pd_sub)[0])
                list_shapes.append(len(new_utc_fillers))
            else:
                pd_sub1 = particle_data[time_jumps[q-1]:time_jumps[q],:,:]
                new_pd.append(pd_sub1)
                new_pd.append(np.zeros((len(new_utc_fillers),47,16)))    
                pd_sub2 = particle_data[jump_idx:,:,:]
                new_pd.append(pd_sub2)
                list_shapes.append(np.shape(pd_sub1)[0])
                list_shapes.append(len(new_utc_fillers))
                list_shapes.append(np.shape(pd_sub2)[0])

        flat_utcs = np.array([x for xs in new_utcs for x in xs])
        all_utcs = np.sort(np.concatenate([aci_dict['UTC'], flat_utcs], axis=0))
        dt_new = []
        for elem in all_utcs:
            dt_new.append(dt.datetime.fromtimestamp(elem,dt.UTC))    

        particle_data_new = np.zeros((len(all_utcs),47,16))
        for k in range(len(list_shapes)):
            if len(list_shapes) > 2:
                if k == 0:
                    indices = [0,list_shapes[k]]
                elif k != 0 and k < len(list_shapes)-1:
                    prior_indices = np.sum(list_shapes[0:k])
                    indices = [prior_indices, prior_indices + list_shapes[k]]
                else:
                    prior_indices = np.sum(list_shapes[0:k])
                    indices = [prior_indices, len(all_utcs)]
            else:
                if k == 0:
                    indices = [0,list_shapes[k]]
                else:
                    prior_indices = np.sum(list_shapes[0:k])
                    indices = [prior_indices, prior_indices + list_shapes[k]]             
            particle_data_new[indices[0]:indices[1],:,:] = new_pd[k]

    else:
        particle_data_new = particle_data.copy()
        dt_new = aci_dict['DT'].copy()
    # +++++++++++++++++++++++++++++++++++++++++++++++

        
    if ax is None:
        fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(8,3))

    if echannel is not None and anode is None:
        particle_data_new = particle_data_new[:,echannel,:]
        e_val = aci_dict['energy'][echannel]
        yvar = aci_dict['anode']
        ylabel = 'Anode [degrees]'
        xx, yy = np.meshgrid(dt_new, aci_dict['anode'])
        plot_title = f'{spacecraft.upper()} ACI L2 Data, E{echannel} ({e_val:.2f} eV)'
        yscale = 'linear'
        if units.lower() == 'def':
            unit_label = 'Differential Energy Flux\n'+r'[eV/(eV cm$^2$ s sr)]'

        
    elif echannel is None and anode is not None:
        particle_data_new = particle_data_new[:,:,anode]
        yvar = aci_dict['energy']
        a_val = aci_dict['anode'][anode]
        ylabel = 'Energy [eV]'
        xx, yy = np.meshgrid(dt_new, aci_dict['energy'])
        plot_title = f'{spacecraft.upper()} ACI L2 Data, A{anode} ({a_val:.0f} degrees)'   
        yscale = 'log'
        if units.lower() == 'def':
            unit_label = 'Differential Energy Flux\n'+r'[eV/(eV cm$^2$ s sr)]'

        
    elif anode_sum is True:
        dphi = np.deg2rad(10)
        dtheta = -np.cos(np.deg2rad(93.5)) + np.cos(np.deg2rad(86.5))
        domega = dphi*dtheta
        solid_angle = np.ones((np.shape(particle_data)))*domega

        particle_data_new = np.nansum(particle_data_new*solid_angle, axis=2)
        xx, yy = np.meshgrid(dt_new, aci_dict['energy'])
        plot_title = f'{spacecraft.upper()} ACI L2 Angle-Integrated Data'
        ylabel = 'Energy [eV]'
        yscale = 'log'
        if units.lower() == 'def':
            unit_label = 'Angle-Integrated\nDifferential Energy Flux\n'+r'[eV/(eV cm$^2$ s)]'

    elif energy_avg is True:
        particle_data_new = np.nanmean(particle_data_new, axis=1)
        xx, yy = np.meshgrid(dt_new, aci_dict['anode'])
        plot_title = f'{spacecraft.upper()} ACI L2 Energy-Averaged Data'
        ylabel = 'Anode [degrees]'
        yscale = 'linear'    
        if units.lower() == 'def':
            unit_label = 'Differential Energy Flux\n'+r'[eV/(eV cm$^2$ sr s)]'
     
    else:
        particle_data_new = np.nanmean(particle_data_new, axis=2)
        xx, yy = np.meshgrid(dt_new, aci_dict['energy'])
        plot_title = f'{spacecraft.upper()} ACI L2 Angle-Averaged Data'
        ylabel = 'Energy [eV]'
        yscale = 'log'
        if units.lower() == 'def':
            unit_label = 'Differential Energy Flux\n'+r'[eV/(eV cm$^2$ s sr)]'


    if time_res is not None:
        ax = time_res_f(ax, dt_new, time_res)

    if zlim is not None:
        min_c = zlim[0]
        max_c = zlim[1]
    else:
        gtz = np.where(particle_data_new.flatten() > 0)[0]
        max_c = np.nanmax(particle_data_new.flatten()[gtz])
        min_c = np.nanmin(particle_data_new.flatten()[gtz])

    if title is not None:
        plot_title = title
    im = ax.pcolormesh(xx, yy, particle_data_new.T, cmap=cmap,shading='nearest',\
                  norm=colors.LogNorm(vmin=0.9*min_c,vmax=1.1*max_c))
    cbax = ax.inset_axes([1.02,0,0.03,1],transform=ax.transAxes)
    cb = plt.colorbar(im, cax=cbax, label=unit_label)
    ax.set_xlim([aci_dict['start_time'], aci_dict['end_time']])
    ax.set_ylabel(ylabel)
    ax.set_title(plot_title)
    ax.set_yscale(yscale)

    return ax
