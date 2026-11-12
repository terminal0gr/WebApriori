import math

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams["font.family"] = "Times New Roman"

algoFamily = "Massive"
algos = ['Eclat Py Goethals', 'HTK-Miner Py Malliaridis', 'Eclat bitset Java SPMF', 'Prepost+ Java SPMF', 'Linear Table Java SPMF', 'dEclat C/C++ Borgelt', 'FP-Growth C/C++ Borgelt', 'HTK-Miner++ C++ Malliaridis']
colors = ['deepskyblue', 'steelblue', 'gray', 'darkgray', 'black', 'lightgreen', 'green', 'darkgreen'] 
 
markers = ['D', 'H', '*', '<', '>', 's', 'p', 'o']



dataset = "webdocs"
defaultFontSize = 18
#
# Common X-axis labels
x_labels = ["100 (0.327)", "1000 (0.216)", "10,000 (0.151)"]
#
runtime = {
    x_labels[0]: [261.11, 141.16, None, 41.69, 15.10,  29.10, 32.06, 31.64],
    x_labels[1]: [307.03, 150.53, None, 48.52, 15.37,  31.62, 33.94, 33.08],
    x_labels[2]: [645.30, 205.93, None, 61.24, 173.68, 43.24, 40.06, 44.58]
}
#
peakMemory = {
    x_labels[0]: [10.526, 1.484, 99.999, 7.266, 1.561, 1.691, 1.693, 5.992],
    x_labels[1]: [12.246, 1.768, 99.999, 7.572, 2.291, 1.692, 1.708, 5.996],
    x_labels[2]: [12.305, 4.854, 99.999, 7.996, 3.836, 1.692, 2.520, 7.264]
}
#
# --- 1. Setup the Shared Figure Canvas ---
# figsize=(16, 6) gives plenty of width for side-by-side plots while maintaining height
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.canvas.manager.set_window_title(algoFamily + '-' + dataset)
#
# ==========================================================
# LEFT PLOT (ax1): Execution Time (Line Chart)
# ==========================================================
ax1.set_xlabel("Top-$K$ (minSup)", fontsize=defaultFontSize)
ax1.set_ylim(0, 350)
ax1.set_xscale('log')
x_numeric = [100, 1000, 10000]
#
ax1.set_xticks(x_numeric)
ax1.set_xticklabels(x_labels, fontsize=defaultFontSize)
ax1.tick_params(axis='y', labelsize=defaultFontSize) 
ax1.set_ylabel("Time (sec)", fontsize=defaultFontSize)
#
ax1.plot(x_numeric, [runtime[key][0] for key in runtime], marker=markers[0], linestyle='-', label=algos[0], markersize=8, color=colors[0])
ax1.plot(8400, 340, marker="$645$", color=colors[0], markersize=16, zorder=5)
ax1.plot(10000, 340, marker=markers[0], markersize=8, color=colors[0], zorder=5)
#
ax1.plot(x_numeric, [runtime[key][1] for key in runtime], marker=markers[1], linestyle='-', label=algos[1], markersize=10, color=colors[1])
#
ax1.plot(100, 340, marker=markers[2], label=algos[2], markersize=11, color=colors[2], zorder=5)
ax1.plot(100, 340, marker='x', color='red', markersize=6, zorder=6)
#
ax1.plot(x_numeric, [runtime[key][3] for key in runtime], marker=markers[3], linestyle='-', label=algos[3], markersize=8, color=colors[3])
ax1.plot(x_numeric, [runtime[key][4] for key in runtime], marker=markers[4], linestyle='-', label=algos[4], markersize=8, color=colors[4])
ax1.plot(x_numeric, [runtime[key][5] for key in runtime], marker=markers[5], linestyle='-', label=algos[5], markersize=8, color=colors[5])
ax1.plot(x_numeric, [runtime[key][6] for key in runtime], marker=markers[6], linestyle='-', label=algos[6], markersize=10, color=colors[6])
ax1.plot(x_numeric, [runtime[key][7] for key in runtime], marker=markers[7], linestyle='-', label=algos[7], markersize=8, color=colors[7])
#
ax1.grid(True)
#
# ==========================================================
# RIGHT PLOT (ax2): Peak Memory (Grouped Bar Chart)
# ==========================================================
#
bar_width = 0.09
gap = 0.02  
indices = np.arange(len(x_labels))
#
for i, k in enumerate(x_labels):
    for j, algo in enumerate(algos):
        x_pos = indices[i] + (j - 2.5) * (bar_width + gap)
        m = peakMemory[k][j]
        
        if m is None: # Timeout (>1,000 s)
            ax2.text(x_pos, 0, 'Timeout (>1,000 s)', ha='center', va='bottom', color=colors[j], 
                    fontsize=defaultFontSize-1, fontweight='normal', rotation=90, zorder=4)
            ax2.bar(x_pos, 0, bar_width, color=colors[j])
        elif m == 99.999: # Special marker for the 12 GB cap (indicating Out of Memory)    
            ax2.text(x_pos, 0, 'Out of Memory (>12 GB)', ha='center', va='bottom', color=colors[j], 
                    fontsize=defaultFontSize-1, fontweight='normal', rotation=90, zorder=4)
            ax2.bar(x_pos, 0, bar_width, color=colors[j])
        elif m == -1: # Special marker for Not FIMI. Format not supported
            ax2.text(x_pos, 0, 'Format not supported', ha='center', va='bottom', color=colors[j], 
                    fontsize=defaultFontSize-1, fontweight='normal', rotation=90, zorder=4)
            ax2.bar(x_pos, 0, bar_width, color=colors[j])
        else:
            ax2.bar(x_pos, m, bar_width, color=colors[j], edgecolor='black', linewidth=0.7, zorder=3)

