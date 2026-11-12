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
    'K=100': [138.22, 78.06, 27.80],
    'K=1000': [138.22, 78.06, 27.80],
    'K=10000': [138.22, 78.06, 27.80]
}
transform = {
    'K=100': [2.76, 0.25, 0.25],
    'K=1000': [10.45, 0.25, 0.42],
    'K=10000': [29.86, 0.50, 1.62]
}
mining = {
    'K=100': [0.19, 2.34, 3.84],
    'K=1000': [1.57, 9.25, 4.36],
    'K=10000': [37.50, 117.14, 13.11]
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
    'K=100': [71.26, 35.67, 3.82],
    'K=1000': [71.26, 35.67, 3.82],
    'K=10000': [71.26, 35.67, 3.82]
}
transform = {
    'K=100': [22.37, 0.17, 0.17],
    'K=1000': [147.73, 0.65, 0.66],
    'K=10000': [148.01, 0.64, 0.66]
}
mining = {
    'K=100': [2.55, 2.15, 0.91],
    'K=1000': [74.29, 54.93, 24.05],
    'K=10000': [3000, 973.87, 439.63]
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
    'K=100': [19.04, 9.10, 0.89],
    'K=1000': [19.04, 9.10, 0.89],
    'K=10000': [19.04, 9.10, 0.89]
}
transform = {
    'K=100': [5.18, 0.10, 0.10],
    'K=1000': [5.18, 0.10, 0.11],
    'K=10000': [5.18, 0.11, 0.11]
}
mining = {
    'K=100': [0.08, 0.07, 0.09],
    'K=1000': [1.80, 1.33, 1.32],
    'K=10000': [54.83, 31.79, 31.07]
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
    'K=100': [15.55, 6.99, 0.81],
    'K=1000': [15.55, 6.99, 0.81],
    'K=10000': [15.55, 6.99, 0.81]
}
transform = {
    'K=100': [2.77, 0.10, 0.10],
    'K=1000': [2.77, 0.10, 0.10],
    'K=10000': [3.00, 0.10, 0.10]
}
mining = {
    'K=100': [0.14, 0.08, 0.08],
    'K=1000': [0.85, 0.47, 0.43],
    'K=10000': [13.59, 4.76, 4.38]
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