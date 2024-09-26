import Main01W as Apriori

identity='79d1727987f200802593e3599119c966'
datasetName='titanic02.csv'
public=0
callType=3
arg1=None
arg2=None

# callType:
# 0 --> My apriori implementation
# 1 --> Retrieve participating items list
# 2 --> mlxtend Apriori implementation
# 3 --> mlxtend FPGrowth implementation
# 4 --> mlxtend FP-max implementation (maximal items sets)

WAInst=Apriori.webApriori(identity,datasetName,public,callType,arg1,arg2)
print(WAInst.runWebApriori())


