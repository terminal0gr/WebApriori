import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams["font.family"] = "Times New Roman"

algoFamily = "Apriori"
algos = ['Apriori Py mlxtend', 'Apriori Py Pami', 'AprioriTID Py Pami', 'AprioriTID Java SPMF', 'AprioriTID bitset Java SPMF', 'Apriori C++ Borgelt']
colors = ['skyblue', 'steelblue', 'blue', 'gray', 'black', 'red'] 
markers = ['D', 'H', '*', '>', 's', 'p']



dataset = "kosarak"
defaultFontSize = 18
#
# Common X-axis labels
x_labels = ["100 (0.023)", "1000 (0.006)", "10,000 (0.002)"]
#
runtime = {
    x_labels[0]: [None, 8, 34, 4, 4, 1.1],
    x_labels[1]: [None, 21, 47, 20, 5, 1.13],
    x_labels[2]: [None, 83, 93, 122, None, 1.81]
}
#
peakMemory = {
    x_labels[0]: [None, 1.369, 0.605, 1.026, 9.056, 0.083],
    x_labels[1]: [None, 1.850, 0.716, 1.524, 9.272, 0.084],
    x_labels[2]: [None, 3.221, 1.848, 5.119, 99.999, 0.094]
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
ax1.plot(100, 128, marker=markers[0], label=algos[0], markersize=8, color=colors[0])
ax1.plot(100, 128, marker='x', color='red', markersize=6, zorder=6)
ax1.plot(x_numeric, [runtime[key][1] for key in runtime], marker=markers[1], linestyle='-', label=algos[1], markersize=8, color=colors[1])
ax1.plot(x_numeric, [runtime[key][2] for key in runtime], marker=markers[2], linestyle='-', label=algos[2], markersize=8, color=colors[2])
ax1.plot(x_numeric, [runtime[key][3] for key in runtime], marker=markers[3], linestyle='-', label=algos[3], markersize=8, color=colors[3])
ax1.plot(x_numeric, [runtime[key][4] for key in runtime], marker=markers[4], linestyle='-', label=algos[4], markersize=8, color=colors[4])
ax1.plot(10000, 128, marker=markers[4], markersize=8, color=colors[4], zorder=5)
ax1.plot(10000, 128, marker='x', color='red', markersize=6, zorder=6)
ax1.plot(x_numeric, [runtime[key][5] for key in runtime], marker=markers[5], linestyle='-', label=algos[5], markersize=8, color=colors[5])
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
           ncol=3, fancybox=False, shadow=False, frameon=False)
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
    x_labels[0]: [0.74, 0.13, 0.05, -1, -1, 0.24],
    x_labels[1]: [5.27, 0.34, 0.11, -1, -1, 0.25],
    x_labels[2]: [136.20, 4.34, 0.36, -1, -1, 0.26],
}
#
peakMemory = {
    x_labels[0]: [0.092, 0.061, 0.057, -1, -1, 0.004],
    x_labels[1]: [0.094, 0.063, 0.057, -1, -1, 0.004],
    x_labels[2]: [0.100, 0.087, 0.063, -1, -1, 0.004],
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
ax1.set_ylim(0, 20)
ax1.set_xscale('log')
x_numeric = [100, 1000, 10000]
#
ax1.set_xticks(x_numeric)
ax1.set_xticklabels(x_labels, fontsize=defaultFontSize)
ax1.tick_params(axis='y', labelsize=defaultFontSize) 
ax1.set_ylabel("Time (sec)", fontsize=defaultFontSize)
#
ax1.plot(x_numeric, [runtime[key][0] for key in runtime], marker=markers[0], linestyle='-', label=algos[0], markersize=8, color=colors[0])
ax1.plot(10000, 19.5, marker="$136$", color=colors[0], markersize=16, zorder=5)
ax1.plot(x_numeric, [runtime[key][1] for key in runtime], marker=markers[1], linestyle='-', label=algos[1], markersize=8, color=colors[1])
ax1.plot(x_numeric, [runtime[key][2] for key in runtime], marker=markers[2], linestyle='-', label=algos[2], markersize=8, color=colors[2])
ax1.plot(100, 19.5, marker=markers[3], linestyle='-', label=algos[3], markersize=8, color=colors[3])
ax1.plot(100, 19.5, marker='x', color='red', markersize=6, zorder=6)
ax1.plot(120, 19.5, marker=markers[4], linestyle='-', label=algos[4], markersize=8, color=colors[4])
ax1.plot(120, 19.5, marker='x', color='red', markersize=6, zorder=6)
ax1.plot(x_numeric, [runtime[key][5] for key in runtime], marker=markers[5], linestyle='-', label=algos[5], markersize=8, color=colors[5])
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
           ncol=3, fancybox=False, shadow=False, frameon=False)
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
    x_labels[0]: [9.41,    9.05,  17.65, 4.47,  0.71, 0.68],
    x_labels[1]: [51.39,   50.04, 27.45, 29.70, 0.74, 0.80],
    x_labels[2]: [1024.14, None,  35.69, None,  1.06, 3.15],
}
#
peakMemory = {
    x_labels[0]: [0.826, 2.347, 0.733, 2.148, 0.701, 0.062],
    x_labels[1]: [0.828, 9.406, 0.754, 9.844, 0.703, 0.062],
    x_labels[2]: [0.828, 99.999, 1.127, 99.999, 0.849, 0.069],
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
ax1.set_ylim(0, 60)
ax1.set_xscale('log')
x_numeric = [100, 1000, 10000]
#
ax1.set_xticks(x_numeric)
ax1.set_xticklabels(x_labels, fontsize=defaultFontSize)
ax1.tick_params(axis='y', labelsize=defaultFontSize) 
ax1.set_ylabel("Time (sec)", fontsize=defaultFontSize)
#
ax1.plot(x_numeric, [runtime[key][0] for key in runtime], marker=markers[0], linestyle='-', label=algos[0], markersize=8, color=colors[0])
ax1.plot(7000, 58, marker="$995$", color=colors[0], markersize=16, zorder=5)
ax1.plot(x_numeric, [runtime[key][1] for key in runtime], marker=markers[1], linestyle='-', label=algos[1], markersize=8, color=colors[1])
ax1.plot(8700, 58, marker=markers[1], color=colors[1], markersize=8, zorder=5)
ax1.plot(8700, 58, marker='x', color='red', markersize=6, zorder=6)
ax1.plot(x_numeric, [runtime[key][2] for key in runtime], marker=markers[2], linestyle='-', label=algos[2], markersize=8, color=colors[2])
ax1.plot(x_numeric, [runtime[key][3] for key in runtime], marker=markers[3], linestyle='-', label=algos[3], markersize=8, color=colors[3])
ax1.plot(10000, 58, marker=markers[3], color=colors[3], markersize=8, zorder=5)
ax1.plot(10000, 58, marker='x', color='red', markersize=6, zorder=6)
ax1.plot(x_numeric, [runtime[key][4] for key in runtime], marker=markers[4], linestyle='-', label=algos[4], markersize=8, color=colors[4])
ax1.plot(x_numeric, [runtime[key][5] for key in runtime], marker=markers[5], linestyle='-', label=algos[5], markersize=8, color=colors[5])
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
           ncol=3, fancybox=False, shadow=False, frameon=False)
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
    x_labels[0]: [1.18, 2.71,  3.02, 2.24,  0.14, 0.34],
    x_labels[1]: [2.70, 12.71, 3.04, 10.05, 0.22, 0.45],
    x_labels[2]: [16.25, 125.69, 3.24, None, 0.57, 1.38],
}
#
peakMemory = {
    x_labels[0]: [0.137, 0.443, 0.109, 0.731, 0.250, 0.015],
    x_labels[1]: [0.138, 2.219, 0.122, 3.634, 0.289, 0.015],
    x_labels[2]: [0.145, 11.590, 0.240, 99.999, 0.547, 0.015],
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
ax1.set_ylim(0, 30)
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
ax1.plot(8000, 29, marker="$125$", color=colors[1], markersize=16, zorder=5)
ax1.plot(x_numeric, [runtime[key][2] for key in runtime], marker=markers[2], linestyle='-', label=algos[2], markersize=8, color=colors[2])
ax1.plot(x_numeric, [runtime[key][3] for key in runtime], marker=markers[3], linestyle='-', label=algos[3], markersize=8, color=colors[3])
ax1.plot(10000, 29, marker=markers[3], color=colors[3], markersize=8, zorder=5)
ax1.plot(10000, 29, marker='x', color='red', markersize=6, zorder=6)
ax1.plot(x_numeric, [runtime[key][4] for key in runtime], marker=markers[4], linestyle='-', label=algos[4], markersize=8, color=colors[4])
ax1.plot(x_numeric, [runtime[key][5] for key in runtime], marker=markers[5], linestyle='-', label=algos[5], markersize=8, color=colors[5])
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
           ncol=3, fancybox=False, shadow=False, frameon=False)
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