from bs4 import BeautifulSoup
import cdflib
import numpy as np
import os 
import requests
import sys

from .msc_file_readers import read_msc_l2_files
from ..general.misc_functions import (getTime, check_file_version)




def retrieve_msc_data(year,month,day,spacecraft,level,local_dir=None):
    
    """
    This routine retrieves MSC data from the UIowa public server. 
    
    Required inputs are year, month, and day of the file you wish to retreive, as well as the spacecraft 
    name ('1' or '2') and data product level (l2 or l3). 
    
    This routine will download the most recent file for that date to a local subdirectory, which
    is indicated as the "local_dir" variable. This is defaulted to ./data/TS1(2)/MSC/LL/YYYY/MM.

    Required inputs
    ---------------------------------------------------------------
    year: YYYY string
    month: MM string
    day: DD string
    spacecraft: '1' or '2' 
    level: 'L2' or 'L3'

    Optional inputs
    ---------------------------------------------------------------
    local_dir: If you have a different path where you'd like to store your data, indicate that here.
    """

    level = level.lower()
    if local_dir is None:
        cwd = os.getcwd()
        local_dir = f'{cwd}/data/TS{spacecraft}/MSC/{level}/{year}/{month}/'
        # checking local directory structure. creating if not already in existence
        # ./data/TS1(2)/MSC/LL/YYYY/MM/
        if os.path.exists(f'{cwd}/data/') is False:
            os.mkdir(f'{cwd}/data/')
        if os.path.exists(f'{cwd}/data/TS{spacecraft}/') is False:
            os.mkdir(f'{cwd}/data/TS{spacecraft}/')
        if os.path.exists(f'{cwd}/data/TS{spacecraft}/MSC/') is False:
            os.mkdir(f'{cwd}/data/TS{spacecraft}/MSC/')   
        if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/MSC/{level}') is False:
            os.mkdir(f'{cwd}/data/TS{spacecraft}/MSC/{level}')
        if os.path.exists(f'{cwd}/data/TS{spacecraft}/MSC/{level}/{year}') is False:
            os.mkdir(f'{cwd}/data/TS{spacecraft}/MSC/{level}/{year}')
        if os.path.exists(f'{cwd}/data/TS{spacecraft}/MSC/{level}/{year}/{month}') is False:
            os.mkdir(f'{cwd}/data/TS{spacecraft}/MSC/{level}/{year}/{month}')

        
    base_url = f"https://tracers-portal.physics.uiowa.edu/{level.upper()}/TS{spacecraft}"
    date_url = f'{base_url}/{year}/{month}/{day}'

    page = requests.get(date_url)
    data = page.text
    soup = BeautifulSoup(data,"html.parser")
    ds = f'{year}{month}{day}'
    all_strings = soup.find_all('a')
    idx = []
    for i in range(len(all_strings)):
        string_name = all_strings[i].get('href')
        if string_name is not None:
            if ds in string_name and level in string_name and 'msc' in string_name:
                idx.append(i)
    if len(idx) > 0:
        day_file = all_strings[idx[-1]].get('href')
        sys.stdout.write('\nDownloading '+f'{day_file}'+'\n')
        file_url_path = date_url + '/' + day_file
        print(file_url_path)
        local_file_path = local_dir + '/' + day_file   
        r = requests.get(file_url_path)
        with open(local_file_path,'wb') as df:
            df.write(r.content)            
    else:
        ymd = f'{year}-{month}-{day}'
        print(f"No MSC {spacecraft.upper()} files for {ymd}!")
    
    return None 






