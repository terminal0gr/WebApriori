import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

# the reading of the dataset which is in CSV format
dsData = pd.read_csv("datasetOfDatasets.csv", encoding='utf-8')

X = dsData.drop(columns=['name','datasetType'])

y = dsData['datasetType'] 

# Random Forest Classifier
rf = RandomForestClassifier(n_estimators=120)

# Stratified K-Fold Cross Validator
skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

# Lists to store metrics for each fold
accuracies = []
precisions = []
recalls = []
f1_scores = []

# Cross-validation loop
for train_index, test_index in skf.split(X, y):
    X_train, X_test = X.iloc[train_index,:],X.iloc[test_index,:]
    y_train, y_test = y[train_index], y[test_index]

    # Train the model
    rf.fit(X_train, y_train)
    
    # Predict on the test set
    y_pred = rf.predict(X_test)
    
    # Calculate metrics
    accuracies.append(accuracy_score(y_test, y_pred))
    precisions.append(precision_score(y_test, y_pred, average=None))
    recalls.append(recall_score(y_test, y_pred, average=None))
    f1_scores.append(f1_score(y_test, y_pred, average=None))
    
    # Compute and display confusion matrix for each fold
    # cm = confusion_matrix(y_test, y_pred)
    # print(f"Confusion Matrix for Fold {len(accuracies)}:\n", cm)
    
    # Plot confusion matrix
    # plt.figure(figsize=(10, 7))
    # sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    # plt.title(f'Confusion Matrix for Fold {len(accuracies)}')
    # plt.xlabel('Predicted')
    # plt.ylabel('Actual')
    # plt.show()

# Average metrics over all folds
avg_accuracy = np.mean(accuracies)
avg_precision = np.mean(precisions, axis=0)
avg_recall = np.mean(recalls, axis=0)
avg_f1_score = np.mean(f1_scores, axis=0)

print("Average Accuracy:", avg_accuracy)
print("Average Precision for each class:", avg_precision)
print("Average Recall for each class:", avg_recall)
print("Average F1 Score for each class:", avg_f1_score)

# Overall predictions for detailed classification report
y_pred_all = cross_val_predict(rf, X, y, cv=skf)
print(classification_report(y, y_pred_all))

# Compute and display overall confusion matrix
overall_cm = confusion_matrix(y, y_pred_all)
print("Overall Confusion Matrix:\n", overall_cm)

# Plot overall confusion matrix
# plt.figure(figsize=(10, 7))
# sns.heatmap(overall_cm, annot=True, fmt='d', cmap='Blues')
# plt.title('Overall Confusion Matrix')
# plt.xlabel('Predicted')
# plt.ylabel('Actual')
# plt.show()