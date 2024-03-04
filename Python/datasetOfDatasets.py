#numpy arrays and pandas dataframes (Datasets)
import numpy as np
import pandas as pd
import os

#For plots
# import matplotlib.pyplot as plt
# import matplotlib.colors as colors

# used for counting time
from time import time

# libraries for SVM experiments and scoring
# from sklearn import preprocessing
# from sklearn.svm import SVC
# from sklearn.model_selection import GridSearchCV
# from sklearn.model_selection import train_test_split
# from sklearn.model_selection import cross_val_score
# from sklearn.model_selection import cross_val_predict
# from sklearn.metrics import classification_report
# from sklearn.metrics import confusion_matrix
# from sklearn.feature_selection import SelectKBest, chi2
# from sklearn.decomposition import PCA

# the reading of the dataset which is in CSV format
# heartdata = pd.read_csv("../input/datasetOfDatasets.csv") 
filepath=os.path.join('features', 'datasetOfDatasets.csv')
dsData = pd.read_csv(filepath)

