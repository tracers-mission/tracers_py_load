from bs4 import BeautifulSoup
import cdflib
import copy 
import datetime as dt
from glob import iglob
import numpy as np
import os 
import pandas as pd 
import requests
from scipy.interpolate import interp1d
import sys
from tqdm import tqdm

from .efi_file_readers import (read_efi_l2_files)
from ..general.misc_functions import (determine_datetime_type, getTime)

def retrieve_efi_data(year,month,day,spacecraft,level,local_dir=None,data_prod=None,username=None,password=None):
    """
    This routine retrieves EFI data from the UIowa server. 
    
    Required inputs are year, month, and day of the file you wish to retreive, as well as the spacecraft 
    name ('1' or '2') and data product level (l2).
    
    This routine will download the most recent file for that date to a local subdirectory, which
    is indicated as the "local_dir" variable. This is defaulted to ./data/TS1(2)/EFI/LL/YYYY/MM/DD.
    """
    if data_prod is None:
        data_prod = 'eac+ehf+hsk+vdc'

    level = level.lower()
    if local_dir is None:
        cwd = os.getcwd()
        local_dir = f'{cwd}/data/TS{spacecraft}/EFI/{level}/{year}/{month}/'
        # checking local directory structure. creating if not already in existence
        # ./data/TS1(2)/EFI/LL/YYYY/MM/DD
        if os.path.exists(f'{cwd}/data/') is False:
            os.mkdir(f'{cwd}/data/')
        if os.path.exists(f'{cwd}/data/TS{spacecraft}/') is False:
            os.mkdir(f'{cwd}/data/TS{spacecraft}/')
        if os.path.exists(f'{cwd}/data/TS{spacecraft}/EFI/') is False:
            os.mkdir(f'{cwd}/data/TS{spacecraft}/EFI/')   
        if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/EFI/{level}') is False:
            os.mkdir(f'{cwd}/data/TS{spacecraft}/EFI/{level}')
        if os.path.exists(f'{cwd}/data/TS{spacecraft}/EFI/{level}/{year}') is False:
            os.mkdir(f'{cwd}/data/TS{spacecraft}/EFI/{level}/{year}')
        if os.path.exists(f'{cwd}/data/TS{spacecraft}/EFI/{level}/{year}/{month}') is False:
            os.mkdir(f'{cwd}/data/TS{spacecraft}/EFI/{level}/{year}/{month}')
            
    # ++++++++++++++++++++++++++++++++++++++++++++++++++
    # ---------------- FOR TEAM MEMBERS ----------------
    # ++++++++++++++++++++++++++++++++++++++++++++++++++
    if username is not None:
        base_url = f'https://tracers-portal.physics.uiowa.edu/teams/flight/EFI/{level}_public/ts{spacecraft}'
        date_url = f'{base_url}/{year}/{month}/{day}'
        print(date_url)
        page = requests.get(date_url,auth=(username, password))
        data = page.text
        soup = BeautifulSoup(data,"html.parser")
        ds = f'{year}{month}{day}'
        all_strings = soup.find_all('a')
        idx_eac = []
        idx_ehf = []
        idx_hsk = []
        idx_vdc = []
        for i in range(len(all_strings)):
            string_name = all_strings[i].get('href')
            if string_name is not None:
                if ds in string_name:
                    if 'eac' in string_name:
                        idx_eac.append(i)
                    elif 'ehf' in string_name:
                        idx_ehf.append(i)
                    elif 'hsk' in string_name:
                        idx_hsk.append(i)
                    elif 'vdc' in string_name:
                        idx_vdc.append(i)
    
        
        # Retrieve EAC ----------------------------------------------
        if 'eac' in data_prod:
            if len(idx_eac) > 0:
                day_file = all_strings[idx_eac[-1]].get('href')
                sys.stdout.write('\nDownloading '+f'{day_file}'+'\n')
                file_url_path = date_url + '/' + day_file
                local_file_path = local_dir + '/' + day_file            
                r = requests.get(file_url_path,auth=(username, password))
                with open(local_file_path,'wb') as df:
                    df.write(r.content)  
            else:
                ymd = f'{year}-{month}-{day}'
                print(f"No EFI {spacecraft.upper()} EAC files for {ymd}!")  
                            
        
        # Retrieve VDC ----------------------------------------------
        if 'vdc' in data_prod:
            if len(idx_vdc) > 0:
                vdc_file = all_strings[idx_vdc[-1]].get('href')
                sys.stdout.write('\nDownloading '+f'{vdc_file}'+'\n')
                file_url_path = date_url + '/' + vdc_file
                local_file_path = local_dir + '/' + vdc_file            
                r = requests.get(file_url_path,auth=(username, password))
                with open(local_file_path,'wb') as df:
                    df.write(r.content)
            else:
                ymd = f'{year}-{month}-{day}'
                print(f"No EFI {spacecraft.upper()} VDC files for {ymd}!")  
                
        
        # Retrieve HSK ----------------------------------------------
        if 'hsk' in data_prod:
            if len(idx_hsk) > 0:
                hsk_file = all_strings[idx_hsk[-1]].get('href')
                sys.stdout.write('\nDownloading '+f'{hsk_file}'+'\n')
                file_url_path = date_url + '/' + hsk_file
                local_file_path = local_dir + '/' + hsk_file            
                r = requests.get(file_url_path,auth=(username, password))
                with open(local_file_path,'wb') as df:
                    df.write(r.content)
            else:
                ymd = f'{year}-{month}-{day}'
                print(f"No EFI {spacecraft.upper()} HSK files for {ymd}!")  
    
    
        # Retrieve EHF ----------------------------------------------
        if 'ehf' in data_prod:
            if len(idx_ehf) > 0:
                ehf_file = all_strings[idx_ehf[-1]].get('href')
                sys.stdout.write('\nDownloading '+f'{ehf_file}'+'\n')
                file_url_path = date_url + '/' + ehf_file
                local_file_path = local_dir + '/' + ehf_file            
                r = requests.get(file_url_path,auth=(username, password))
                with open(local_file_path,'wb') as df:
                    df.write(r.content)
            else:
                ymd = f'{year}-{month}-{day}'
                print(f"No EFI {spacecraft.upper()} EHF files for {ymd}!")  

    # ++++++++++++++++++++++++++++++++++++++++++++
    # ---------------- FOR PUBLIC ----------------
    # ++++++++++++++++++++++++++++++++++++++++++++
    else:
        print('Currently no public facing EFI data :(')
    
    return None 





