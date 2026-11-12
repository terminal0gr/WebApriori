import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

ALGO='Java'
DATASET1='Kosarak' 
DATASETTYPE='Sparse'
DATASET1_SUBTITLES = ['Kosarak $K$=100 ($minSup\simeq$0.023)', 'Kosarak $K$ = 10,000 ($minSup\simeq$0.002)']

# visible area
LEFT_RT1 = 30
LEFT_MEM1 = 2
RIGHT_RT1 = 150
RIGHT_MEM1 = 12
# Manipulate overflow offset for failed executions to avoid overlap in annotations
overflow_offset=[1,1]  # Separate offsets for left and right charts


# Helper function to plot a point on a specific axis
def plot_point(ax, rt_val, mem_val, chart_id):
    global overflow_offset
    rt_str = str(rt_val).strip()
    mem_str = str(mem_val).strip()
    
    is_timeout = '1000+' in rt_str
    is_oom = '12GB+' in mem_str
    not_FIMI = 'not FIMI' in rt_str or 'not FIMI' in mem_str
    internal_err = 'internal_error' in rt_str or 'internal_error' in mem_str
    
    # Place on the chart borders if failed, otherwise plot actual value
    if chart_id == 0:  # Left Top Chart (top-K 100)
        rt = LEFT_RT1
        mem = LEFT_MEM1
    else:  # Right Top Chart (top-K 10000)    
        rt = RIGHT_RT1
        mem = RIGHT_MEM1
    
    if is_timeout or is_oom or not_FIMI or internal_err:
        # *Methodology Compliance*: If failed, overlay an 'x' inside the circle
        ax.scatter(rt-rt*0.06, mem-(mem*0.05*overflow_offset[chart_id]), color='red', marker='x', s=50, zorder=5)
        # Add a clean text indicator indicating timeout or OOM
        ax.text(rt-rt*0.08, mem-(mem*0.05*overflow_offset[chart_id]), 'timeout (>1000 s)' if is_timeout else 'OOM (>12GB)' if is_oom else 'not FIMI' if not_FIMI else 'internal error', ha='right', va='center', fontsize=9, color='darkred', alpha=0.5, style='italic', zorder=2)
        rt_str=rt       
        mem_str=mem  
    if float(rt_str)>=rt:
        # Plot as a circle
        scatter = ax.scatter(rt-rt*0.06, mem-(mem*0.05*overflow_offset[chart_id]), color=color, marker='o', s=200, edgecolors='black', alpha=1, zorder=4)
        if not is_timeout and not is_oom and not not_FIMI and not internal_err:
            ax.text(rt-rt*0.08, mem-(mem*0.05*overflow_offset[chart_id]), 'rt:'+str(int(float(rt_val)))+'s PM:'+format(float(mem_str)/1024.0, '.1f')+'GB', ha='right', va='center', fontsize=9, color='black', alpha=0.6, style='italic', zorder=2)
            ax.annotate(str(alg_id), (rt-rt*0.06, mem-(mem*0.05*overflow_offset[chart_id])), xytext=(0, -1), textcoords='offset points', ha='center', va='center', fontsize=10, zorder=6)
        else:
            ax.annotate(str(alg_id), (rt-rt*0.06, mem-(mem*0.05*overflow_offset[chart_id])), xytext=(7, -5), textcoords='offset points', fontsize=12, zorder=6)
        overflow_offset[chart_id]+=1    
    elif float(mem_str)/1024.0>=mem:
        # Plot as a circle
        scatter = ax.scatter(float(rt_str), mem-(mem*0.03), color=color, marker='o', s=200, edgecolors='black', alpha=1, zorder=4)
        if not is_timeout and not is_oom and not not_FIMI and not internal_err:
            # Only for this chart
            if chart_id == 0 and alg_id==2:
                ax.text(float(rt_str)-float(rt_str)*0.06, mem-(mem*0.03), 'PM:'+format(float(mem_str)/1024.0, '.1f')+'GB', ha='right', va='center', fontsize=9, color='black', alpha=0.6, style='italic', zorder=2)
                ax.annotate(str(alg_id), (float(rt_str), mem-(mem*0.03)), xytext=(0, -1), textcoords='offset points', ha='center', va='center', fontsize=10, zorder=6)
            elif chart_id == 0 and alg_id==4:
                ax.text(float(rt_str)-float(rt_str)*0.06, mem-(mem*0.08), 'PM:'+format(float(mem_str)/1024.0, '.1f')+'GB', ha='right', va='center', fontsize=9, color='black', alpha=0.6, style='italic', zorder=2)
                ax.annotate(str(alg_id), (float(rt_str), mem-(mem*0.08)), xytext=(0, -1), textcoords='offset points', ha='center', va='center', fontsize=10, zorder=6)
            elif chart_id == 0 and alg_id==6:
                ax.text(float(rt_str)-float(rt_str)*0.06, mem-(mem*0.13), 'PM:'+format(float(mem_str)/1024.0, '.1f')+'GB', ha='right', va='center', fontsize=9, color='black', alpha=0.6, style='italic', zorder=2)
                ax.annotate(str(alg_id), (float(rt_str), mem-(mem*0.13)), xytext=(0, -1), textcoords='offset points', ha='center', va='center', fontsize=10, zorder=6)
            else:                
                ax.text(float(rt_str)-float(rt_str)*0.06, mem-(mem*0.03), 'PM:'+format(float(mem_str)/1024.0, '.1f')+'GB', ha='right', va='center', fontsize=9, color='black', alpha=0.6, style='italic', zorder=2)
                ax.annotate(str(alg_id), (float(rt_str), mem-(mem*0.03)), xytext=(0, -1), textcoords='offset points', ha='center', va='center', fontsize=10, zorder=6)
        else:    
            ax.annotate(str(alg_id), (float(rt_str), mem-(mem*0.03)), xytext=(7, -5), textcoords='offset points', fontsize=12, zorder=6)
    else:
        # Plot as a circle
        scatter = ax.scatter(float(rt_str), float(mem_str)/1024.0, color=color, marker='o', s=200, edgecolors='black', alpha=1, zorder=4)        
        # Annotate with just the ID number
        # ax.annotate(str(alg_id), (float(rt_str), float(mem_str)/1024.0), xytext=(6, -5), textcoords='offset points', fontsize=14, zorder=6)
        ax.annotate(str(alg_id), (float(rt_str), float(mem_str)/1024.0), xytext=(0, -1), textcoords='offset points', ha='center', va='center', fontsize=10, zorder=6)

    return scatter



