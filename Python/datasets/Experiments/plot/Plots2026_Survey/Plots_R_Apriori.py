import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42


dataset="kosarak"
plt.figure(dataset)
# plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-K (minSup)", fontsize=18)
plt.ylim(0,140)
plt.xscale('log')
x = [100, 1000, 10000]
x_labels = ["$10^2$\n(0.023)", "$10^3$\n(0.006)", "$10^4$\n(0.002)"]
plt.xticks(ticks=x, labels=x_labels, fontsize=18)
#
plt.yticks(fontsize=18) 
plt.ylabel("Time (sec)", fontsize=18)
plt.plot(100, 135, marker='x', color='skyblue', markersize=10, zorder=5)
# Dummy plot just to populate the legend correctly
plt.plot([], [], marker='D', linestyle='-', label="Apriori Py mlxtend", color='skyblue')
y = [8, 21, 83]
plt.plot(x, y, marker='H', linestyle='-', label="Apriori Py Pami", color='steelblue')
y = [34, 47, 93]
plt.plot(x, y, marker='*', linestyle='-', label="AprioriTID Py Pami", markersize='8', color='blue')
y = [4, 20, 122]
plt.plot(x, y, marker='>', linestyle='-', label="AprioriTID Java SPMF", color='gray')
y = [4, 5, None]

# Plot the successful segment first (100 to 1000)
plt.plot(x[:2], [4, 5], marker='s', linestyle='-', label="AprioriTID bitset Java SPMF", color='black')
# Place the red 'X' at the end of the trendline
plt.plot(1000, 5, marker='x', color='black', markersize=10, zorder=5)

y = [1.1, 1.13, 1.81]
plt.plot(x, y, marker='p', linestyle='-', label="Apriori C++ Borgelt", color='red')
#
# plt.legend(fontsize=18) #legends inside
# Τοποθέτηση λεζάντας πάνω από το γράφημα (outside)
plt.legend(fontsize=14, loc='lower center', bbox_to_anchor=(0.5, 1),  ncol=2, fancybox=False, shadow=False, frameon=False)
# Προσαρμογή του πάνω μέρους του γραφήματος για να χωρέσει η λεζάντα
plt.subplots_adjust(top=0.85)
#
plt.tight_layout()
plt.grid(True)
#
plt.savefig('fig_R_' + dataset + '.pdf', format='pdf', bbox_inches='tight')
# plt.savefig('fig_R_' + dataset + '_B.eps', format='eps', bbox_inches='tight')




# dataset = "kosarak"
# plt.figure(dataset)
# plt.xlabel("Top-K (minSup)", fontsize=18)
# plt.ylim(0, 150)
# plt.xscale('log')

# x = [100, 1000, 10000]
# x_labels = ["$10^2$\n(0.023)", "$10^3$\n(0.006)", "$10^4$\n(0.002)"]
# plt.xticks(ticks=x, labels=x_labels, fontsize=18)
# plt.yticks(fontsize=18) 
# plt.ylabel("Time (sec)", fontsize=18)

# # --- 1. Apriori Py mlxtend (y = [990, None, None]) ---
# # Since the first value (990) is already way past 150, we place a red 'X' 
# # at the very first point on the ceiling to show it instantly timed out/failed.
# plt.plot(100, 145, marker='X', color='red', markersize=10, zorder=5)
# # Dummy plot just to populate the legend correctly
# plt.plot([], [], marker='D', linestyle='-', label="Apriori Py mlxtend", color='skyblue')

# # --- 2. Standard Successful Runs ---
# y = [8, 21, 83]
# plt.plot(x, y, marker='H', linestyle='-', label="Apriori Py Pami", color='steelblue')

# y = [34, 47, 93]
# plt.plot(x, y, marker='1', linestyle='-', label="AprioriTID Py Pami", color='blue')

# y = [4, 20, 122]
# plt.plot(x, y, marker='2', linestyle='-', label="AprioriTID Java SPMF", color='gray')

# # --- 3. AprioriTID bitset Java SPMF (y = [4, 5, None]) ---
# # Plot the successful segment first (100 to 1000)
# plt.plot(x[:2], [4, 5], marker='3', linestyle='-', label="AprioriTID bitset Java SPMF", color='black')
# # Draw a dashed trendline up to the ceiling (y=145) to show the trajectory of failure
# plt.plot([1000, 10000], [5, 145], linestyle='--', color='black', alpha=0.7)
# # Place the red 'X' at the end of the trendline
# plt.plot(10000, 145, marker='X', color='red', markersize=10, zorder=5)

# # --- 4. Apriori C++ Borgelt ---
# y = [1.1, 1.13, 1.81]
# plt.plot(x, y, marker='4', linestyle='-', label="Apriori C++ Borgelt", color='red')

# # --- Layout & Legend Formatting ---
# plt.legend(fontsize=14, loc='lower center', bbox_to_anchor=(0.5, 0.95), ncol=2, fancybox=False, shadow=False, frameon=False)
# plt.subplots_adjust(top=0.85)

# plt.tight_layout()
# plt.grid(True, linestyle=':', alpha=0.6)

# # Save and Show
# plt.savefig('fig_' + dataset + '_B.pdf', format='pdf', bbox_inches='tight')




plt.show()