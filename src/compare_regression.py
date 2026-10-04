import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 1. Load the dataset and prepare the data (same as before)
df = pd.read_csv("data/processed/student-mat-featured.csv")

features = ["school", "sex", "age", "studytime", "failures", "absences", "G1", "G2"]
X = pd.get_dummies(df[features], drop_first=True)
y = df["G3"]

# Same split as before so the comparison is fair
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 2. Load the saved models
models = {
    "Linear Regression": joblib.load("models/linear_regression.pkl"),
    "Random Forest": joblib.load("models/random_forest_regressor.pkl"),
}

# 3. Calculate metrics for each model
results = []
for name, model in models.items():
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    results.append({
        "Model": name,
        "MAE": round(mean_absolute_error(y_test, y_pred), 2),
        "MSE": round(mse, 2),
        "RMSE": round(np.sqrt(mse), 2),
        "R2": round(r2_score(y_test, y_pred), 2),
    })

# 4. Print the comparison table and save it as CSV
results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))

results_df.to_csv("reports/regression_comparison.csv", index=False)
print("\nSaved to: reports/regression_comparison.csv")