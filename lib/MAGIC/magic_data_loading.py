from bs4 import BeautifulSoup
import datetime as dt
import numpy as np
import os 
import requests
import sys

from .magic_file_readers import read_magic_l2_files
from ..general.misc_functions import (getTime, check_file_version)



def retrieve_magic_data(year,month,day,spacecraft,level,local_dir=None):
    
    """
    This routine retrieves MAGIC data from the public UIowa server. 
    
    Required inputs are year ('YYYY'), month ('MM'), and day ('DD') of the file you wish to retreive, as well as the spacecraft 
    name ('1' or '2') and data product level ('l2' or 'l3').
    
    This routine will download the most recent file for that date to a local subdirectory, which
    is indicated as the "local_dir" variable. This is defaulted to ./data/TS1(2)/MAGIC/LL/YYYY/MM.

    """

    level = level.lower()
    if local_dir is None:
        cwd = os.getcwd()
        local_dir = f'{cwd}/data/TS{spacecraft}/MAGIC/{level}/{year}/{month}/'
        # checking local directory structure. creating if not already in existence
        # ./data/TS1(2)/MAGIC/LL/YYYY/MM/
        if os.path.exists(f'{cwd}/data/') is False:
            os.mkdir(f'{cwd}/data/')
        if os.path.exists(f'{cwd}/data/TS{spacecraft}/') is False:
            os.mkdir(f'{cwd}/data/TS{spacecraft}/')
        if os.path.exists(f'{cwd}/data/TS{spacecraft}/MAGIC/') is False:
            os.mkdir(f'{cwd}/data/TS{spacecraft}/MAGIC/')   
        if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/MAGIC/{level}') is False:
            os.mkdir(f'{cwd}/data/TS{spacecraft}/MAGIC/{level}')
        if os.path.exists(f'{cwd}/data/TS{spacecraft}/MAGIC/{level}/{year}') is False:
            os.mkdir(f'{cwd}/data/TS{spacecraft}/MAGIC/{level}/{year}')
        if os.path.exists(f'{cwd}/data/TS{spacecraft}/MAGIC/{level}/{year}/{month}') is False:
            os.mkdir(f'{cwd}/data/TS{spacecraft}/MAGIC/{level}/{year}/{month}')

    base_url = f"https://tracers-portal.physics.uiowa.edu/MAGIC/TS{spacecraft}/{level.upper()}"
    date_url = f'{base_url}/{year}/{month}/'
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
            if ds in string_name and level in string_name and 'magic' in string_name:
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
        print(f"No public MAGIC {spacecraft.upper()} files for {ymd}!")
        
    return None 





class MAGIC_L2(getTime):
    # *******************************************************************
    def __init__(self,t0,tf,spacecraft):
        super().__init__(t0=t0,tf=tf,spacecraft=spacecraft)  
        self.spacecraft = spacecraft
    # *******************************************************************
    def read_data(self,local_dir=None,version_check=None):
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
                local_dir = f'{cwd}/data/TS{self.spacecraft}/MAGIC/l2/{year}/{month}/'
                # checking local directory structure. creating if not already in existence
                # ./data/TS1(2)/MAGIC/LL/YYYY/MM/
                if os.path.exists(f'{cwd}/data/') is False:
                    os.mkdir(f'{cwd}/data/')
                if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/') is False:
                    os.mkdir(f'{cwd}/data/TS{self.spacecraft}/')
                if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/MAGIC/') is False:
                    os.mkdir(f'{cwd}/data/TS{self.spacecraft}/MAGIC/')   
                if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/MAGIC/l2') is False:
                    os.mkdir(f'{cwd}/data/TS{self.spacecraft}/MAGIC/l2')
                if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/MAGIC/l2/{year}') is False:
                    os.mkdir(f'{cwd}/data/TS{self.spacecraft}/MAGIC/l2/{year}')
                if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/MAGIC/l2/{year}/{month}') is False:
                    os.mkdir(f'{cwd}/data/TS{self.spacecraft}/MAGIC/l2/{year}/{month}')

                date_dir = f'{cwd}/data/TS{self.spacecraft}/MAGIC/l2/{year}/{month}'

            else:
                date_dir = local_dir
            
            f2find = f'{date_dir}/ts{self.spacecraft}_l2_magic_**{date_string}**.cdf'
            out = os.popen(f'ls -rt {f2find}').read()
            magic_local_files = out.split('\n')[0:-1]
            
            if len(magic_local_files) > 0:
                if version_check is True:
                    print('Checking version...')
                    remote_file_version = check_file_version(year,month,day,self.spacecraft,'l2','magic')
                    my_local_file = magic_local_files[-1]
                    my_local_version = (my_local_file.split('_')[-1]).split('.cdf')[0]
                    if remote_file_version != my_local_version:
                        print('Retrieving most recent file...')
                        n = retrieve_magic_data(year,month,day,self.spacecraft,'l2',local_dir=local_dir)
                        f2find = f'{date_dir}/ts{self.spacecraft}_l2_magic_**{date_string}**.cdf'
                        out = os.popen(f'ls -rt {f2find}').read()
                        magic_local_files = out.split('\n')[0:-1]
                        files2load.append(magic_local_files[-1])
                    else:
                        files2load.append(magic_local_files[-1])
                else:
                    files2load.append(magic_local_files[-1])
            else:
                n = retrieve_magic_data(year,month,day,self.spacecraft,'l2',local_dir=local_dir)
                f2find = f'{date_dir}/ts{self.spacecraft}_l2_magic_**{date_string}**.cdf'
                out = os.popen(f'ls -rt {f2find}').read()
                magic_local_files = out.split('\n')[0:-1]
                files2load.append(magic_local_files[-1])
                
        self.filenames = files2load

        if len(files2load) > 0:
            # Loading in data from each L2 CDF
            magic_dict = read_magic_l2_files(files2load, start=self.start, end=self.end)
        else:
            magic_dict = {}
            print('No MAGIC L2 files to load!')
        return magic_dict


    # *******************************************************************

        