class MSC_L2(getTime):
    """This class will initiate and load MSC L2 data. Inputs are start and stop time in string format, as well as
    the spacecraft you wish to analyze ('1' or '2'). After initializing the class, load the data by employing read_data().

    
    Keys: 'DT', 'UTC',  'bac_tscs', 'bac_fac', 'start_time', 'end_time', 'spacecraft'
    
    ex: 
    msc = MSC_L2('2025-11-19/12:00','2025-11-19/13:00','2')
    msc_l2 = msc.read_data()
    
    """
    # *******************************************************************
    def __init__(self,t0,tf,spacecraft):
        super().__init__(t0=t0,tf=tf,spacecraft=spacecraft)  
        self.spacecraft = spacecraft
    # *******************************************************************
    def read_data(self,local_dir=None,version_check=None):
        """
        Optional Input
        ---------------------------------------------------------
        local_dir: Directory where you'd like to put your data
        version_check: Default is False - This checks to see if you have the most recent file version on your local machine.
        If you want to make sure you have the most up to date file, set this argument to True.
        """
        # Creating subdirectories for data that match format of server, finding local files,
        # and downloading MSC files where need be.
        if version_check is None:
            version_check = False
            
        files2load = []
        for d in range(len(self.date_list)):
            ds = self.date_list[d]
            year = ds.split('/')[0]
            month = ds.split('/')[1]
            day = ds.split('/')[2]
            date_string = year+month+day

            cwd = os.getcwd()
    
            if local_dir is None:
                local_dir = f'{cwd}/data/TS{self.spacecraft}/MSC/l2/{year}/{month}/'
                # checking local directory structure. creating if not already in existence
                # ./data/TS1(2)/MSC/LL/YYYY/MM/
                if os.path.exists(f'{cwd}/data/') is False:
                    os.mkdir(f'{cwd}/data/')
                if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/') is False:
                    os.mkdir(f'{cwd}/data/TS{self.spacecraft}/')
                if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/MSC/') is False:
                    os.mkdir(f'{cwd}/data/TS{self.spacecraft}/MSC/')   
                if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/MSC/l2') is False:
                    os.mkdir(f'{cwd}/data/TS{self.spacecraft}/MSC/l2')
                if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/MSC/l2/{year}') is False:
                    os.mkdir(f'{cwd}/data/TS{self.spacecraft}/MSC/l2/{year}')
                if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/MSC/l2/{year}/{month}') is False:
                    os.mkdir(f'{cwd}/data/TS{self.spacecraft}/MSC/l2/{year}/{month}')

                date_dir = f'{cwd}/data/TS{self.spacecraft}/MSC/l2/{year}/{month}'

            else:
                date_dir = local_dir
            
            f2find = f'{date_dir}/ts{self.spacecraft}_l2_msc**{date_string}**.cdf'
            out = os.popen(f'ls -rt {f2find}').read()
            msc_local_files = out.split('\n')[0:-1]
            
            if len(msc_local_files) > 0:
                if version_check is True:
                    print('Checking version...')
                    remote_file_version = check_file_version(year,month,day,self.spacecraft,'l2','msc')
                    my_local_file = msc_local_files[-1]
                    my_local_version = (my_local_file.split('_')[-1]).split('.cdf')[0]
                    if remote_file_version != my_local_version:
                        print('Retrieving most recent file...')
                        n = retrieve_msc_data(year,month,day,self.spacecraft,'l2',local_dir=local_dir)
                        f2find = f'{date_dir}/ts{self.spacecraft}_l2_msc**{date_string}**.cdf'
                        out = os.popen(f'ls -rt {f2find}').read()
                        msc_local_files = out.split('\n')[0:-1]
                        files2load.append(msc_local_files[-1])
                    else:
                        files2load.append(msc_local_files[-1])
                else:
                    files2load.append(msc_local_files[-1])
            else:
                n = retrieve_msc_data(year,month,day,self.spacecraft,'l2',local_dir=local_dir)
                f2find = f'{date_dir}/ts{self.spacecraft}_l2_msc**{date_string}**.cdf'
                out = os.popen(f'ls -rt {f2find}').read()
                msc_local_files = out.split('\n')[0:-1]
                files2load.append(msc_local_files[-1])
                
        self.filenames = files2load
        
        # Loading in data from each L2 CDF
        msc_dict = read_msc_l2_files(files2load, start=self.start, end=self.end)

        return msc_dict