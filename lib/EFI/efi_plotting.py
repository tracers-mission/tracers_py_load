import matplotlib.pyplot as plt
import datetime as dt
from ..general.misc_functions import time_res_f



def plot_efi_eac_spec(efi,ax=None,cmap='jet',title=None,ylabel='Frequency (Hz)',
                      xlabel=None, zlim=(1e-12, 1e-10), time_res=None):
    spacecraft = efi['spacecraft']
    dt_new = efi['eac']['Epoch']

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
    im=ax.pcolormesh(efi['eac'][f'{spacecraft}_l2_eac_packet_start'],
                     efi['eac']['Frequency'],
                     efi['eac'][f'{spacecraft}_l2_eac_x_spec'].T,
                     cmap=cmap, norm='log', vmin=zlim[0], vmax=zlim[1])
    cbax = ax.inset_axes([1.01,0,0.03,1],transform=ax.transAxes)
    cb = plt.colorbar(im, cax=cbax, label='$(V/m)^2/Hz$')

    if title is not None:
        ax.set_title(title)
    else:
        ax.set_title(f'{spacecraft.upper()} EFI EAC')

    if xlabel is not None:
        ax.set_xlabel(xlabel)

    if ylabel is not None:
        ax.set_ylabel(ylabel)

    if time_res is not None:
        ax = time_res_f(ax, dt_new, time_res)

    return ax


    

def plot_efi_eac_ts(efi,ax=None,cmap='jet',title=None,ylabel='$E$ (V/m)',
                      xlabel=None,time_res=None):
    spacecraft = efi['spacecraft']
    dt_new = efi['eac']['Epoch']

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
    pl=ax.plot(efi['eac']['Epoch'], efi['eac'][f'{spacecraft}_l2_eac'])

    if title is not None:
        ax.set_title(title)
    else:
        ax.set_title(f'{spacecraft.upper()} EFI EAC Time Series')

    if xlabel is not None:
        ax.set_xlabel(xlabel)

    if ylabel is not None:
        ax.set_ylabel(ylabel)

    if time_res is not None:
        ax = time_res_f(ax, dt_new, time_res)

    return ax



def plot_efi_ehf_spec(efi,ax=None,cmap='jet',title=None,ylabel='Frequency (kHz)',
                      xlabel=None, zlim=(1e-17, 1e-11),time_res=None):
    spacecraft = efi['spacecraft']
    dt_new = efi['ehf']['Epoch']

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    im=ax.pcolormesh(efi['ehf'][f'{spacecraft}_l2_ehf_snapshot_start'],
                     efi['ehf']['Frequency'],
                     efi['ehf'][f'{spacecraft}_l2_hf_spec'].T,
                     cmap=cmap, norm='log', vmin=zlim[0], vmax=zlim[1])
    cbax = ax.inset_axes([1.01,0,0.03,1],transform=ax.transAxes)
    cb = plt.colorbar(im, cax=cbax, label='$(V/m)^2/Hz$')

    if time_res is not None:
        ax = time_res_f(ax, dt_new, time_res)
    
    if title is not None:
        ax.set_title(title)
    else:
        ax.set_title(f'{spacecraft.upper()} EFI EFH')

    if xlabel is not None:
        ax.set_xlabel(xlabel)

    if ylabel is not None:
        ax.set_ylabel(ylabel)


    return ax



def plot_efi_ehf_ts(efi,ax=None,cmap='jet',title=None,ylabel='$E$ (V/m)',
                      xlabel=None,time_res=None):
    spacecraft = efi['spacecraft']
    dt_new = efi['ehf']['Epoch']

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
    pl=ax.plot(dt_new, efi['ehf'][f'{spacecraft}_l2_hf'])

    if title is not None:
        ax.set_title(title)
    else:
        ax.set_title(f'{spacecraft.upper()} EFI EFH Time Series')

    if xlabel is not None:
        ax.set_xlabel(xlabel)

    if ylabel is not None:
        ax.set_ylabel(ylabel)

    if time_res is not None:
        ax = time_res_f(ax, dt_new, time_res)

    return ax



def plot_efi_hsk(efi,ax=None,time_res=None,variable=None):
    """    
    List of available housekeeping variables are listed below:
    
    ['ts2_l2_efi_beb_fifo_overflow', 'ts2_l2_efi_cmd_count', 'ts2_l2_efi_cmd_err', 'ts2_l2_efi_cmd_frame_err', 'ts2_l2_efi_cmd_parity_err',
     'ts2_l2_efi_cmd_sync_err', 'ts2_l2_efi_eac_pkt_err', 'ts2_l2_efi_edc_b_pkt_err', 'ts2_l2_efi_edc_r_pkt_err', 'ts2_l2_efi_hf_adc_overflow',
     'ts2_l2_efi_mem_err_cnt', 'ts2_l2_efi_msc_pkt_err', 'ts2_l2_efi_pps_err', 'ts2_l2_efi_tlm_sram_timeout', 'ts2_l2_efi_vdc_b_pkt_err',
     'ts2_l2_efi_vdc_r_pkt_err', 'ts2_l2_dump_addr', 'ts2_l2_dump_data', 'ts2_l2_efi_bias1_dig', 'ts2_l2_efi_bias2_dig', 'ts2_l2_efi_bias3_dig',
     'ts2_l2_efi_bias4_dig', 'ts2_l2_efi_bias1_hsk', 'ts2_l2_efi_bias2_hsk', 'ts2_l2_efi_bias3_hsk', 'ts2_l2_efi_bias4_hsk', 'ts2_l2_efi_beb_tmon',
     'ts2_l2_efi_esp_tmon', 'ts2_l2_efi_pa1_tmon', 'ts2_l2_efi_pa2_tmon', 'ts2_l2_efi_pa3_tmon', 'ts2_l2_efi_pa4_tmon', 'ts2_l2_efi_fltr12_tmon',
     'ts2_l2_efi_fltr34_tmon', 'ts2_l2_efi_pn30v_tmon', 'ts2_l2_efi_pn30v_imon', 'ts2_l2_efi_fltr12_imon', 'ts2_l2_efi_fltr34_imon', 'ts2_l2_efi_p1v5v_imon',
     'ts2_l2_efi_p1v5v_vmon', 'ts2_l2_efi_p2v5v_vmon', 'ts2_l2_efi_n2v5v_vmon', 'Epoch']
    """
    spacecraft = efi['spacecraft']
    dt_new = efi['hsk']['Epoch']

    if variable is None:
        variable = f'{spacecraft}_l2_efi_cmd_count'
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
    pl=ax.plot(dt_new, efi['ehf'][variable])
    return ax