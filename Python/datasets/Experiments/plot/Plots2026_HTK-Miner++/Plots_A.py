import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42


# Data Extraction from your stats
ks = ['K=100', 'K=1000', 'K=10000']
algos = [' HTK py', ' HTK C++', ' HTK++']



dataset="webdocs"
# Execution times per phase (seconds)
# Format: [HTK py, HTK_C++, HTK_PlusPlus]
reading = {
    'K=100': [138.22, 83.62, 28.39],
    'K=1000': [138.03, 83.62, 28.40],
    'K=10000': [138.34, 83.62, 28.39]
}
transform = {
    'K=100': [2.76, 0.26, 0.26],
    'K=1000': [10.45, 0.25, 0.25],
    'K=10000': [29.86, 0.52, 0.53]
}
mining = {
    'K=100': [0.19, 2.58, 3.99],
    'K=1000': [1.57, 10.45, 4.44],
    'K=10000': [37.50, 139.75, 14.65]
}
#
# Setup Plot
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.22
gap = 0.05
indices = np.arange(len(ks))
colors = ['#3498db', '#e67e22', '#2ecc71'] # Blue=Reading, Orange=Transform, Green=Mining
#
for i, k in enumerate(ks):
    for j, algo in enumerate(algos):
        # Calculate horizontal position for each bar in the group
        x_pos = i + (j - 1) * (bar_width + gap)
        
        r, t, m = reading[k][j], transform[k][j], mining[k][j]
        
        # Stacked bar logic: p2 sits on p1, p3 sits on (p1+p2)
        ax.bar(x_pos, r, bar_width, color=colors[0], label='Reading' if i==0 and j==0 else "")
        ax.bar(x_pos, t, bar_width, bottom=r, color=colors[1], label='Transform' if i==0 and j==0 else "")
        ax.bar(x_pos, m, bar_width, bottom=r+t, color=colors[2], label='Mining' if i==0 and j==0 else "")
        
        # Add algorithm label vertically at the base of the bar
        ax.text(x_pos, 0.15, algos[j], ha='center', va='bottom',rotation=90, fontsize=16, fontweight='normal')
# Styling for ACM Publication
# ax.set_yscale('log')
ax.set_yscale('linear')
ax.set_ylabel('Execution Time (seconds)', fontsize=18)
#ax.set_yticklabels(['1', '10', '50', '100', '500', '1000', '3000'], fontsize=20)
ax.tick_params(axis='y', labelsize=18)
# ax.set_title('Performance Breakdown: ' + dataset, fontsize=18)
ax.set_xticks(indices)
ax.set_xticklabels(ks, fontsize=18)
ax.set_xlabel('Top-K Itemsets', fontsize=18)
ax.legend(fontsize=18)
plt.grid(axis='y', which='both', linestyle='--', alpha=0.4)
# right=0.95 means the plot ends at 95% of the figure width 
# (leaving only a 5% margin)
plt.subplots_adjust(right=0.97)
plt.tight_layout()
#
# plt.savefig('fig_' + dataset + '_A.pdf', format='pdf', dpi=300)
plt.savefig('fig_' + dataset + '_A.eps', format='eps', bbox_inches='tight')




