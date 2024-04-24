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
from sklearn.model_selection import KFold, LeaveOneOut
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.decomposition import PCA

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# the reading of the dataset which is in CSV format
dsTrain = pd.read_csv("datasetOfDatasets.csv", encoding='utf-8')
dsTest = pd.read_csv("datasetTest.csv", encoding='utf-8')

# To apply an classifier on this data, we need to flatten the image, to
# Put in X the dataset excluding the 'Class' column (X=features)
# X = dsData.drop('datasetType ', axis=1)  
X_train = dsTrain.drop(columns=['name','datasetType'])
X_test  = dsTest.drop(columns=['name','datasetType'])

# Put in y the class column
y_train = dsTrain['datasetType'] 
y_test  = dsTest['datasetType'] 

# Step 2: Instantiate the Model

#Decision tree classifier
#rf_classifier = DecisionTreeClassifier()

#Random forest classifier
rf_classifier = RandomForestClassifier(n_estimators=120)

#Gaussian Naive Bayes classifier
# rf_classifier = GaussianNB()

#SVM with linear Kernel
#rf_classifier = SVC(kernel='linear')
#SVM with RBF Kernel
#rf_classifier = SVC(kernel='rbf',C=1.0, gamma=0.3)
#KNN Classifier
#rf_classifier=KNeighborsClassifier(n_neighbors=30)

#MinNaxScaler to [0..1) Must used in SVM and KNN algorithms
# X = X.values
# min_max_scaler = preprocessing.MinMaxScaler()
# X = min_max_scaler.fit_transform(X)
# X = pd.DataFrame(X)

# Train the classifier on the training data
rf_classifier.fit(X_train, y_train)

# Make predictions on the testing data
y_pred = rf_classifier.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Print classification report
print("Classification Report:")
print(classification_report(y_test, y_pred))


#Record mistaken predictions
#mySqlTasks
import sys
sys.path.append('../')
import mySqlTasks as mySql1
mySql=mySql1.mySqlTasks()
mySql._ConnectTobase()

for row_index, (prediction, label) in enumerate(zip(y_pred, y_test)):

    if prediction != label:
        print('Dataset', y_test.index[row_index], dsTest['name'].iloc[y_test.index[row_index]], 'classified as ', prediction, 'should be ', label)

        strsql = "UPDATE `datasetwrongclassification` \
                    set instances=instances+1 \
                Where `datasetName`=%s \
                And   `realClass`  =%s \
                And   `predictedClass`=%s"
        queryParams=(dsTest['name'].iloc[y_test.index[row_index]],int(label),int(prediction))
        mySql.myQuery(strsql,queryParams)

        strsql = "INSERT INTO `datasetwrongclassification`(`datasetName`, `realClass`, `predictedClass`, `instances`)  \
                SELECT %s, %s, %s, 1 \
                WHERE NOT EXISTS (SELECT `datasetName` \
                    FROM `datasetwrongclassification` \
                    WHERE `datasetName`=%s \
                    AND   `realClass`=%s \
                    AND   `predictedClass`=%s)"
        queryParams=(dsTest['name'].iloc[y_test.index[row_index]],int(label),int(prediction),dsTest['name'].iloc[y_test.index[row_index]],int(label),int(prediction))
        mySql.myQuery(strsql,queryParams)

            