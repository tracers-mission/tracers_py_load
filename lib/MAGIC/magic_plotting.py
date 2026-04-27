import matplotlib.pyplot as plt

def plot_magic_ts(magic_dict,ax=None,coords='gei2000',time_res=None,title=None,\
                  xlabel=None,ylabel='B [nT]'):
    """
    Coordinates where B field is available: gei2000, magic, and nec
    """
    spacecraft = magic_dict['spacecraft']

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)


    var = f'bdc_{coords.lower()}'
    var2plot = magic_dict[var]
    ax.plot(magic_dict['DT'], var2plot[:,0],label=r'B$_X$',c='#D81B60')
    ax.plot(magic_dict['DT'], var2plot[:,1], label=r'B$_Y$',c='#1E88E5')
    ax.plot(magic_dict['DT'], var2plot[:,2], label=r'B$_Z$',c='#FFC107')

    if title is not None:
        ax.set_title(title)
    else:
        ax.set_title(f'{spacecraft.upper()} MAGIC Time Series ({coords.upper()} Coords.)')

    if xlabel is not None:
        ax.set_xlabel(xlabel)

    if ylabel is not None:
        ax.set_ylabel(ylabel)

    if time_res is not None:
        ax = time_res_f(ax, dt_new, time_res)


    ax.set_xlim([magic_dict['start_time'], magic_dict['end_time']])
    ax.legend()

    return ax
