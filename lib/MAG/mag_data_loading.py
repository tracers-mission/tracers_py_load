from bs4 import BeautifulSoup
import os
import requests
import sys
from lib.MAG.mag_file_readers import read_mag_l2_files
from lib.general.misc_functions import (determine_datetime_type, getTime)



def retrieve_mag_l2_data(year,month,day,spacecraft,local_dir=None):

    """
    This routine retrieves ACE data from the UIowa server. 
    
    Required inputs are year, month, and day of the file you wish to retreive, as well as the spacecraft 
    name ('1' or '2').
    
    This routine will download the most recent file for that date to a local subdirectory, which
    is indicated as the "local_dir" variable. This is defaulted to ./data/TS1(2)/MAG/LL/YYYY/MM.
    """

    if local_dir is None:
        cwd = os.getcwd()
        local_dir = f'{cwd}/data/TS{spacecraft}/MAG/l2/{year}/{month}/'
        # checking local directory structure. creating if not already in existence
        # ./data/TS1(2)/MAG/LL/YYYY/MM/
        if os.path.exists(f'{cwd}/data/') is False:
            os.mkdir(f'{cwd}/data/')
        if os.path.exists(f'{cwd}/data/TS{spacecraft}/') is False:
            os.mkdir(f'{cwd}/data/TS{spacecraft}/')
        if os.path.exists(f'{cwd}/data/TS{spacecraft}/MAG/') is False:
            os.mkdir(f'{cwd}/data/TS{spacecraft}/MAG/')   
        if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/MAG/l2') is False:
            os.mkdir(f'{cwd}/data/TS{spacecraft}/MAG/l2')
        if os.path.exists(f'{cwd}/data/TS{spacecraft}/MAG/l2/{year}') is False:
            os.mkdir(f'{cwd}/data/TS{spacecraft}/MAG/l2/{year}')
        if os.path.exists(f'{cwd}/data/TS{spacecraft}/MAG/l2/{year}/{month}') is False:
            os.mkdir(f'{cwd}/data/TS{spacecraft}/MAG/l2/{year}/{month}')

    base_url = f"https://tracers-portal.physics.uiowa.edu/L2/TS{spacecraft}"
    date_url = f'{base_url}/{year}/{month}/{day}'
    print(date_url)
    page = requests.get(date_url)
    data = page.text
    soup = BeautifulSoup(data,"html.parser")
    ds = f'{year}{month}{day}'
    all_strings = soup.find_all('a')
    idx = []
    for i in range(len(all_strings)):
        string_name = all_strings[i].get('href')
        if string_name is not None:
            if ds in string_name and 'l2' in string_name and 'mag' in string_name:
                idx.append(i)
    if len(idx) > 0:
        day_file = all_strings[idx[-1]].get('href')
        sys.stdout.write('\nDownloading '+f'{day_file}'+'\n')
        file_url_path = date_url + '/' + day_file
        local_file_path = local_dir + '/' + day_file   
        r = requests.get(file_url_path)
        with open(local_file_path,'wb') as df:
            df.write(r.content)           
    else:
        ymd = f'{year}-{month}-{day}'
        print(f"No public MAG L2 TS{spacecraft} files for {ymd}!")

    return None 





