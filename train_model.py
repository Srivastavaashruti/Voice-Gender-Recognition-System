# train_model.py
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from extract_features import extract_features

# Load your dataset CSV
data = pd.read_csv("dataset.csv")
print("data....",data)

features = []
labels = []

for index, row in data.iterrows():
    mfccs = extract_features(row['path'])
    if mfccs is not None:
        features.append(mfccs)
        labels.append(1 if row['label'] == 'male' else 0)

X = np.array(features)
y = np.array(labels)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save the model
with open("model.pkl", "wb") as f:
    pickle.dump(clf, f)
