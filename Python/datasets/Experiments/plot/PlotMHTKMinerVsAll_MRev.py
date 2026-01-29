import matplotlib.pyplot as plt

diagram="MemoryAll"



dataset="Kosarak"
plt.figure(dataset + diagram)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,150)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Memory consuption in MB", fontsize=22)
x = [100, 1000, 10007]

y = [74, 215, 2500]
plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner")
y = [435, None, None]
plt.plot(x, y, marker='H', linestyle='-', label="HTK-negFIN")
y = [2500, None, None]
plt.plot(x, y, marker='X', linestyle='-', label="BTK")
y = [20, 238, 760]
plt.plot(x, y, marker='*', linestyle='-', label="negFIN (minSup)")


# plt.legend(fontsize=20) #legends inside
# Τοποθέτηση λεζάντας πάνω από το γράφημα (outside)
plt.legend(fontsize=18, loc='lower center', bbox_to_anchor=(0.5, 0.95),  ncol=2, fancybox=False, shadow=False, frameon=False)
# Προσαρμογή του πάνω μέρους του γραφήματος για να χωρέσει η λεζάντα
plt.subplots_adjust(top=0.85)

plt.tight_layout()
plt.grid(True)
# plt.savefig(dataset + diagram + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + diagram + ".pdf", format="pdf", dpi=300)  # High-quality output



dataset = "Accidents"
plt.figure(dataset + diagram)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,150)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Memory consuption in MB", fontsize=22)
x = [100, 1000, 10007]

y = [28, 77, 603]
plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner")
y = [3800, None, None]
plt.plot(x, y, marker='H', linestyle='-', label="HTK-negFIN")
y = [2600, None, None]
plt.plot(x, y, marker='X', linestyle='-', label="BTK")
y = [7, 12, 79]
plt.plot(x, y, marker='*', linestyle='-', label="negFIN (minSup)")

# plt.legend(fontsize=20) #legends inside
# Τοποθέτηση λεζάντας πάνω από το γράφημα (outside)
plt.legend(fontsize=18, loc='lower center', bbox_to_anchor=(0.5, 0.95),  ncol=2, fancybox=False, shadow=False, frameon=False)
# Προσαρμογή του πάνω μέρους του γραφήματος για να χωρέσει η λεζάντα
plt.subplots_adjust(top=0.85)

plt.tight_layout()
plt.grid(True)
# plt.savefig(dataset + diagram + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + diagram + ".pdf", format="pdf", dpi=300)  # High-quality output



dataset = "Chess"
plt.figure(dataset + diagram)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,150)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Memory consuption in MB", fontsize=22)
x = [100, 1000, 10007]

y = [11, 13, 26]
plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner")
y = [54, 56, 105]
plt.plot(x, y, marker='H', linestyle='-', label="HTK-negFIN")
y = [38, 38, 43]
plt.plot(x, y, marker='X', linestyle='-', label="BTK")
y = [7, 8, 9]
plt.plot(x, y, marker='*', linestyle='-', label="negFIN (minSup)")

# plt.legend(fontsize=20) #legends inside
# Τοποθέτηση λεζάντας πάνω από το γράφημα (outside)
plt.legend(fontsize=18, loc='lower center', bbox_to_anchor=(0.5, 0.95),  ncol=2, fancybox=False, shadow=False, frameon=False)
# Προσαρμογή του πάνω μέρους του γραφήματος για να χωρέσει η λεζάντα
plt.subplots_adjust(top=0.85)

plt.tight_layout()
plt.grid(True)
# plt.savefig(dataset + diagram + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + diagram + ".pdf", format="pdf", dpi=300)  # High-quality output



dataset="Connect"
plt.figure(dataset + diagram)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,150)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Memory consuption in MB", fontsize=22)
x = [100, 1000, 10007]

