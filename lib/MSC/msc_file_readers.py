import cdflib
import datetime as dt
import numpy as np
import pandas as pd

def read_msc_l2_files(files2load,start=None,end=None):
    """
    This function reads MSC L2 files. Input variable must be a list of files. If loading one single file, you'll have to "listify" it first. 

    Optional inputs
    ---------------------------------------------------------------
    start: start time of observation in datetime timestring format
    end: end time of observation in datetime timestring format (default is to load entire calendar day)
    """
    spacecraft = (files2load[0].split('/')[-1]).split('_')[0]
    data_dict = {'utc':[],'dt':[],'flags':[],'bac_fac':[],\
                'bac_tscs':[]}
    for i in range(len(files2load)):
        msc_file = files2load[i]
        print(msc_file)
        msc_cdf = cdflib.CDF(msc_file)
        
        # Epoch TT2000
        epoch = msc_cdf['Epoch'] # n_times
        
        # Epoch Offset (packets of 1024)
        epoch_offset = msc_cdf['EpochOffset'] # 1024
        
        # AC Magnetic Field (Field Aligned Coordinates)
        bac_fac = msc_cdf[f'{spacecraft}_l2_bac_fac'] # n_times, 1024, 3

        # AC Magnetic Field (TRACERS Spacecraft Coordinates)
        bac_tscs = msc_cdf[f'{spacecraft}_l2_bac_tscs'] # n_times, 1024, 3

        # Flags
        flags = msc_cdf['flags']
        
        # --- Flattening time series since packets are sent down in 1024 ---
        
        msc_times = []
        for k in range(len(epoch)):
            t_off = epoch[k] + epoch_offset
            msc_times.append(t_off)

        # --- Reshaping arrays ---
        
        n_times = len(epoch)
        n_offset = len(epoch_offset)
        n_elem = n_times*n_offset
        
        msc_bac_fac = bac_fac.reshape((n_elem,3))    
        msc_bac_tscs = bac_tscs.reshape((n_elem,3))    
        msc_flat_times = [x for xs in msc_times for x in xs]
        msc_datetimes = cdflib.cdfepoch.to_datetime(msc_flat_times) 
        utcs = cdflib.cdfepoch.unixtime(msc_flat_times)
        dts = [pd.Timestamp(x) for x in msc_datetimes]

        # raw_epoch = cdflib.cdfepoch.to_datetime(epoch)
        # raw_epoch_dt = [pd.Timestamp(x) for x in raw_epoch]
        # raw_epoch_utc = [(x - pd.Timestamp('1970-01-01'))/pd.Timedelta('1s') for x in raw_epoch_dt]

        data_dict['utc'].append(utcs)
        data_dict['dt'].append(dts)
        data_dict['flags'].append(flags)
        data_dict['bac_fac'].append(msc_bac_fac)
        data_dict['bac_tscs'].append(msc_bac_tscs)


    # ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    # RESHAPING ARRAYS BASED ON MULTIPLE FILES  

    n_files = len(files2load)
    t_tot = 0
    t_shapes = []
    for i in range(n_files):
        d2 = np.shape(data_dict['dt'][i])[0]
        t_tot = t_tot + int(d2)
        t_shapes.append(d2)

    times = np.zeros(t_tot)
    bac_tscs_vals = np.zeros((t_tot,3))
    bac_fac_vals = np.zeros((t_tot,3))
    # location_vals = np.zeros((t_tot/1024.,3))
    
    for k in range(n_files):
        if k == 0:
            indices = [0,t_shapes[k]]
        elif k != 0 and k < n_files - 1:
            prior_indices = np.sum(t_shapes[0:k])
            indices = [prior_indices,prior_indices+t_shapes[k]]
        else:
            prior_indices = np.sum(t_shapes[0:k])
            indices = [prior_indices,t_tot]

        times[indices[0]:indices[1]] = data_dict['utc'][k]
        bac_tscs_vals[indices[0]:indices[1],:] = data_dict['bac_tscs'][k]
        bac_fac_vals[indices[0]:indices[1],:] = data_dict['bac_fac'][k]
        
    nan_idx = list(np.where(np.isfinite(times) == False)[0])

    if len(nan_idx) > 0:
        for idx in nan_idx:
            if idx == 0 :
                ii = [idx+1, idx+2]
                time_res = abs(times[ii[1]] - times[ii[0]])
                new_time = times[ii[0]] - time_res
            elif idx != len(data_dict['utc']) - 1:
                ii = [idx-1,idx+2]
                new_time = (times[ii[0]] + times[ii[1]])/2.
            else:
                ii = [idx-2, idx-1]
                time_res = abs(times[ii[1]] - times[ii[0]])
                new_time = times[ii[1]] + time_res                
            times[idx] = new_time 

    if start is None and end is None:
        f_time = (files2load[0].split('v')[0]).split('_')[4]
        start = dt.datetime.strptime(f_time,'%Y%m%d')
        end = start + dt.timedelta(days=1)
    
    if isinstance(start,str):
        dt_fmt = determine_datetime_type(start)
        start = dt.datetime.strptime(start, dt_fmt)
        end = dt.datetime.strptime(end, dt_fmt)

    start_time = (start - dt.datetime(1970,1,1)).total_seconds()
    end_time = (end - dt.datetime(1970,1,1)).total_seconds()
    time_mask = (times >= start_time)&(times <= end_time) 

    msc_dict = {}
    msc_dict['bac_tscs'] = bac_tscs_vals[time_mask,:]
    msc_dict['bac_fac'] = bac_fac_vals[time_mask,:]
    msc_dict['UTC'] = times[time_mask]
    msc_dict['DT'] = []
    for elem in msc_dict['UTC']:
        msc_dict['DT'].append(dt.datetime.fromtimestamp(elem,dt.UTC))
    msc_dict['start_time'] = start
    msc_dict['end_time'] = end
    msc_dict['spacecraft'] = spacecraft    

    return msc_dict

