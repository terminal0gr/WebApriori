import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Read Data
# Replace 'Python_Kosarak.csv' with your exact file path
file_path = 'Python_Kosarak.csv'

# Skip the two header rows and assign clean column names
df = pd.read_csv(file_path, skiprows=2, header=None)
df.columns = ['Algorithm', 'RT_100', 'Mem_100', 'RT_10000', 'Mem_10000']
df.dropna(subset=['Algorithm'], inplace=True)

# Insert the numeric identifiers (1 to 14)
df.insert(0, 'ID', range(1, len(df) + 1))

# 2. Setup Figure and Subplots (1 Row, 2 Columns)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5))

# Generate 14 distinct colors using the 'tab20' colormap
colors = plt.cm.tab20(np.linspace(0, 1, len(df)))

# Determine axis boundaries to handle timeout (+++) outliers
# Capping at 350s and 14GB keeps the successful executions clearly visible
MAX_RT = 350  
MAX_MEM = 14  

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
    
    # Helper function to plot a point on a specific axis
    def plot_point(ax, rt_val, mem_val):
        rt_str = str(rt_val).strip()
        mem_str = str(mem_val).strip()
        
        is_timeout = '+++' in rt_str
        is_oom = '+++' in mem_str
        
        # Place on the chart borders if failed, otherwise plot actual value
        x = MAX_RT if is_timeout else float(rt_str)
        y = MAX_MEM if is_oom else float(mem_str) / 1024.0 # Convert MB to GB
        
        # Plot as a circle as requested
        scatter = ax.scatter(x, y, color=color, marker='o', s=120, edgecolors='black', alpha=0.8, zorder=4)
        
        # *Methodology Compliance*: If failed, overlay a small 'x' inside the circle
        if is_timeout or is_oom:
            ax.scatter(x, y, color='red', marker='x', s=40, zorder=5)
        
        # Annotate with just the ID number
        ax.annotate(str(alg_id), (x, y), xytext=(7, 5), textcoords='offset points', 
                    fontsize=10, fontweight='bold', zorder=6)
        
        return scatter

    # Plot on Left Chart (top-K 100)
    scatter_handle = plot_point(ax1, row['RT_100'], row['Mem_100'])
    handles.append(scatter_handle) # Only need to save handles once for the shared legend
    
    # Plot on Right Chart (top-K 10000)
    plot_point(ax2, row['RT_10000'], row['Mem_10000'])

# 4. Formatting the Subplots
for ax, subtitle in zip([ax1, ax2], ['Top-$k$ = 100', 'Top-$k$ = 10,000']):
    ax.set_title(subtitle, fontsize=12, fontweight='bold', pad=10)
    ax.set_xlabel('Execution Runtime (seconds)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Peak Memory Consumption (GB)', fontsize=11, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.5, zorder=0)
    
    # Apply identical limits to both charts for visual consistency
    ax.set_xlim(0, MAX_RT + 20)
    ax.set_ylim(0, MAX_MEM + 1)

# 5. Add Shared Title and Legend Outside the Charts
fig.suptitle('Intra-Ecosystem Algorithmic Benchmarking (Python Configurations)\nDataset: Kosarak', 
             fontsize=15, fontweight='bold', y=1.05)

# Place the legend at the top, spread across 4 columns
fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.94), 
           ncol=4, fontsize=10, frameon=True, shadow=True)

# Adjust the internal layout so the charts are pushed down to make room for the legend
plt.subplots_adjust(top=0.72, bottom=0.1, left=0.08, right=0.95, wspace=0.2)

# 6. Save and Display
plt.savefig('Python_Kosarak_DualChart.png', dpi=300, format='png', bbox_inches='tight')
plt.show()