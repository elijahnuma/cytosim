import os 
import re 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Units and terminology descriptions are in readmejargon.txt in cytosim directory

plot_length, plot_height = 10, 10
font_size = 8

def searchcytosiminfo(group_num):
    """
    finds information of group in cytosiminformation.txt
    
    args: 
        group_num (int): group number
    
    returns information as tuple
    """
    with open('cytosiminformation.txt', 'r') as f:
        # removes newlines
        file = f.read().splitlines()
        # grabs test information
        # s for string
        group_line = [s for s in file if f"Group Tests {group_num}:" in s][0]
        group_tests = eval(re.sub(f'Group Tests {group_num}: ', '', group_line))
        group_name_line = [s for s in file if f"Group Name {group_num}:" in s][0]
        group_name = re.sub(f'Group Name {group_num}: ', '', group_name_line)
        motors_line = [s for s in file if f"Motors {group_num}:" in s][0]
        motor_list = eval(re.sub(f'Motors {group_num}: ', '', motors_line))
        motor_type_line = [s for s in file if f"Motor Type {group_num}:" in s][0]
        motor_type = re.sub(f'Motor Type {group_num}: ', '', motor_type_line)
        var_name_line = [s for s in file if f"Variable Name {group_num}:" in s][0]
        var_name = re.sub(f'Variable Name {group_num}: ', '', var_name_line)
        var_line = [s for s in file if f"Variable {group_num}:" in s][0]
        var_list = eval(re.sub(f'Variable {group_num}: ', '', var_line))
        binding_ranges_line = [s for s in file if f"Binding Ranges {group_num}:" in s][0]
        binding_ranges = eval(re.sub(f'Binding Ranges {group_num}: ', '', binding_ranges_line))
        time_frames_line = [s for s in file if f"Time Frames {group_num}:" in s][0]
        time_frames = re.sub(f'Time Frames {group_num}: ', '', time_frames_line) # time_frames is evaled after sim_time
        sim_time_line = [s for s in file if f"Sim Time {group_num}:" in s][0]
        sim_time = eval(re.sub(f'Sim Time {group_num}: ', '', sim_time_line))
        sim_num_line = [s for s in file if f"Sim Num {group_num}:" in s][0]
        sim_num = eval(re.sub(f'Sim Num {group_num}: ', '', sim_num_line))
    # test numbers, group description, motor type, motor values, variable name, variable values, binding ranges, ...
    # time subdivisions, simulation time, number of simulations
    return (group_tests, group_name, motor_type, motor_list, var_name, var_list, binding_ranges, eval(time_frames), sim_time, sim_num)
    
def anchor_maker(heads_num, motor_type, bare_zone):
    """ 
    makes anchors for rod motors in .cym file
    
    args:
        heads_num (int): number of heads
        motor_type (str): rod type
        bare_zone (float): middle bare zone as percentage
    
    """
    L = 0.8                     # 0.8 um rod length
    mp = bare_zone/100          # middle percent
    b = 0.5 - mp/2              # left end bare zone marker
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

def metadata(info_num, log=True, show_plot=True):
    """ 
    plots computational time and max memory used against motor count 
    
    args:
        info_num (int): information folders checked
        log (bool): sets log scale; default True
        show_plot (bool): shows plot; default True
    
    returns computational times and memory usages as dict of dicts
    """
    _, group_name, _, motor_list, var_name, var_list, binding_ranges, _, sim_time, sim_num, = searchcytosiminfo(info_num)
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
        # number of times motor count is changed
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
        # sort arrays organized by motor count -> variable count
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
            title_suffix = f'(binding range = {br} um) ({sim_time} seconds) {group_name} '
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
    # saving dataframes into readable csvs
    messages_df = pd.DataFrame.from_dict(messages_dicts, 'index').stack().rename_axis(['Binding Range', 'Heads'])
    messages_df = messages_df.apply(pd.Series, index=motor_list).reset_index()
    messages_df.to_csv(path_or_buf=cwd + f"\\csvs\\metadata\\computationaltime\\computationaltime{csv_suffix}.csv", index=False)
    memorys_df = pd.DataFrame.from_dict(memorys_dicts, 'index').stack().rename_axis(['Binding Range', 'Heads'])
    memorys_df = memorys_df.apply(pd.Series, index=motor_list).reset_index()
    memorys_df.to_csv(path_or_buf=cwd + f"\\csvs\\metadata\\memoryusage\\memoryusage{csv_suffix}.csv", index=False)
    return messages_dicts, memorys_dicts
        
