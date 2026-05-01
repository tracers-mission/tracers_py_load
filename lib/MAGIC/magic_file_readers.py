import cdflib
import datetime as dt
import numpy as np
import pandas as pd
from lib.general.misc_functions import determine_datetime_type 


def read_magic_l2_files(files2load,start=None,end=None):
    sc = (files2load[0].split('/')[-1]).split('_')[0]
    data_dict = {'utc':[],'dt':[],'flags':[],'bdc_gei2000':[],\
                'bdc_magic':[],'bdc_nec':[]}
    for i in range(len(files2load)):
        magic_file = files2load[i]
        print(magic_file)
        magic_cdf = cdflib.CDF(magic_file)
        
        # Epoch TT2000
        epoch = magic_cdf['Epoch'] # n_times
        
        # Magnetic Field GEI2000
        bdc_gei2000 = magic_cdf[f'{sc}_l2_magic_gei2000_bdc'] # n_times, 3

        # Magnetic Field MAGIC
        bdc_magic = magic_cdf[f'{sc}_l2_magic_{sc}_magic_bdc'] # n_times, 3

        # Magnetic Field MAGIC
        bdc_nec = magic_cdf[f'{sc}_l2_magic_{sc}_nec_bdc'] # n_times, 3

        # Flags
        flags = magic_cdf[f'{sc}_l2_magic_b_flag_qual']
        
        dt_from_cdf = cdflib.cdfepoch.to_datetime(epoch)
        dts = pd.to_datetime(dt_from_cdf)
        utcs = [(x - pd.Timestamp('1970-01-01'))/pd.Timedelta('1s') for x in dts]
        # utcs = cdflib.cdfepoch.unixtime(epoch)
        # dts = [pd.Timestamp(x) for x in magic_datetimes]

        data_dict['utc'].append(utcs)
        data_dict['dt'].append(dts)
        data_dict['flags'].append(flags)
        data_dict['bdc_gei2000'].append(bdc_gei2000)
        data_dict['bdc_magic'].append(bdc_magic)
        data_dict['bdc_nec'].append(bdc_magic)


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
    bdc_gei2000_vals = np.zeros((t_tot,3))
    bdc_magic_vals = np.zeros((t_tot,3))
    bdc_nec_vals = np.zeros((t_tot,3))
    
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
        bdc_gei2000_vals[indices[0]:indices[1],:] = data_dict['bdc_gei2000'][k]
        bdc_magic_vals[indices[0]:indices[1],:] = data_dict['bdc_magic'][k]
        bdc_nec_vals[indices[0]:indices[1],:] = data_dict['bdc_nec'][k]

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

    magic_dict = {}
    magic_dict['bdc_gei2000'] = bdc_gei2000_vals[time_mask,:]
    magic_dict['bdc_magic'] = bdc_magic_vals[time_mask,:]
    magic_dict['bdc_nec'] = bdc_nec_vals[time_mask,:]
    
    magic_dict['UTC'] = times[time_mask]
    magic_dict['DT'] = []
    for elem in magic_dict['UTC']:
        magic_dict['DT'].append(dt.datetime.fromtimestamp(elem,dt.UTC))
    magic_dict['start_time'] = start
    magic_dict['end_time'] = end
    magic_dict['spacecraft'] = sc    

    return magic_dict











    
    
    # return ddict
    # sc = 'ts'+(file.split('ts')[1]).split('_')[0]
    # cdf = pycdf.CDF(file)
    # start_ind = bisect.bisect_left(cdf['Epoch'], start)
    # end_ind = bisect.bisect_right(cdf['Epoch'], end)

    #     ddict = {}
    # ddict['Epoch'] = cdf['Epoch'][start_ind:end_ind]
    # ddict['Quality Flag'] = cdf[f'{sc}_l2_magic_b_flag_qual'][start_ind:end_ind]
    # ddict[f'{sc}_l2_magic_gei2000_bdc'] = cdf[f'{sc}_l2_magic_gei2000_bdc'][start_ind:end_ind,:]
    # ddict[f'{sc}_l2_magic_{sc}_magic_bdc'] = cdf[f'{sc}_l2_magic_{sc}_magic_bdc'][start_ind:end_ind,:]
    # ddict[f'{sc}_l2_magic_{sc}_nec_bdc'] = cdf[f'{sc}_l2_magic_{sc}_nec_bdc'][start_ind:end_ind,:]
    # ddict['spacecraft'] = sc