y = [15, 23, 113]
plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner")
y = [1050, None, None]
plt.plot(x, y, marker='H', linestyle='-', label="HTK-negFIN")
y = [456, 456, None]
plt.plot(x, y, marker='X', linestyle='-', label="BTK")
y = [7, 7, 9]
plt.plot(x, y, marker='*', linestyle='-', label="negFIN (minSup)")

# plt.legend(fontsize=20) #legends inside
# Τοποθέτηση λεζάντας πάνω από το γράφημα (outside)
plt.legend(fontsize=18, loc='lower center', bbox_to_anchor=(0.5, 0.95),  ncol=2, fancybox=False, shadow=False, frameon=False)
# Προσαρμογή του πάνω μέρους του γραφήματος για να χωρέσει η λεζάντα
plt.subplots_adjust(top=0.85)

plt.tight_layout()
plt.grid(True)
# plt.savefig(dataset + diagram + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + diagram + ".pdf", format="pdf", dpi=300)  # High-quality output



dataset="Mushroom"
plt.figure(dataset + diagram)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,150)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Memory consuption in MB", fontsize=22)
x = [100, 1000, 10007]

y = [11, 13, 30]
plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner")
y = [63, 74, 219]
plt.plot(x, y, marker='H', linestyle='-', label="HTK-negFIN")
y = [39, 40, 42]
plt.plot(x, y, marker='X', linestyle='-', label="BTK")
y = [7, 8, 10]
plt.plot(x, y, marker='*', linestyle='-', label="negFIN (minSup)")

# plt.legend(fontsize=20) #legends inside
# Τοποθέτηση λεζάντας πάνω από το γράφημα (outside)
plt.legend(fontsize=18, loc='lower center', bbox_to_anchor=(0.5, 0.95),  ncol=2, fancybox=False, shadow=False, frameon=False)
# Προσαρμογή του πάνω μέρους του γραφήματος για να χωρέσει η λεζάντα
plt.subplots_adjust(top=0.85)

plt.tight_layout()
plt.grid(True)
# plt.savefig(dataset + diagram + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + diagram + ".pdf", format="pdf", dpi=300)  # High-quality output



dataset="pumsb"
plt.figure(dataset + diagram)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,150)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Memory consuption in MB", fontsize=22)
x = [100, 1000, 10007]

y = [14, 22, 105]
plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner")
y = [508, None, None]
plt.plot(x, y, marker='H', linestyle='-', label="HTK-negFIN")
y = [742, 742, None]
plt.plot(x, y, marker='X', linestyle='-', label="BTK")
y = [8, 8, 28]
plt.plot(x, y, marker='*', linestyle='-', label="negFIN (minSup)")

# plt.legend(fontsize=20) #legends inside
# Τοποθέτηση λεζάντας πάνω από το γράφημα (outside)
plt.legend(fontsize=18, loc='lower center', bbox_to_anchor=(0.5, 0.95),  ncol=2, fancybox=False, shadow=False, frameon=False)
# Προσαρμογή του πάνω μέρους του γραφήματος για να χωρέσει η λεζάντα
plt.subplots_adjust(top=0.85)

plt.tight_layout()
plt.grid(True)
# plt.savefig(dataset + diagram + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + diagram + ".pdf", format="pdf", dpi=300)  # High-quality output



dataset="T40I10D100K"
plt.figure(dataset + diagram)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,150)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Memory consuption in MB", fontsize=22)
x = [100, 1000, 10007]

y = [17, 29, 257]
plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner")
y = [407, 2035, None]
plt.plot(x, y, marker='H', linestyle='-', label="HTK-negFIN")
y = [1557, 1558, None]
plt.plot(x, y, marker='X', linestyle='-', label="BTK")
y = [358, 1428, 1658]
plt.plot(x, y, marker='*', linestyle='-', label="negFIN (minSup)")

