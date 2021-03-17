import os 
import re 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plot_length, plot_height = 10, 10

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
            description = re.search("\'([a-z]|[A-Z]|[0-9]|\s)+\'", test_line).group(0)[1:-1] # [1:-1] to strip quotation marks
            test_info = re.search("\(.*\)", test_line).group(0)
            names_key, test_range_key, sim_time, motor_type = eval(test_info)
            # regex for names, test range list, and motor type
            names_line = [s for s in file if f"Names {names_key}:" in s][0]
            names = eval(re.sub(f'Names {names_key}: ', '', names_line))
            test_range_line = [s for s in file if f"Variable Range {test_range_key}:" in s][0]
            test_range = eval(re.sub(f'Variable Range {test_range_key}: ', '', test_range_line))
            attach_name_line = [s for s in file if f"Attach Name {motor_type}:" in s][0]
            attach_name = re.sub(f'Attach Name {motor_type}: ', '', attach_name_line)
        return (description, names, test_range, sim_time, motor_type, attach_name)
    if mode == 'group':
        group_name = request
        with open('cytosiminformation.txt', 'r') as f:
            file = f.read().splitlines()
            group_line = [s for s in file if f"{group_name}:" in s][0]
            group_info = group_line.split(": ")[1]
        return eval(group_info)
    if mode == 'metadata':
        motor_key = heads_key = sim_time_key = sim_num_key = var_range_key = var_name_key = request
        with open('cytosiminformation.txt', 'r') as f:
            file = f.read().splitlines()
            motors_line = [s for s in file if f"Motors {motor_key}:" in s][0]
            motors = eval(re.sub(f'Motors {motor_key}: ', '', motors_line))
            heads_line = [s for s in file if f"Heads {heads_key}:" in s][0]
            heads = eval(re.sub(f'Heads {heads_key}: ', '', heads_line))
            var_range_line = [s for s in file if f"Variables {var_range_key}:" in s][0]
            var_range = eval(re.sub(f'Variables {var_range_key}: ', '', var_range_line))
            var_name_line = [s for s in file if f"Variable Name {var_name_key}:" in s][0]
            var_name = re.sub(f'Variable Name {var_name_key}: ', '', var_name_line)
            sim_time_line = [s for s in file if f"Sim Time {sim_time_key}:" in s][0]
            sim_time = eval(re.sub(f'Sim Time {sim_time_key}: ', '', sim_time_line))
            sim_num_line = [s for s in file if f"Sim Num {sim_num_key}:" in s][0]
            sim_num = eval(re.sub(f'Sim Num {sim_num_key}: ', '', sim_num_line))
        return (motors, heads, var_range, var_name, sim_time, sim_num)
    
