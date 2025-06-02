# author: Bart Goethals, University of Antwerp, Belgium
# contributor: Malliaridis Konstantinos, International Hellenic University, Greece

from sys import argv
import csv
import math

class goethals_Eclat():

    def __init__(self, filename, minSup=0.1, separator=" "):
        self.filename = filename
        self.minSup=minSup
        self.minSupA=0 #Absolute minSup (e.g. 400)
        self.FIM_Count=0
        self.separator=separator 


    def eclat(self, prefix, items):
        while items:
            i,itids = items.pop()
            isupp = len(itids)
            if isupp >= self.minSupA:
                self.FIM_Count+=1
                # print(sorted(prefix+[i]), ':', isupp)
                suffix = [] 
                for j, ojtids in items:
                    jtids = itids & ojtids
                    if len(jtids) >= self.minSupA:
                        suffix.append((j,jtids))
                goethals_Eclat.eclat(self, prefix+[i], sorted(suffix, key=lambda item: len(item[1]), reverse=True))

    def mine(self):
        data = {}
        trans = 0
        self.FIM_Count=0


        # Malliaridis 23/11/2024
        with open(self.filename, encoding='utf-8-sig') as file_input:
            reader = csv.reader(file_input, delimiter=self.separator)
            for transaction in reader:
                trans += 1
                for item in transaction:
                    if item=='': continue
                    if item not in data:
                        data[item] = set()
                    data[item].add(trans)
        # f = open(self.filename, 'r')
        # for row in f:
        #     trans += 1
        #     for item in row.split(self.separator):
        #         if item not in data:
        #             data[item] = set()
        #         data[item].add(trans)
        # f.close()

        self.minSupA=math.ceil(float(self.minSup)*trans) #transform minSup from percentage to real count of minSup

        goethals_Eclat.eclat(self,[], sorted(data.items(), key=lambda item: len(item[1]), reverse=True))