ax2.set_yscale('linear')
ax2.set_ylabel('Peak Memory (GB)', fontsize=defaultFontSize)
ax2.tick_params(axis='y', labelsize=defaultFontSize)
ax2.set_xticks(indices)
ax2.set_xticklabels(x_labels, fontsize=defaultFontSize)
ax2.set_xlabel('Top-$K$ (minSup)', fontsize=defaultFontSize)
ax2.grid(axis='y', which='both', linestyle='--', alpha=0.4, zorder=1)
#
# ==========================================================
# UNIFIED LEGEND & LAYOUT RENDERING
# ==========================================================
# Extract the handles and labels from the left plot (ax1)
handles, labels = ax1.get_legend_handles_labels()
#
# Create a single, overarching legend attached to the Figure (not an individual axis)
# ncol=3 spreads the 6 algorithms into 2 clean rows across the wide top span
fig.legend(handles, labels, fontsize=defaultFontSize-2, loc='upper center', bbox_to_anchor=(0.5, 1), 
           ncol=4, fancybox=False, shadow=False, frameon=False)
#
# Apply tight layout FIRST to calculate boundaries
plt.tight_layout()
#
# Adjust the top margin to create space for the shared legend
# wspace creates a slight gap between the two side-by-side charts
fig.subplots_adjust(top=0.83, wspace=0.15)
#
# Save and Show
plt.savefig('fig_' + algoFamily + '_' + dataset + '.pdf', format='pdf', bbox_inches='tight')




