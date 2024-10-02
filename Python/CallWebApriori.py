import Main01W as Apriori

identity='79d1727987f200802593e3599119c966' 
datasetName='H-MineSample.txt'
datasetName='0fish_catches.csv'
public=1
callType=2
arg1=None
arg2=None

# callType:
# 0 --> My apriori implementation
# 1 --> Retrieve participating items list
# 2 --> mlxtend Apriori implementation
# 3 --> mlxtend FPGrowth implementation
# 4 --> mlxtend H-Mine implementation 

WAInst=Apriori.webApriori(identity,datasetName,public,callType,arg1,arg2)
print(WAInst.runWebApriori())


