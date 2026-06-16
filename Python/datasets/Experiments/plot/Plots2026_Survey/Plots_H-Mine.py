import math

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams["font.family"] = "Times New Roman"

algoFamily = "H-Mine"
algos = ['H-Mine Py mlxtend', 'H-Mine Java SPMF']
colors = ['blue', 'gray'] 
markers = ['D', 's']



dataset = "kosarak"
defaultFontSize = 18
#
# Common X-axis labels
x_labels = ["100 (0.023)", "1000 (0.006)", "10,000 (0.002)"]
#
runtime = {
    x_labels[0]: [195.27, 2.21],
    x_labels[1]: [220.54, 2.74],
    x_labels[2]: [273.03, 6.43],
}
#
peakMemory = {
    x_labels[0]: [11.423, 0.565],
    x_labels[1]: [12.305, 0.633],
    x_labels[2]: [12.322, 3.396],
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
ax1.set_ylim(0, 300)
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
           ncol=4, fancybox=False, shadow=False, frameon=False)
#
# Apply tight layout FIRST to calculate boundaries
plt.tight_layout()
#
# Adjust the top margin to create space for the shared legend
# wspace creates a slight gap between the two side-by-side charts
fig.subplots_adjust(top=0.90, wspace=0.15)
#
# Save and Show
plt.savefig('fig_' + algoFamily + '_' + dataset + '.pdf', format='pdf', bbox_inches='tight')






# dataset = "L-0023"
# defaultFontSize = 18
# #
# # Common X-axis labels
# x_labels = ["100 (0.033)", "1000 (0.012)", "10,000 (0.005)"]
# #
# runtime = {
#     x_labels[0]: [2.58, 0.11, None, 0.25],
#     x_labels[1]: [4.55, 0.27, None, 0.26],
#     x_labels[2]: [70.30, 0.66, None, 0.26],
# }
# #
# peakMemory = {
#     x_labels[0]: [0.096, 0.059, -1, 0.004],
#     x_labels[1]: [0.105, 0.067, -1, 0.004],
#     x_labels[2]: [0.119, 0.076, -1, 0.004],
# }
# #
# # --- 1. Setup the Shared Figure Canvas ---
# # figsize=(16, 6) gives plenty of width for side-by-side plots while maintaining height
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
# fig.canvas.manager.set_window_title(algoFamily + '-' + dataset)
# #
# # ==========================================================
# # LEFT PLOT (ax1): Execution Time (Line Chart)
# # ==========================================================
# ax1.set_xlabel("Top-K (minSup)", fontsize=defaultFontSize)
# ax1.set_ylim(0, 20)
# ax1.set_xscale('log')
# x_numeric = [100, 1000, 10000]
# #
# ax1.set_xticks(x_numeric)
# ax1.set_xticklabels(x_labels, fontsize=defaultFontSize)
# ax1.tick_params(axis='y', labelsize=defaultFontSize) 
# ax1.set_ylabel("Time (sec)", fontsize=defaultFontSize)
# #
# ax1.plot(x_numeric, [runtime[key][0] for key in runtime], marker=markers[0], linestyle='-', label=algos[0], markersize=8, color=colors[0])
# ax1.plot(10000, 19.5, marker="$70$", color=colors[0], markersize=16, zorder=5)
# ax1.plot(x_numeric, [runtime[key][1] for key in runtime], marker=markers[1], linestyle='-', label=algos[1], markersize=8, color=colors[1])
# ax1.plot(100, 19.5, marker=markers[2], label=algos[2], markersize=8, color=colors[2], zorder=5)
# ax1.plot(100, 19.5, marker='x', color='red', markersize=6, zorder=6)
# ax1.plot(x_numeric, [runtime[key][3] for key in runtime], marker=markers[3], linestyle='-', label=algos[3], markersize=8, color=colors[3])
# #
# ax1.grid(True)
# #
# # ==========================================================
# # RIGHT PLOT (ax2): Peak Memory (Grouped Bar Chart)
# # ==========================================================
# #
# bar_width = 0.10
# gap = 0.03  
# indices = np.arange(len(x_labels))
# #
# for i, k in enumerate(x_labels):
#     for j, algo in enumerate(algos):
#         x_pos = indices[i] + (j - 2.5) * (bar_width + gap)
#         m = peakMemory[k][j]
        
