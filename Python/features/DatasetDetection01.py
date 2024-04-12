#numpy arrays and pandas dataframes (Datasets)
import numpy as np
import pandas as pd

#For plots
# import matplotlib.pyplot as plt
# import matplotlib.colors as colors

# used for counting time
from time import time

# libraries for SVM experiments and scoring
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import KFold
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

#mySqlTasks
import sys
sys.path.append('../')
import mySqlTasks as mySql1
mySql=mySql1.mySqlTasks()
mySql._ConnectTobase()

# the reading of the dataset which is in CSV format
dsData = pd.read_csv("datasetOfDatasets.csv", encoding='utf-8')

# print(dsData.describe())
# print(dsData.head())

# To apply an classifier on this data, we need to flatten the image, to
# Put in X the dataset excluding the 'Class' column (X=features)
# X = dsData.drop('datasetType ', axis=1)  
X = dsData.drop(columns=['name','datasetType'])

# Put in y the class column [0,1]
y = dsData['datasetType'] 

# Step 2: Instantiate the Model
#rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier = RandomForestClassifier(n_estimators=120)

# Step 3: Perform ?-fold Cross-Validation
split=8

for i in range(10):

    kf = KFold(n_splits=split, shuffle=True)
    fold = 1

    acc_score = []

    for train_index, test_index in kf.split(X):
        X_train, X_test = X.iloc[train_index,:],X.iloc[test_index,:]
        y_train, y_test = y[train_index], y[test_index]
        
        # Train the model
        rf_classifier.fit(X_train, y_train)
        
        # Predict on the test set
        y_pred = rf_classifier.predict(X_test)
        
        acc = accuracy_score(y_pred , y_test)
        acc_score.append(acc)
        
        #print()
        for row_index, (input, prediction, label) in enumerate(zip (X_test, y_pred, y_test)):
          if prediction != label:
        
            #print('Dataset', y_test.index[row_index], dsData['name'].iloc[y_test.index[row_index]], 'classified as ', prediction, 'should be ', label)
        
            strsql = "UPDATE `datasetwrongclassification` \
                        set instances=instances+1 \
                    Where `datasetName`=%s \
                    And   `realClass`  =%s \
                    And   `predictedClass`=%s"
            queryParams=(dsData['name'].iloc[y_test.index[row_index]],int(label),int(prediction))
            mySql.myQuery(strsql,queryParams)

            strsql = "INSERT INTO `datasetwrongclassification`(`datasetName`, `realClass`, `predictedClass`, `instances`)  \
                    SELECT %s, %s, %s, 1 \
                    WHERE NOT EXISTS (SELECT `datasetName` \
                        FROM `datasetwrongclassification` \
                        WHERE `datasetName`=%s \
                        AND   `realClass`=%s \
                        AND   `predictedClass`=%s)"
            queryParams=(dsData['name'].iloc[y_test.index[row_index]],int(label),int(prediction),dsData['name'].iloc[y_test.index[row_index]],int(label),int(prediction))
            mySql.myQuery(strsql,queryParams)

        # Compute confusion matrix
        #cm = confusion_matrix(y_test, y_pred)
        
        # Print confusion matrix for the fold
        #print(f"Fold {fold} Accuracy {acc} Confusion Matrix:")
        #print(cm)
        
        # Increment fold counter
        fold += 1
        
    #percentages = ["{:.1f}%".format(number * 100) for number in acc_score]
    #print('accuracy of each fold - {}'.format(percentages))
    avgper="{:.1f}%".format(sum(acc_score)/split*100)
    print(f'aa {i+1}: Avg accuracy : {avgper}')