dataset="TH2FIM"
# Execution times per phase (seconds)
# Format: [HTK py, HTK_C++, HTK_PlusPlus]
reading = {
    'K=100': [71.26, 36.67, 3.93],
    'K=1000': [71.26, 36.67, 3.93],
    'K=10000': [71.26, 36.67, 3.93]
}
transform = {
    'K=100': [22.37, 0.20, 0.19],
    'K=1000': [147.73, 0.73, 0.73],
    'K=10000': [147.73, 0.73, 0.73]
}
mining = {
    'K=100': [2.55, 3.39, 2.29],
    'K=1000': [74.29, 138.00, 68.38],
    'K=10000': [3000, 1602.15, 906.84]
}
#
# Setup Plot
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.22
gap = 0.05
indices = np.arange(len(ks))
colors = ['#3498db', '#e67e22', '#2ecc71'] # Blue=Reading, Orange=Transform, Green=Mining
#
for i, k in enumerate(ks):
    for j, algo in enumerate(algos):
        # Calculate horizontal position for each bar in the group
        x_pos = i + (j - 1) * (bar_width + gap)
        
        r, t, m = reading[k][j], transform[k][j], mining[k][j]
        
        # Stacked bar logic: p2 sits on p1, p3 sits on (p1+p2)
        ax.bar(x_pos, r, bar_width, color=colors[0], label='Reading' if i==0 and j==0 else "")
        ax.bar(x_pos, t, bar_width, bottom=r, color=colors[1], label='Transform' if i==0 and j==0 else "")
        ax.bar(x_pos, m, bar_width, bottom=r+t, color=colors[2], label='Mining' if i==0 and j==0 else "")
        
        # Add algorithm label vertically at the base of the bar
        ax.text(x_pos, 0.15, algos[j], ha='center', va='bottom',rotation=90, fontsize=18, fontweight='normal')
# Styling for ACM Publication
# ax.set_yscale('log')
ax.set_yscale('linear')
ax.set_ylabel('Execution Time (seconds)', fontsize=18)
#ax.set_yticklabels(['1', '10', '50', '100', '500', '1000', '3000'], fontsize=20)
ax.tick_params(axis='y', labelsize=18)
# ax.set_title('Performance Breakdown: ' + dataset, fontsize=18)
ax.set_xticks(indices)
ax.set_xticklabels(ks, fontsize=18)
ax.set_xlabel('Top-K Itemsets', fontsize=18)
ax.legend(fontsize=18)
plt.grid(axis='y', which='both', linestyle='--', alpha=0.4)
# right=0.95 means the plot ends at 95% of the figure width 
# (leaving only a 5% margin)
plt.subplots_adjust(right=0.97)
plt.tight_layout()
#
# plt.savefig('fig_' + dataset + '_A.pdf', format='pdf', dpi=300)
plt.savefig('fig_' + dataset + '_A.eps', format='eps', bbox_inches='tight')




dataset="Susy"
# Execution times per phase (seconds)
# Format: [HTK py, HTK_C++, HTK_PlusPlus]
reading = {
    'K=100': [19.38, 9.26, 0.89],
    'K=1000': [19.38, 9.26, 0.89],
    'K=10000': [19.38, 9.26, 0.89]
}
transform = {
    'K=100': [5.18, 0.11, 0.11],
    'K=1000': [5.18, 0.11, 0.11],
    'K=10000': [5.18, 0.11, 0.11]
}
mining = {
    'K=100': [0.08, 0.10, 0.13],
    'K=1000': [1.80, 2.48, 2.42],
    'K=10000': [54.83, 63.71, 57.26]
}
#
# Setup Plot
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.22
gap = 0.05
indices = np.arange(len(ks))
colors = ['#3498db', '#e67e22', '#2ecc71'] # Blue=Reading, Orange=Transform, Green=Mining
#
for i, k in enumerate(ks):
    for j, algo in enumerate(algos):
        # Calculate horizontal position for each bar in the group
        x_pos = i + (j - 1) * (bar_width + gap)
        
        r, t, m = reading[k][j], transform[k][j], mining[k][j]
        
        # Stacked bar logic: p2 sits on p1, p3 sits on (p1+p2)
        ax.bar(x_pos, r, bar_width, color=colors[0], label='Reading' if i==0 and j==0 else "")
        ax.bar(x_pos, t, bar_width, bottom=r, color=colors[1], label='Transform' if i==0 and j==0 else "")
        ax.bar(x_pos, m, bar_width, bottom=r+t, color=colors[2], label='Mining' if i==0 and j==0 else "")
        
        # Add algorithm label vertically at the base of the bar
        ax.text(x_pos, 0.15, algos[j], ha='center', va='bottom',rotation=90, fontsize=18, fontweight='normal')
