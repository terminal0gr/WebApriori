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
y = [13.8, 139.0, 900]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [11.3, 17.2, 143.0]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [30.48, 300.0, 1500]
plt.plot(x, y, marker='.', linestyle='-', label="DTS")
y = [11.4, 18.9, 186.0]
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
y = [17.2, 242.1, 1200]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [9.2, 10.1, 20.5]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [10.1, 187.4, 900]
plt.plot(x, y, marker='.', linestyle='-', label="DTS")
y = [9.2, 10.2, 24.3]
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
y = [0.1, 1.1, 18.9]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [0.3, 0.4, 6.8]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [0.08, 0.5, 11.8]
plt.plot(x, y, marker='.', linestyle='-', label="DTS")
y = [0.3, 0.4, 7.0]
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
y = [2.7, 30.3, 300]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [1.3, 1.4, 8.7]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [1.2, 10.9, 120.1]
plt.plot(x, y, marker='.', linestyle='-', label="DTS")
y = [1.3, 1.5, 11.9]
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
y = [0.3, 2.6, 25.7]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [0.3, 0.39, 7.8]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [0.2, 2.8, 33.8]
plt.plot(x, y, marker='X', linestyle='-', label="DTS")
y = [0.3, 0.4, 9.4]
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
y = [2.3, 29.5, 330]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [1.4, 1.7, 9.2]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [1.3, 12.6, 220.2]
plt.plot(x, y, marker='X', linestyle='-', label="DTS")
y = [1.3, 1.8, 12.2]
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
y = [6.8, 87.2, 251.0]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [1.5, 3.1, 17.6]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [8.4, 156.1, 400.0]
plt.plot(x, y, marker='X', linestyle='-', label="DTS")
y = [1.4, 3.5, 23.6]
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
y = [0.1, 1.0, 10.3]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [0.3, 0.5, 7.1]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [0.1, 1.5, 14.7]
plt.plot(x, y, marker='X', linestyle='-', label="DTS")
y = [0.1, 1.4, 8.6]
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
y = [5.0, 31.1, 220.4]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [0.9, 1.1, 7.0]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [2.6, 8.2, 49.5]
plt.plot(x, y, marker='X', linestyle='-', label="DTS")
y = [0.9, 1.1, 9.6]
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
# plt.ylim(0,300)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Time (sec)", fontsize=22)
y = [317.0, 626.0, 6000.0]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [317.0, 626.0, 6000.0]
plt.plot(x, y, marker='v', linestyle='-', label="DBSN")
plt.legend(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.savefig(dataset + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + ".pdf", format="pdf", dpi=300)  # High-quality output

plt.show()


