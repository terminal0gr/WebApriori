import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Load the data (skipping the first two metadata rows: Dataset, Top-K)
# Replace the filename with your actual local path if needed
file_path = 'Python_Kosarak_10000.csv'
df = pd.read_csv(file_path, skiprows=2)

# Rename columns for easier access
df.columns = ['Algorithm', 'Runtime', 'Memory']

# Drop any completely empty rows
df.dropna(subset=['Algorithm'], inplace=True)

# 2. Setup the Plot
fig, ax = plt.subplots(figsize=(10, 7))

# Define chart boundaries for outliers (adjust these limits as needed for visual scale)
MAX_RUNTIME_LIMIT = 350  
MAX_MEMORY_LIMIT = 12000  

# Dictionaries to handle custom legend entries without duplicating them
legend_handles = {}

# 3. Process and Plot Each Algorithm
for index, row in df.iterrows():
    algo = str(row['Algorithm']).strip()
    runtime_raw = str(row['Runtime']).strip()
    memory_raw = str(row['Memory']).strip()
    
    # Determine Ecosystem Color (C++ in Reds, Python in Blues)
    if 'Borgelt' in algo or 'Malliaridis' in algo:
        color = 'firebrick' # C++
        ecosystem = 'C++ Ecosystem'
    else:
        color = 'royalblue' # Python
        ecosystem = 'Python Ecosystem'
        
    # Check for execution failures (Timeouts or Out of Memory)
    is_timeout = '+++' in runtime_raw
    is_oom = '+++' in memory_raw
    
    if is_timeout or is_oom:
        # Place failed algorithms at the borders
        x_val = MAX_RUNTIME_LIMIT if is_timeout else float(runtime_raw)
        y_val = MAX_MEMORY_LIMIT if is_oom else float(memory_raw)
        
        # Plot Red 'x' for failures
        scatter = ax.scatter(x_val, y_val, color='red', marker='x', s=100, linewidths=2, zorder=5)
        
        # Annotate the specific error text next to the 'x'
        error_text = runtime_raw if is_timeout else memory_raw
        ax.annotate(f"{algo}\n({error_text})", (x_val, y_val), 
                    xytext=(-10, -10), textcoords='offset points', 
                    ha='right', va='top', fontsize=8, color='red')
        
        legend_handles['Failed/OOM'] = scatter
        
    else:
        # Standard successful execution
        x_val = float(runtime_raw)
        y_val = float(memory_raw)
        
        scatter = ax.scatter(x_val, y_val, color=color, marker='o', s=80, edgecolors='black', alpha=0.8, zorder=4)
        legend_handles[ecosystem] = scatter
        
        # Annotate the algorithm name slightly offset from the point
        ax.annotate(algo, (x_val, y_val), xytext=(8, 4), textcoords='offset points', 
                    fontsize=8, color='black')

# 4. Formatting and Beautification (ESWA Journal Standards)
ax.set_title('Cross-Ecosystem Algorithmic Benchmarking\nKosarak Dataset (top-$k$ = 10,000)', 
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Execution Runtime (seconds)', fontsize=12, fontweight='bold')
ax.set_ylabel('Peak Memory Consumption (MB)', fontsize=12, fontweight='bold')

# Add a grid for easier value reading (Pareto analysis)
ax.grid(True, linestyle='--', alpha=0.6, zorder=0)

# Set limits slightly beyond max valid data to fit annotations
ax.set_xlim(0, MAX_RUNTIME_LIMIT + 20)
ax.set_ylim(0, MAX_MEMORY_LIMIT + 1000)

# Create a clean, consolidated legend
handles = [legend_handles[key] for key in legend_handles]
labels = list(legend_handles.keys())
ax.legend(handles, labels, loc='upper left', fontsize=10, frameon=True, shadow=True)

# Highlight the Pareto optimal zone (Bottom-Left)
ax.axvspan(0, 50, ymin=0, ymax=0.2, color='green', alpha=0.5, zorder=1)
ax.text(25, 1000, 'Highly Efficient\n(Optimal Zone)', ha='center', va='center', 
        fontsize=10, color='darkgreen', alpha=0.5, style='italic')

plt.tight_layout()

# Save as a high-resolution image suitable for Elsevier
plt.savefig('Python_Kosarak_10000.pdf', dpi=300, format='pdf', bbox_inches='tight')

# Display the plot
plt.show()