dataset = "TH2FIM"
defaultFontSize = 18
#
# Common X-axis labels
x_labels = ["100 (0.041)", "1000 (0.014)", "10,000 (0.005)"]
#
runtime = {
    x_labels[0]: [240.08, 96.19,  None, 73.70,  91.15,  35.22,  30.94,  6.42],
    x_labels[1]: [None,   293.18, None, 145.21, 909.78, 157.87, 71.63,  68.39],
    x_labels[2]: [None,   None,   None, None,   None,   464.43, 128.04, 911.50],
}
#
peakMemory = {
    x_labels[0]: [10.802, 0.372,  99.999, 7.220,  4.496,  2.391, 2.978,  2.727],
    x_labels[1]: [None,   3.857,  99.999, 7.244,  10.766, 3.055, 6.501,  6.231],
    x_labels[2]: [None,   99.999, 99.999, 99.999, 99.999, 3.318, 10.852, 11.567],
}
#
# --- 1. Setup the Shared Figure Canvas ---
# figsize=(16, 6) gives plenty of width for side-by-side plots while maintaining height
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.canvas.manager.set_window_title(algoFamily + '-' + dataset)
#
# ==========================================================
# LEFT PLOT (ax1): Execution Time (Line Chart)
# ==========================================================
ax1.set_xlabel("Top-$K$ (minSup)", fontsize=defaultFontSize)
ax1.set_ylim(0, 1000)
ax1.set_xscale('log')
x_numeric = [100, 1000, 10000]
#
ax1.set_xticks(x_numeric)
ax1.set_xticklabels(x_labels, fontsize=defaultFontSize)
ax1.tick_params(axis='y', labelsize=defaultFontSize) 
ax1.set_ylabel("Time (sec)", fontsize=defaultFontSize)
#
ax1.plot(1000, 970, marker=markers[0], markersize=8, color=colors[0], zorder=5)
ax1.plot(1000, 970, marker='x', color='red', markersize=6, zorder=6)
ax1.plot(x_numeric, [runtime[key][0] for key in runtime], marker=markers[0], linestyle='-', label=algos[0], markersize=8, color=colors[0])
#
ax1.plot(8000, 970, marker=markers[1], markersize=10, color=colors[1], zorder=5)
ax1.plot(8000, 970, marker='x', color='red', markersize=6, zorder=6)
ax1.plot(x_numeric, [runtime[key][1] for key in runtime], marker=markers[1], linestyle='-', label=algos[1], markersize=10, color=colors[1])
#
ax1.plot(100, 970, marker=markers[2], label=algos[2], markersize=11, color=colors[2], zorder=5)
ax1.plot(100, 970, marker='x', color='red', markersize=6, zorder=6)
#
ax1.plot(x_numeric, [runtime[key][3] for key in runtime], marker=markers[3], linestyle='-', label=algos[3], markersize=8, color=colors[3])
ax1.plot(9000, 970, marker=markers[3], markersize=8, color=colors[3], zorder=5)
ax1.plot(9000, 970, marker='x', color='red', markersize=6, zorder=6)
#
ax1.plot(x_numeric, [runtime[key][4] for key in runtime], marker=markers[4], linestyle='-', label=algos[4], markersize=8, color=colors[4])
ax1.plot(10000, 970, marker=markers[4], markersize=8, color=colors[4], zorder=5)
ax1.plot(10000, 970, marker='x', color='red', markersize=6, zorder=6)
#
ax1.plot(x_numeric, [runtime[key][5] for key in runtime], marker=markers[5], linestyle='-', label=algos[5], markersize=8, color=colors[5])
ax1.plot(x_numeric, [runtime[key][6] for key in runtime], marker=markers[6], linestyle='-', label=algos[6], markersize=10, color=colors[6])
ax1.plot(x_numeric, [runtime[key][7] for key in runtime], marker=markers[7], linestyle='-', label=algos[7], markersize=8, color=colors[7])
#
ax1.grid(True)
#
# ==========================================================
# RIGHT PLOT (ax2): Peak Memory (Grouped Bar Chart)
# ==========================================================
#
bar_width = 0.09
gap = 0.02  
indices = np.arange(len(x_labels))
#
for i, k in enumerate(x_labels):
    for j, algo in enumerate(algos):
        x_pos = indices[i] + (j - 2.5) * (bar_width + gap)
        m = peakMemory[k][j]
        
        if m is None: # Timeout (>1,000 s)
            ax2.text(x_pos, 0, 'Timeout (>1,000 s)', ha='center', va='bottom', color=colors[j], 
                    fontsize=defaultFontSize-1, fontweight='normal', rotation=90, zorder=4)
            ax2.bar(x_pos, 0, bar_width, color=colors[j])
        elif m == 99.999: # Special marker for the 12 GB cap (indicating Out of Memory)    
            ax2.text(x_pos, 0, 'Out of Memory (>12 GB)', ha='center', va='bottom', color=colors[j], 
                    fontsize=defaultFontSize-1, fontweight='normal', rotation=90, zorder=4)
            ax2.bar(x_pos, 0, bar_width, color=colors[j])
        elif m == -1: # Special marker for Not FIMI. Format not supported
            ax2.text(x_pos, 0, 'Format not supported', ha='center', va='bottom', color=colors[j], 
                    fontsize=defaultFontSize-1, fontweight='normal', rotation=90, zorder=4)
            ax2.bar(x_pos, 0, bar_width, color=colors[j])
        else:
            ax2.bar(x_pos, m, bar_width, color=colors[j], edgecolor='black', linewidth=0.7, zorder=3)

