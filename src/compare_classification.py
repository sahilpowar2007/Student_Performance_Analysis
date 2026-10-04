import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# 1. Load the dataset and prepare the data (same as before)
df = pd.read_csv("data/processed/student-mat-featured.csv")

features = ["school", "sex", "age", "studytime", "failures", "absences", "G1", "G2"]
X = pd.get_dummies(df[features], drop_first=True)
y = df["performance_level"]

# Same split as before so the comparison is fair
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 2. Load the saved classification models
models = {
    "Logistic Regression": joblib.load("models/logistic_regression.pkl"),
    "Decision Tree": joblib.load("models/decision_tree.pkl"),
    "Random Forest": joblib.load("models/random_forest_classifier.pkl"),
}

# 3. Calculate metrics for each model (weighted average over Low/Average/High)
results = []
for name, model in models.items():
    y_pred = model.predict(X_test)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, y_pred, average="weighted"
    )
    results.append({
        "Model": name,
        "Accuracy": round(accuracy_score(y_test, y_pred), 2),
        "Precision": round(precision, 2),
        "Recall": round(recall, 2),
        "F1-score": round(f1, 2),
    })

# 4. Print the comparison table and save it as CSV
results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))

results_df.to_csv("reports/classification_comparison.csv", index=False)
print("\nSaved to: reports/classification_comparison.csv")