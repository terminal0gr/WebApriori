import matplotlib.pyplot as plt

plt.figure("KosarakR")
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
plt.ylim(0,300)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Time (sec)", fontsize=22)
x = [100, 1000, 10007]
y = [12, 113, 990]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [11, 16, 126]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [28, 942, 10000]
plt.plot(x, y, marker='.', linestyle='-', label="DTS")
y = [11, 17, 163]
plt.plot(x, y, marker='v', linestyle='-', label="DBSN")
plt.legend(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.savefig("KosarakR.svg", format="svg", dpi=300)  # High-quality output
plt.savefig("KosarakR.pdf", format="pdf", dpi=300)  # High-quality output

plt.figure("AccidentsR")
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
plt.ylim(0,300)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Time (sec)", fontsize=22)
x = [100, 1000, 10000]
y = [14, 194, 1000]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [9,  10, 18]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [7, 102, 800]
plt.plot(x, y, marker='.', linestyle='-', label="DTS")
y = [9, 10, 19]
plt.plot(x, y, marker='v', linestyle='-', label="DBSN")
plt.legend(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.savefig("AccidentsR.svg", format="svg", dpi=300)  # High-quality output
plt.savefig("AccidentsR.pdf", format="pdf", dpi=300)  # High-quality output

plt.figure("ChessR")
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,300)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Time (sec)", fontsize=22)
x = [102, 1001, 10028]
y = [0.1, 1.0, 15.5]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [0.3, 0.4, 5.5]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [0.07, 0.4, 9.9]
plt.plot(x, y, marker='.', linestyle='-', label="DTS")
y = [0.3, 0.4, 5.4]
plt.plot(x, y, marker='v', linestyle='-', label="DBSN")
plt.legend(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.savefig("ChessR.svg", format="svg", dpi=300)  # High-quality output
plt.savefig("ChessR.pdf", format="pdf", dpi=300)  # High-quality output

plt.figure("ConnectR")
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
plt.ylim(0,300)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Time (sec)", fontsize=22)
x = [100, 1003, 10015]
y = [1.7, 23.2, 310]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [1.3, 1.4, 6.8]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [1.0, 5.99, 69.8]
plt.plot(x, y, marker='.', linestyle='-', label="DTS")
y = [1.3, 1.4, 7.1]
plt.plot(x, y, marker='v', linestyle='-', label="DBSN")
plt.legend(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.savefig("ConnectR.svg", format="svg", dpi=300)  # High-quality output
plt.savefig("ConnectR.pdf", format="pdf", dpi=300)  # High-quality output

plt.figure("MushroomR")
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,300)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Time (sec)", fontsize=22)
x = [106, 1008, 10011]
y = [0.3, 2.3, 20.2]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [0.3, 0.39, 6.1]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [0.2, 2.4, 25.2]
plt.plot(x, y, marker='X', linestyle='-', label="DTS")
y = [0.3, 0.4, 6.1]
plt.plot(x, y, marker='v', linestyle='-', label="DBSN")
plt.legend(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.savefig("MushroomR.svg", format="svg", dpi=300)  # High-quality output
plt.savefig("MushroomR.pdf", format="pdf", dpi=300)  # High-quality output

dataset="pumsbR"
x = [100, 1000, 10002]
plt.figure(dataset)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
plt.ylim(0,300)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Time (sec)", fontsize=22)
y = [1.9, 21.8, 268.1]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [1.3, 1.7, 7.2]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [1.1, 6.0, 83.4]
plt.plot(x, y, marker='X', linestyle='-', label="DTS")
y = [1.3, 1.7, 7.4]
plt.plot(x, y, marker='v', linestyle='-', label="DBSN")
plt.legend(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.savefig(dataset + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + ".pdf", format="pdf", dpi=300)  # High-quality output

dataset="T40I10D100KR"
x = [100, 1000, 10018]
plt.figure(dataset)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
plt.ylim(0,300)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Time (sec)", fontsize=22)
y = [6.6, 79.5, 226.8]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [1.4, 3.0, 15.9]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [8.3, 142.7, 800.0]
plt.plot(x, y, marker='X', linestyle='-', label="DTS")
y = [1.4, 3.2, 17.4]
plt.plot(x, y, marker='v', linestyle='-', label="DBSN")
plt.legend(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.savefig(dataset + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + ".pdf", format="pdf", dpi=300)  # High-quality output

dataset="L-0023R"
x = [100, 1025, 11257]
plt.figure(dataset)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,300)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Time (sec)", fontsize=22)
y = [0.09, 1.05, 8.6]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [0.3, 0.5, 6.5]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [0.16, 1.6, 13.7]
plt.plot(x, y, marker='X', linestyle='-', label="DTS")
y = [0.3, 0.6, 6.7]
plt.plot(x, y, marker='v', linestyle='-', label="DBSN")
plt.legend(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.savefig(dataset + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + ".pdf", format="pdf", dpi=300)  # High-quality output

dataset="T16IT20D100KR"
x = [100, 1000, 10034]
plt.figure(dataset)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,300)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Time (sec)", fontsize=22)
y = [4.8, 29.7, 193]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [0.9, 1.1, 6.6]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [2.7, 8.1, 45]
plt.plot(x, y, marker='X', linestyle='-', label="DTS")
y = [0.9, 1.1, 6.8]
plt.plot(x, y, marker='v', linestyle='-', label="DBSN")
plt.legend(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.savefig(dataset + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + ".pdf", format="pdf", dpi=300)  # High-quality output


dataset="WebdocsR"
x = [100, 1000, 10000]
plt.figure(dataset)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
plt.ylim(0,1000)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Time (sec)", fontsize=22)
y = [229, 1200, 12000]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [295, 606, 970]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [225, 1300, 14000]
plt.plot(x, y, marker='X', linestyle='-', label="DTS")
y = [290, 608, 1006]
plt.plot(x, y, marker='v', linestyle='-', label="DBSN")
plt.legend(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.savefig(dataset + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + ".pdf", format="pdf", dpi=300)  # High-quality output

plt.show()