ax2.set_yscale('linear')
ax2.set_ylabel('Peak Memory (GB)', fontsize=defaultFontSize)
ax2.tick_params(axis='y', labelsize=defaultFontSize)
ax2.set_xticks(indices)
ax2.set_xticklabels(x_labels, fontsize=defaultFontSize)
ax2.set_xlabel('Top-$K$ (minSup)', fontsize=defaultFontSize)
ax2.grid(axis='y', which='both', linestyle='--', alpha=0.4, zorder=1)
#
# ==========================================================
# UNIFIED LEGEND & LAYOUT RENDERING
# ==========================================================
# Extract the handles and labels from the left plot (ax1)
handles, labels = ax1.get_legend_handles_labels()
#
# Create a single, overarching legend attached to the Figure (not an individual axis)
# ncol=3 spreads the 6 algorithms into 2 clean rows across the wide top span
fig.legend(handles, labels, fontsize=defaultFontSize-2, loc='upper center', bbox_to_anchor=(0.5, 1), 
           ncol=4, fancybox=False, shadow=False, frameon=False)
#
# Apply tight layout FIRST to calculate boundaries
plt.tight_layout()
#
# Adjust the top margin to create space for the shared legend
# wspace creates a slight gap between the two side-by-side charts
fig.subplots_adjust(top=0.83, wspace=0.15)
#
# Save and Show
plt.savefig('fig_' + algoFamily + '_' + dataset + '.pdf', format='pdf', bbox_inches='tight')





dataset = "T80I100D1M"
defaultFontSize = 18
#
# Common X-axis labels
x_labels = ["100 (0.798)", "1000 (0.643)", "10,000 (0.519)"]
#
runtime = {
    x_labels[0]: [205.78, 18.47, 1.03, 28.69, 100.07, 18.44, 29.05,  1.17],
    x_labels[1]: [419.14, 19.19, 1.20, 33.63, 859.41, 25.01, 48.79,  2.20],
    x_labels[2]: [None,   32.23, 6.24, 735.60, None,  188.52, None,  18.62],
}
#
peakMemory = {
    x_labels[0]: [3.241,  0.032, 1.526, 7.141, 4.758, 0.641, 2.468,  0.722],
    x_labels[1]: [4.015,  0.188, 1.600, 7.181, 4.758, 0.657, 2.635,  0.724],
    x_labels[2]: [None,   0.989, 7.645, 7.189, None,  0.702, 99.999, 1.506],
}
#
# --- 1. Setup the Shared Figure Canvas ---
# figsize=(16, 6) gives plenty of width for side-by-side plots while maintaining height
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.canvas.manager.set_window_title(algoFamily + '-' + dataset)
#
# ==========================================================
# LEFT PLOT (ax1): Execution Time (Line Chart)
# ==========================================================
ax1.set_xlabel("Top-$K$ (minSup)", fontsize=defaultFontSize)
ax1.set_ylim(0, 250)
ax1.set_xscale('log')
x_numeric = [100, 1000, 10000]
#
ax1.set_xticks(x_numeric)
ax1.set_xticklabels(x_labels, fontsize=defaultFontSize)
ax1.tick_params(axis='y', labelsize=defaultFontSize) 
ax1.set_ylabel("Time (sec)", fontsize=defaultFontSize)
#
ax1.plot(x_numeric, [runtime[key][0] for key in runtime], marker=markers[0], linestyle='-', label=algos[0], markersize=8, color=colors[0])
ax1.plot(1000, 243, marker=markers[0], markersize=8, color=colors[0], zorder=5)
ax1.plot(840, 243, marker="$419$", color=colors[0], markersize=16, zorder=5)
ax1.plot(8000, 243, marker=markers[0], markersize=8, color=colors[0], zorder=5)
ax1.plot(8000, 243, marker='x', color='red', markersize=6, zorder=6)

#
ax1.plot(x_numeric, [runtime[key][1] for key in runtime], marker=markers[1], linestyle='-', label=algos[1], markersize=10, color=colors[1])
ax1.plot(x_numeric, [runtime[key][2] for key in runtime], marker=markers[2], linestyle='-', label=algos[2], markersize=11, color=colors[2])
#
ax1.plot(x_numeric, [runtime[key][3] for key in runtime], marker=markers[3], linestyle='-', label=algos[3], markersize=8, color=colors[3])
ax1.plot(8400, 230, marker="$735$", color=colors[3], markersize=16, zorder=5)
ax1.plot(10000, 230, marker=markers[3], markersize=8, color=colors[3], zorder=5)

