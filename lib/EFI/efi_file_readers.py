from spacepy import pycdf
import bisect


def _read_efi_l2_eac(file, start, end):
    """
    Creates dict from cdf file usable for plotting for EAC data.
    """
    sc = 'ts'+(file.split('ts')[1]).split('_')[0]
    cdf = pycdf.CDF(file)
    start_ind_ts = bisect.bisect_left(cdf['Epoch'], start)
    end_ind_ts = bisect.bisect_left(cdf['Epoch'], end)

    start_ind_spec = bisect.bisect_left(cdf[f'{sc}_l2_eac_packet_start'], start)
    end_ind_spec = bisect.bisect_left(cdf[f'{sc}_l2_eac_packet_start'], end)

    ddict = {}
    ddict['Epoch'] = cdf['Epoch'][start_ind_ts:end_ind_ts]
    ddict[f'{sc}_l2_eac'] = cdf[f'{sc}_l2_eac'][start_ind_ts:end_ind_ts,:]

    ddict['Frequency'] = cdf['Frequency']
    ddict[f'{sc}_l2_eac_packet_start'] = cdf[f'{sc}_l2_eac_packet_start'][start_ind_spec:end_ind_spec]
    ddict[f'{sc}_l2_eac_x_spec'] = cdf[f'{sc}_l2_eac_x_spec'][start_ind_spec:end_ind_spec]
    ddict[f'{sc}_l2_eac_y_spec'] = cdf[f'{sc}_l2_eac_y_spec'][start_ind_spec:end_ind_spec]
    
    return ddict




def _read_efi_l2_edc(file, start, end):

    sc = 'ts'+(file.split('ts')[1]).split('_')[0]
    cdf = pycdf.CDF(file)
    start_ind = bisect.bisect_left(cdf['Epoch'], start)
    end_ind = bisect.bisect_left(cdf['Epoch'], end)
    
    ddict = {}
    ddict['Epoch'] = cdf['Epoch'][start_ind:end_ind]
    ddict[f'{sc}_l2_edc_TSCS'] = cdf[f'{sc}_l2_edc_TSCS'][start_ind:end_ind,:]
    ddict[f'{sc}_l2_edc_fac'] = cdf[f'{sc}_l2_edc_fac'][start_ind:end_ind,:]
    ddict[f'{sc}_l2_edc_fvc'] = cdf[f'{sc}_l2_edc_fvc'][start_ind:end_ind,:]
    ddict[f'{sc}_l2_edc_gei'] = cdf[f'{sc}_l2_edc_gei'][start_ind:end_ind,:]

    return ddict




def _read_efi_l2_ehf(file, start, end):
    """
    Creates dict from cdf file usable for plotting for high frequency data.
    """    
    sc = 'ts'+(file.split('ts')[1]).split('_')[0]
    cdf = pycdf.CDF(file)
    start_ind = bisect.bisect_left(cdf['Epoch'], start)
    end_ind = bisect.bisect_left(cdf['Epoch'], end)

    start_ind_spec = bisect.bisect_left(cdf[f'{sc}_l2_ehf_snapshot_start'], start)
    end_ind_spec = bisect.bisect_left(cdf[f'{sc}_l2_ehf_snapshot_start'], end)

    
    ddict = {}
    ddict['Epoch'] = cdf['Epoch'][start_ind:end_ind]
    ddict['Frequency'] = cdf['Frequency']
    ddict[f'{sc}_l2_ehf_snapshot_start'] = cdf[f'{sc}_l2_ehf_snapshot_start'][start_ind_spec:end_ind_spec]
    ddict[f'{sc}_l2_hf'] = cdf[f'{sc}_l2_hf'][start_ind:end_ind]
    ddict[f'{sc}_l2_hf_spec'] = cdf[f'{sc}_l2_hf_spec'][start_ind_spec:end_ind_spec,:]

    return ddict  


def _read_efi_l2_vdc(file, start, end):
    """
    Creates dict from cdf file usable for plotting for DC field data.
    """
    sc = 'ts'+(file.split('ts')[1]).split('_')[0]
    ddict = {}
    cdf = pycdf.CDF(file)
    start_ind = bisect.bisect_left(cdf['Epoch'], start)
    end_ind = bisect.bisect_left(cdf['Epoch'], end)

    for k in ['Epoch', f'{sc}_l2_vdc_xminus', f'{sc}_l2_vdc_xplus', f'{sc}_l2_vdc_yminus', f'{sc}_l2_vdc_yplus']:
        ddict[k] = cdf[k][start_ind:end_ind]
    
    return ddict


def _read_efi_l2_hsk(file, start, end):
    """
    Creates dict from cdf file usable for plotting for housekeeping data.
    """
    sc = 'ts'+(file.split('ts')[1]).split('_')[0]
    ddict = {}
    cdf = pycdf.CDF(file)
    start_ind = bisect.bisect_left(cdf['Epoch'], start)
    end_ind = bisect.bisect_left(cdf['Epoch'], end)
    var_list = list(cdf.keys())
    for k in var_list:
        ddict[k] = cdf[k][start_ind:end_ind]
    
    return ddict    


def read_efi_l2_files(files2load,start=None,end=None,data_prod=None):
    """
    Reads in a specific user indicated EFI L2 file. Outputs a dictionary with data for each input data product type specified.
    """
    # Loading in data from each L2 CDF
    data_dict = {}
    spacecraft = (files2load[0].split('/')[-1]).split('_')[0]
    data_dict['spacecraft'] = spacecraft
    if data_prod is None:
        data_prod = 'eac'
    for dp in data_prod.split('+'):
        # Find the file for that data product (vdc, eac, ehf, and hsk)
        for f in files2load:
            if dp in f:
                relevant_file = f

        if dp=='eac':
            print(relevant_file)
            data_dict[dp] = _read_efi_l2_eac(relevant_file,start,end)
        elif dp=='vdc':
            print(relevant_file)
            data_dict[dp] = _read_efi_l2_vdc(relevant_file,start,end)
        elif dp=='ehf':
            print(relevant_file)
            data_dict[dp] = _read_efi_l2_ehf(relevant_file,start,end)
        elif dp=='hsk':
            print(relevant_file)
            data_dict[dp] = _read_efi_l2_hsk(relevant_file,start,end)
            
    return data_dict
