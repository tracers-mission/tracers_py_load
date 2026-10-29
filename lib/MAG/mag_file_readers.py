import cdflib
import datetime as dt
import numpy as np

def read_mag_l2_files(files2load, spacecraft, \
                      att_coords = None, b_coords = None, \
                      delta_b_coords = None, igrf_coords = None,  \
                      start = None, end = None):
    if att_coords is None:
        att_coords = 'gei2000'
    else:
        att_coords = att_coords.lower()
    
    if b_coords is None:
        b_coords = 'gei2000'
    else:
        b_coords = b_coords.lower()
    
    if delta_b_coords is None:
        delta_b_coords = 'gei2000'
    else:
        delta_b_coords = delta_b_coords.lower()

    if igrf_coords is None:
        igrf_coords = 'gei2000'
    else:
        igrf_coords = igrf_coords.lower()


    data_dict = {'UTC':[],'UTC_1sps':[],'Bx':[],'By':[],'Bz':[], \
                 'deltaB_x':[],'deltaB_y':[],'deltaB_z':[],\
                 'IGRF_x':[],'IGRF_y':[],'IGRF_z':[], \
                 'TS_x':[],'TS_y':[],'TS_z':[],\
                 'TS_vx':[],'TS_vy':[],'TS_vz':[]}
    for file in files2load:
        print(file)
        mag_data = cdflib.CDF(file)
        
        s_j2000 = mag_data[f'ts{spacecraft}_l2_mag_16sps_epoch']/1e9 # seconds since jan 1 2000

        s_j2000_1sps = mag_data[f'ts{spacecraft}_l2_mag_1sps_epoch']/1e9 # seconds since jan 1 2000
        
        epoch_16sps = mag_data[f'ts{spacecraft}_l2_mag_16sps_epoch']
        epoch_1sps = mag_data[f'ts{spacecraft}_l2_mag_1sps_epoch']
        
        # Convert CDF TT2000 epochs to datetime64 timestamps
        time_16sps = cdflib.cdfepoch.to_datetime(epoch_16sps)
        time_1sps = cdflib.cdfepoch.to_datetime(epoch_1sps)
        
        # Convert datetime64 to Unix seconds (UTC)
        utcs = (time_16sps.astype('datetime64[ns]').astype('int64') / 1e9)
        utc_1sps = (time_1sps.astype('datetime64[ns]').astype('int64') / 1e9)


    
        # Time x 3 (B total)
        b_data = mag_data[f'ts{spacecraft}_l2_mag_16sps_{b_coords}_b']

        data_dict['UTC'].append(utcs)
        data_dict['UTC_1sps'].append(utc_1sps)
        
        data_dict['Bx'].append(b_data[:,0])
        data_dict['By'].append(b_data[:,1])
        data_dict['Bz'].append(b_data[:,2])

        # Time x 3 (delta_B)
        delta_b_data = mag_data[f'ts{spacecraft}_l2_mag_16sps_{delta_b_coords}_deltab']
        data_dict['deltaB_x'].append(delta_b_data[:,0])
        data_dict['deltaB_y'].append(delta_b_data[:,1])
        data_dict['deltaB_z'].append(delta_b_data[:,2])

        # Time x 3 (IGRF)
        igrf_data = mag_data[f'ts{spacecraft}_l2_mag_1sps_{igrf_coords}_igrf']
        data_dict['IGRF_x'].append(igrf_data[:,0])
        data_dict['IGRF_y'].append(igrf_data[:,1])
        data_dict['IGRF_z'].append(igrf_data[:,2])  

        # Time x 3 (spacecraft position)
        pos_data = mag_data[f'ts{spacecraft}_l2_mag_1sps_{att_coords}_pos']
        data_dict['TS_x'].append(pos_data[:,0])
        data_dict['TS_y'].append(pos_data[:,1])
        data_dict['TS_z'].append(pos_data[:,2])
        
        
        # Time x 3 (spacecraft velocity)
        vel_data = mag_data[f'ts{spacecraft}_l2_mag_1sps_{att_coords}_vel']
        data_dict['TS_vx'].append(vel_data[:,0])
        data_dict['TS_vy'].append(vel_data[:,1])
        data_dict['TS_vz'].append(vel_data[:,2])

        

    times = np.array([x for elem in data_dict['UTC'] for x in elem])
    times_1sps = np.array([x for elem in data_dict['UTC_1sps'] for x in elem])
    
    bx = np.array([x for elem in data_dict['Bx'] for x in elem])
    by = np.array([x for elem in data_dict['By'] for x in elem])
    bz = np.array([x for elem in data_dict['Bz'] for x in elem])

    deltabx = np.array([x for elem in data_dict['deltaB_x'] for x in elem])
    deltaby = np.array([x for elem in data_dict['deltaB_y'] for x in elem])
    deltabz = np.array([x for elem in data_dict['deltaB_z'] for x in elem])

    igrfx = np.array([x for elem in data_dict['IGRF_x'] for x in elem])
    igrfy = np.array([x for elem in data_dict['IGRF_y'] for x in elem])
    igrfz = np.array([x for elem in data_dict['IGRF_z'] for x in elem])
    
    tsx = np.array([x for elem in data_dict['TS_x'] for x in elem])
    tsy = np.array([x for elem in data_dict['TS_y'] for x in elem])
    tsz = np.array([x for elem in data_dict['TS_z'] for x in elem])

    tsvx = np.array([x for elem in data_dict['TS_vx'] for x in elem])
    tsvy = np.array([x for elem in data_dict['TS_vy'] for x in elem])
    tsvz = np.array([x for elem in data_dict['TS_vz'] for x in elem])


    start_time = (start - dt.datetime(1970,1,1)).total_seconds()
    end_time = (end - dt.datetime(1970,1,1)).total_seconds()
    
    time_mask = (times >= start_time)&(times <= end_time) 

    time_1sps_mask = (times_1sps >= start_time)&(times_1sps <= end_time)
    
    mag_dict = {'DT':[],'DT_1sps':[]}
    mag_dict['UTC'] = times[time_mask]
    mag_dict['UTC_1sps'] = times_1sps[time_1sps_mask]
    
    mag_dict['Bx'] = bx[time_mask]
    mag_dict['By'] = by[time_mask]
    mag_dict['Bz'] = bz[time_mask]
    mag_dict['|B|'] = np.sqrt((bx[time_mask])**2 + (by[time_mask])**2 + (bz[time_mask])**2)

    mag_dict['deltaBx'] = deltabx[time_mask]
    mag_dict['deltaBy'] = deltaby[time_mask]
    mag_dict['deltaBz'] = deltabz[time_mask]

    mag_dict['IGRFx'] = igrfx[time_1sps_mask]
    mag_dict['IGRFy'] = igrfy[time_1sps_mask]
    mag_dict['IGRFz'] = igrfz[time_1sps_mask]

    mag_dict['TSx'] = tsx[time_1sps_mask]
    mag_dict['TSy'] = tsy[time_1sps_mask]
    mag_dict['TSz'] = tsz[time_1sps_mask]

    mag_dict['TSvx'] = tsvx[time_1sps_mask]
    mag_dict['TSvy'] = tsvy[time_1sps_mask]
    mag_dict['TSvz'] = tsvz[time_1sps_mask]
    
    mag_dict['Attitude Coordinates'] = att_coords
    mag_dict['B Coordinates'] = b_coords
    mag_dict['delta_B Coordinates'] = delta_b_coords
    mag_dict['IGRF Coordinates'] = igrf_coords

    for elem in mag_dict['UTC']:
        mag_dict['DT'].append(dt.datetime.fromtimestamp(elem,dt.UTC))

    for elem in mag_dict['UTC_1sps']:
        mag_dict['DT_1sps'].append(dt.datetime.fromtimestamp(elem,dt.UTC))
        
    mag_dict['start_time'] = start
    mag_dict['end_time'] = end

    return mag_dict
