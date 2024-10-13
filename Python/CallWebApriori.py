import Main01W as Apriori

identity='79d1727987f200802593e3599119c966' 
# datasetName='H-MineSample.txt'
# datasetName='0fish_catches.csv'
# datasetName='invoiceType1.csv'
datasetName='invoiceType2.csv'
# datasetName='Transactional_T10I4D100K.csv'
# datasetName='Titanic02.csv'
public=0
callType=101
arg1='IDInvoice'
arg2='ProduitID'

# callType:
#   0 --> My apriori implementation
#  10 --> mlxtend Apriori implementation
#  11 --> mlxtend FPGrowth implementation
#  12 --> mlxtend H-Mine implementation 
# 100 --> Retrieve participating items list

WAInst=Apriori.webApriori(identity,datasetName,public,callType,arg1,arg2)
print(WAInst.runWebApriori())