def anchor_maker(anchor_num, bare=True):
    """ 
    makes anchors for rod motors in .cym file
    
    args:
        anchor_num (int): number of anchors
        bare (bool): creates bare zone from 0.3 to 0.7 of rod
        
    """
    if bare:
        x = list(np.linspace(0.05, 0.3, anchor_num//2)) + list(np.linspace(0.7, 0.95, anchor_num//2))
    else:
        x = list(np.linspace(0.05, 0.95, anchor_num))
    for i, per in enumerate(x, 1):
        print(f'    anchor{i} = point1, point2, {round(per, 2)}, myosin;')  

def metadata(info_num, log=True, show_plot=True):
    """ 
    plots computational time and max memory used against motor count 
    
    args:
        info_num (int): information folders checked
        log (bool): sets log scale; default True
        show_plot (bool): shows plot; default True
    
    returns average computational times and memory usages for each variable as dict of dicts
    """
    # motor count list, heads count, variable range, simulated time, number of simulations
    motor_list, heads_list, var_range, var_name, sim_time, sim_num = searchcytosiminfo(info_num, 'metadata')
    cwd = os.getcwd()
    # number of messagescmo files, messagescmo and outtxt numbers should be equal 
    msg_num = len(os.listdir(os.path.join(cwd, 'metadata', f'messages_{info_num}')))
    messages_dicts, memorys_dicts = [], []
    # index of binding_range = 0.01 um is at 3
    for i, var in enumerate(var_range):
        messages, memorys = [], []
        for j in range(i, msg_num, len(var_range)):
            with open(cwd + f'\\metadata\\messages_{info_num}\\messages{j}.cmo', 'r') as f:
                file = f.readlines()
                seconds = file[-1]
                seconds = re.search('[0-9]+', seconds)[0]
                messages.append(seconds)
            with open(cwd + f'\\metadata\\outs_{info_num}\\out{j}.txt', 'r') as f:
                file = f.readlines()
                seconds = [s for s in file if "Max Memory" in s][0]
                seconds = re.search('[0-9]+\.[0-9]+', seconds)[0]
                memorys.append(seconds)
        # number of times motors variable is changed
        motor_num = len(motor_list)
        # number of times heads variable is changed
        heads_num = len(heads_list)
        # standard deviation calculator for array
        std = lambda arr: np.sqrt(sum((arr-np.mean(arr))**2)/len(arr))
        # reshape arrays
        messages = np.array(messages).astype(np.float64).reshape(motor_num, heads_num, sim_num)
        memorys = np.array(memorys).astype(np.float64).reshape(motor_num, heads_num, sim_num)
        # standard deivations
        messages_errors = np.apply_along_axis(std, 2, messages)
        memory_errors = np.apply_along_axis(std, 2, memorys)
        # average by simulation
        messages = np.mean(messages, axis=2)
        memorys = np.mean(memorys, axis=2)
        # sort arrays organized by motor multiplier -> heads count
        messages = np.column_stack(messages)
        memorys = np.column_stack(memorys)
        messages_errors = np.column_stack(messages_errors)
        memory_errors = np.column_stack(memory_errors)
        # sort into dictionaries for easier indexing
        messages_dict = {h: messages[i] for i, h in enumerate(heads_list)}
        memorys_dict = {h: memorys[i] for i, h in enumerate(heads_list)}
        messages_errors_dict = {h: messages_errors[i] for i, h in enumerate(heads_list)}
        memory_errors_dict = {h: memory_errors[i] for i, h in enumerate(heads_list)}
        if show_plot:
            # messages plot
            fig, ax = plt.subplots(figsize=(plot_length, plot_height))
            fignamelog = 'comptimelog' if log else 'comptimenolog'
            ax.set_title(f'Computational time vs. motors ({sim_time} second simulation) ({var_name} {var})')
            ax.set_xlabel('Motor #')
            ax.set_ylabel('Seconds (S)')
            if log:
                ax.set_xscale('log')
                ax.set_yscale('log')
            for head in sorted(messages_dict.keys()):
                ax.scatter(motor_list, messages_dict[head], label=f'{head} heads')
                ax.errorbar(motor_list, messages_dict[head], yerr=messages_errors_dict[head], fmt='none')
            ax.legend()
            ax.grid(True, which='both')
            plt.savefig(cwd + f"\\cytosimplots\\messages{info_num}{fignamelog}{var_name.replace(' ', '').lower()}{var}.png")
            # memory plot
            fig, ax = plt.subplots(figsize=(plot_length, plot_height))
            fignamelog = 'memorylog' if log else 'memorynolog'
            ax.set_title(f'Memory used vs. motors ({sim_time} second simulation) ({var_name} {var})')
            ax.set_xlabel('Motor #')
            ax.set_ylabel('Memory (MB)')
            if log:
                ax.set_xscale('log')
                ax.set_yscale('log')
            for head in sorted(memorys_dict.keys()):
                ax.scatter(motor_list, memorys_dict[head], label=f'{head} heads')
                ax.errorbar(motor_list, memorys_dict[head], yerr=memory_errors_dict[head], fmt='none')
            ax.legend()
            ax.grid(True, which='both')
            plt.savefig(cwd + f"\\cytosimplots\\memory{info_num}{fignamelog}{var_name.replace(' ', '').lower()}{var}.png")
        messages_dicts.append(messages_dict)
        memorys_dicts.append(memorys_dict)
    messages_dicts = dict(zip(var_range, messages_dicts)) 
    memorys_dicts = dict(zip(var_range, memorys_dicts)) 
    return messages_dicts, memorys_dicts
        
def plot_handler(df, title, test_num, description, y_label):
    """
    handles plots with many lines
    
    args:
        df (pandas.DataFrame): dataframe of interest
        title (str): title of plot
        test_num (int): test number
        description (str): description of plot for fig
        y_label (str): y label
        
    """
    fig, axes = plt.subplots(nrows=3, ncols=1)
    plt.subplots_adjust(hspace=0.5)
    df.plot(kind='line', y=test_range[:len(test_range)//3], figsize=(plot_length, plot_height), title=f'{title}', ax=axes[0]).set(ylabel=f'{y_label}')
    df.plot(kind='line', y=test_range[len(test_range)//3:2*len(test_range)//3], figsize=(plot_length, plot_height), ax=axes[1]).set(ylabel=f'{y_label}')
    df.plot(kind='line', y=test_range[2*len(test_range)//3:], figsize=(plot_length, plot_height), ax=axes[2]).set(ylabel=f'{y_label}')
    fig.savefig(cwd + f'\\cytosimplots\\{description}\\test{test_num}_{description}.png', bbox_inches='tight')
# %% Main loops
# saves dfs from each group to compare
compared_cluster_delta_dfs = []
compared_max_contraction_dfs = []
compared_max_contraction_time_dfs = []
compared_attach_dfs = []
# groups under consideration
groups = [f'{m} motors (2 sec)' for m in sorted(set([10**o + j*10**o for o in range(2, 5) for j in range(0, 10)]))]
for group in groups:  
    # color linestyle pairs generator
    linestyles = ['-', '--', ':', '-.']
    colors = ['red', 'blue', 'green', 'cyan', 'magenta', 'yellow', 'orange']
    color_linestyles = ((c, l) for l in linestyles for c in colors)
    ## plot and dataframe initialization 
    fig_cluster_delta, ax_cluster_delta = plt.subplots(nrows=1, ncols=1)
    fig_max_contraction, ax_max_contraction = plt.subplots(nrows=1, ncols=1)
    fig_max_contraction_time, ax_max_contraction_time = plt.subplots(nrows=1, ncols=1)
    fig_attach_delta, ax_attach_delta = plt.subplots(nrows=1, ncols=1)
    ax_attach_delta.set_ylim(0, 1)
    # saves dfs from each test for this group
    test_group_cluster_delta_dfs = []
    test_group_max_contraction_dfs = []
    test_group_max_contraction_time_dfs = []
    test_group_attach_dfs = []
    # sets group information
    group_tests, group_log, title_parenthetical, metadata_num = searchcytosiminfo(group, 'group')
    # runs through each test
    for test_number in group_tests:
        # sets test information
        test_description, names_list, test_range, sim_time, motor_type, attach_name = searchcytosiminfo(test_number, 'test')
        # color linestyle pairs
        color, linestyle = next(color_linestyles)
        cwd = os.getcwd()
        # number of sims of one run
        sim_num = len(os.listdir(os.path.join(cwd, 'tests', f'test_{test_number}')))
        # number of runs
        try:
            run_count = len(os.listdir(os.path.join(cwd, 'tests', f'test_{test_number}', '0', 'reports')))
        except FileNotFoundError:
            print('FileNotFoundError: There is no report')
        ## csv compiling
        # concats csv files together as DataFrame
        df_cluster_size_list = []
        df_contraction_list = []
        for sim in range(sim_num): 
            df_cluster_size_list.append(pd.read_csv(cwd + f'\\tests\\test_{test_number}\\{sim}\\Data_Files\\Rdata.csv', names=names_list).set_index(test_range).transpose().rename_axis('Second (s)'))
            df_contraction_list.append(pd.read_csv(cwd + f'\\tests\\test_{test_number}\\{sim}\\Data_Files\\Cdata.csv', names=names_list).set_index(test_range).transpose().rename_axis('Second (s)'))
        df_cluster_concat = pd.concat(df_cluster_size_list)
        df_contraction_concat = pd.concat(df_contraction_list)
        # averaging the concat dfs over simulations
        df_cluster = df_cluster_concat.groupby(df_cluster_concat.index).mean()
        df_contraction = df_contraction_concat.groupby(df_contraction_concat.index).mean()
        ## further analyzes csv DataFrames
        # cluster size delta from beginning to end
        df_cluster_delta = pd.DataFrame(df_cluster.iloc[-1] - df_cluster.iloc[0]).rename(columns={df_cluster.index[0]: test_description}).rename_axis('Binding Range (um)')
        test_group_cluster_delta_dfs.append(df_cluster_delta.copy())
        # max contraction rate (min is because contraction is negative)
        df_max_contraction = pd.DataFrame(df_contraction.min()).rename(columns={df_contraction.index[0]: test_description}).rename_axis('Binding Range (um)')
        test_group_max_contraction_dfs.append(df_max_contraction.copy())
        # max contraction rate time (min is because contraction is negative)
        df_max_contraction_time = pd.DataFrame(df_contraction.idxmin()).rename(columns={df_contraction.index[0]: test_description}).rename_axis('Binding Range (um)')
        test_group_max_contraction_time_dfs.append(df_max_contraction_time.copy())          
        # attachment of hands over time   
        if attach_name != None:
            df_dict = {float(run): [] for run in range(run_count)}
            for sim in range(sim_num):
                for run in range(run_count):
                    run_str = f'run000{run+1}' if run+1 < 10 else f'run00{run+1}' if run+1 < 100 else f'run0{run+1}'
                    filename = cwd + f'\\tests\\test_{test_number}\\{sim}\\reports\\{run_str}report.txt'
                    with open(filename) as f:
                        # puts each line into as a string into a list
                        lines = f.read().splitlines()
                    # keeps all strings with the motor name
                    lines = [line for line in lines if attach_name in line]
                    # keeps value in last column
                    lines = [line.split()[-1] for line in lines]
                    df = pd.DataFrame(lines).set_index(names_list)
                    # renames column to independent variable
                    df = df.rename(columns={df.columns[-1]: test_range[run]})
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
            df_report = pd.concat(df_concats, axis=1).fillna(0)
            # attachment of hands over time
            attach_title = f'{test_description} attachment of hands {title_parenthetical}'
            plot_handler(df=df_report, title=attach_title, test_num=test_number, description=f'attachhandsovertime', y_label='Hands attached')
            # divides final value by maximum number of hands
            df_attach_delta = pd.DataFrame(df_report.iloc[-1]/df_report.max().max())
            # attachment of hands delta as percent, renames column to description, renames index
            df_attach_delta = df_attach_delta.rename(columns={df_cluster.index[-1]: test_description}).rename_axis('Binding range (um)')
            # cluster size delta from beginning to end plot
            df_attach_delta.plot(kind='line', figsize=(plot_length, plot_height), color=color, linestyle=linestyle, ax=ax_attach_delta, title=f'Attachment of hands % delta {title_parenthetical}', logx=group_log).set(ylabel='Attachment of hands delta (%)')
            test_group_attach_dfs.append(df_attach_delta.copy())
        ## plots
        # cluster size over time plot
        cluster_title = f'{test_description} {title_parenthetical} (Average over {sim_num} sims)'
        plot_handler(df=df_cluster, title=cluster_title, test_num=test_number, description=f'clustersizeovertime', y_label='Cluster size')
        # contraction rate over time plot
        contraction_title = f'{test_description} {title_parenthetical} (Average over {sim_num} sims)'
        plot_handler(df=df_contraction, title=contraction_title, test_num=test_number, description=f'contractionrateovertime', y_label='Contraction rate')
        # cluster size delta from beginning to end plot
        df_cluster_delta.plot(kind='line', figsize=(plot_length, plot_height), color=color, linestyle=linestyle, ax=ax_cluster_delta, title=f'Cluster size delta {title_parenthetical}', logx=group_log).set(ylabel='Cluster size delta (um)')
        # max contraction rate plot
        df_max_contraction.plot(kind='line', figsize=(plot_length, plot_height), color=color, linestyle=linestyle, ax=ax_max_contraction, title=f'Max contraction {title_parenthetical}', logx=group_log).set(ylabel='Max contraction (um/s)')        
        # max contraction rate plot
        df_max_contraction_time.plot(kind='line', figsize=(plot_length, plot_height), color=color, linestyle=linestyle, ax=ax_max_contraction_time, title=f'Max contraction time {title_parenthetical}', logx=group_log).set(ylabel='Max contraction time (s)')  
    # save delta, doesn't save if individual test done
    if group != 'manual':
        fig_cluster_delta.savefig(cwd + f"\\cytosimplots\\clusterdelta\\clusterdelta{group.replace(' ', '')}.png", bbox_inches='tight')
        fig_max_contraction.savefig(cwd + f"\\cytosimplots\\maxcontraction\\maxcontraction{group.replace(' ', '')}.png", bbox_inches='tight')
        fig_max_contraction_time.savefig(cwd + f"\\cytosimplots\\maxcontractiontime\\maxcontractiontime{group.replace(' ', '')}.png", bbox_inches='tight')
        fig_attach_delta.savefig(cwd + f"\\cytosimplots\\attachdelta\\attachdelta{group.replace(' ', '')}.png", bbox_inches='tight')
    compared_cluster_delta_dfs.append(pd.concat(test_group_cluster_delta_dfs, axis=1))
    compared_max_contraction_dfs.append(pd.concat(test_group_max_contraction_dfs, axis=1))
    compared_max_contraction_time_dfs.append(pd.concat(test_group_max_contraction_time_dfs, axis=1))
    compared_attach_dfs.append(pd.concat(test_group_attach_dfs, axis=1))
# %% Initializer
motor_list = sorted(set([10**o + j*10**o for o in range(2, 5) for j in range(0, 10)]))
heads_list = [2, 4, 6, 8, 16, 32]
binding_ranges = [0.001, 0.004, 0.007, 0.01, 0.04, 0.07, 0.1, 0.4, 0.7, 1]
metadata_num = 6
# %% Motor-head superposition
# creates copies of DataFrames for list of DataFrames
df_copier = lambda df_list: [df.copy() for df in df_list]
# cluster delta copies
clusterdeltas = df_copier(compared_cluster_delta_dfs)
col_names = list(clusterdeltas[0].columns)
# renames columns
for i, m in enumerate(motor_list):
    clusterdeltas[i].columns = [col + f' {m} motors' for col in col_names]
clusterdeltas = pd.concat(clusterdeltas, axis=1)
# concat by heads
clusterdeltasheads = {h: clusterdeltas.filter(regex=f'Rod {h} heads') for h in heads_list}
clusterdeltasmotors = {m: clusterdeltas.filter(regex=f' {m} motors') for m in motor_list}
## plots
# Baseline motor count for comparison, must be from motor_list
baseline_motor = 1000
# motor multipler of interest
for motor in motor_list:
    motor_multiplier = motor
    # vs part of title, can set manually
    vs_title = f'{motor_multiplier}'
    dfs = [clusterdeltasmotors[baseline_motor], clusterdeltasmotors[motor_multiplier]]
    # Baseline motor counts are black, others are assorted colors
    styles = ['k' for _ in range(len(clusterdeltasmotors[baseline_motor].columns))] + colors[:len(clusterdeltasmotors[motor_multiplier].columns)]
    pd.concat(dfs, axis=1).plot(kind='line', figsize=(plot_length, plot_height), style=styles, title='Cluster size delta', logx=True).set(ylabel='Cluster size delta difference (um)')
    plt.savefig(cwd + f"\\cytosimplots\\motorheadsuperposition\\clustersizedeltasmotors{sim_time}sec{vs_title}.png")
    plt.close()
# compared heads
for head in heads_list:
    head_count = head
    # vs part of title, can set manually
    vs_title = f'{head_count}'
    dfs = [clusterdeltasmotors[baseline_motor], clusterdeltasheads[head_count].drop(f'Rod {head_count} heads {baseline_motor} motors', axis=1)]
    # Baseline motor counts are black, others are assorted colors
    styles = ['k' for _ in range(len(clusterdeltasmotors[baseline_motor].columns))] + colors[:len(clusterdeltasheads[head_count].columns)]
    pd.concat(dfs, axis=1).plot(kind='line', figsize=(plot_length, plot_height), style=styles, title='Cluster size delta', logx=True).set(ylabel='Cluster size delta difference (um)')
    plt.savefig(cwd + f"\\cytosimplots\\motorheadsuperposition\\clustersizedeltasheads{sim_time}sec{vs_title}.png")
    plt.close()
# %% Analyzing rod data with respect to motor count
# metadata
times, memory = metadata(info_num=metadata_num, show_plot=False)
# binding ranges of interest
for binding_range in binding_ranges:
    times_df = pd.DataFrame(times[binding_range], index=motor_list)
    memory_df = pd.DataFrame(memory[binding_range], index=motor_list)
    ## contraction delta per computational time vs motor (contraction time efficiency)
    deltas = [df.loc[binding_range] for df in df_copier(compared_cluster_delta_dfs)]
    # negative for contraction to be a positive value
    deltas_df = -pd.DataFrame(deltas, index=motor_list).rename_axis('Motor count')
    efficiency_df = deltas_df/times_df.values
    efficiency_df.plot(figsize=(plot_length, plot_height), logx=True, title=f'Contraction delta magnitude per computational time vs motor count over {sim_time} seconds (binding range = {binding_range} um)').set(ylabel='Contraction delta magnitude per computational time (um/s)')
    plt.grid(True, which='both')
    plt.savefig(cwd + f"\\cytosimplots\\efficiency\\contractiondelta\\contractiontimeefficiency{sim_time}sec{binding_range}bindingrange.png")
    ## contraction delta per memory usage vs motor (contraction memory efficiency)
    efficiency_df = deltas_df/memory_df.values
    efficiency_df.plot(figsize=(plot_length, plot_height), logx=True, title=f'Contraction delta magnitude per memory usage vs motor count over {sim_time} seconds (binding range = {binding_range} um)').set(ylabel='Contraction delta magnitude per memory usage (um/MB)')
    plt.grid(True, which='both')
    plt.savefig(cwd + f"\\cytosimplots\\efficiency\\contractiondelta\\contractionmemoryefficiency{sim_time}sec{binding_range}bindingrange.png")
    ## contraction delta magnitude vs motor (work)
    deltas_df.plot(figsize=(plot_length, plot_height), logx=True, title=f'Contraction delta magnitude vs motor count over {sim_time} seconds (binding range = {binding_range} um)').set(ylabel='Contraction delta magnitude (um)')
    plt.grid(True, which='both')
    plt.savefig(cwd + f"\\cytosimplots\\work\\work{sim_time}sec{binding_range}bindingrange.png")
    ## contraction delta rate per computational time vs motor (contraction rate time efficiency)
    contractions = [df.loc[binding_range] for df in df_copier(compared_max_contraction_dfs)]
    contractions_df = -pd.DataFrame(contractions, index=motor_list).rename_axis('Motor count')
    efficiency_df = contractions_df/times_df.values
    efficiency_df.plot(figsize=(plot_length, plot_height), logx=True, title=f'Max contraction rate magnitude per computational time vs motor count over {sim_time} seconds (binding range = {binding_range} um)').set(ylabel='Max contraction rate magnitude per computational time (um/s/S)')
    plt.grid(True, which='both')
    plt.savefig(cwd + f"\\cytosimplots\\efficiency\\contractionrate\\contractionratetimeefficiency{sim_time}sec{binding_range}bindingrange.png")
    ## contraction delta rate per memory usage vs motor (contraction rate memory efficiency)
    efficiency_df = contractions_df/memory_df.values
    efficiency_df.plot(figsize=(plot_length, plot_height), logx=True, title=f'Contraction delta rate magnitude per memory usage vs motor count over {sim_time} seconds (binding range = {binding_range} um)').set(ylabel='Contraction delta magnitude per memory usage (um/MB)')
    plt.grid(True, which='both')
    plt.savefig(cwd + f"\\cytosimplots\\efficiency\\contractionrate\\contractionratememoryefficiency{sim_time}sec{binding_range}bindingrange.png")
    ## max contraction rate vs motor (max power)
    contractions_df.plot(figsize=(plot_length, plot_height), logx=True, title=f'Max contraction rate magnitude vs motor count over {sim_time} seconds (binding range = {binding_range} um)').set(ylabel='Contraction rate magnitude (um/s)')
    plt.grid(True, which='both')
    plt.savefig(cwd + f"\\cytosimplots\\maxpower\\maxpower{sim_time}sec{binding_range}bindingrange.png")
    ## max contraction rate time vs motor (max power time)
    contraction_times = [df.loc[binding_range] for df in df_copier(compared_max_contraction_time_dfs)]
    contraction_times_df = pd.DataFrame(contraction_times, index=motor_list).rename_axis('Motor count')
    contraction_times_df.plot(figsize=(plot_length, plot_height), logx=True, title=f'Max contraction rate time vs motor count over {sim_time} seconds (binding range = {binding_range} um)').set(ylabel='Seconds (s)')
    plt.grid(True, which='both')
    plt.savefig(cwd + f"\\cytosimplots\\maxpowertime\\maxpowertime{sim_time}sec{binding_range}bindingrange.png")
# %% Tracking diffusion
# intializers
test_number = 578
_, times, *_, motor_type, _ = searchcytosiminfo(test_number, 'test')
sim_num = len(os.listdir(os.path.join(os.getcwd(), 'tests', f'test_{test_number}')))
coord_columns = ['cenX', 'cenY'] if motor_type == 'rod' else ['posX', 'posY']
actin_num = 1000
# store displacement magnitudes
displacements = []
for sim in range(sim_num): 
    filename = os.getcwd() + f'\\tests\\test_{test_number}\\{sim}\\reports\\run0001report.txt'
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
ax.set_title(f'Motor displacement over time (1000 motors) (Average over {sim_num} simulations)')
ax.set_xlabel('Seconds (s)')
ax.set_ylabel('Displacement Squared (um^2)')
ax.plot(times, displacements)
plt.savefig(os.getcwd() + f"\\cytosimplots\\{motor_type}diffusion.png")
# %% Compiler data
starting_job = 410
names_list = 3
test_range = 1
sim_time = 5
sim_num = 10
# %% Test-job matcher 
test = starting_job
for i, m in enumerate(motor_list):
    for j, h in enumerate(heads_list):
        for k in range(sim_num):
            print(f'{sim_time} seconds test_{test} job{sim_num*len(heads_list)*i + sim_num*j + k}: {m} motors, {h} heads')
        test += 1
# %% Tests in cytosiminformation.txt 
for t, tup in enumerate([(i, k) for i in motor_list for k in heads_list], starting_job):
    m, h = tup
    print(f"{t}: 'Rod {h} heads' ({names_list}, {test_range}, {sim_time}, 'rod') # {m} motors") if h == heads_list[0] else print(f"{t}: 'Rod {h} heads' (3, 1, {sim_time}, 'rod')")
# %% Groups in cytosiminformation.txt 
for i, m in enumerate(motor_list):
    heads_num = len(heads_list)
    print(f"{m} motors ({sim_time} sec): ({[starting_job + heads_num*i + j for j in range(heads_num)]}, True, '({m} motors)')")
# %% Metadata generator
info_name = 'Variable Name'
info = ['Binding Range', 'Binding Range', 'Binding Range', 'Binding Range', 'Binding Range', 'Binding Range']
for i, v in enumerate(info, 3):
    print(f'{info_name} {i}: {v}')