# Styling for ACM Publication
# ax.set_yscale('log')
ax.set_yscale('linear')
ax.set_ylabel('Execution Time (seconds)', fontsize=18)
#ax.set_yticklabels(['1', '10', '50', '100', '500', '1000', '3000'], fontsize=20)
ax.tick_params(axis='y', labelsize=18)
# ax.set_title('Performance Breakdown: ' + dataset, fontsize=18)
ax.set_xticks(indices)
ax.set_xticklabels(ks, fontsize=18)
ax.set_xlabel('Top-K Itemsets', fontsize=18)
ax.legend(fontsize=18)
plt.grid(axis='y', which='both', linestyle='--', alpha=0.4)
# right=0.95 means the plot ends at 95% of the figure width 
# (leaving only a 5% margin)
plt.subplots_adjust(right=0.97)
plt.tight_layout()
#
# plt.savefig('fig_' + dataset + '_A.pdf', format='pdf', dpi=300)
plt.savefig('fig_' + dataset + '_A.eps', format='eps', bbox_inches='tight')




dataset="T80I100D1M"
# Execution times per phase (seconds)
# Format: [HTK py, HTK_C++, HTK_PlusPlus]
reading = {
    'K=100': [15.55, 7.02, 0.83],
    'K=1000': [15.55, 7.02, 0.83],
    'K=10000': [15.55, 7.02, 0.83]
}
transform = {
    'K=100': [2.77, 0.10, 0.10],
    'K=1000': [2.77, 0.10, 0.10],
    'K=10000': [3.00, 0.10, 0.10]
}
mining = {
    'K=100': [0.14, 0.22, 0.25],
    'K=1000': [0.85, 1.21, 1.26],
    'K=10000': [13.59, 11.84, 12.35]
}
#
# Setup Plot
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.22
gap = 0.05
indices = np.arange(len(ks))
colors = ['#3498db', '#e67e22', '#2ecc71'] # Blue=Reading, Orange=Transform, Green=Mining
#
for i, k in enumerate(ks):
    for j, algo in enumerate(algos):
        # Calculate horizontal position for each bar in the group
        x_pos = i + (j - 1) * (bar_width + gap)
        
        r, t, m = reading[k][j], transform[k][j], mining[k][j]
        r, t, m = reading[k][j], transform[k][j], mining[k][j]
        
        # Stacked bar logic: p2 sits on p1, p3 sits on (p1+p2)
        ax.bar(x_pos, r, bar_width, color=colors[0], label='Reading' if i==0 and j==0 else "")
        ax.bar(x_pos, t, bar_width, bottom=r, color=colors[1], label='Transform' if i==0 and j==0 else "")
        ax.bar(x_pos, m, bar_width, bottom=r+t, color=colors[2], label='Mining' if i==0 and j==0 else "")
        
        # Add algorithm label vertically at the base of the bar
        ax.text(x_pos, 0.15, algos[j], ha='center', va='bottom',rotation=90, fontsize=18, fontweight='normal')
# Styling for ACM Publication
# ax.set_yscale('log')
ax.set_yscale('linear')
ax.set_ylabel('Execution Time (seconds)', fontsize=18)
#ax.set_yticklabels(['1', '10', '50', '100', '500', '1000', '3000'], fontsize=20)
ax.tick_params(axis='y', labelsize=18)
# ax.set_title('Performance Breakdown: ' + dataset, fontsize=18)
ax.set_xticks(indices)
ax.set_xticklabels(ks, fontsize=18)
ax.set_xlabel('Top-K Itemsets', fontsize=18)
ax.legend(fontsize=18)
plt.grid(axis='y', which='both', linestyle='--', alpha=0.4)
# right=0.95 means the plot ends at 95% of the figure width 
# (leaving only a 5% margin)
plt.subplots_adjust(right=0.97)
plt.tight_layout()
#
# plt.savefig('fig_' + dataset + '_A.pdf', format='pdf', dpi=300)
plt.savefig('fig_' + dataset + '_A.eps', format='eps', bbox_inches='tight')


plt.show()