class EFI_L2(getTime):
    """This class will initiate and load EFI L2 data. Inputs are start and stop time in string format, as well as
    the spacecraft you wish to analyze ('1' or '2'). After initializing the class, load the data by employing read_data().

    ex: 
    efi = EFI_L2('2025-11-19/12:00','2025-11-19/13:00','2')
    efi_l2 = efi.read_data(data_prod='eac+vdc',username='username_info',password='password_here')
    
    """
    # *******************************************************************
    def __init__(self,t0,tf,spacecraft):
        super().__init__(t0=t0,tf=tf,spacecraft=spacecraft)  
        self.spacecraft = spacecraft
    # *******************************************************************
    def read_data(self,local_dir=None,data_prod='vdf+eac',username=None,password=None):
        # Creating subdirectories for data that match format of server, finding local files,
        # and downloading EFI files where need be.
        # data_prod: which EFI data products to load?
        #   Options: 'vdc', 'eac', 'ehf', or 'hsk' (DC E-field, AC E-field, HF E-field, or Housekeeping)
        #   Note: You can concatenate them, so 'vdc+eac' is a valid option

        files2load = []
        for d in range(len(self.date_list)):
            ds = self.date_list[d]
            year = ds.split('/')[0]
            month = ds.split('/')[1]
            day = ds.split('/')[2]
            date_string = year+month+day

            cwd = os.getcwd()
    
            if local_dir is None:
                local_dir = f'{cwd}/data/TS{self.spacecraft}/EFI/l2/{year}/{month}/{day}/'
                # checking local directory structure. creating if not already in existence
                # ./data/TS1(2)/EFI/LL/YYYY/MM/DD/
                if os.path.exists(f'{cwd}/data/') is False:
                    os.mkdir(f'{cwd}/data/')
                if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/') is False:
                    os.mkdir(f'{cwd}/data/TS{self.spacecraft}/')
                if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/EFI/') is False:
                    os.mkdir(f'{cwd}/data/TS{self.spacecraft}/EFI/')   
                if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/EFI/l2') is False:
                    os.mkdir(f'{cwd}/data/TS{self.spacecraft}/EFI/l2')
                if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/EFI/l2/{year}') is False:
                    os.mkdir(f'{cwd}/data/TS{self.spacecraft}/EFI/l2/{year}')
                if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/EFI/l2/{year}/{month}') is False:
                    os.mkdir(f'{cwd}/data/TS{self.spacecraft}/EFI/l2/{year}/{month}')
                if os.path.exists(f'{cwd}/data/TS{self.spacecraft}/EFI/l2/{year}/{month}/{day}') is False:
                    os.mkdir(f'{cwd}/data/TS{self.spacecraft}/EFI/l2/{year}/{month}/{day}')

                date_dir = f'{cwd}/data/TS{self.spacecraft}/EFI/l2/{year}/{month}/{day}'
                print(date_dir)

            else:
                date_dir = local_dir
           
            avail_data_prods = []
            # ---- Finding files for each indicated data product ----
            # **** EAC ****
            if 'eac' in data_prod:
                f2find_eac = f'{date_dir}/ts{self.spacecraft}_l2_efi_eac**{date_string}**.cdf'
                out = os.popen(f'ls -rt {f2find_eac}').read()
                eac_local_files = out.split('\n')[0:-1]
                if len(eac_local_files) > 0:
                        files2load.append(eac_local_files[-1])
                        avail_data_prods.append('eac')                    
                else:
                    n = retrieve_efi_data(year,month,day,self.spacecraft,'l2',\
                                          local_dir=local_dir,data_prod='eac',\
                                          username=username,password=password)
                    f2find = f'{date_dir}/ts{self.spacecraft}_l2_efi_eac**{date_string}**.cdf'
                    out = os.popen(f'ls -rt {f2find}').read()
                    eac_local_files = out.split('\n')[0:-1]
                    if len(eac_local_files) > 0:
                        files2load.append(eac_local_files[-1])
                        avail_data_prods.append('eac')

            # **** VDC ****
            if 'vdc' in data_prod:
                f2find_vdc = f'{date_dir}/ts{self.spacecraft}_l2_efi_vdc**{date_string}**.cdf'
                out = os.popen(f'ls -rt {f2find_vdc}').read()
                vdc_local_files = out.split('\n')[0:-1]
                if len(vdc_local_files) > 0:
                    files2load.append(vdc_local_files[-1])
                    avail_data_prods.append('vdc')
                else:
                    n = retrieve_efi_data(year,month,day,self.spacecraft,'l2',\
                                          local_dir=local_dir,data_prod='vdc',\
                                          username=username,password=password)
                    f2find_vdc = f'{date_dir}/ts{self.spacecraft}_l2_efi_vdc**{date_string}**.cdf'
                    out = os.popen(f'ls -rt {f2find_vdc}').read()
                    vdc_local_files = out.split('\n')[0:-1]
                    if len(vdc_local_files) > 0:
                        files2load.append(vdc_local_files[-1])
                        avail_data_prods.append('vdc')


            # *** EHF ***
            if 'ehf' in data_prod:
                f2find_ehf = f'{date_dir}/ts{self.spacecraft}_l2_efi_ehf**{date_string}**.cdf'
                out = os.popen(f'ls -rt {f2find_ehf}').read()
                ehf_local_files = out.split('\n')[0:-1]
                if len(ehf_local_files) > 0:
                    files2load.append(ehf_local_files[-1])
                    avail_data_prods.append('ehf')
                else:
                    n = retrieve_efi_data(year,month,day,self.spacecraft,'l2',\
                                          local_dir=local_dir,data_prod='ehf',\
                                          username=username,password=password)
                    f2find_ehf = f'{date_dir}/ts{self.spacecraft}_l2_efi_ehf**{date_string}**.cdf'
                    out = os.popen(f'ls -rt {f2find_ehf}').read()
                    ehf_local_files = out.split('\n')[0:-1]
                    if len(ehf_local_files) > 0:
                        files2load.append(ehf_local_files[-1])
                        avail_data_prods.append('ehf')


            # *** HSK ***
            if 'hsk' in data_prod:
                f2find_hsk = f'{date_dir}/ts{self.spacecraft}_l2_efi_hsk**{date_string}**.cdf'
                out = os.popen(f'ls -rt {f2find_hsk}').read()
                hsk_local_files = out.split('\n')[0:-1]
                if len(hsk_local_files) > 0:
                    files2load.append(hsk_local_files[-1])
                    avail_data_prods.append('hsk')
                else:
                    n = retrieve_efi_data(year,month,day,self.spacecraft,'l2',\
                                          local_dir=local_dir,data_prod='hsk',\
                                          username=username,password=password)
                    f2find_hsk = f'{date_dir}/ts{self.spacecraft}_l2_efi_hsk**{date_string}**.cdf'
                    out = os.popen(f'ls -rt {f2find_hsk}').read()
                    hsk_local_files = out.split('\n')[0:-1]
                    if len(hsk_local_files) > 0:
                        files2load.append(hsk_local_files[-1])
                        avail_data_prods.append('hsk')
                
        self.filenames = files2load
        # Loading in data from each L2 CDF
        if len(files2load) > 0:
            available_products = '+'.join(avail_data_prods)
            efi_dict = read_efi_l2_files(files2load, start=self.start, end=self.end, data_prod=available_products)
        else:
            efi_dict = None
            print('No EFI files to load for this period.')
            
        return efi_dict

    
    # *******************************************************************
