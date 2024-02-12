import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import operator
import glob
import os
from scipy.ndimage import gaussian_filter1d
from numpy import diff

def Liplt_anode(file, time, cycles):
    files = glob.glob('*.csv')
    dfs = []
    for dataframe in files:
        df = pd.read_csv(dataframe, skiprows = 1, delimiter = '\t')
        dfs.append(df)
    
    cycles = [2, 3]
    labels = ['C10', '3C']
    colors = ['red', 'blue']
    fig, ax = plt.subplots(figsize = (6, 5))
    fig, ax1 = plt.subplots(1, 1, figsize = (6, 5))
    for i,cycle in enumerate(cycles):
        c=file
        end_step_r_NKSC = dfs[c].loc[(dfs[c]["Cycle P"] == cycle) & 
                                     (dfs[c]["Step Time (sec)"] == time) & (dfs[c]["ES"] == 1)]
        end_step_d_NKSC = dfs[c].loc[(dfs[c]["Cycle P"] == cycle) & (dfs[c]["ES"] == 129)]
        step_current = dfs[c].loc[(dfs[c]["Cycle P"] == cycle) & (dfs[c]["ES"] == 164)]
    
        current = np.array(step_current['Current (A)'].iloc[0])
        x1_n = np.array(end_step_r_NKSC['Voltage (V)'].iloc[0:])
        x2_n = np.array(end_step_d_NKSC['Voltage (V)'].iloc[0:])
        y_n = (x2_n - x1_n)/current
        x_n = np.linspace(1, len(x2_n), len(x2_n))
        y_smooth = gaussian_filter1d(y_n, sigma = 2)
        #ax.plot(x_g, y_g, color = colors[i], linestyle = 'solid', label = labels[i])
        ax.plot(x_n, y_n, color = colors[i], linestyle = 'solid', label = labels[i])
        ax.plot(x_n, y_smooth, color = colors[i], linestyle = 'solid', label = labels[i])
        ax.set_xlabel('SoC %')
        ax.set_ylabel("Resistance (ohms)")
        ax.set_xlim(0, 101)
        ax.legend()
        
        dydx = diff(y_smooth)/diff(x_n)
        ax1.plot(x_n[0:-1], dydx, color = colors[i], label = labels[i])
        ax1.legend()
    #plt.title('G49-39139')
    fig.tight_layout()