# plt.legend(fontsize=20) #legends inside
# Τοποθέτηση λεζάντας πάνω από το γράφημα (outside)
plt.legend(fontsize=18, loc='lower center', bbox_to_anchor=(0.5, 0.95),  ncol=2, fancybox=False, shadow=False, frameon=False)
# Προσαρμογή του πάνω μέρους του γραφήματος για να χωρέσει η λεζάντα
plt.subplots_adjust(top=0.85)

plt.tight_layout()
plt.grid(True)
# plt.savefig(dataset + diagram + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + diagram + ".pdf", format="pdf", dpi=300)  # High-quality output



dataset="L-0023"
plt.figure(dataset + diagram)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,150)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Memory consuption in MB", fontsize=22)
x = [100, 1000, 10007]

y = [11, 13, 28]
plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner")
y = [14, 38, None]
plt.plot(x, y, marker='H', linestyle='-', label="HTK-negFIN")
y = [37, 39, 60]
plt.plot(x, y, marker='X', linestyle='-', label="BTK")
y = [12, 24, 36]
plt.plot(x, y, marker='*', linestyle='-', label="negFIN (minSup)")

# plt.legend(fontsize=20) #legends inside
# Τοποθέτηση λεζάντας πάνω από το γράφημα (outside)
plt.legend(fontsize=18, loc='lower center', bbox_to_anchor=(0.5, 0.95),  ncol=2, fancybox=False, shadow=False, frameon=False)
# Προσαρμογή του πάνω μέρους του γραφήματος για να χωρέσει η λεζάντα
plt.subplots_adjust(top=0.85)

plt.tight_layout()
plt.grid(True)
# plt.savefig(dataset + diagram + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + diagram + ".pdf", format="pdf", dpi=300)  # High-quality output



dataset="T16IT20D100K"
plt.figure(dataset + diagram)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,150)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Memory consuption in MB", fontsize=22)
x = [100, 1000, 10007]

y = [14, 26, 84]
plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner")
y = [52, 54, 65]
plt.plot(x, y, marker='H', linestyle='-', label="HTK-negFIN")
y = [202, 222, None]
plt.plot(x, y, marker='X', linestyle='-', label="BTK")
y = [49, 50, 51]
plt.plot(x, y, marker='*', linestyle='-', label="negFIN (minSup)")

# plt.legend(fontsize=20) #legends inside
# Τοποθέτηση λεζάντας πάνω από το γράφημα (outside)
plt.legend(fontsize=18, loc='lower center', bbox_to_anchor=(0.5, 0.95),  ncol=2, fancybox=False, shadow=False, frameon=False)
# Προσαρμογή του πάνω μέρους του γραφήματος για να χωρέσει η λεζάντα
plt.subplots_adjust(top=0.85)

plt.tight_layout()
plt.grid(True)
# plt.savefig(dataset + diagram + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + diagram + ".pdf", format="pdf", dpi=300)  # High-quality output



dataset="Webdocs"
plt.figure(dataset + diagram)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,150)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Memory consuption in MB", fontsize=22)
x = [100, 1000, 10007]

y = [1500, 1800, 5100]
plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner")
y = [10900, None, None]
plt.plot(x, y, marker='H', linestyle='-', label="HTK-negFIN")
y = [11000, None, None]
plt.plot(x, y, marker='X', linestyle='-', label="BTK")
y = [370, 2957, 10353]
plt.plot(x, y, marker='*', linestyle='-', label="negFIN (minSup)")

# plt.legend(fontsize=20) #legends inside
# Τοποθέτηση λεζάντας πάνω από το γράφημα (outside)
plt.legend(fontsize=18, loc='lower center', bbox_to_anchor=(0.5, 0.95),  ncol=2, fancybox=False, shadow=False, frameon=False)
# Προσαρμογή του πάνω μέρους του γραφήματος για να χωρέσει η λεζάντα
plt.subplots_adjust(top=0.85)

plt.tight_layout()
plt.grid(True)
# plt.savefig(dataset + diagram + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + diagram + ".pdf", format="pdf", dpi=300)  # High-quality output


plt.show()