# 1. Setup Figure and Subplots (2 Row, 2 Columns)
fig, axes = plt.subplots(1, 2, figsize=(14, 7))
(ax1, ax2) = axes.flatten()  # Flatten the 2D array of axes for easier indexing
fig.canvas.manager.set_window_title(ALGO + '-' + DATASETTYPE)

ax1.set_xlim(0, LEFT_RT1)
ax1.set_ylim(0, LEFT_MEM1)
ax2.set_xlim(0, RIGHT_RT1)
ax2.set_ylim(0, RIGHT_MEM1)



# --- Create a Custom Green-to-Transparent Gradient Colormap ---
n_colors = 256
color_array = np.zeros((n_colors, 4))
color_array[:, 0] = 0.133  # Red component for an elegant Forest Green
color_array[:, 1] = 0.545  # Green component
color_array[:, 2] = 0.133  # Blue component
color_array[:, 3] = np.linspace(0.0, 0.18, n_colors)  # Alpha scales from 0 (transparent) to 0.18 (soft green)
green_fade_cmap = mcolors.ListedColormap(color_array)

# Create a 2D mesh grid that is strongest at (0,0) and decays toward the boundaries
x_intensity = np.linspace(1, 0, 100)
y_intensity = np.linspace(1, 0, 100)
X_mesh, Y_mesh = np.meshgrid(x_intensity, y_intensity)
gradient_data = X_mesh * Y_mesh  # 1.0 at origin, 0.0 at edges
# ------------------------------------------------------------------

