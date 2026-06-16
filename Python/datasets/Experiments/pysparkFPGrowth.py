import os
import sys

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
os.environ['HADOOP_HOME'] = 'D:\\winutils'

from pyspark import SparkContext
from pyspark.mllib.fpm import FPGrowth

sc = SparkContext("local", "MyApp")

data = sc.textFile("datasets/webdocs.dat")
transactions = data.map(lambda line: line.strip().split(' '))
model = FPGrowth.train(transactions, minSupport=0.327204591739643, numPartitions=6)
result = model.freqItemsets().collect()
for fi in result:
    print(fi)