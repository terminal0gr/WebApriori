import matplotlib.pyplot as plt
import numpy as np

dataset="KosarakM"
plt.figure(dataset)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,300)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Memory consuption in MB", fontsize=22)
x = [100, 1000, 10000]
y = [86, 131, 303]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [74, 210, 2500]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [314, 2200, None]
plt.plot(x, y, marker='.', linestyle='-', label="DTS")
y = [74, 220, 2595]
plt.plot(x, y, marker='v', linestyle='-', label="DBSN")
plt.legend(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.savefig(dataset + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + ".pdf", format="pdf", dpi=300)  # High-quality output


dataset="AccidentsM"
plt.figure(dataset)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,300)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Memory consuption in MB", fontsize=22)
x = [100, 1000, 10000]
y = [240, 1485, None]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [26, 75, 600]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [113, 1526, None]
plt.plot(x, y, marker='.', linestyle='-', label="DTS")
y = [27, 78, 620]
plt.plot(x, y, marker='v', linestyle='-', label="DBSN")
plt.legend(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.savefig(dataset + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + ".pdf", format="pdf", dpi=300)  # High-quality output

dataset="ChessM"
plt.figure(dataset)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,300)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Memory consuption in MB", fontsize=22)
x = [100, 1000, 10000]
y = [13, 32, 184]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [10, 12, 24]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [12, 22, 106]
plt.plot(x, y, marker='.', linestyle='-', label="DTS")
y = [11, 13, 26]
plt.plot(x, y, marker='v', linestyle='-', label="DBSN")
plt.legend(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.savefig(dataset + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + ".pdf", format="pdf", dpi=300)  # High-quality output

dataset="ConnectM"
plt.figure(dataset)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,300)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Memory consuption in MB", fontsize=22)
x = [100, 1000, 10000]
y = [67, 471, 4200]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [15, 20, 108]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [44, 188, 1926]
plt.plot(x, y, marker='.', linestyle='-', label="DTS")
y = [15, 24, 117]
plt.plot(x, y, marker='v', linestyle='-', label="DBSN")
plt.legend(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.savefig(dataset + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + ".pdf", format="pdf", dpi=300)  # High-quality output

dataset="MushroomM"
plt.figure(dataset)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,300)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Memory consuption in MB", fontsize=22)
x = [100, 1000, 10000]
y = [15, 35, 148]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [10, 12, 30]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [14, 45, 244]
plt.plot(x, y, marker='.', linestyle='-', label="DTS")
y = [12, 14, 32]
plt.plot(x, y, marker='v', linestyle='-', label="DBSN")
plt.legend(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.savefig(dataset + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + ".pdf", format="pdf", dpi=300)  # High-quality output

dataset="pumsbM"
plt.figure(dataset)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,300)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Memory consuption in MB", fontsize=22)
x = [100, 1000, 10000]
y = [51, 342, 2900]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [14, 20, 99]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [38, 128, 2350]
plt.plot(x, y, marker='.', linestyle='-', label="DTS")
y = [16, 24, 111]
plt.plot(x, y, marker='v', linestyle='-', label="DBSN")
plt.legend(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.savefig(dataset + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + ".pdf", format="pdf", dpi=300)  # High-quality output

dataset="T40I10D100KM"
plt.figure(dataset)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,300)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Memory consuption in MB", fontsize=22)
x = [100, 1000, 10000]
y = [23, 50, 210]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [17, 28, 256]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [26, 135, None]
plt.plot(x, y, marker='.', linestyle='-', label="DTS")
y = [17, 30, 260]
plt.plot(x, y, marker='v', linestyle='-', label="DBSN")
plt.legend(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.savefig(dataset + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + ".pdf", format="pdf", dpi=300)  # High-quality output

dataset="L-0023M"
plt.figure(dataset)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,300)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Memory consuption in MB", fontsize=22)
x = [100, 1000, 10000]
y = [11, 12, 21]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [11, 13, 28]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [11, 13, 50]
plt.plot(x, y, marker='.', linestyle='-', label="DTS")
y = [11, 13, 29]
plt.plot(x, y, marker='v', linestyle='-', label="DBSN")
plt.legend(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.savefig(dataset + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + ".pdf", format="pdf", dpi=300)  # High-quality output

dataset="T16IT20D100KM"
plt.figure(dataset)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,300)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Memory consuption in MB", fontsize=22)
x = [100, 1000, 10000]
y = [69, 412, 1700]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [14, 25, 81]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [31, 103, 370]
plt.plot(x, y, marker='.', linestyle='-', label="DTS")
y = [14, 27, 87]
plt.plot(x, y, marker='v', linestyle='-', label="DBSN")
plt.legend(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.savefig(dataset + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + ".pdf", format="pdf", dpi=300)  # High-quality output

dataset="WebdocsM"
plt.figure(dataset)
plt.rcParams["font.family"] = "Times New Roman"
plt.xlabel("Top-(K) frequent patterns", fontsize=22)
# plt.ylim(0,300)
plt.xscale('log')
plt.xticks(fontsize=22) 
plt.yticks(fontsize=22) 
plt.ylabel("Memory consuption in MB", fontsize=22)
x = [100, 1000, 10000]
y = [1900, None, None]
plt.plot(x, y, marker='o', linestyle='-', label="TS")
y = [1500, 1800, 5000]
plt.plot(x, y, marker='*', linestyle='-', label="BSN")
y = [1950, None, None]
plt.plot(x, y, marker='.', linestyle='-', label="DTS")
y = [1500, 1850, 5100]
plt.plot(x, y, marker='v', linestyle='-', label="DBSN")
plt.legend(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.savefig(dataset + ".svg", format="svg", dpi=300)  # High-quality output
plt.savefig(dataset + ".pdf", format="pdf", dpi=300)  # High-quality output

plt.show()


