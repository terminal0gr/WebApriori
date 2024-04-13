import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from joblib import dump

# the reading of the dataset which is in CSV format
dsData = pd.read_csv("datasetOfDatasets.csv", encoding='utf-8')

# Put in X the dataset excluding the 'Class' column (X=features)
X = dsData.drop(columns=['name','datasetType'])

# Put in y the class column [2,3,4,0]
y = dsData['datasetType'] 

# Step 2: Instantiate the Model
rf_classifier = RandomForestClassifier(n_estimators=180)

# Step 3: # Train the model
rf_classifier.fit(X, y)
        
# Step 4: # Save the trained model to a file
dump(rf_classifier, 'TrainedModel.joblib')

