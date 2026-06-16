import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

# Data Extraction
ks = ['$10^2$\n(0.023)', '$10^3$\n(0.006)', '$10^4$\n(0.002)']
algos = ['Apriori Py mlxtend', 'Apriori Py Pami', 'AprioriTID Py Pami', 'AprioriTID Java SPMF', 'AprioriTID bitset Java SPMF', 'Apriori C++ Borgelt']
colors = ['skyblue', 'steelblue', 'blue', 'gray', 'black', 'red'] 
dataset = "kosarak" 


# Use None instead of 0 to represent the execution timeout cleanly
peakMemory = {
    '$10^2$\n(0.023)': [None, 1.369, 0.605, 1.026, 9.056, 0.083],
    '$10^3$\n(0.006)': [None, 1.850, 0.716, 1.524, 9.272, 0.084],
    '$10^4$\n(0.002)': [None, 3.221, 1.848, 5.119, 12.000, 0.094]
}

# Setup Plot
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.10
gap = 0.03  # Slightly narrowed gap to perfectly bundle the 6 bars 
indices = np.arange(len(ks))
fig.canvas.manager.set_window_title(dataset)


for i, k in enumerate(ks):
    for j, algo in enumerate(algos):
        # Calculate distinct horizontal positions for each algorithm bar within the K group
        x_pos = indices[i] + (j - 2.5) * (bar_width + gap)
        m = peakMemory[k][j]
        
        if m is None:
            # If the algorithm timed out, leave the bar space blank and write a clean, vertical red 'T/O'
            ax.text(x_pos, 0.1, 'Timeout (>1,000 s)', ha='center', va='bottom', color='red', 
                    fontsize=11, fontweight='bold', rotation=90, zorder=4)
            
            # Draw an empty dummy bar just to make sure the label links up to the legend correctly
            ax.bar(x_pos, 0, bar_width, color=colors[j], label=algos[j] if i == 0 else "")
        else:
            # Regular successful runs draw standard bars
            ax.bar(x_pos, m, bar_width, color=colors[j], edgecolor='black', linewidth=0.7,
                   label=algos[j] if i == 0 else "", zorder=3)

# Academic Styling adjustments for ESWA Layout
ax.set_yscale('linear')
ax.set_ylabel('Peak Memory (GB)', fontsize=16)
ax.tick_params(axis='y', labelsize=16)

ax.set_xticks(indices)
ax.set_xticklabels(ks, fontsize=16)
ax.set_xlabel('Top-k (minSup)', fontsize=18)

# Outer Legend Configuration
plt.legend(fontsize=14, loc='lower center', bbox_to_anchor=(0.5, 1),  ncol=2, fancybox=False, shadow=False, frameon=False)

plt.grid(axis='y', which='both', linestyle='--', alpha=0.4, zorder=1)
plt.subplots_adjust(right=0.97)

plt.subplots_adjust(top=0.85)
plt.tight_layout()

# Save and Show
plt.savefig('fig_M_' + dataset + '.pdf', format='pdf', bbox_inches='tight')
plt.show()