# 2.1. Read Data for DATASET1
file_path = ALGO + '_' + DATASET1 + '.csv'

# Skip the two header rows and assign clean column names
df = pd.read_csv(file_path, skiprows=2, header=None)
df.columns = ['Algorithm', 'RT_100', 'Mem_100', 'RT_10000', 'Mem_10000']
df.dropna(subset=['Algorithm'], inplace=True)

# Insert the numeric identifiers (1 to maximum number of algorithms)
df.insert(0, 'ID', range(1, len(df) + 1))

# Generate a distinct color for every algorithm using the 'tab20' colormap. 
# Use only once for both datasets to ensure consistent coloring across charts.
colors = plt.cm.tab20(np.linspace(0, 1, len(df)))

handles = []
labels = []

# 2.2. Process and Plot Data for DATASET1
for index, row in df.iterrows():
    alg_id = row['ID']
    algo_name = str(row['Algorithm']).strip()
    color = colors[index]
    
    # Format the legend label exactly as requested (e.g., "2. Eclat PAMI")
    label_text = f"{alg_id}. {algo_name}"
    labels.append(label_text)
    
    # Plot on Left Chart (top-K 100)
    scatter_handle = plot_point(ax1, row['RT_100'], row['Mem_100'], 0)
    handles.append(scatter_handle) # Only need to save handles once for the shared legend
    
    # Plot on Right Chart (top-K 10000)
    plot_point(ax2, row['RT_10000'], row['Mem_10000'], 1)

# 2.3. Formatting the Subplots
for ax, subtitle in zip([ax1, ax2], DATASET1_SUBTITLES):
    ax.set_title(subtitle, fontsize=14, pad=10)
    ax.set_xlabel('Runtime (seconds)', fontsize=14)
    ax.tick_params(axis='x', labelsize=14)
    ax.set_ylabel('Peak Memory (GB)', fontsize=14)
    ax.tick_params(axis='y', labelsize=14)
    ax.grid(True, linestyle='--', alpha=0.5, zorder=0)

    # --- NEW: Apply the Gradient Background Box to each chart ---
    ax.imshow(gradient_data, 
              extent=[0, LEFT_RT1, 0, LEFT_MEM1] if ax == ax1 else [0, RIGHT_RT1, 0, RIGHT_MEM1],
              cmap=green_fade_cmap, 
              origin='lower', 
              aspect='auto', 
              zorder=1) # Keeps it safely behind your scatter data points (zorder=4)
    
    # Add a clean text indicator inside the zone
    ax.text((LEFT_RT1 if ax == ax1 else RIGHT_RT1)/4, (LEFT_MEM1 if ax == ax1 else RIGHT_MEM1)/6, 'Optimal Zone', 
            ha='center', va='center', fontsize=9, color='darkgreen', alpha=0.6, style='italic', zorder=2)
    



# 4. Add Shared Title and Legend Outside the Charts
# fig.suptitle('Intra-Ecosystem Algorithmic Benchmarking\n (Java Configurations) Dataset: Kosarak', fontsize=14, y=0.98)

# Place the legend at the top, spread across 4 columns
fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.99), 
           ncol=5, fontsize=12, fancybox=False, shadow=False, frameon=False)


# Adjust the internal layout so the charts are pushed down to make room for the legend
# plt.subplots_adjust(top=0.83, bottom=0.08, left=0.08, right=0.97, wspace=0.15, hspace=0.32)
plt.subplots_adjust(top=0.75, bottom=0.1, left=0.07, right=0.96, wspace=0.15)


# 5. Save and Display
plt.savefig('fig_' + ALGO + '_' + DATASETTYPE + '.pdf', format='pdf', bbox_inches='tight')
plt.show()