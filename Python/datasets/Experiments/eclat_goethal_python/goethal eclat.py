# author: Bart Goethals, University of Antwerp, Belgium

from sys import argv


def eclat(prefix, items):
    global FIM_Count
    while items:
        i,itids = items.pop()
        isupp = len(itids)
        if isupp >= minSup:
            FIM_Count+=1
            # print(sorted(prefix+[i]), ':', isupp)
            suffix = [] 
            for j, ojtids in items:
                jtids = itids & ojtids
                if len(jtids) >= minSup:
                    suffix.append((j,jtids))
            eclat(prefix+[i], sorted(suffix, key=lambda item: len(item[1]), reverse=True))


data = {}
trans = 0
FIM_Count=0

f = open(argv[1], 'r')
for row in f:
    trans += 1
    for item in row.split():
        if item not in data:
            data[item] = set()
        data[item].add(trans)
f.close()

minSup=int(float(argv[2])*trans) #transform minSup from percentage to real count of minSup

eclat([], sorted(data.items(), key=lambda item: len(item[1]), reverse=True))

print(FIM_Count)