#
ax1.plot(x_numeric, [runtime[key][4] for key in runtime], marker=markers[4], linestyle='-', label=algos[4], markersize=8, color=colors[4])
ax1.plot(1000, 230, marker=markers[4], markersize=8, color=colors[4], zorder=5)
ax1.plot(840, 230, marker="$859$", color=colors[4], markersize=16, zorder=5)
ax1.plot(9000, 243, marker=markers[4], markersize=8, color=colors[4], zorder=5)
ax1.plot(9000, 243, marker='x', color='red', markersize=6, zorder=6)
#
ax1.plot(x_numeric, [runtime[key][5] for key in runtime], marker=markers[5], linestyle='-', label=algos[5], markersize=8, color=colors[5])
# 
ax1.plot(x_numeric, [runtime[key][6] for key in runtime], marker=markers[6], linestyle='-', label=algos[6], markersize=10, color=colors[6])
ax1.plot(10000, 243, marker=markers[6], markersize=10, color=colors[6], zorder=5)
ax1.plot(10000, 243, marker='x', color='red', markersize=6, zorder=6)
#
ax1.plot(x_numeric, [runtime[key][7] for key in runtime], marker=markers[7], linestyle='-', label=algos[7], markersize=8, color=colors[7])
#
ax1.grid(True)
#
# ==========================================================
# RIGHT PLOT (ax2): Peak Memory (Grouped Bar Chart)
# ==========================================================
#
bar_width = 0.09
gap = 0.02  
indices = np.arange(len(x_labels))
#
for i, k in enumerate(x_labels):
    for j, algo in enumerate(algos):
        x_pos = indices[i] + (j - 2.5) * (bar_width + gap)
        m = peakMemory[k][j]
        
        if m is None: # Timeout (>1,000 s)
            ax2.text(x_pos, 0, 'Timeout (>1,000 s)', ha='center', va='bottom', color=colors[j], 
                    fontsize=defaultFontSize-1, fontweight='normal', rotation=90, zorder=4)
            ax2.bar(x_pos, 0, bar_width, color=colors[j])
        elif m == 99.999: # Special marker for the 12 GB cap (indicating Out of Memory)    
            ax2.text(x_pos, 0, 'Out of Memory (>12 GB)', ha='center', va='bottom', color=colors[j], 
                    fontsize=defaultFontSize-1, fontweight='normal', rotation=90, zorder=4)
            ax2.bar(x_pos, 0, bar_width, color=colors[j])
        elif m == -1: # Special marker for Not FIMI. Format not supported
            ax2.text(x_pos, 0, 'Format not supported', ha='center', va='bottom', color=colors[j], 
                    fontsize=defaultFontSize-1, fontweight='normal', rotation=90, zorder=4)
            ax2.bar(x_pos, 0, bar_width, color=colors[j])
        else:
            ax2.bar(x_pos, m, bar_width, color=colors[j], edgecolor='black', linewidth=0.7, zorder=3)

ax2.set_yscale('linear')
ax2.set_ylabel('Peak Memory (GB)', fontsize=defaultFontSize)
ax2.tick_params(axis='y', labelsize=defaultFontSize)
ax2.set_xticks(indices)
ax2.set_xticklabels(x_labels, fontsize=defaultFontSize)
ax2.set_xlabel('Top-$K$ (minSup)', fontsize=defaultFontSize)
ax2.grid(axis='y', which='both', linestyle='--', alpha=0.4, zorder=1)
#
# ==========================================================
# UNIFIED LEGEND & LAYOUT RENDERING
# ==========================================================
# Extract the handles and labels from the left plot (ax1)
handles, labels = ax1.get_legend_handles_labels()
#
# Create a single, overarching legend attached to the Figure (not an individual axis)
# ncol=3 spreads the 6 algorithms into 2 clean rows across the wide top span
fig.legend(handles, labels, fontsize=defaultFontSize-2, loc='upper center', bbox_to_anchor=(0.5, 1), 
           ncol=4, fancybox=False, shadow=False, frameon=False)
#
# Apply tight layout FIRST to calculate boundaries
plt.tight_layout()
#
# Adjust the top margin to create space for the shared legend
# wspace creates a slight gap between the two side-by-side charts
fig.subplots_adjust(top=0.83, wspace=0.15)
#
# Save and Show
plt.savefig('fig_' + algoFamily + '_' + dataset + '.pdf', format='pdf', bbox_inches='tight')


plt.show()