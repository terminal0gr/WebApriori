import math

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams["font.family"] = "Times New Roman"

algoFamily = "Eclat"
algos = ['Eclat Py Borgelt', 'Eclat Py Goethals', 'Eclat Py Pami', 'Eclat bitset Py Pami', 'Eclat Java SPMF', 'Eclat bitset Java SPMF', 'Eclat C++ Borgelt']
colors = ['deepskyblue', 'steelblue', 'blue', 'navy', 'gray', 'black', 'red'] 
markers = ['D', 'H', '*', '+', '>', 's', 'p']



dataset = "kosarak"
defaultFontSize = 18
#
# Common X-axis labels
x_labels = ["100 (0.023)", "1000 (0.006)", "10,000 (0.002)"]
#
runtime = {
    x_labels[0]: [10.40, 3.71, 4.24, 35.12, 2.57, 3.02, 1.01],
    x_labels[1]: [13.92, 5.87, 7.20, 46.75, 5.08, 3.30, 1.12],
    x_labels[2]: [30.58, 17.87, 20.66, 94.56, 17.79, 6.52, 1.43],
}
#
peakMemory = {
    x_labels[0]: [1.070, 0.522, 0.810, 0.592, 0.881, 8.669, 0.081],
    x_labels[1]: [1.126, 0.532, 1.283, 0.697, 1.180, 9.240, 0.108],
    x_labels[2]: [1.200, 0.534, 2.621, 1.805, 1.273, 10.804, 0.128],
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
ax1.set_xlabel("Top-k (minSup)", fontsize=defaultFontSize)
ax1.set_ylim(0, 100)
ax1.set_xscale('log')
x_numeric = [100, 1000, 10000]
#
ax1.set_xticks(x_numeric)
ax1.set_xticklabels(x_labels, fontsize=defaultFontSize)
ax1.tick_params(axis='y', labelsize=defaultFontSize) 
ax1.set_ylabel("Time (sec)", fontsize=defaultFontSize)
#
ax1.plot(x_numeric, [runtime[key][0] for key in runtime], marker=markers[0], linestyle='-', label=algos[0], markersize=8, color=colors[0])
ax1.plot(x_numeric, [runtime[key][1] for key in runtime], marker=markers[1], linestyle='-', label=algos[1], markersize=8, color=colors[1])
ax1.plot(x_numeric, [runtime[key][2] for key in runtime], marker=markers[2], linestyle='-', label=algos[2], markersize=8, color=colors[2])
ax1.plot(x_numeric, [runtime[key][3] for key in runtime], marker=markers[3], linestyle='-', label=algos[3], markersize=8, color=colors[3])
ax1.plot(x_numeric, [runtime[key][4] for key in runtime], marker=markers[4], linestyle='-', label=algos[4], markersize=8, color=colors[4])
ax1.plot(x_numeric, [runtime[key][5] for key in runtime], marker=markers[5], linestyle='-', label=algos[5], markersize=8, color=colors[5])
ax1.plot(x_numeric, [runtime[key][6] for key in runtime], marker=markers[6], linestyle='-', label=algos[6], markersize=8, color=colors[6])
#
ax1.grid(True)
#
# ==========================================================
# RIGHT PLOT (ax2): Peak Memory (Grouped Bar Chart)
# ==========================================================
#
bar_width = 0.10
gap = 0.03  
indices = np.arange(len(x_labels))
#
for i, k in enumerate(x_labels):
    for j, algo in enumerate(algos):
        x_pos = indices[i] + (j - 2.5) * (bar_width + gap)
        m = peakMemory[k][j]
        
        if m is None: # Timeout (>1,000 s)
            ax2.text(x_pos, 0.1, 'Timeout (>1,000 s)', ha='center', va='bottom', color='red', 
                    fontsize=defaultFontSize, fontweight='normal', rotation=90, zorder=4)
            ax2.bar(x_pos, 0, bar_width, color=colors[j])
        elif m == 99.999: # Special marker for the 12 GB cap (indicating Out of Memory)    
            ax2.text(x_pos, 0.1, 'Out of Memory (>12 GB)', ha='center', va='bottom', color='red', 
                    fontsize=defaultFontSize, fontweight='normal', rotation=90, zorder=4)
            ax2.bar(x_pos, 0, bar_width, color=colors[j])
        else:
            ax2.bar(x_pos, m, bar_width, color=colors[j], edgecolor='black', linewidth=0.7, zorder=3)

ax2.set_yscale('linear')
ax2.set_ylabel('Peak Memory (GB)', fontsize=defaultFontSize)
ax2.tick_params(axis='y', labelsize=defaultFontSize)
ax2.set_xticks(indices)
ax2.set_xticklabels(x_labels, fontsize=defaultFontSize)
ax2.set_xlabel('Top-K (minSup)', fontsize=defaultFontSize)
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
fig.legend(handles, labels, fontsize=defaultFontSize, loc='upper center', bbox_to_anchor=(0.5, 1), 
           ncol=math.ceil(len(algos)/2), fancybox=False, shadow=False, frameon=False)
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






dataset = "L-0023"
defaultFontSize = 18
#
# Common X-axis labels
x_labels = ["100 (0.033)", "1000 (0.012)", "10,000 (0.005)"]
#
runtime = {
    x_labels[0]: [None, 0.08, 0.11, 0.05, None, None, 0.24],
    x_labels[1]: [None, 0.24, 0.24, 0.11, None, None, 0.24],
    x_labels[2]: [None, 0.51, 0.63, 0.36, None, None, 0.24],
}
#
peakMemory = {
    x_labels[0]: [-1, 0.050, 0.057, 0.056, -1, -1, 0.004],
    x_labels[1]: [-1, 0.051, 0.060, 0.057, -1, -1, 0.004],
    x_labels[2]: [-1, 0.051, 0.083, 0.062, -1, -1, 0.004],
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
ax1.set_xlabel("Top-K (minSup)", fontsize=defaultFontSize)
ax1.set_ylim(0, 1)
ax1.set_xscale('log')
x_numeric = [100, 1000, 10000]
#
ax1.set_xticks(x_numeric)
ax1.set_xticklabels(x_labels, fontsize=defaultFontSize)
ax1.tick_params(axis='y', labelsize=defaultFontSize) 
ax1.set_ylabel("Time (sec)", fontsize=defaultFontSize)
#
ax1.plot(100, 0.97, marker=markers[0], label=algos[0], markersize=8, color=colors[0], zorder=5)
ax1.plot(100, 0.97, marker='x', color='red', markersize=6, zorder=6)
ax1.plot(x_numeric, [runtime[key][1] for key in runtime], marker=markers[1], linestyle='-', label=algos[1], markersize=8, color=colors[1])
ax1.plot(x_numeric, [runtime[key][2] for key in runtime], marker=markers[2], linestyle='-', label=algos[2], markersize=8, color=colors[2])
ax1.plot(x_numeric, [runtime[key][3] for key in runtime], marker=markers[3], linestyle='-', label=algos[3], markersize=8, color=colors[3])
ax1.plot(120, 0.97, marker=markers[4], label=algos[4], markersize=8, color=colors[4], zorder=5)
ax1.plot(120, 0.97, marker='x', color='red', markersize=6, zorder=6)
ax1.plot(140, 0.97, marker=markers[5], label=algos[5], markersize=8, color=colors[5], zorder=5)
ax1.plot(140, 0.97, marker='x', color='red', markersize=6, zorder=6)
ax1.plot(x_numeric, [runtime[key][6] for key in runtime], marker=markers[6], linestyle='-', label=algos[6], markersize=8, color=colors[6])
#
ax1.grid(True)
#
# ==========================================================
# RIGHT PLOT (ax2): Peak Memory (Grouped Bar Chart)
# ==========================================================
#
bar_width = 0.10
gap = 0.03  
indices = np.arange(len(x_labels))
#
for i, k in enumerate(x_labels):
    for j, algo in enumerate(algos):
        x_pos = indices[i] + (j - 2.5) * (bar_width + gap)
        m = peakMemory[k][j]
        
        if m is None: # Timeout (>1,000 s)
            ax2.text(x_pos, 0, 'Timeout (>1,000 s)', ha='center', va='bottom', color='red', 
                    fontsize=defaultFontSize, fontweight='normal', rotation=90, zorder=4)
            ax2.bar(x_pos, 0, bar_width, color=colors[j])
        elif m == 99.999: # Special marker for the 12 GB cap (indicating Out of Memory)    
            ax2.text(x_pos, 0, 'Out of Memory (>12 GB)', ha='center', va='bottom', color='red', 
                    fontsize=defaultFontSize, fontweight='normal', rotation=90, zorder=4)
            ax2.bar(x_pos, 0, bar_width, color=colors[j])
        elif m == -1: # Special marker for Not FIMI. Format not supported
            ax2.text(x_pos, 0, 'Format not supported', ha='center', va='bottom', color='red', 
                    fontsize=defaultFontSize, fontweight='normal', rotation=90, zorder=4)
            ax2.bar(x_pos, 0, bar_width, color=colors[j])
        else:
            ax2.bar(x_pos, m, bar_width, color=colors[j], edgecolor='black', linewidth=0.7, zorder=3)

ax2.set_yscale('linear')
ax2.set_ylabel('Peak Memory (GB)', fontsize=defaultFontSize)
ax2.tick_params(axis='y', labelsize=defaultFontSize)
ax2.set_xticks(indices)
ax2.set_xticklabels(x_labels, fontsize=defaultFontSize)
ax2.set_xlabel('Top-K (minSup)', fontsize=defaultFontSize)
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
fig.legend(handles, labels, fontsize=defaultFontSize, loc='upper center', bbox_to_anchor=(0.5, 1), 
           ncol=math.ceil(len(algos)/2), fancybox=False, shadow=False, frameon=False)
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





dataset = "accidents"
defaultFontSize = 18
#
# Common X-axis labels
x_labels = ["100 (0.820)", "1000 (0.656)", "10,000 (0.482)"]
#
runtime = {
    x_labels[0]: [17.33, 3.87,  4.24,  17.12, 2.60,  0.19, 0.68],
    x_labels[1]: [88.65, 13.85, 16.10, 27.55, 11.43, 0.22, 0.89],
    x_labels[2]: [615.81, 112.25, None, 35.23, 76.28, 0.32, 1.10],
}
#
peakMemory = {
    x_labels[0]: [1.388, 0.621, 1.624, 0.733, 1.309, 0.512, 0.062],
    x_labels[1]: [1.458, 0.723, 8.686, 0.754, 8.064, 0.555, 0.062],
    x_labels[2]: [1.520, 0.879, 99.999, 1.127, 8.438, 0.591, 0.081],
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
ax1.set_xlabel("Top-K (minSup)", fontsize=defaultFontSize)
ax1.set_ylim(0, 130)
ax1.set_xscale('log')
x_numeric = [100, 1000, 10000]
#
ax1.set_xticks(x_numeric)
ax1.set_xticklabels(x_labels, fontsize=defaultFontSize)
ax1.tick_params(axis='y', labelsize=defaultFontSize) 
ax1.set_ylabel("Time (sec)", fontsize=defaultFontSize)
#
ax1.plot(x_numeric, [runtime[key][0] for key in runtime], marker=markers[0], linestyle='-', label=algos[0], markersize=8, color=colors[0])
ax1.plot(8400, 127, marker="$615$", color=colors[0], markersize=16, zorder=5)
ax1.plot(x_numeric, [runtime[key][1] for key in runtime], marker=markers[1], linestyle='-', label=algos[1], markersize=8, color=colors[1])
ax1.plot(x_numeric, [runtime[key][2] for key in runtime], marker=markers[2], linestyle='-', label=algos[2], markersize=8, color=colors[2])
ax1.plot(10000, 127, marker=markers[2], color=colors[2], markersize=8, zorder=5)
ax1.plot(10000, 127, marker='x', color='red', markersize=6, zorder=6)
ax1.plot(x_numeric, [runtime[key][3] for key in runtime], marker=markers[3], linestyle='-', label=algos[3], markersize=8, color=colors[3])
ax1.plot(x_numeric, [runtime[key][4] for key in runtime], marker=markers[4], linestyle='-', label=algos[4], markersize=8, color=colors[4])
ax1.plot(x_numeric, [runtime[key][5] for key in runtime], marker=markers[5], linestyle='-', label=algos[5], markersize=8, color=colors[5])
ax1.plot(x_numeric, [runtime[key][6] for key in runtime], marker=markers[6], linestyle='-', label=algos[6], markersize=8, color=colors[6])
#
ax1.grid(True)
#
# ==========================================================
# RIGHT PLOT (ax2): Peak Memory (Grouped Bar Chart)
# ==========================================================
#
bar_width = 0.10
gap = 0.03  
indices = np.arange(len(x_labels))
#
for i, k in enumerate(x_labels):
    for j, algo in enumerate(algos):
        x_pos = indices[i] + (j - 2.5) * (bar_width + gap)
        m = peakMemory[k][j]
        
        if m is None: # Timeout (>1,000 s)
            ax2.text(x_pos, 0, 'Timeout (>1,000 s)', ha='center', va='bottom', color='red', 
                    fontsize=defaultFontSize, fontweight='normal', rotation=90, zorder=4)
            ax2.bar(x_pos, 0, bar_width, color=colors[j])
        elif m == 99.999: # Special marker for the 12 GB cap (indicating Out of Memory)    
            ax2.text(x_pos, 0, 'Out of Memory (>12 GB)', ha='center', va='bottom', color='red', 
                    fontsize=defaultFontSize, fontweight='normal', rotation=90, zorder=4)
            ax2.bar(x_pos, 0, bar_width, color=colors[j])
        elif m == -1: # Special marker for Not FIMI. Format not supported
            ax2.text(x_pos, 0, 'Format not supported', ha='center', va='bottom', color='red', 
                    fontsize=defaultFontSize, fontweight='normal', rotation=90, zorder=4)
            ax2.bar(x_pos, 0, bar_width, color=colors[j])
        else:
            ax2.bar(x_pos, m, bar_width, color=colors[j], edgecolor='black', linewidth=0.7, zorder=3)

ax2.set_yscale('linear')
ax2.set_ylabel('Peak Memory (GB)', fontsize=defaultFontSize)
ax2.tick_params(axis='y', labelsize=defaultFontSize)
ax2.set_xticks(indices)
ax2.set_xticklabels(x_labels, fontsize=defaultFontSize)
ax2.set_xlabel('Top-K (minSup)', fontsize=defaultFontSize)
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
fig.legend(handles, labels, fontsize=defaultFontSize, loc='upper center', bbox_to_anchor=(0.5, 1), 
           ncol=math.ceil(len(algos)/2), fancybox=False, shadow=False, frameon=False)
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




dataset = "T16I20D100K"
defaultFontSize = 18
#
# Common X-axis labels
x_labels = ["100 (0.799)", "1000 (0.643)", "10,000 (0.518)"]
#
runtime = {
    x_labels[0]: [1.66, 1.24, 1.39, 3.02, 1.69, 0.05, 0.35],
    x_labels[1]: [5.94, 7.71, 8.41, 3.03, 8.29, 0.06, 0.45],
    x_labels[2]: [24.05, 48.49, 72.14, 3.33, 40.84, 0.13, 0.67],
}
#
peakMemory = {
    x_labels[0]: [0.188, 0.147, 0.346, 0.109, 0.585, 0.152, 0.020],
    x_labels[1]: [0.188, 0.192, 2.121, 0.122, 1.201, 0.188, 0.021],
    x_labels[2]: [0.188, 0.238, 10.912, 0.241, 7.447, 0.418, 0.023],
}
#
# --- 1. Setup the Shared Figure Canvas ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.canvas.manager.set_window_title(algoFamily + '-' + dataset)
#
# ==========================================================
# LEFT PLOT (ax1): Execution Time (Line Chart)
# ==========================================================
ax1.set_xlabel("Top-K (minSup)", fontsize=defaultFontSize)
ax1.set_ylim(0, 80)
ax1.set_xscale('log')
x_numeric = [100, 1000, 10000]
#
ax1.set_xticks(x_numeric)
ax1.set_xticklabels(x_labels, fontsize=defaultFontSize)
ax1.tick_params(axis='y', labelsize=defaultFontSize) 
ax1.set_ylabel("Time (sec)", fontsize=defaultFontSize)
#
ax1.plot(x_numeric, [runtime[key][0] for key in runtime], marker=markers[0], linestyle='-', label=algos[0], markersize=8, color=colors[0])
ax1.plot(x_numeric, [runtime[key][1] for key in runtime], marker=markers[1], linestyle='-', label=algos[1], markersize=8, color=colors[1])
ax1.plot(x_numeric, [runtime[key][2] for key in runtime], marker=markers[2], linestyle='-', label=algos[2], markersize=8, color=colors[2])
ax1.plot(x_numeric, [runtime[key][3] for key in runtime], marker=markers[3], linestyle='-', label=algos[3], markersize=8, color=colors[3])
ax1.plot(x_numeric, [runtime[key][4] for key in runtime], marker=markers[4], linestyle='-', label=algos[4], markersize=8, color=colors[4])
ax1.plot(x_numeric, [runtime[key][5] for key in runtime], marker=markers[5], linestyle='-', label=algos[5], markersize=8, color=colors[5])
ax1.plot(x_numeric, [runtime[key][6] for key in runtime], marker=markers[6], linestyle='-', label=algos[6], markersize=8, color=colors[6])
#
ax1.grid(True)
#
# ==========================================================
# RIGHT PLOT (ax2): Peak Memory (Grouped Bar Chart)
# ==========================================================
#
bar_width = 0.10
gap = 0.03  
indices = np.arange(len(x_labels))
#
for i, k in enumerate(x_labels):
    for j, algo in enumerate(algos):
        x_pos = indices[i] + (j - 2.5) * (bar_width + gap)
        m = peakMemory[k][j]
        
        if m is None: # Timeout (>1,000 s)
            ax2.text(x_pos, 0, 'Timeout (>1,000 s)', ha='center', va='bottom', color='red', 
                    fontsize=defaultFontSize, fontweight='normal', rotation=90, zorder=4)
            ax2.bar(x_pos, 0, bar_width, color=colors[j])
        elif m == 99.999: # Special marker for the 12 GB cap (indicating Out of Memory)    
            ax2.text(x_pos, 0, 'Out of Memory (>12 GB)', ha='center', va='bottom', color='red', 
                    fontsize=defaultFontSize, fontweight='normal', rotation=90, zorder=4)
            ax2.bar(x_pos, 0, bar_width, color=colors[j])
        elif m == -1: # Special marker for Not FIMI. Format not supported
            ax2.text(x_pos, 0, 'Format not supported', ha='center', va='bottom', color='red', 
                    fontsize=defaultFontSize, fontweight='normal', rotation=90, zorder=4)
            ax2.bar(x_pos, 0, bar_width, color=colors[j])
        else:
            ax2.bar(x_pos, m, bar_width, color=colors[j], edgecolor='black', linewidth=0.7, zorder=3)

ax2.set_yscale('linear')
ax2.set_ylabel('Peak Memory (GB)', fontsize=defaultFontSize)
ax2.tick_params(axis='y', labelsize=defaultFontSize)
ax2.set_xticks(indices)
ax2.set_xticklabels(x_labels, fontsize=defaultFontSize)
ax2.set_xlabel('Top-K (minSup)', fontsize=defaultFontSize)
ax2.grid(axis='y', which='both', linestyle='--', alpha=0.4, zorder=1)
#
# ==========================================================
# UNIFIED LEGEND & LAYOUT RENDERING
# ==========================================================
# Extract the handles and labels from the left plot (ax1)
handles, labels = ax1.get_legend_handles_labels()
#
# Create a single, overarching legend attached to the Figure (not an individual axis)
fig.legend(handles, labels, fontsize=defaultFontSize, loc='upper center', bbox_to_anchor=(0.5, 1), 
           ncol=math.ceil(len(algos)/2), fancybox=False, shadow=False, frameon=False)
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