#         if m is None: # Timeout (>1,000 s)
#             ax2.text(x_pos, 0, 'Timeout (>1,000 s)', ha='center', va='bottom', color='red', 
#                     fontsize=defaultFontSize, fontweight='normal', rotation=90, zorder=4)
#             ax2.bar(x_pos, 0, bar_width, color=colors[j])
#         elif m == 99.999: # Special marker for the 12 GB cap (indicating Out of Memory)    
#             ax2.text(x_pos, 0, 'Out of Memory (>12 GB)', ha='center', va='bottom', color='red', 
#                     fontsize=defaultFontSize, fontweight='normal', rotation=90, zorder=4)
#             ax2.bar(x_pos, 0, bar_width, color=colors[j])
#         elif m == -1: # Special marker for Not FIMI. Format not supported
#             ax2.text(x_pos, 0, 'Format not supported', ha='center', va='bottom', color='red', 
#                     fontsize=defaultFontSize, fontweight='normal', rotation=90, zorder=4)
#             ax2.bar(x_pos, 0, bar_width, color=colors[j])
#         else:
#             ax2.bar(x_pos, m, bar_width, color=colors[j], edgecolor='black', linewidth=0.7, zorder=3)

# ax2.set_yscale('linear')
# ax2.set_ylabel('Peak Memory (GB)', fontsize=defaultFontSize)
# ax2.tick_params(axis='y', labelsize=defaultFontSize)
# ax2.set_xticks(indices)
# ax2.set_xticklabels(x_labels, fontsize=defaultFontSize)
# ax2.set_xlabel('Top-K (minSup)', fontsize=defaultFontSize)
# ax2.grid(axis='y', which='both', linestyle='--', alpha=0.4, zorder=1)
# #
# # ==========================================================
# # UNIFIED LEGEND & LAYOUT RENDERING
# # ==========================================================
# # Extract the handles and labels from the left plot (ax1)
# handles, labels = ax1.get_legend_handles_labels()
# #
# # Create a single, overarching legend attached to the Figure (not an individual axis)
# # ncol=3 spreads the 6 algorithms into 2 clean rows across the wide top span
# fig.legend(handles, labels, fontsize=defaultFontSize, loc='upper center', bbox_to_anchor=(0.5, 1), 
#            ncol=4, fancybox=False, shadow=False, frameon=False)
# #
# # Apply tight layout FIRST to calculate boundaries
# plt.tight_layout()
# #
# # Adjust the top margin to create space for the shared legend
# # wspace creates a slight gap between the two side-by-side charts
# fig.subplots_adjust(top=0.90, wspace=0.15)
# #
# # Save and Show
# plt.savefig('fig_' + algoFamily + '_' + dataset + '.pdf', format='pdf', bbox_inches='tight')



# dataset = "accidents"
# defaultFontSize = 18
# #
# # Common X-axis labels
# x_labels = ["100 (0.820)", "1000 (0.656)", "10,000 (0.482)"]
# #
# runtime = {
#     x_labels[0]: [63.68, 4.53, 1.25, 0.69],
#     x_labels[1]: [649.95, 7.79, 1.54, 0.82],
#     x_labels[2]: [None, 8.79, 1.99, 1.04],
# }
# #
# peakMemory = {
#     x_labels[0]: [0.826, 0.649, 0.619, 0.062],
#     x_labels[1]: [0.829, 0.654, 0.619, 0.062],
#     x_labels[2]: [None, 0.717, 0.619, 0.062],
# }
# #
# # --- 1. Setup the Shared Figure Canvas ---
# # figsize=(16, 6) gives plenty of width for side-by-side plots while maintaining height
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
# fig.canvas.manager.set_window_title(algoFamily + '-' + dataset)
# #
# # ==========================================================
# # LEFT PLOT (ax1): Execution Time (Line Chart)
# # ==========================================================
# ax1.set_xlabel("Top-K (minSup)", fontsize=defaultFontSize)
# ax1.set_ylim(0, 70)
# ax1.set_xscale('log')
# x_numeric = [100, 1000, 10000]
# #
# ax1.set_xticks(x_numeric)
# ax1.set_xticklabels(x_labels, fontsize=defaultFontSize)
# ax1.tick_params(axis='y', labelsize=defaultFontSize) 
# ax1.set_ylabel("Time (sec)", fontsize=defaultFontSize)
# #
# ax1.plot(x_numeric, [runtime[key][0] for key in runtime], marker=markers[0], linestyle='-', label=algos[0], markersize=8, color=colors[0])
# ax1.plot(1000, 68, marker="$650$", color=colors[0], markersize=16, zorder=5)
# ax1.plot(10000, 68, marker=markers[0], color=colors[0], markersize=8, zorder=5)
# ax1.plot(10000, 68, marker='x', color='red', markersize=6, zorder=6)
# ax1.plot(x_numeric, [runtime[key][1] for key in runtime], marker=markers[1], linestyle='-', label=algos[1], markersize=8, color=colors[1])
# ax1.plot(x_numeric, [runtime[key][2] for key in runtime], marker=markers[2], linestyle='-', label=algos[2], markersize=8, color=colors[2])
# ax1.plot(x_numeric, [runtime[key][3] for key in runtime], marker=markers[3], linestyle='-', label=algos[3], markersize=8, color=colors[3])
# #
# ax1.grid(True)
# #
# # ==========================================================
# # RIGHT PLOT (ax2): Peak Memory (Grouped Bar Chart)
# # ==========================================================
# #
# bar_width = 0.10
# gap = 0.03  
# indices = np.arange(len(x_labels))
# #
# for i, k in enumerate(x_labels):
#     for j, algo in enumerate(algos):
#         x_pos = indices[i] + (j - 2.5) * (bar_width + gap)
#         m = peakMemory[k][j]
        
