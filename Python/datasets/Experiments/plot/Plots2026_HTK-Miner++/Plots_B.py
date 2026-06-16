import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42


dataset="webdocs"
plt.figure(dataset)
# plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-K (minSup)", fontsize=18)
# plt.ylim(0,150)
plt.xscale('log')
x = [100, 1000, 10000]
x_labels = ["$10^2$\n(0.327)", "$10^3$\n(0.216)", "$10^4$\n(0.150)"]
plt.xticks(ticks=x, labels=x_labels, fontsize=18)
#
plt.yticks(fontsize=18) 
plt.ylabel("Time (sec)", fontsize=18)
y = [31, 33, 44]
plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner++", color='blue')
# y = [31, 33, 44]
# plt.plot(x, y, marker='H', linestyle='-', label="negFIN", color='red')
y = [32, 34, 45]
plt.plot(x, y, marker='X', linestyle='-', label="FP-growth",   color='purple')
y = [30, 38, 48]
plt.plot(x, y, marker='*', linestyle='-', label="Eclat", color='orange')
#
# plt.legend(fontsize=18) #legends inside
# Τοποθέτηση λεζάντας πάνω από το γράφημα (outside)
plt.legend(fontsize=18, loc='lower center', bbox_to_anchor=(0.5, 0.95),  ncol=2, fancybox=False, shadow=False, frameon=False)
# Προσαρμογή του πάνω μέρους του γραφήματος για να χωρέσει η λεζάντα
plt.subplots_adjust(top=0.85)
#
plt.tight_layout()
plt.grid(True)
#
# plt.savefig("fig_" + dataset + "_B.pdf", format="pdf", dpi=300)  # High-quality output
plt.savefig('fig_' + dataset + '_B.eps', format='eps', bbox_inches='tight')



dataset="TH2FIM"
plt.figure(dataset)
# plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-K (minSup)", fontsize=18)
plt.ylim(0,1000)
plt.xscale('log')
x = [100, 1000, 10000]
x_labels = ["$10^2$\n(0.040)", "$10^3$\n(0.013)", "$10^4$\n(0.005)"]
plt.xticks(ticks=x, labels=x_labels, fontsize=18)

plt.yticks(fontsize=18) 
plt.ylabel("Time (sec)", fontsize=18)
y = [6, 68, 911]
plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner++", color='blue')
y = [94, None, None]
plt.plot(x, y, marker='H', linestyle='-', label="negFIN", color='red')
y = [31, 72, 128]
plt.plot(x, y, marker='X', linestyle='-', label="FP-growth",   color='purple')
y = [40, 77, 150]
plt.plot(x, y, marker='*', linestyle='-', label="Eclat", color='orange')

# plt.legend(fontsize=18) #legends inside
# Τοποθέτηση λεζάντας πάνω από το γράφημα (outside)
plt.legend(fontsize=18, loc='lower center', bbox_to_anchor=(0.5, 0.95),  ncol=2, fancybox=False, shadow=False, frameon=False)
# Προσαρμογή του πάνω μέρους του γραφήματος για να χωρέσει η λεζάντα
plt.subplots_adjust(top=0.85)

plt.tight_layout()
plt.grid(True)
#
# plt.savefig("fig_" + dataset + "_B.pdf", format="pdf", dpi=300)  # High-quality output
plt.savefig('fig_' + dataset + '_B.eps', format='eps', bbox_inches='tight')





dataset="Susy"
plt.figure(dataset)
# plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-K (minSup)", fontsize=18)
# plt.ylim(0,1000)
plt.xscale('log')
x = [100, 1000, 10000]
x_labels = ["$10^2$\n(0.870)", "$10^3$\n(0.729)", "$10^4$\n(0.151)"]
plt.xticks(ticks=x, labels=x_labels, fontsize=18)

plt.yticks(fontsize=18) 
plt.ylabel("Time (sec)", fontsize=18)
y = [1, 3.4, 58]
plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner++", color='blue')
y = [5.5, 6, 7]
plt.plot(x, y, marker='H', linestyle='-', label="negFIN", color='red')
y = [5.8, 6, 7]
plt.plot(x, y, marker='X', linestyle='-', label="FP-growth",   color='purple')
y = [5.7, 5.9, 7.2]
plt.plot(x, y, marker='*', linestyle='-', label="Eclat", color='orange')

# plt.legend(fontsize=18) #legends inside
# Τοποθέτηση λεζάντας πάνω από το γράφημα (outside)
plt.legend(fontsize=18, loc='lower center', bbox_to_anchor=(0.5, 0.95),  ncol=2, fancybox=False, shadow=False, frameon=False)
# Προσαρμογή του πάνω μέρους του γραφήματος για να χωρέσει η λεζάντα
plt.subplots_adjust(top=0.85)

plt.tight_layout()
plt.grid(True)
#
# plt.savefig("fig_" + dataset + "_B.pdf", format="pdf", dpi=300)  # High-quality output
plt.savefig('fig_' + dataset + '_B.eps', format='eps', bbox_inches='tight')



dataset="T80I100D1M"
plt.figure(dataset)
# plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-K (minSup)", fontsize=18)
# plt.ylim(0,1000)
plt.xscale('log')
x = [100, 1000, 10000]
x_labels = ["$10^2$\n(0.798)", "$10^3$\n(0.642)", "$10^4$\n(0.518)"]
plt.xticks(ticks=x, labels=x_labels, fontsize=18)

plt.yticks(fontsize=18) 
plt.ylabel("Time (sec)", fontsize=18)
y = [1, 2, 13]
plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner++", color='blue')
y = [119, 125, 921]
plt.plot(x, y, marker='H', linestyle='-', label="negFIN", color='red')
y = [29, 49, None]
plt.plot(x, y, marker='X', linestyle='-', label="FP-growth",   color='purple')
y = [16, 34, 571]
plt.plot(x, y, marker='*', linestyle='-', label="Eclat", color='orange')

# plt.legend(fontsize=18) #legends inside
# Τοποθέτηση λεζάντας πάνω από το γράφημα (outside)
plt.legend(fontsize=18, loc='lower center', bbox_to_anchor=(0.5, 0.95),  ncol=2, fancybox=False, shadow=False, frameon=False)
# Προσαρμογή του πάνω μέρους του γραφήματος για να χωρέσει η λεζάντα
plt.subplots_adjust(top=0.85)

plt.tight_layout()
plt.grid(True)
#
# plt.savefig("fig_" + dataset + "_B.pdf", format="pdf", dpi=300)  # High-quality output
plt.savefig('fig_' + dataset + '_B.eps', format='eps', bbox_inches='tight')



plt.show()


