import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 1. Load the feature-engineered dataset
df = pd.read_csv("data/processed/student-mat-featured.csv")

# 2. Select input features (G3 is NOT included to avoid target leakage)
features = ["school", "sex", "age", "studytime", "failures", "absences", "G1", "G2"]

X = pd.get_dummies(df[features], drop_first=True)
y = df["performance_level"]  # target: Low / Average / High

# 3. Split data into train and test sets (80% / 20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Create and train the model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# 5. Predict on test data
y_pred = model.predict(X_test)

# 6. Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Logistic Regression Results")
print("---------------------------")
print("Accuracy:", round(accuracy, 2))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred, labels=["Low", "Average", "High"]))

# 7. Save the trained model
model_path = "models/logistic_regression.pkl"
joblib.dump(model, model_path)

print("\nModel saved successfully!")
print("Saved to:", model_path)