#         if m is None: # Timeout (>1,000 s)
#             ax2.text(x_pos, 0, 'Timeout (>1,000 s)', ha='center', va='bottom', color='red', 
#                     fontsize=defaultFontSize, fontweight='normal', rotation=90, zorder=4)
#             ax2.bar(x_pos, 0, bar_width, color=colors[j])
#         elif m == 99.999: # Special marker for the 12 GB cap (indicating Out of Memory)    
#             ax2.text(x_pos, 0, 'Out of Memory (>12 GB)', ha='center', va='bottom', color='red', 
#                     fontsize=defaultFontSize, fontweight='normal', rotation=90, zorder=4)
#             ax2.bar(x_pos, 0, bar_width, color=colors[j])
#         elif m == -1: # Special marker for Not FIMI. Format not supported
#             ax2.text(x_pos, 0, 'Format not supported', ha='center', va='bottom', color='red', 
#                     fontsize=defaultFontSize, fontweight='normal', rotation=90, zorder=4)
#             ax2.bar(x_pos, 0, bar_width, color=colors[j])
#         else:
#             ax2.bar(x_pos, m, bar_width, color=colors[j], edgecolor='black', linewidth=0.7, zorder=3)

# ax2.set_yscale('linear')
# ax2.set_ylabel('Peak Memory (GB)', fontsize=defaultFontSize)
# ax2.tick_params(axis='y', labelsize=defaultFontSize)
# ax2.set_xticks(indices)
# ax2.set_xticklabels(x_labels, fontsize=defaultFontSize)
# ax2.set_xlabel('Top-K (minSup)', fontsize=defaultFontSize)
# ax2.grid(axis='y', which='both', linestyle='--', alpha=0.4, zorder=1)
# #
# # ==========================================================
# # UNIFIED LEGEND & LAYOUT RENDERING
# # ==========================================================
# # Extract the handles and labels from the left plot (ax1)
# handles, labels = ax1.get_legend_handles_labels()
# #
# # Create a single, overarching legend attached to the Figure (not an individual axis)
# # ncol=3 spreads the 6 algorithms into 2 clean rows across the wide top span
# fig.legend(handles, labels, fontsize=defaultFontSize, loc='upper center', bbox_to_anchor=(0.5, 1), 
#            ncol=4, fancybox=False, shadow=False, frameon=False)
# #
# # Apply tight layout FIRST to calculate boundaries
# plt.tight_layout()
# #
# # Adjust the top margin to create space for the shared legend
# # wspace creates a slight gap between the two side-by-side charts
# fig.subplots_adjust(top=0.90, wspace=0.15)
# #
# # Save and Show
# plt.savefig('fig_' + algoFamily + '_' + dataset + '.pdf', format='pdf', bbox_inches='tight')




dataset = "T16I20D100K"
defaultFontSize = 18
#
# Common X-axis labels
x_labels = ["100 (0.799)", "1000 (0.643)", "10,000 (0.518)"]
#
runtime = {
    x_labels[0]: [1.40, 1.20],
    x_labels[1]: [4.06, 5.16],
    x_labels[2]: [23.80, 23.67],
}
#
peakMemory = {
    x_labels[0]: [0.138, 0.563],
    x_labels[1]: [0.138, 1.301],
    x_labels[2]: [0.146, 7.266],
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
ax1.set_ylim(0, 25)
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
           ncol=4, fancybox=False, shadow=False, frameon=False)
#
# Apply tight layout FIRST to calculate boundaries
plt.tight_layout()
#
# Adjust the top margin to create space for the shared legend
# wspace creates a slight gap between the two side-by-side charts
fig.subplots_adjust(top=0.90, wspace=0.15)
#
# Save and Show
plt.savefig('fig_' + algoFamily + '_' + dataset + '.pdf', format='pdf', bbox_inches='tight')




plt.show()