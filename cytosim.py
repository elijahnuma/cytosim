import os 
import re 
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Units and terminology descriptions are in readme.md in plots directory

plot_length, plot_height = 10, 10
font_size = 8

def searchcytosiminfo(request, mode):
    """
    finds information of request in cytosiminformation.txt
    
    args: 
        request (str): input to search text file
        mode (str): section of file to search
    
    returns information as tuple
    """
    if mode == 'test':
        test_number = request
        with open('cytosiminformation.txt', 'r') as f:
            # removes newlines
            file = f.read().splitlines()
            # grabs test information
            # s for string
            test_line = [s for s in file if f"{test_number}:" in s][0]
            test_info = re.search("\(.*\)", test_line).group(0) # information within parathesis
            time_frames_key, binding_ranges_key, variable_value, sim_time, motor_type = eval(test_info)
            # regex for names, test range list, and motor type using keys
            time_frames_line = [s for s in file if f"Time Frames {time_frames_key}:" in s][0]
            time_frames = eval(re.sub(f'Time Frames {time_frames_key}: ', '', time_frames_line))
            binding_ranges_line = [s for s in file if f"Test Binding Ranges {binding_ranges_key}:" in s][0]
            binding_ranges = eval(re.sub(f'Test Binding Ranges {binding_ranges_key}: ', '', binding_ranges_line))
            attach_name_line = [s for s in file if f"Attach Name {motor_type}:" in s][0]
            attach_name = re.sub(f'Attach Name {motor_type}: ', '', attach_name_line)
        # time subdivisions, binding ranges, variable value, simulation time, motor type, attach name
        return (time_frames, binding_ranges, variable_value, sim_time, motor_type, attach_name)
    if mode == 'group':
        group_num = request
        with open('cytosiminformation.txt', 'r') as f:
            file = f.read().splitlines()
            group_line = [s for s in file if f"Group {group_num}:" in s][0]
            group_info = group_line.split(": ")[1]
            group_tests, group_name = eval(group_info)
            motor_key = var_key = sim_time_key = sim_num_key = binding_ranges_key = var_name_key = group_num
            motors_line = [s for s in file if f"Motors {motor_key}:" in s][0]
            motor_list = eval(re.sub(f'Motors {motor_key}: ', '', motors_line))
            var_line = [s for s in file if f"Variable {var_key}:" in s][0]
            var_list = eval(re.sub(f'Variable {var_key}: ', '', var_line))
            binding_ranges_line = [s for s in file if f"Metadata Binding Ranges {binding_ranges_key}:" in s][0]
            binding_ranges = eval(re.sub(f'Metadata Binding Ranges {binding_ranges_key}: ', '', binding_ranges_line))
            var_name_line = [s for s in file if f"Variable Name {var_name_key}:" in s][0]
            var_name = re.sub(f'Variable Name {var_name_key}: ', '', var_name_line)
            sim_time_line = [s for s in file if f"Sim Time {sim_time_key}:" in s][0]
            sim_time = eval(re.sub(f'Sim Time {sim_time_key}: ', '', sim_time_line))
            sim_num_line = [s for s in file if f"Sim Num {sim_num_key}:" in s][0]
            sim_num = eval(re.sub(f'Sim Num {sim_num_key}: ', '', sim_num_line))
        # test numbers, group description, motor values, variable values, binding ranges, variable name, simtulation time, number of simulations
        return (group_tests, group_name, motor_list, var_list, binding_ranges, var_name, sim_time, sim_num)
    
