import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

ALGO='Python'
DATASET='Kosarak'

# visible area
LEFT_RT = 80
LEFT_MEM = 2
RIGHT_RT = 150
RIGHT_MEM = 4
# Manipulate overflow offset for failed executions to avoid overlap in annotations
overflow_offset=[1,1]  # Separate offsets for left and right charts


# Helper function to plot a point on a specific axis
def plot_point(ax, rt_val, mem_val, chart_id):
    global overflow_offset
    rt_str = str(rt_val).strip()
    mem_str = str(mem_val).strip()
    
    is_timeout = '+++' in rt_str
    is_oom = '+++' in mem_str
    
    # Place on the chart borders if failed, otherwise plot actual value
    if chart_id == 0:  # Left Chart (top-K 100)
        rt = LEFT_RT
        mem = LEFT_MEM
    else:  # Right Chart (top-K 10000)
        rt = RIGHT_RT
        mem = RIGHT_MEM
    
    if is_timeout or is_oom:
        # *Methodology Compliance*: If failed, overlay a small 'x' inside the circle
        ax.scatter(rt-rt*0.06, mem-(mem*0.05*overflow_offset[chart_id]), color='red', marker='x', s=50, zorder=5)
        rt_str=rt       
        mem_str=mem  

    if float(rt_str)>=rt or float(mem_str)/1024.0>=mem:
        # Plot as a circle
        scatter = ax.scatter(rt-rt*0.06, mem-(mem*0.05*overflow_offset[chart_id]), color=color, marker='o', s=140, edgecolors='black', alpha=1, zorder=4)
        ax.annotate(str(alg_id), (rt-rt*0.06, mem-(mem*0.05*overflow_offset[chart_id])), xytext=(7, -5), textcoords='offset points', fontsize=14, zorder=6)
        overflow_offset[chart_id]+=1    
    else:
        # Plot as a circle
        scatter = ax.scatter(float(rt_str), float(mem_str)/1024.0, color=color, marker='o', s=140, edgecolors='black', alpha=1, zorder=4)        
        # Annotate with just the ID number
        ax.annotate(str(alg_id), (float(rt_str), float(mem_str)/1024.0), xytext=(6, -5), textcoords='offset points', fontsize=14, zorder=6)

    return scatter




# 1. Read Data
file_path = ALGO + '_' + DATASET + '.csv'

# Skip the two header rows and assign clean column names
df = pd.read_csv(file_path, skiprows=2, header=None)
df.columns = ['Algorithm', 'RT_100', 'Mem_100', 'RT_10000', 'Mem_10000']
df.dropna(subset=['Algorithm'], inplace=True)

# Insert the numeric identifiers (1 to maximum number of algorithms)
df.insert(0, 'ID', range(1, len(df) + 1))


# 2. Setup Figure and Subplots (1 Row, 2 Columns)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
fig.canvas.manager.set_window_title(ALGO + '-' + DATASET)

# Generate a distinct color for every algorithm using the 'tab20' colormap
colors = plt.cm.tab20(np.linspace(0, 1, len(df)))

# --- NEW: Create a Custom Green-to-Transparent Gradient Colormap ---
n_colors = 256
color_array = np.zeros((n_colors, 4))
color_array[:, 0] = 0.133  # Red component for an elegant Forest Green
color_array[:, 1] = 0.545  # Green component
color_array[:, 2] = 0.133  # Blue component
color_array[:, 3] = np.linspace(0.0, 0.18, n_colors)  # Alpha scales from 0 (transparent) to 0.18 (soft green)
green_fade_cmap = mcolors.ListedColormap(color_array)

# Define the boundaries of your "Optimal Zone"
GRAD_X_MAX = 60    # Fades out by 60 seconds
GRAD_Y_MAX = 2.5   # Fades out by 2.5 GB

# Create a 2D mesh grid that is strongest at (0,0) and decays toward the boundaries
x_intensity = np.linspace(1, 0, 100)
y_intensity = np.linspace(1, 0, 100)
X_mesh, Y_mesh = np.meshgrid(x_intensity, y_intensity)
gradient_data = X_mesh * Y_mesh  # 1.0 at origin, 0.0 at edges
# ------------------------------------------------------------------

handles = []
labels = []

# 3. Process and Plot Data
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

ax1.set_xlim(0, LEFT_RT)
ax1.set_ylim(0, LEFT_MEM)
ax2.set_xlim(0, RIGHT_RT)
ax2.set_ylim(0, RIGHT_MEM)

# 4. Formatting the Subplots
for ax, subtitle in zip([ax1, ax2], ['Top-$k$ = 100', 'Top-$k$ = 10,000']):
    ax.set_title(subtitle, fontsize=14, pad=10)
    ax.set_xlabel('Runtime (seconds)', fontsize=14)
    ax.tick_params(axis='x', labelsize=14)
    ax.set_ylabel('Peak Memory (GB)', fontsize=14)
    ax.tick_params(axis='y', labelsize=14)
    ax.grid(True, linestyle='--', alpha=0.5, zorder=0)

    # --- NEW: Apply the Gradient Background Box to each chart ---
    ax.imshow(gradient_data, 
              extent=[0, LEFT_RT, 0, LEFT_MEM] if ax == ax1 else [0, RIGHT_RT, 0, RIGHT_MEM],
              cmap=green_fade_cmap, 
              origin='lower', 
              aspect='auto', 
              zorder=1) # Keeps it safely behind your scatter data points (zorder=4)
    
    # Add a clean text indicator inside the zone
    ax.text((LEFT_RT if ax == ax1 else RIGHT_RT)/4, (LEFT_MEM if ax == ax1 else RIGHT_MEM)/6, 'Optimal Zone', 
            ha='center', va='center', fontsize=9, color='darkgreen', alpha=0.6, style='italic', zorder=2)
    

# 5. Add Shared Title and Legend Outside the Charts
# fig.suptitle('Intra-Ecosystem Algorithmic Benchmarking\n (Python Configurations) Dataset: Kosarak', fontsize=14, y=0.98)

# Place the legend at the top, spread across 4 columns
fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.99), 
           ncol=4, fontsize=14, fancybox=False, shadow=False, frameon=False)

# Adjust the internal layout so the charts are pushed down to make room for the legend
plt.subplots_adjust(top=0.75, bottom=0.1, left=0.07, right=0.96, wspace=0.15)

# 6. Save and Display
plt.savefig('fig_' + ALGO + '_' + DATASET + '.pdf', format='pdf', bbox_inches='tight')
plt.show()