def plot_handler(df, plot_title, y_label, legend_label, vs, fig_location, slice_plot):
    """
    handles plots
    
    args:
        df (pandas.DataFrame): dataframe of interest
        plot_title (str): title of plot
        y_label (str): y label
        legend_label (str): name of legend
        vs (str): versus metric of plot
        fig_location (list of str): figure save location
        slice_plot (bool): slice data into three plot
        
    """
    if slice_plot:
        # creates figures and axes
        fig, axes = plt.subplots(nrows=3, ncols=1)
        plt.subplots_adjust(hspace=0.5)
        # adds label to legend
        df = df.add_prefix('Binding Range = ')
        # plot
        df.plot(kind='line', y=df.columns[:len(df.columns)//3], figsize=(plot_length, plot_height), title=plot_title, ax=axes[0]).set(ylabel=y_label)
        df.plot(kind='line', y=df.columns[len(df.columns)//3:2*len(df.columns)//3], figsize=(plot_length, plot_height), ax=axes[1]).set(ylabel=y_label)
        df.plot(kind='line', y=df.columns[2*len(df.columns)//3:], figsize=(plot_length, plot_height), ax=axes[2]).set(ylabel=y_label)
        for a in axes:
            a.grid(True, which='both')
            a.title.set_size(font_size)
    else:
        fig, ax = plt.subplots(nrows=1, ncols=1)
        # check if df has NaN values
        has_nan = df.isnull().values.any()
        if has_nan:
            # plots columns seperately if there are NaN values
            for c in df.columns:
                df[c].dropna().plot(kind='line', figsize=(plot_length, plot_height), ax=ax, title=plot_title, logx=True).set(ylabel=y_label)
        else:
            df.plot(kind='line', figsize=(plot_length, plot_height), ax=ax, title=plot_title, logx=True).set(ylabel=y_label)
        ax.grid(True, which='both')
        ax.legend(title=f'{legend_label}:')
        ax.title.set_size(font_size)
    fig_location = '\\'.join(fig_location)
    fig.savefig(cwd + f'\\plots\\plotsvs{vs}\\{fig_location}.png')
    df.to_csv(path_or_buf=cwd + f"\\csvs\\csvsvs{vs}\\{fig_location}.csv", index=True)
# %% Main loops
# groups under consideration
for group_num in [*range(6, 22)]:
    # saves dfs at group-level to compare
    group_cluster_delta_dfs = []
    group_max_contraction_dfs = []
    group_max_contraction_time_dfs = []
    group_attach_dfs = []
    # sets group information
    group_tests, group_name, motor_type, motor_list, var_name, var_list, binding_ranges, time_frames, sim_time, sim_num = searchcytosiminfo(group_num)
    # runs through each test, enumerating for variable and motor cycling
    for t, test_number in enumerate(group_tests):
        ## test initialization
        var = var_list[t % len(var_list)]
        motor_count = motor_list[t//len(var_list)]
        # dataframe initialization when variable cycle resets
        if var == var_list[0]:
            # saves dfs at variable-level to compare
            variable_cluster_delta_dfs = []
            variable_max_contraction_dfs = []
            variable_max_contraction_time_dfs = []
            variable_attach_dfs = []
        cwd = os.getcwd()
        # number of sims of one run
        sim_num = len(os.listdir(os.path.join(cwd, 'data', f'test_{test_number}')))
        # number of runs
        run_count = len(os.listdir(os.path.join(cwd, 'data', f'test_{test_number}', '0', 'reports')))
        ## csv compiling
        # concats all sims of csv files together as DataFrame
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
        ## further analyzes csv dataframes
        # cluster size delta from beginning to end (negative so we capture magnitude)
        df_cluster_delta = -pd.DataFrame(df_cluster.iloc[-1] - df_cluster.iloc[0]).rename(columns={df_cluster.index[0]: var}).rename_axis('Binding range (um)')
        # max contraction rate
        df_max_contraction = pd.DataFrame(df_contraction.max()).rename(columns={df_contraction.index[0]: var}).rename_axis('Binding range (um)')
        # max contraction rate time (min is because contraction is negative)
        df_max_contraction_time = pd.DataFrame(df_contraction.idxmax()).rename(columns={df_contraction.index[0]: var}).rename_axis('Binding range (um)')
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
                lines = [line for line in lines if 'myosin' in line]
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
        df_attach_delta = df_attach_delta.rename(columns={df_cluster.index[-1]: var}).rename_axis('Binding range (um)')*100
        # add dataframes to running list
        variable_cluster_delta_dfs.append(df_cluster_delta.copy())
        group_cluster_delta_dfs.append(df_cluster_delta.copy())
        variable_max_contraction_dfs.append(df_max_contraction.copy())
        group_max_contraction_dfs.append(df_max_contraction.copy())
        variable_max_contraction_time_dfs.append(df_max_contraction_time.copy())
        group_max_contraction_time_dfs.append(df_max_contraction_time.copy())
        variable_attach_dfs.append(df_attach_delta.copy())
        group_attach_dfs.append(df_attach_delta.copy())
        ## plots and csvs
        # metric plotted
        vs_metric = 'time'
        # suffixes
        title_suffix = f'({var} {var_name}) ({motor_count} motors) ({sim_time} sec) {group_name}'
        fig_suffix = f"({var}{var_name})({motor_count}motors)({sim_time}seconds){group_name.replace(' ', '').lower()}"
        # cluster size over time plot
        df_title = f'Cluster size vs {vs_metric} {title_suffix}'
        locations = ['work', f'work{fig_suffix}']
        plot_handler(df=df_cluster, plot_title=df_title, y_label='Cluster size (um)', legend_label=var_name, vs=vs_metric, fig_location=locations, slice_plot=True)
        # contraction rate over time plot
        df_title = f'Contraction rate magnitude vs {vs_metric} {title_suffix}'
        locations = ['power', f'power{fig_suffix}']
        plot_handler(df=df_contraction, plot_title=df_title, y_label='Contraction rate magnitude (um/s)', legend_label=var_name, vs=vs_metric, fig_location=locations, slice_plot=True)
        # attachment of hands over time
        df_title = f'Attachment of hands vs {vs_metric} {title_suffix}'
        locations = ['attachhands', f'attachhands{fig_suffix}']
        plot_handler(df=df_attach, plot_title=df_title, y_label='Hands attached', legend_label=var_name, vs=vs_metric, fig_location=locations, slice_plot=True)
        # analysis before variable cycle reset
        if var == var_list[-1]:
            # new suffix since this is variable-level
            title_suffix = f'({motor_count} motors) ({sim_time} sec) {group_name}'
            fig_suffix = f"({motor_count}motors)({sim_time}seconds){group_name.replace(' ', '').lower()}"
            csv_suffix = fig_suffix
            # metric plotted
            vs_metric = 'binding range'
            # flatten variable dataframes to plot
            variable_cluster_delta_dfs = pd.concat(variable_cluster_delta_dfs, axis=1)
            variable_max_contraction_dfs = pd.concat(variable_max_contraction_dfs, axis=1)
            variable_max_contraction_time_dfs = pd.concat(variable_max_contraction_time_dfs, axis=1)
            variable_attach_dfs = pd.concat(variable_attach_dfs, axis=1)
            # cluster size delta from beginning to end plot
            df_title = f'Contraction delta magnitude vs {vs_metric} {title_suffix}'
            metric_description = 'Contraction delta magnitude (um)'
            locations = ['work', f'work{fig_suffix}']
            plot_handler(df=variable_cluster_delta_dfs, plot_title=df_title, y_label=metric_description, legend_label=var_name, vs=vs_metric, fig_location=locations, slice_plot=False)
            # max contraction rate plot
            df_title = f'Max contraction rate magnitude vs {vs_metric} {title_suffix}'
            metric_description = 'Max contraction rate magnitude (um/s)'
            locations = ['maxpower', f'maxpower{fig_suffix}']
            plot_handler(df=variable_max_contraction_dfs, plot_title=df_title, y_label=metric_description, legend_label=var_name, vs=vs_metric, fig_location=locations, slice_plot=False)
            # max contraction rate time plot
            df_title = f'Max contraction rate time vs {vs_metric} {title_suffix}'
            metric_description = 'Max contraction rate time (s)'
            locations = ['maxpowertime', f'maxpowertime{fig_suffix}']
            plot_handler(df=variable_max_contraction_time_dfs, plot_title=df_title, y_label=metric_description, legend_label=var_name, vs=vs_metric, fig_location=locations, slice_plot=False)
            # attachment of hands % delta from beginning to end plot
            df_title = f'Attachment of hands % delta vs {vs_metric} {title_suffix}'
            metric_description = 'Attachment of hands delta (%)'
            locations = ['attachdelta', f'attachdelta{fig_suffix}']
            plot_handler(df=variable_attach_dfs, plot_title=df_title, y_label=metric_description, legend_label=var_name, vs=vs_metric, fig_location=locations, slice_plot=False)
    # flattens dfs
    group_cluster_delta_dfs = pd.concat(group_cluster_delta_dfs, axis=1)
    group_max_contraction_dfs = pd.concat(group_max_contraction_dfs, axis=1)
    group_max_contraction_time_dfs = pd.concat(group_max_contraction_time_dfs, axis=1)
    ## Analyzing motor data with respect to motor count
    # metadata
    times, memory = metadata(info_num=group_num)
    # column names
    col_names = list(group_cluster_delta_dfs.copy().columns)
    cols = col_names[:len(var_list)]
    # binding ranges of interest
    for binding_range in binding_ranges:
        # suffixes
        title_suffix = f'(binding range = {binding_range} um) ({sim_time} seconds) {group_name}'
        fig_suffix = f"({binding_range}bindingrange)({sim_time}seconds){group_name.replace(' ', '').lower()}"
        # metadata dfs
        times_df = pd.DataFrame(times[binding_range], index=motor_list)
        memory_df = pd.DataFrame(memory[binding_range], index=motor_list)
        ## analysis
        # contraction delta magnitude vs motor (work)
        delta = pd.DataFrame(group_cluster_delta_dfs.loc[binding_range].values.reshape((group_cluster_delta_dfs.shape[1]//len(cols), len(cols))), index=motor_list, columns=cols)
        delta_df = pd.DataFrame(delta, index=motor_list).rename_axis('Motor count')
        # contraction delta per computational time vs motor (work time efficiency)
        delta_time_efficiency_df = delta_df/times_df.values
        # contraction delta per memory usage vs motor (work memory efficiency)
        delta_memory_efficiency_df = delta_df/memory_df.values
        # max contraction rate vs motor (max power)
        max_contraction = pd.DataFrame(group_max_contraction_dfs.loc[binding_range].values.reshape((group_max_contraction_dfs.shape[1]//len(cols), len(cols))), index=motor_list, columns=cols)
        max_contraction_df = pd.DataFrame(max_contraction, index=motor_list).rename_axis('Motor count')        
        # max contraction rate vs total motor count (by scaling) (max power)
        df = max_contraction_df.copy()
        # multiplies by number of heads per motor, for point motors there are only 2 heads
        scaling_max_contraction_df = pd.concat([df[v].rename(index=dict(zip(df[v].index, df[v].index*(2 if motor_type == 'point' else v)))) for v in var_list], axis=1)
        scaling_max_contraction_df = scaling_max_contraction_df.rename_axis('Total head count')
        # max contraction rate per computational time vs motor (max power time efficiency)
        max_contraction_time_efficiency_df = max_contraction_df/times_df.values
        # max contraction rate per computational time vs total motor count (by scaling) (max power time efficiency)
        df = max_contraction_time_efficiency_df.copy()
        # multiplies by number of heads per motor, for point motors there are only 2 heads
        scaling_max_contraction_time_efficiency_df = pd.concat([df[v].rename(index=dict(zip(df[v].index, df[v].index*(2 if motor_type == 'point' else v)))) for v in var_list], axis=1)
        scaling_max_contraction_time_efficiency_df = scaling_max_contraction_time_efficiency_df.rename_axis('Total head count')
        # max contraction rate per memory usage vs motor (max power memory efficiency)
        max_contraction_memory_efficiency_df = max_contraction_df/memory_df.values
        # max contraction rate time vs motor (max power time)
        max_contraction_time = pd.DataFrame(group_max_contraction_time_dfs.loc[binding_range].values.reshape((group_max_contraction_time_dfs.shape[1]//len(cols), len(cols))), index=motor_list, columns=cols)
        max_contraction_time_df = pd.DataFrame(max_contraction_time, index=motor_list).rename_axis('Motor count')
        ## plots
        # metric plotted
        vs_metric = 'motors'
        # contraction delta magnitude vs motor (work)
        df_title = f'Contraction delta magnitude vs {vs_metric} {title_suffix}'
        metric_description = 'Contraction delta magnitude (um)'
        locations = ['work', 'work', f'work{fig_suffix}']
        plot_handler(df=delta_df, plot_title=df_title, y_label=metric_description, legend_label=var_name, vs=vs_metric, fig_location=locations, slice_plot=False)
        # contraction delta per computational time vs motor (work time efficiency)
        df_title = f'Contraction delta magnitude per computational time vs {vs_metric} {title_suffix}'
        metric_description = 'Contraction delta magnitude per computational time (um/S)'
        locations = ['work', 'efficiency', 'computationaltime', f'worktimeefficiency{fig_suffix}']
        plot_handler(df=delta_time_efficiency_df, plot_title=df_title, y_label=metric_description, legend_label=var_name, vs=vs_metric, fig_location=locations, slice_plot=False)
        # contraction delta per memory usage vs motor (work memory efficiency)
        df_title = f'Contraction delta magnitude per memory usage vs {vs_metric} {title_suffix}'
        metric_description = 'Contraction delta magnitude per memory usage (um/MB)'
        locations = ['work', 'efficiency', 'memoryusage', f'workmemoryefficiency{fig_suffix}']
        plot_handler(df=delta_memory_efficiency_df, plot_title=df_title, y_label=metric_description, legend_label=var_name, vs=vs_metric, fig_location=locations, slice_plot=False)
        # max contraction rate vs motor (max power)
        df_title = f'Max contraction rate magnitude vs {vs_metric} {title_suffix}'
        metric_description = 'Max contraction rate magnitude (um/s)'
        locations = ['maxpower', 'maxpower', 'nonscaling', f'maxpower{fig_suffix}']
        plot_handler(df=max_contraction_df, plot_title=df_title, y_label=metric_description, legend_label=var_name, vs=vs_metric, fig_location=locations, slice_plot=False)
        # max contraction rate vs total motor count (by scaling) (max power)
        scaling_max_contraction_title = f'Max contraction rate magnitude vs total head count {title_suffix}'
        metric_description = 'Max contraction rate magnitude (um/s)'
        locations = ['maxpower', 'maxpower', 'scaling', f'scalingmaxpower{fig_suffix}']
        plot_handler(df=scaling_max_contraction_df, plot_title=df_title, y_label=metric_description, legend_label=var_name, metric=vs_metric, fig_location=locations, slice_plot=False)
        # max contraction rate per computational time vs motor (max power time efficiency)
        df_title = f'Max contraction rate magnitude per computational time vs {vs_metric} {title_suffix}'
        metric_description = 'Max contraction rate magnitude per computational time (um/s/S)'
        locations = ['maxpower', 'efficiency', 'computationaltime', f'maxpowertimeefficiency{fig_suffix}']
        plot_handler(df=max_contraction_time_efficiency_df, plot_title=df_title, y_label=metric_description, legend_label=var_name, metric=vs_metric, fig_location=locations, slice_plot=False)
        # max contraction rate per computational time vs motor (by scaling) (max power time efficiency)
        scaling_max_contraction_time_efficiency_title = f'Max contraction rate magnitude per computational time vs total head count {title_suffix}'
        metric_description = 'Max contraction rate magnitude per computational time (um/s/S)'
        locations = ['maxpower', 'efficiency', 'scalingcomputationaltime', f'scalingmaxpowertimeefficiency{fig_suffix}']
        plot_handler(df=scaling_max_contraction_time_efficiency_df, plot_title=df_title, y_label=metric_description, legend_label=var_name, metric=vs_metric, fig_location=locations, slice_plot=False)
        # max contraction rate per memory usage vs motor (max power memory efficiency)
        df_title = f'Max contraction rate magnitude per memory usage vs {vs_metric} {title_suffix}'
        metric_description = 'Max contraction rate magnitude per memory usage (um/s/MB)'
        locations = ['maxpower', 'efficiency', 'memoryusage', f'maxpowermemoryefficiency{fig_suffix}']
        plot_handler(df=max_contraction_memory_efficiency_df, plot_title=df_title, y_label=metric_description, legend_label=var_name, metric=vs_metric, fig_location=locations, slice_plot=False)
        # max contraction rate time vs motor (max power time)
        df_title = f'Max contraction rate time vs {vs_metric} {title_suffix}'
        metric_description = 'Seconds (s)'
        locations = ['maxpower', 'maxpowertime', f'maxpowertime{fig_suffix}']
        plot_handler(df=max_contraction_time_df, plot_title=df_title, y_label=metric_description, legend_label=var_name, metric=vs_metric, fig_location=locations, slice_plot=False)
# %% Tracking diffusion
# intializers
test_number = 579
motor_types = {578: 'rod', 579: 'point'}
sim_time = 10
times = np.concatenate([np.linspace(0, 0.25, 2), np.linspace(0.5, sim_time + 0.5, 101)])
motor_type = motor_types[test_number]
sim_num = len(os.listdir(os.path.join(os.getcwd(), 'data', f'test_{test_number}')))
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
    col_name_len = len(col_names)
    # keeps all strings with the relevant information
    lines = [line.split() for line in lines if len(line.split()) == col_name_len]
    # center of mass coordinates 
    df = pd.DataFrame(lines, columns=col_names)[coord_columns].astype('float64')
    # starting coordinates repeated for proper row subtraction
    xy_series = pd.concat([df[coord_columns][0:actin_num]]*len(times), ignore_index=True)
    # difference in center of mass coordinates at time frame
    diff = ((df[coord_columns] - xy_series)**2).assign(dummy=df.index//actin_num).groupby(by='dummy').mean()
    # magnitude of displacement 
    displ = diff.apply(lambda x: x[0] + x[1], axis=1)
    displacements.append(list(displ))
# averages displacements
displacements = np.array(displacements).mean(axis=0)
fig, ax = plt.subplots(figsize=(plot_length, plot_height))
ax.set_title(f'{motor_type.capitalize()} motor displacement over time (1000 motors) (Average over {sim_num} simulations)')
ax.set_xlabel('Seconds (s)')
ax.set_ylabel('Displacement Squared (um^2)')
ax.plot(times, displacements)
plt.savefig(os.getcwd() + f"\\plots\\\diffusion\\{motor_type}diffusion.png")
# %% Group initialization compiler
# initialization
group_num = 20
starting_test = 1525
motor_list = sorted(set([10**o + j*10**o for o in range(2, 4) for j in range(0, 10)]))
motor_type = 'rod'
var_list = [2, 4, 6, 8, 16, 32]
sim_time = 5
group_name = f'(flexible {motor_type} motor) (with motor velocity) (90% bare zone)'
# %% Groups in cytosiminformation.txt 
var_num = len(var_list)
print(f"Group {group_num}: ({[starting_test + var_num*i + j for i in range(len(motor_list)) for j in range(var_num)]}, '{group_name}')")
# %% Test-job matcher
group = 21 
*_, motor_list, _, var_list, _, _, sim_time, sim_num = searchcytosiminfo(group)
test = starting_test
for i, m in enumerate(motor_list):
    for j, v in enumerate(var_list):
        for k in range(sim_num):
            print(f'{sim_time} seconds test_{test} job{sim_num*len(var_list)*i + sim_num*j + k}: {m} motors, {var_name} = {v}')
        test += 1
# %% Group and test file information
with open('groupstestsinformation.txt', 'w') as f:
    for group in range(6, 22):
        # names of group info variables
        group_info_names = ['Tests', 'Group Name', 'Motor Type', 'Motor Counts', 'Variable Name', 'Variable List', 'Binding Ranges (um)',
                            'Time Frames (s)', 'Simulation Time (s)', 'Number of Simulations']
        group_info = dict(zip(group_info_names, searchcytosiminfo(group)))
        # sets Pandas series and numpy arrays to lists
        group_info['Binding Ranges (um)'] = list(group_info['Binding Ranges (um)'])
        group_info['Time Frames (s)'] = list(group_info['Time Frames (s)'].round(2))
        # finds test info for first test to print tests
        f.write(f'Group {group}\n')
        for name, info in group_info.items():
            f.write(f'{name}: {info}\n')
        f.write('\n')
    for group in range(6, 22):
        # names of group info variables
        group_info_names = ['Tests', 'Group Name', 'Motor Type', 'Motor Counts', 'Variable Name', 'Variable List', 'Binding Ranges (um)',
                            'Time Frames (s)', 'Simulation Time (s)', 'Number of Simulations']
        group_info = dict(zip(group_info_names, searchcytosiminfo(group)))
        # sets Pandas series and numpy arrays to lists
        group_info['Binding Ranges (um)'] = list(group_info['Binding Ranges (um)'])
        group_info['Time Frames (s)'] = list(group_info['Time Frames (s)'].round(2))
        for t, test in enumerate(group_info['Tests']):
            test_info = group_info.copy()
            # change variable and motor count lists to test variable and motor count
            test_info['Variable List'] = group_info['Variable List'][t % len(group_info['Variable List'])]
            test_info['Variable'] = test_info['Variable List']
            del test_info['Variable List']
            test_info['Motor Counts'] = group_info['Motor Counts'][t//len(group_info['Variable List'])]
            test_info['Motor Count'] = test_info['Motor Counts']
            del test_info['Motor Counts']
            # delete unneeded group information
            del test_info['Tests']
            # finds test info for first test to print tests
            f.write(f'Test {test}\n')
            for name, info in test_info.items():
                f.write(f'{name}: {info}\n')
            f.write('\n')
        # writes in diffusion tests
        if group == 8:
            f.write('Test 578\nRod Diffusion\n\nTest 579\nPoint Diffusion\n\n')
f.close()
