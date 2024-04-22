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
dsData = pd.read_csv("datasetOfDatasets.csv", encoding='utf-8')
dsTest = pd.read_csv("datasetTest.csv", encoding='utf-8')

# To apply an classifier on this data, we need to flatten the image, to
# Put in X the dataset excluding the 'Class' column (X=features)
# X = dsData.drop('datasetType ', axis=1)  
X_train = dsData.drop(columns=['name','datasetType'])
X_test  = dsTest.drop(columns=['name','datasetType'])

# Put in y the class column
y_train = dsData['datasetType'] 
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
        