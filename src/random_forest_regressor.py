import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 1. Dataset load करणे
df = pd.read_csv("data/processed/student-mat-featured.csv")

# 2. Features आणि target (आधीसारखेच, G3 input मध्ये नाही)
features = [
    "school",
    "sex",
    "age",
    "studytime",
    "failures",
    "absences",
    "G1",
    "G2"
]

X = df[features]
y = df["G3"]

X = pd.get_dummies(X, drop_first=True)

# 3. तोच split (तुलना योग्य व्हावी म्हणून random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# 4. Random Forest model बनवणे आणि train करणे
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Prediction
y_pred = model.predict(X_test)

# 6. Metrics
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("Random Forest Regressor Results")
print("-------------------------------")
print("MAE :", round(mae, 2))
print("MSE :", round(mse, 2))
print("RMSE:", round(rmse, 2))
print("R2  :", round(r2, 2))

# 7. Model save करणे
model_path = "models/random_forest_regressor.pkl"
joblib.dump(model, model_path)

print("\nModel saved successfully!")
print("Saved to:", model_path)