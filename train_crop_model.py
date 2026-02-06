
# Detailed Training Script

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import os

# Create models directory if not exists
if not os.path.exists('models'):
    os.makedirs('models')

# Load dataset
print("Loading dataset...")
df = pd.read_csv('Crop_recommendation (1).csv')

# Prepare features and target
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['label']

# Encode target labels
print("Encoding labels...")
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Save label encoder
with open('models/label_encoder.pkl', 'wb') as f:
    pickle.dump(le, f)
print("Label encoder saved to models/label_encoder.pkl")

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train Random Forest Model
print("Training Random Forest Classifier...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate model
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy*100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=le.classes_))

# Save model
with open('models/crop_recommendation_model.pkl', 'wb') as f:
    pickle.dump(rf_model, f)
print("Model saved to models/crop_recommendation_model.pkl")

print("\nVerifying model loading...")
# Verify loading
with open('models/crop_recommendation_model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

# Test prediction
test_input = np.array([[90, 42, 43, 20.8, 82.0, 6.5, 202.9]])
prediction_idx = loaded_model.predict(test_input)[0]
prediction_label = le.inverse_transform([prediction_idx])[0]
print(f"Test Prediction for Rice-like conditions: {prediction_label}")
