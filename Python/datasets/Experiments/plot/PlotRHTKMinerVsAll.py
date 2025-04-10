import matplotlib.pyplot as plt

diagram="RuntimeAll"



dataset="Kosarak"
plt.figure(dataset + diagram)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
plt.ylim(0,150)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Time (sec)", fontsize=22)
x = [100, 1000, 10007]

y = [11, 17, 125]
plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner")
y = [57, 600, 1000]
plt.plot(x, y, marker='H', linestyle='-', label="HTK-negFIN")
y = [148, 1000, 1000]
plt.plot(x, y, marker='X', linestyle='-', label="BTK")
# y = [24, 1200, 1000]
# plt.plot(x, y, marker='v', linestyle='-', label="SPMF Apriori TopK")
# y = [3, 10, 1000]
# plt.plot(x, y, marker='o', linestyle='-', label="SPMF Fpgrowth TopK")
y = [5, 11, 58]
plt.plot(x, y, marker='*', linestyle='-', label="negFIN (minSup)")

plt.legend(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.savefig(dataset + diagram + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + diagram + ".pdf", format="pdf", dpi=300)  # High-quality output



# dataset = "Accidents"
# plt.figure(dataset + diagram)
# plt.rcParams["font.family"] = "Times New Roman"
# plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,300)
# plt.xscale('log')
# plt.xticks(fontsize=22) 
# plt.yticks(fontsize=22) 
# plt.ylabel("Time (sec)", fontsize=22)
# x = [100, 1000, 10007]

# y = [9, 10, 17]
# plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner")
# y = [290, 1000, 1000]
# plt.plot(x, y, marker='H', linestyle='-', label="HTK-negFIN")
# y = [243, 1000, 1000]
# plt.plot(x, y, marker='X', linestyle='-', label="BTK")
# # y = [49, 1000, 1000]
# # plt.plot(x, y, marker='v', linestyle='-', label="SPMF Apriori TopK")
# # y = [9, 1000, 1000]
# # plt.plot(x, y, marker='o', linestyle='-', label="SPMF Fpgrowth TopK")
# y = [4, 5, 6]
# plt.plot(x, y, marker='*', linestyle='-', label="negFIN (minSup)")

# # plt.legend(fontsize=20)
# plt.tight_layout()
# plt.grid(True)
# plt.savefig(dataset + diagram + ".svg", format="svg", dpi=300)  # High-quality output
# plt.savefig(dataset + diagram + ".pdf", format="pdf", dpi=300)  # High-quality output



# dataset = "Chess"
# plt.figure(dataset + diagram)
# plt.rcParams["font.family"] = "Times New Roman"
# plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,100)
# plt.xscale('log')
# plt.xticks(fontsize=22) 
# plt.yticks(fontsize=22) 
# plt.ylabel("Time (sec)", fontsize=22)
# x = [100, 1000, 10007]

# y = [0.2, 0.3, 5]
# plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner")
# y = [1.1, 8, 43]
# plt.plot(x, y, marker='H', linestyle='-', label="HTK-negFIN")
# y = [0.6, 4.2, 354]
# plt.plot(x, y, marker='X', linestyle='-', label="BTK")
# # y = [0.5, 4.5, 36]
# # plt.plot(x, y, marker='v', linestyle='-', label="SPMF Apriori TopK")
# # y = [297, 1000, 1000]
# # plt.plot(x, y, marker='o', linestyle='-', label="SPMF Fpgrowth TopK")
# y = [0.04, 0.05, 0.06]
# plt.plot(x, y, marker='*', linestyle='-', label="negFIN (minSup)")

# # plt.legend(fontsize=20)
# plt.tight_layout()
# plt.grid(True)
# plt.savefig(dataset + diagram + ".svg", format="svg", dpi=300)  # High-quality output
# plt.savefig(dataset + diagram + ".pdf", format="pdf", dpi=300)  # High-quality output



# dataset="Connect"
# plt.figure(dataset + diagram)
# plt.rcParams["font.family"] = "Times New Roman"
# plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,100)
# plt.xscale('log')
# plt.xticks(fontsize=22) 
# plt.yticks(fontsize=22) 
# plt.ylabel("Time (sec)", fontsize=22)
# x = [100, 1000, 10007]

# y = [1.2, 1.3, 6.9]
# plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner")
# y = [73, 800, 1000]
# plt.plot(x, y, marker='H', linestyle='-', label="HTK-negFIN")
# y = [20, 34, 1000]
# plt.plot(x, y, marker='X', linestyle='-', label="BTK")
# # y = [17, 130, 1000]
# # plt.plot(x, y, marker='v', linestyle='-', label="SPMF Apriori TopK")
# # y = [4.1, 1000, 1000]
# # plt.plot(x, y, marker='o', linestyle='-', label="SPMF Fpgrowth TopK")
# y = [0.9, 1, 1.1]
# plt.plot(x, y, marker='*', linestyle='-', label="negFIN (minSup)")

# # plt.legend(fontsize=20)
# plt.tight_layout()
# plt.grid(True)
# plt.savefig(dataset + diagram + ".svg", format="svg", dpi=300)  # High-quality output
# plt.savefig(dataset + diagram + ".pdf", format="pdf", dpi=300)  # High-quality output



# dataset="Mushroom"
# plt.figure(dataset + diagram)
# plt.rcParams["font.family"] = "Times New Roman"
# plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# #plt.ylim(0,300)
# plt.xscale('log')
# plt.xticks(fontsize=22) 
# plt.yticks(fontsize=22) 
# plt.ylabel("Time (sec)", fontsize=22)
# x = [100, 1000, 10007]

# y = [0.3, 0.4, 6]
# plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner")
# y = [2.8, 23, 64]
# plt.plot(x, y, marker='H', linestyle='-', label="HTK-negFIN")
# y = [0.6, 1.2, 43]
# plt.plot(x, y, marker='X', linestyle='-', label="BTK")
# # y = [1, 6, 34]
# # plt.plot(x, y, marker='v', linestyle='-', label="SPMF Apriori TopK")
# # y = [1, 3, 4]
# # plt.plot(x, y, marker='o', linestyle='-', label="SPMF Fpgrowth TopK")
# y = [0.1, 0.1, 0.2]
# plt.plot(x, y, marker='*', linestyle='-', label="negFIN (minSup)")

# # plt.legend(fontsize=20)
# plt.tight_layout()
# plt.grid(True)
# plt.savefig(dataset + diagram + ".svg", format="svg", dpi=300)  # High-quality output
# plt.savefig(dataset + diagram + ".pdf", format="pdf", dpi=300)  # High-quality output



# dataset="pumsb"
# plt.figure(dataset + diagram)
# plt.rcParams["font.family"] = "Times New Roman"
# plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,300)
# plt.xscale('log')
# plt.xticks(fontsize=22) 
# plt.yticks(fontsize=22) 
# plt.ylabel("Time (sec)", fontsize=22)
# x = [100, 1000, 10007]

# y = [1.3, 1.7, 7.2]
# plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner")
# y = [24, 800, 1000]
# plt.plot(x, y, marker='H', linestyle='-', label="HTK-negFIN")
# y = [206, 271, 1000]
# plt.plot(x, y, marker='X', linestyle='-', label="BTK")
# # y = [20, 1000, 1000]
# # plt.plot(x, y, marker='v', linestyle='-', label="SPMF Apriori TopK")
# # y = [297, 1000, 1000]
# # plt.plot(x, y, marker='o', linestyle='-', label="SPMF Fpgrowth TopK")
# y = [1.2, 1.3, 1.4]
# plt.plot(x, y, marker='*', linestyle='-', label="negFIN (minSup)")

# # plt.legend(fontsize=20)
# plt.tight_layout()
# plt.grid(True)
# plt.savefig(dataset + diagram + ".svg", format="svg", dpi=300)  # High-quality output
# plt.savefig(dataset + diagram + ".pdf", format="pdf", dpi=300)  # High-quality output



# dataset="T40I10D100K"
# plt.figure(dataset + diagram)
# plt.rcParams["font.family"] = "Times New Roman"
# plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,300)
# plt.xscale('log')
# plt.xticks(fontsize=22) 
# plt.yticks(fontsize=22) 
# plt.ylabel("Time (sec)", fontsize=22)
# x = [100, 1000, 10007]

# y = [1.4, 3, 15]
# plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner")
# y = [15, 750, 7000]
# plt.plot(x, y, marker='H', linestyle='-', label="HTK-negFIN")
# y = [63, 575, 5000]
# plt.plot(x, y, marker='X', linestyle='-', label="BTK")
# # y = [8, 945, 9000]
# # plt.plot(x, y, marker='v', linestyle='-', label="SPMF Apriori TopK")
# # y = [2, 1000, 1000]
# # plt.plot(x, y, marker='o', linestyle='-', label="SPMF Fpgrowth TopK")
# y = [10.5, 101, 211]
# plt.plot(x, y, marker='*', linestyle='-', label="negFIN (minSup)")

# # plt.legend(fontsize=20)
# plt.tight_layout()
# plt.grid(True)
# plt.savefig(dataset + diagram + ".svg", format="svg", dpi=300)  # High-quality output
# plt.savefig(dataset + diagram + ".pdf", format="pdf", dpi=300)  # High-quality output



# dataset="L-0023"
# plt.figure(dataset + diagram)
# plt.rcParams["font.family"] = "Times New Roman"
# plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,150)
# plt.xscale('log')
# plt.xticks(fontsize=22) 
# plt.yticks(fontsize=22) 
# plt.ylabel("Time (sec)", fontsize=22)
# x = [100, 1000, 10007]

# y = [0.3, 0.5, 6.2]
# plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner")
# y = [0.2, 4, 1000]
# plt.plot(x, y, marker='H', linestyle='-', label="HTK-negFIN")
# y = [9, 13, 158]
# plt.plot(x, y, marker='X', linestyle='-', label="BTK")
# # y = [296, 1000, 1000]
# # plt.plot(x, y, marker='v', linestyle='-', label="SPMF Apriori TopK")
# # y = [292, 1000, 1000]
# # plt.plot(x, y, marker='o', linestyle='-', label="SPMF Fpgrowth TopK")
# y = [0.1, 0.8, 2]
# plt.plot(x, y, marker='*', linestyle='-', label="negFIN (minSup)")

# # plt.legend(fontsize=20)
# plt.tight_layout()
# plt.grid(True)
# plt.savefig(dataset + diagram + ".svg", format="svg", dpi=300)  # High-quality output
# plt.savefig(dataset + diagram + ".pdf", format="pdf", dpi=300)  # High-quality output



# dataset="T16IT20D100K"
# plt.figure(dataset + diagram)
# plt.rcParams["font.family"] = "Times New Roman"
# plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,50)
# plt.xscale('log')
# plt.xticks(fontsize=22) 
# plt.yticks(fontsize=22) 
# plt.ylabel("Time (sec)", fontsize=22)
# x = [100, 1000, 10007]

# y = [0.9, 1, 6]
# plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner")
# y = [3, 12, 35]
# plt.plot(x, y, marker='H', linestyle='-', label="HTK-negFIN")
# y = [7, 23, 1000]
# plt.plot(x, y, marker='X', linestyle='-', label="BTK")
# # y = [1, 3, 15]
# # plt.plot(x, y, marker='v', linestyle='-', label="SPMF Apriori TopK")
# # y = [1, 1.4, 2]
# # plt.plot(x, y, marker='o', linestyle='-', label="SPMF Fpgrowth TopK")
# y = [1.2, 2.6, 9.6]
# plt.plot(x, y, marker='*', linestyle='-', label="negFIN (minSup)")

# # plt.legend(fontsize=20)
# plt.tight_layout()
# plt.grid(True)
# plt.savefig(dataset + diagram + ".svg", format="svg", dpi=300)  # High-quality output
# plt.savefig(dataset + diagram + ".pdf", format="pdf", dpi=300)  # High-quality output



# dataset="Webdocs"
# plt.figure(dataset + diagram)
# plt.rcParams["font.family"] = "Times New Roman"
# plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,1000)
# plt.xscale('log')
# plt.xticks(fontsize=22) 
# plt.yticks(fontsize=22) 
# plt.ylabel("Time (sec)", fontsize=22)
# x = [100, 1000, 10007]

# y = [224, 605, 970]
# plt.plot(x, y, marker='D', linestyle='-', label="HTK-Miner")
# y = [297, 3000, 3000]
# plt.plot(x, y, marker='H', linestyle='-', label="HTK-negFIN")
# y = [294, 2000, 3000]
# plt.plot(x, y, marker='X', linestyle='-', label="BTK")
# # y = [363, 4000, 4000]
# # plt.plot(x, y, marker='v', linestyle='-', label="SPMF Apriori TopK")
# # y = [112, 1500, 3000]
# # plt.plot(x, y, marker='o', linestyle='-', label="SPMF Fpgrowth TopK")
# y = [117, 212, 740]
# plt.plot(x, y, marker='*', linestyle='-', label="negFIN (minSup)")

# # plt.legend(fontsize=20)
# plt.tight_layout()
# plt.grid(True)
# plt.savefig(dataset + diagram + ".svg", format="svg", dpi=300)  # High-quality output
# plt.savefig(dataset + diagram + ".pdf", format="pdf", dpi=300)  # High-quality output

plt.show()