def anchor_maker(heads_num, motor_type, barezone):
    """ 
    makes anchors for rod motors in .cym file
    
    args:
        heads_num (int): number of heads
        motor_type (str): rod type
        barezone (float): middle bare zone as percentage
    
    """
    L = 0.8                 # 0.8 um rod length
    mp = barezone/100       # middle percent
    b = 0.5 - mp/2          # left end bare zone marker
    if motor_type == 'rigid':
        # subtracting heads number by two because a two head motor has anchors at ends
        anchors = sorted((b - np.linspace(0, b, (heads_num-2)//2, endpoint=False))) + list(np.linspace(1-b, 1, (heads_num-2)//2, endpoint=False))
        for i, per in enumerate(anchors, 1):
            print(f'    anchor{i} = point1, point2, {round(per, 4)}, myosin;')  
    if motor_type == 'flexible':
        anchors = np.linspace(0*L, b*L, heads_num//2, endpoint=False)[1:]
        # starts counting at three as first two as ends of rod
        for i, ma in enumerate(anchors, 3):    
            print(f'    attach{i} = myosin, {round(ma, 4)}, minus_end')
        # iterating anchors position backwards, enumerate starts where last for loop left off
        for i, pa in enumerate(anchors[::-1], 3 + len(anchors)):
            print(f'    attach{i} = myosin, {round(pa, 4)}, plus_end')

def metadata(info_num, log=True, show_plot=False):
    """ 
    plots computational time and max memory used against motor count 
    
    args:
        info_num (int): information folders checked
        log (bool): sets log scale; default True
        show_plot (bool): shows plot; default False
    
    returns average computational times and memory usages for each variable as dict of dicts
    """
    _, group_name, motor_list, var_list, binding_ranges, var_name, sim_time, sim_num = searchcytosiminfo(info_num, 'group')
    cwd = os.getcwd()
    # number of messagescmo files, messagescmo and outtxt numbers should be equal 
    msg_num = len(os.listdir(os.path.join(cwd, 'data', f'messages_{info_num}')))
    messages_dicts, memorys_dicts = [], []
    for i, br in enumerate(binding_ranges):
        messages, memorys = [], []
        for j in range(i, msg_num, len(binding_ranges)):
            with open(cwd + f'\\data\\messages_{info_num}\\messages{j}.cmo', 'r') as f:
                file = f.readlines()
                seconds = file[-1]
                seconds = re.search('[0-9]+', seconds)[0]
                messages.append(seconds)
            with open(cwd + f'\\data\\outs_{info_num}\\out{j}.txt', 'r') as f:
                file = f.readlines()
                seconds = [s for s in file if "Max Memory" in s][0]
                seconds = re.search('[0-9]+\.[0-9]+', seconds)[0]
                memorys.append(seconds)
        # number of times motors variable is changed
        motor_num = len(motor_list)
        # number of times variable is changed
        var_num = len(var_list)
        # standard deviation calculator for array
        std = lambda arr: np.sqrt(sum((arr-np.mean(arr))**2)/len(arr))
        # reshape arrays
        messages = np.array(messages).astype(np.float64).reshape(motor_num, var_num, sim_num)
        memorys = np.array(memorys).astype(np.float64).reshape(motor_num, var_num, sim_num)
        # standard deivations
        messages_errors = np.apply_along_axis(std, 2, messages)
        memory_errors = np.apply_along_axis(std, 2, memorys)
        # average by simulation
        messages = np.mean(messages, axis=2)
        memorys = np.mean(memorys, axis=2)
        # sort arrays organized by motor multiplier -> variable count
        messages = np.column_stack(messages)
        memorys = np.column_stack(memorys)
        messages_errors = np.column_stack(messages_errors)
        memory_errors = np.column_stack(memory_errors)
        # sort into dictionaries for easier indexing
        messages_dict = {h: messages[i] for i, h in enumerate(var_list)}
        memorys_dict = {h: memorys[i] for i, h in enumerate(var_list)}
        messages_errors_dict = {h: messages_errors[i] for i, h in enumerate(var_list)}
        memory_errors_dict = {h: memory_errors[i] for i, h in enumerate(var_list)}
        if show_plot:
            # messages plot
            fig, ax = plt.subplots(figsize=(plot_length, plot_height))
            fignamelog = 'log' if log else 'nolog'
            title_suffix = f'{group_name} (binding range = {br} um) ({sim_time} seconds)'
            fig_suffix = f"({br}bindingrange)({sim_time}seconds){fignamelog}{group_name.replace(' ', '').lower()}"
            ax.set_title(f'Computational time vs. motors {title_suffix}', fontdict={'fontsize':font_size})
            ax.set_xlabel('Motor count')
            ax.set_ylabel('Seconds (S)')
            if log:
                ax.set_xscale('log')
                ax.set_yscale('log')
            for var in sorted(messages_dict.keys()):
                ax.scatter(motor_list, messages_dict[var], label=f'{var}')
                ax.errorbar(motor_list, messages_dict[var], yerr=messages_errors_dict[var], fmt='none')
            ax.legend(title=f'{var_name}:')
            ax.grid(True, which='both')
            plt.savefig(cwd + f"\\plots\\metadata\\computationaltime\\computationaltime{fig_suffix}.png")
            # memory plot
            fig, ax = plt.subplots(figsize=(plot_length, plot_height))
            fignamelog = 'memorylog' if log else 'memorynolog'
            ax.set_title(f'Memory used vs. motors {title_suffix}', fontdict={'fontsize':font_size})
            ax.set_xlabel('Motor count')
            ax.set_ylabel('Memory (MB)')
            if log:
                ax.set_xscale('log')
                ax.set_yscale('log')
            for var in sorted(memorys_dict.keys()):
                ax.scatter(motor_list, memorys_dict[var], label=f'{var}')
                ax.errorbar(motor_list, memorys_dict[var], yerr=memory_errors_dict[var], fmt='none')
            ax.legend(title=f'{var_name}:')
            ax.grid(True, which='both')
            plt.savefig(cwd + f"\\plots\\metadata\\memoryusage\\memoryusage{fig_suffix}.png")
        messages_dicts.append(messages_dict)
        memorys_dicts.append(memorys_dict)
    csv_suffix = f"({sim_time}seconds){group_name.replace(' ', '').lower()}"
    messages_dicts = dict(zip(binding_ranges, messages_dicts)) 
    memorys_dicts = dict(zip(binding_ranges, memorys_dicts)) 
    messages_df = pd.DataFrame.from_dict(messages_dicts, 'index').stack().rename_axis(['Binding Range', 'Heads'])
    messages_df = messages_df.apply(pd.Series, index=motor_list).reset_index()
    messages_df.to_csv(path_or_buf=cwd + f"\\csvs\\metadata\\computationaltime\\computationaltime{csv_suffix}.csv", index=False)
    memorys_df = pd.DataFrame.from_dict(memorys_dicts, 'index').stack().rename_axis(['Binding Range', 'Heads'])
    memorys_df = memorys_df.apply(pd.Series, index=motor_list).reset_index()
    memorys_df.to_csv(path_or_buf=cwd + f"\\csvs\\metadata\\memoryusage\\memoryusage{csv_suffix}.csv", index=False)
    return messages_dicts, memorys_dicts
        
def plot_handler(df, title, metric, figname, y_label):
    """
    handles plots with many lines
    
    args:
        df (pandas.DataFrame): dataframe of interest
        title (str): title of plot
        metric (str): metric for plot
        figname (str): description of plot for fig save
        y_label (str): y label
        
    """
    # creates figures and axes
    fig, axes = plt.subplots(nrows=3, ncols=1)
    plt.subplots_adjust(hspace=0.5)
    # adds label to legend
    df = df.add_prefix('Binding Range = ')
    # plot
    df.plot(kind='line', y=df.columns[:len(df.columns)//3], figsize=(plot_length, plot_height), title=f'{title}', ax=axes[0]).set(ylabel=f'{y_label}')
    df.plot(kind='line', y=df.columns[len(df.columns)//3:2*len(df.columns)//3], figsize=(plot_length, plot_height), ax=axes[1]).set(ylabel=f'{y_label}')
    df.plot(kind='line', y=df.columns[2*len(df.columns)//3:], figsize=(plot_length, plot_height), ax=axes[2]).set(ylabel=f'{y_label}')
    # adds grid
    for a in axes:
        a.grid(True, which='both')
    fig.savefig(cwd + f'\\plots\\plotsvstime\\{metric}\\{metric}{figname}.png', bbox_inches='tight')
# %% Main loops
# group under consideration
for group_num in [14]:
    # color linestyle pairs generator, cycles forever, for groups
    linestyles = ['-', '--', ':', '-.']
    colors = ['red', 'blue', 'green', 'cyan', 'magenta', 'orange']
    color_linestyles = [(c, l) for l in linestyles for c in colors]
    color_linestyles_cycle = itertools.cycle(color_linestyles)
    # saves dfs from each group to compare
    cluster_delta_dfs = []
    max_contraction_dfs = []
    max_contraction_time_dfs = []
    attach_dfs = []
    # sets group information
    group_tests, group_name, motor_list, var_list, binding_ranges, var_name, sim_time, sim_num = searchcytosiminfo(group_num, 'group')
    # runs through each test, enumerating for motor list
    for m, test_number in enumerate(group_tests):
        ## plot and dataframe initialization when variable cycle resets
        if m % len(var_list) == 0:
            fig_cluster_delta, ax_cluster_delta = plt.subplots(nrows=1, ncols=1)
            fig_max_contraction, ax_max_contraction = plt.subplots(nrows=1, ncols=1)
            fig_max_contraction_time, ax_max_contraction_time = plt.subplots(nrows=1, ncols=1)
            fig_attach_delta, ax_attach_delta = plt.subplots(nrows=1, ncols=1)
            ax_attach_delta.set_ylim(0, 1)
        # sets test information
        time_frames, _, var_value, _, motor_type, attach_name = searchcytosiminfo(test_number, 'test')
        motor_count = motor_list[m//len(var_list)]
        # color linestyle pairs
        color, linestyle = next(color_linestyles_cycle)
        cwd = os.getcwd()
        # number of sims of one run
        sim_num = len(os.listdir(os.path.join(cwd, 'data', f'test_{test_number}')))
        # number of runs
        try:
            run_count = len(os.listdir(os.path.join(cwd, 'data', f'test_{test_number}', '0', 'reports')))
        except FileNotFoundError:
            print('FileNotFoundError: There is no report')
        ## csv compiling
        # concats csv files together as DataFrame
        df_cluster_size_list = []
        df_contraction_list = []
        for sim in range(sim_num): 
            df_cluster_size_list.append(pd.read_csv(cwd + f'\\data\\test_{test_number}\\{sim}\\Data_Files\\Rdata.csv', names=time_frames).set_index(binding_ranges).transpose().rename_axis('Second (s)'))
            df_contraction_list.append(pd.read_csv(cwd + f'\\data\\test_{test_number}\\{sim}\\Data_Files\\Cdata.csv', names=time_frames).set_index(binding_ranges).transpose().rename_axis('Second (s)'))
        df_cluster_concat = pd.concat(df_cluster_size_list)
        df_contraction_concat = pd.concat(df_contraction_list)
        # averages the concat dfs over simulations
        df_cluster = df_cluster_concat.groupby(df_cluster_concat.index).mean()
        # negative so we can capture magnitude
        df_contraction = -df_contraction_concat.groupby(df_contraction_concat.index).mean()
        ## further analyzes csv DataFrames
        # cluster size delta from beginning to end (negative so we capture magnitude)
        df_cluster_delta = -pd.DataFrame(df_cluster.iloc[-1] - df_cluster.iloc[0]).rename(columns={df_cluster.index[0]: var_value}).rename_axis('Binding Range (um)')
        cluster_delta_dfs.append(df_cluster_delta.copy())
        # max contraction rate
        df_max_contraction = pd.DataFrame(df_contraction.max()).rename(columns={df_contraction.index[0]: var_value}).rename_axis('Binding Range (um)')
        max_contraction_dfs.append(df_max_contraction.copy())
        # max contraction rate time (min is because contraction is negative)
        df_max_contraction_time = pd.DataFrame(df_contraction.idxmax()).rename(columns={df_contraction.index[0]: var_value}).rename_axis('Binding Range (um)')
        max_contraction_time_dfs.append(df_max_contraction_time.copy())          
        # attachment of hands over time   
        df_dict = {float(run): [] for run in range(run_count)}
        for sim in range(sim_num):
            for run in range(run_count):
                run_str = f'run000{run+1}' if run+1 < 10 else f'run00{run+1}' if run+1 < 100 else f'run0{run+1}'
                filename = cwd + f'\\data\\test_{test_number}\\{sim}\\reports\\{run_str}report.txt'
                with open(filename) as f:
                    # puts each line into as a string into a list
                    lines = f.read().splitlines()
                # keeps all strings with the motor name
                lines = [line for line in lines if attach_name in line]
                # keeps value in last column
                lines = [line.split()[-1] for line in lines]
                df = pd.DataFrame(lines).set_index(time_frames)
                # renames column to independent variable
                df = df.rename(columns={df.columns[-1]: binding_ranges[run]})
                # sets to floating point and renames index
                df = df.astype('float64').rename_axis('Second (s)') 
                # seperates non-zero values as it will mess up the scale of the plot
                df = df[df.values != 0]
                # adds run from simulation number
                df_dict[run].append(df)   
        # combines every simulation for each run into a df for that run
        run_dfs = [pd.concat(df_dict[run]) for run in range(run_count)]
        # averages each dataframe by index in above list
        df_concats = [df.groupby(df.index).mean() for df in run_dfs]
        # combines each column in above list into a single dataframe
        df_attach = pd.concat(df_concats, axis=1).fillna(0)
        # divides final value by maximum number of hands
        df_attach_delta = pd.DataFrame(df_attach.iloc[-1]/df_attach.max().max())
        # attachment of hands delta as percent, renames column to description, renames index
        df_attach_delta = df_attach_delta.rename(columns={df_cluster.index[-1]: var_value}).rename_axis('Binding range (um)')
        attach_dfs.append(df_attach_delta.copy())
        ## plots
        title_suffix = f'({motor_count} motors) ({sim_time} sec) {group_name}'
        fig_suffix = f"({motor_count}motors)({sim_time}seconds){group_name.replace(' ', '').lower()}"
        # cluster size over time plot
        cluster_title = f'Cluster size over time {title_suffix}'
        plot_handler(df=df_cluster, title=cluster_title, metric='work', figname=fig_suffix, y_label='Cluster size')
        # contraction rate over time plot
        contraction_title = f'Contraction rate magnitude over time {title_suffix}'
        plot_handler(df=df_contraction, title=contraction_title, metric='power', figname=fig_suffix, y_label='Contraction rate magnitude')
        # cluster size delta from beginning to end plot
        cluster_delta_title = f'Contraction delta magnitude {title_suffix}'
        df_cluster_delta.plot(kind='line', figsize=(plot_length, plot_height), color=color, linestyle=linestyle, ax=ax_cluster_delta, title=cluster_delta_title, logx=True).set(ylabel='Contraction delta magnitude (um)')
        ax_cluster_delta.grid(True, which='both')
        ax_cluster_delta.legend(title=f'{var_name}:')
        # max contraction rate plot
        max_contraction_title = f'Max contraction rate magnitude {title_suffix}'
        df_max_contraction.plot(kind='line', figsize=(plot_length, plot_height), color=color, linestyle=linestyle, ax=ax_max_contraction, title=max_contraction_title, logx=True, logy=True).set(ylabel='Max contraction rate magnitude (um/s)')        
        ax_max_contraction.grid(True, which='both')
        ax_max_contraction.legend(title=f'{var_name}:')
        # max contraction rate time plot
        max_contraction_time_title = f'Max contraction rate time {title_suffix}'
        df_max_contraction_time.plot(kind='line', figsize=(plot_length, plot_height), color=color, linestyle=linestyle, ax=ax_max_contraction_time, title=max_contraction_time_title, logx=True).set(ylabel='Max contraction rate time (s)')  
        ax_max_contraction_time.grid(True, which='both')
        ax_max_contraction_time.legend(title=f'{var_name}:')
        # attachment of hands over time
        attach_title = f'Attachment of hands {title_suffix}'
        plot_handler(df=df_attach, title=attach_title, metric='attachhands', figname=fig_suffix, y_label='Hands attached')
        # attachment of hands % delta from beginning to end plot
        attach_delta_title = f'Attachment of hands % delta {title_suffix}'
        df_attach_delta.plot(kind='line', figsize=(plot_length, plot_height), color=color, linestyle=linestyle, ax=ax_attach_delta, title=attach_delta_title, logx=True).set(ylabel='Attachment of hands delta (%)')
        ax_attach_delta.grid(True, which='both')
        ax_attach_delta.legend(title=f'{var_name}:')
        # save figures before variable cycle resets
        if (m % len(var_list) == len(var_list)-1):
            fig_cluster_delta.savefig(cwd + f"\\plots\\plotsvsbindingrange\\work\\work{fig_suffix}.png", bbox_inches='tight')
            fig_max_contraction.savefig(cwd + f"\\plots\\plotsvsbindingrange\\maxpower\\maxpower{fig_suffix}.png", bbox_inches='tight')
            fig_max_contraction_time.savefig(cwd + f"\\plots\\plotsvsbindingrange\\maxpowertime\\maxpowertime{fig_suffix}.png", bbox_inches='tight')
            fig_attach_delta.savefig(cwd + f"\\plots\\plotsvsbindingrange\\attachdelta\\attachdelta{fig_suffix}.png", bbox_inches='tight')
    # flattens dfs
    cluster_delta_dfs = pd.concat(cluster_delta_dfs, axis=1)
    max_contraction_dfs = pd.concat(max_contraction_dfs, axis=1)
    max_contraction_time_dfs = pd.concat(max_contraction_time_dfs, axis=1)
    # % Motor-variable superposition
    # cluster delta copies
    clusterdeltas = cluster_delta_dfs.copy()
    # renames columns by adding motor count
    col_names = list(clusterdeltas.columns)
    column_suffixes = [f' ({m} motors)' for m in motor_list for _ in var_list]
    clusterdeltas.columns = [str(c) + s for c, s in zip(col_names, column_suffixes)]
    # filter by variable and motor count
    clusterdeltasvariables = {v: clusterdeltas.filter(regex=f'{v}') for v in var_list}
    clusterdeltasmotors = {m: clusterdeltas.filter(regex=f' \({m} motors\)') for m in motor_list}
    ## plots
    # Baseline motor count for comparison, must be from motor_list
    baseline_motor = 1000
    # motor multipler of interest
    for motor in motor_list:
        fig_suffix = f"({motor}motors)({sim_time}seconds){group_name.replace(' ', '').lower()}"
        dfs = [clusterdeltasmotors[baseline_motor], clusterdeltasmotors[motor]]
        # Baseline motor counts are black, others are assorted colors
        styles = ['k' for _ in range(len(clusterdeltasmotors[baseline_motor].columns))] + [c[0]+l for (c,l) in color_linestyles[:len(clusterdeltasmotors[motor].columns)]]
        pd.concat(dfs, axis=1).plot(kind='line', figsize=(plot_length, plot_height), style=styles, title=f'Contraction delta {group_name}', logx=True).set(ylabel='Contraction delta magnitude (um)')
        plt.grid(True, which='both')
        plt.legend(title=f'{var_name}:')
        plt.savefig(cwd + f"\\plots\\plotsvsbindingrange\\motorvariablesuperposition\\clustersizedeltas{fig_suffix}.png")
    # compared variables
    for var in var_list:
        fig_suffix = f"({var}{var_name.lower().replace(' ', '')})({sim_time}seconds){group_name.replace(' ', '').lower()}"
        dfs = [clusterdeltasmotors[baseline_motor], clusterdeltasvariables[var].drop(f'{var} ({baseline_motor} motors)', axis=1)]
        # Baseline motor counts are black, others are assorted colors
        styles = ['k' for _ in range(len(clusterdeltasmotors[baseline_motor].columns))] + [c[0]+l for (c,l) in color_linestyles[:len(clusterdeltasvariables[var].columns)]]
        pd.concat(dfs, axis=1).plot(kind='line', figsize=(plot_length, plot_height), style=styles, title=f'Contraction delta {group_name}', logx=True).set(ylabel='Contraction delta magnitude (um)')
        plt.grid(True, which='both')
        plt.legend(title=f'{var_name}:')
        plt.savefig(cwd + f"\\plots\\plotsvsbindingrange\\motorvariablesuperposition\\clustersizedeltas{fig_suffix}.png")
    # % Analyzing motor data with respect to motor count
    # metadata
    times, memory = metadata(info_num=group_num, show_plot=True)
    cols = col_names[:len(var_list)] # column names
    # binding ranges of interest
    for binding_range in binding_ranges:
        title_suffix = f'(binding range = {binding_range} um) ({sim_time} seconds) {group_name}'
        fig_suffix = f"({binding_range}bindingrange)({sim_time}seconds){group_name.replace(' ', '').lower()}"
        times_df = pd.DataFrame(times[binding_range], index=motor_list)
        memory_df = pd.DataFrame(memory[binding_range], index=motor_list)
        ## contraction delta magnitude vs motor (work)
        deltas = pd.DataFrame(cluster_delta_dfs.loc[binding_range].values.reshape((cluster_delta_dfs.shape[1]//len(cols), len(cols))), index=motor_list, columns=cols)
        deltas_df = pd.DataFrame(deltas, index=motor_list).rename_axis('Motor count')
        deltas_df.plot(figsize=(plot_length, plot_height), logx=True).set(ylabel='Contraction delta magnitude (um)')
        plt.title(f'Contraction delta magnitude vs motor count {title_suffix}', fontdict={'fontsize':font_size})
        plt.grid(True, which='both')
        plt.legend(title=f'{var_name}:')
        plt.savefig(cwd + f"\\plots\\plotsvsmotors\\work\\work\\work{fig_suffix}.png")
        ## contraction delta per computational time vs motor (work time efficiency)
        delta_time_efficiency_df = deltas_df/times_df.values
        delta_time_efficiency_df.plot(figsize=(plot_length, plot_height), logx=True).set(ylabel='Contraction delta magnitude per computational time (um/S)')
        plt.title(f'Contraction delta magnitude per computational time vs motor count {title_suffix}', fontdict={'fontsize':font_size})
        plt.grid(True, which='both')
        plt.legend(title=f'{var_name}:')
        plt.savefig(cwd + f"\\plots\\plotsvsmotors\\work\\efficiency\\computationaltime\\worktimeefficiency{fig_suffix}.png")
        ## contraction delta per memory usage vs motor (work memory efficiency)
        delta_memory_efficiency_df = deltas_df/memory_df.values
        delta_memory_efficiency_df.plot(figsize=(plot_length, plot_height), logx=True).set(ylabel='Contraction delta magnitude per memory usage (um/MB)')
        plt.title(f'Contraction delta magnitude per memory usage vs motor count {title_suffix}', fontdict={'fontsize':font_size})
        plt.grid(True, which='both')
        plt.legend(title=f'{var_name}:')
        plt.savefig(cwd + f"\\plots\\plotsvsmotors\\work\\efficiency\\memoryusage\\workmemoryefficiency{fig_suffix}.png")
        ## max contraction rate vs motor (max power)
        max_contractions = pd.DataFrame(max_contraction_dfs.loc[binding_range].values.reshape((max_contraction_dfs.shape[1]//len(cols), len(cols))), index=motor_list, columns=cols)
        max_contractions_df = pd.DataFrame(max_contractions, index=motor_list).rename_axis('Motor count')
        max_contractions_df.plot(figsize=(plot_length, plot_height), logx=True).set(ylabel='Max contraction rate magnitude (um/s)')
        plt.title(f'Max contraction rate magnitude vs motor count {title_suffix}', fontdict={'fontsize':font_size})
        plt.grid(True, which='both')
        plt.legend(title=f'{var_name}:')
        plt.savefig(cwd + f"\\plots\\plotsvsmotors\\maxpower\\maxpower\\nonscaling\\maxpower{fig_suffix}.png")
        ## max contraction rate vs total motor count (by scaling) (max power)
        df = max_contractions_df.copy()
        # multiplies by number of heads per motor, for point motors there are only 2 heads
        scaling_max_contractions_df = pd.concat([df[v].rename(index=dict(zip(df[v].index, df[v].index*(2 if motor_type == 'point' else v)))) for v in var_list], axis=1)
        scaling_max_contractions_df = scaling_max_contractions_df.rename_axis('Total head count')
        fig, ax = plt.subplots(nrows=1, ncols=1)
        for v in var_list:
            pd.DataFrame(scaling_max_contractions_df[v].dropna()).plot(figsize=(plot_length, plot_height), logx=True, ax=ax).set(ylabel='Max contraction rate magnitude (um/s)')
        plt.title(f'Max contraction rate magnitude vs total head count {title_suffix}', fontdict={'fontsize':font_size})
        plt.grid(True, which='both')
        plt.legend(title=f'{var_name}:')
        plt.savefig(cwd + f"\\plots\\plotsvsmotors\\maxpower\\maxpower\\scaling\\maxpowertotalheadcount{fig_suffix}.png")
        ## max contraction rate per computational time vs motor (max power time efficiency)
        max_contractions_time_efficiency_df = max_contractions_df/times_df.values
        max_contractions_time_efficiency_df.plot(figsize=(plot_length, plot_height), logx=True).set(ylabel='Max contraction rate magnitude per computational time (um/s/S)')
        plt.title(f'Max contraction rate magnitude per computational time vs motor count {title_suffix}', fontdict={'fontsize':font_size})
        plt.grid(True, which='both')
        plt.legend(title=f'{var_name}:')
        plt.savefig(cwd + f"\\plots\\plotsvsmotors\\maxpower\\efficiency\\computationaltime\\maxpowertimeefficiency{fig_suffix}.png")
        ## max contraction rate per computational time vs total motor count (by scaling) (max power time efficiency)
        df = max_contractions_time_efficiency_df.copy()
        # multiplies by number of heads per motor, for point motors there are only 2 heads
        scaling_max_contractions_time_efficiency_df = pd.concat([df[v].rename(index=dict(zip(df[v].index, df[v].index*(2 if motor_type == 'point' else v)))) for v in var_list], axis=1)
        scaling_max_contractions_time_efficiency_df = scaling_max_contractions_time_efficiency_df.rename_axis('Total head count')
        fig, ax = plt.subplots(nrows=1, ncols=1)
        for v in var_list:
            pd.DataFrame(scaling_max_contractions_time_efficiency_df[v].dropna()).plot(figsize=(plot_length, plot_height), logx=True, ax=ax).set(ylabel='Max contraction rate magnitude per computational time (um/s/S)')
        plt.title(f'Max contraction rate magnitude per computational time vs total head count {title_suffix}', fontdict={'fontsize':font_size})
        plt.grid(True, which='both')
        plt.legend(title=f'{var_name}:')
        plt.savefig(cwd + f"\\plots\\plotsvsmotors\\maxpower\\efficiency\\scalingcomputationaltime\\maxpowertimeefficiencypointmotorscaling{fig_suffix}.png")
        ## max contraction rate per memory usage vs motor (max power memory efficiency)
        max_contractions_memory_efficiency_df = max_contractions_df/memory_df.values
        max_contractions_memory_efficiency_df.plot(figsize=(plot_length, plot_height), logx=True).set(ylabel='Max contraction rate magnitude per memory usage (um/MB)')
        plt.title(f'Max contraction rate magnitude per memory usage vs motor count {title_suffix}', fontdict={'fontsize':font_size})
        plt.grid(True, which='both')
        plt.legend(title=f'{var_name}:')
        plt.savefig(cwd + f"\\plots\\plotsvsmotors\\maxpower\\efficiency\\memoryusage\\maxpowermemoryefficiency{fig_suffix}.png")
        ## max contraction rate time vs motor (max power time)
        max_contraction_times = pd.DataFrame(max_contraction_time_dfs.loc[binding_range].values.reshape((max_contraction_time_dfs.shape[1]//len(cols), len(cols))), index=motor_list, columns=cols)
        max_contraction_times_df = pd.DataFrame(max_contraction_times, index=motor_list).rename_axis('Motor count')
        max_contraction_times_df.plot(figsize=(plot_length, plot_height), logx=True).set(ylabel='Seconds (s)')
        plt.title(f'Max contraction rate time vs motor count {title_suffix}', fontdict={'fontsize':font_size})
        plt.grid(True, which='both')
        plt.legend(title=f'{var_name}:')
        plt.savefig(cwd + f"\\plots\\plotsvsmotors\\maxpower\\maxpowertime\\maxpowertime{fig_suffix}.png")
# %% Tracking diffusion
# need to update searchcytosiminfo 
# intializers
test_number = 579
times, *_, motor_type, _ = searchcytosiminfo(test_number, 'test')
sim_num = len(os.listdir(os.path.join(os.getcwd(), 'tests', f'test_{test_number}')))
coord_columns = ['cenX', 'cenY'] if motor_type == 'rod' else ['posX', 'posY']
actin_num = 1000
# store displacement magnitudes
displacements = []
for sim in range(sim_num): 
    filename = os.getcwd() + f'\\data\\test_{test_number}\\{sim}\\reports\\run0001report.txt'
    with open(filename) as f:
        # puts each line into as a string into a list
        lines = f.read().splitlines()
    # column names located on this line
    col_names = lines[4].split()[1:]
    # keeps all strings with the relevant information
    lines = [line.split() for line in lines if len(line.split()) == (8 if motor_type == 'rod' else 9)]
    # center of mass coordinates 
    df = pd.DataFrame(lines, columns=col_names)[coord_columns].astype('float64')
    # starting coordinates repeated for proper row subtraction
    xy_series = pd.concat([df[coord_columns][0:actin_num]]*len(times), ignore_index=True)
    # difference in center of mass coordinates at time frame
    diff = ((df[coord_columns] - xy_series)**2).assign(dummy=df.index//actin_num).groupby(by='dummy').mean()
    # magnitude of displacement 
    displ = diff.apply(lambda x: x[0] + x[1], axis=1)
    displacements.append(list(displ))
displacements = np.array(displacements).mean(axis=0)
fig, ax = plt.subplots(figsize=(plot_length, plot_height))
ax.set_title(f'{motor_type.capitalize()} motor displacement over time (1000 motors) (Average over {sim_num} simulations)')
ax.set_xlabel('Seconds (s)')
ax.set_ylabel('Displacement Squared (um^2)')
ax.plot(times, displacements)
plt.savefig(os.getcwd() + f"\\plots\\\diffusion\\{motor_type}diffusion.png")
# %% Compiler data
# initialization
# needed for group
group_num = 20
starting_test = 1525
motor_list = sorted(set([10**o + j*10**o for o in range(2, 4) for j in range(0, 10)]))
motor_type = 'rod'
var_list = [2, 4, 6, 8, 16, 32]
sim_time = 5
group_name = f'(flexible {motor_type} motor) (with motor velocity) (90% bare zone)'
# needed for test
var_name = 'heads'
time_frames_key = 3
binding_ranges_key = 10
sim_num = 10
# %% Tests in cytosiminformation.txt 
for t, tup in enumerate([(i, k) for i in motor_list for k in var_list], starting_test):
    m, v = tup
    test_str = f"{t}: ({time_frames_key}, {binding_ranges_key}, {v}, {sim_time}, '{motor_type}')"
    print(test_str) if v != var_list[0] else print(test_str + f" # {m} motors")
# %% Groups in cytosiminformation.txt 
var_num = len(var_list)
print(f"Group {group_num}: ({[starting_test + var_num*i + j for i in range(len(motor_list)) for j in range(var_num)]}, '{group_name}')")
# %% Test-job matcher 
motor_list = sorted(set([10**o + j*10**o for o in range(2, 4) for j in range(0, 10)]))
test = starting_test
for i, m in enumerate(motor_list):
    for j, v in enumerate(var_list):
        for k in range(sim_num):
            print(f'{sim_time} seconds test_{test} job{sim_num*len(var_list)*i + sim_num*j + k}: {m} motors, {var_name} = {v}')
        test += 1
# %% Group information
group = 16
group_tests, group_name, motor_list, var_list, binding_ranges, var_name, sim_time, sim_num = searchcytosiminfo(group, 'group')
print(f'Tests: {group_tests} \nGroup Name: {group_name} \nMotor Counts: {motor_list} \nVariable List: {var_list} \n'
      f'Binding Ranges: {list(binding_ranges)} \nVariable Name: {var_name.capitalize()} \nSimulation Time: {sim_time} \n'
      f'Number of Simulations: {sim_num}')