class MAG_L2(getTime):
    """
    Loads MAG L2 from TRACERS portal. Required inputs are t0 (start of observation in datetime string
    format), tf (final time of observation), spacecraft ('1' or '2'). Data products include magnetic field,
    delta_B, model IGRF field, TRACERS spacecraft velocity, and TRACERS position. Default coordinate system
    is GEI2000.

    Optional
    ---------------------
    att_coords: Coordinates for attitude data (position and velocity). Options are gei2000 or geo.
    
    b_coords: Coordinates you wish to load MAG products in. Valid coordinate systems
    for B are tss (TRACERS spin sun coordinates), gei2000 (geocentric equatorial inertial coordinates for epoch J2000),
    and geo (geographic coordinates: Z along spin axis or Earth pointing north, X points to 0 degree longitude reference
    meridian, Y completes right-handed system)
    
    delta_b_coords: Coordinates you wish to load delta_B products in. Valid coordinate systems for DELTA_B are
    fac (field aligned coordinates), fvc (field velocity coordinates), tss, tscs, gei2000, geo, and 
    sm (solar magnetic coordinates). 

    igrf_coords: Coordinates for IGRF data. Options are gei2000 or geo.
    """
    
    # ******************************************************
    
    def __init__(self,t0,tf,spacecraft,att_coords=None,b_coords=None,\
                 delta_b_coords=None,igrf_coords=None):
        super().__init__(t0=t0,tf=tf,spacecraft=spacecraft)
        if att_coords is None:
            self.att_coords = 'gei2000'
        else:
            self.att_coords = att_coords.lower()
        
        if b_coords is None:
            self.b_coords = 'gei2000'
        else:
            self.b_coords = b_coords.lower()
        
        if delta_b_coords is None:
            self.delta_b_coords = 'gei2000'
        else:
            self.delta_b_coords = delta_b_coords.lower()

        if igrf_coords is None:
            self.igrf_coords = 'gei2000'
        else:
            self.igrf_coords = igrf_coords.lower()
        
    # ******************************************************
            
    def read_data(self,local_dir=None):
        files2load = []
        for d in range(len(self.date_list)):
            ds = self.date_list[d]
            year = ds.split('/')[0]
            month = ds.split('/')[1]
            day = ds.split('/')[2]
            date_string = year+month+day
        
            cwd = os.getcwd()
        
            if local_dir is None:
                local_dir = f'{cwd}/data/TS{self.spacecraft}/MAG/l2/{year}/{month}/'
                # checking local directory structure. creating if not already in existence
                # ./data/TS1(2)/MAG/LL/YYYY/MM/
                if os.path.exists(f'{cwd}/data/') is False:
                    os.mkdir(f'{cwd}/data/')
                if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/') is False:
                    os.mkdir(f'{cwd}/data/TS{self.spacecraft}/')
                if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/MAG/') is False:
                    os.mkdir(f'{cwd}/data/TS{self.spacecraft}/MAG/')   
                if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/MAG/l2') is False:
                    os.mkdir(f'{cwd}/data/TS{self.spacecraft}/MAG/l2')
                if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/MAG/l2/{year}') is False:
                    os.mkdir(f'{cwd}/data/TS{self.spacecraft}/MAG/l2/{year}')
                if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/MAG/l2/{year}/{month}') is False:
                    os.mkdir(f'{cwd}/data/TS{self.spacecraft}/MAG/l2/{year}/{month}')
        
                date_dir = f'{cwd}/data/TS{self.spacecraft}/MAG/l2/{year}/{month}'
        
            else:
                date_dir = local_dir
           
            
            f2find = f'{date_dir}/ts{self.spacecraft}_l2_mag**{date_string}**.cdf'
            out = os.popen(f'ls -rt {f2find}').read()
            mag_local_files = out.split('\n')[0:-1]
            
            if len(mag_local_files) > 0:
                files2load.append(mag_local_files[-1])
            else:
                print('Retrieving MAG L2 data...')
                n = retrieve_mag_l2_data(year,month,day,self.spacecraft,local_dir=local_dir)
                f2find = f'{date_dir}/ts{self.spacecraft}_l2_mag**{date_string}**.cdf'
                out = os.popen(f'ls -rt {f2find}').read()
                mag_local_files = out.split('\n')[0:-1]
                files2load.append(mag_local_files[-1])
                
        self.filenames = files2load
        
        # Loading in data from each l2 CDF
        mag_dict = read_mag_l2_files(files2load, self.spacecraft, start=self.start, end=self.end, \
                                     att_coords = self.att_coords, b_coords = self.b_coords, \
                                     delta_b_coords = self.delta_b_coords, igrf_coords=self.igrf_coords)
        
        return mag_dict
    
