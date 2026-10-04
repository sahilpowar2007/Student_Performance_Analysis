import pandas as pd
import joblib
import matplotlib.pyplot as plt

# 1. Load the dataset and prepare the same features as before
df = pd.read_csv("data/processed/student-mat-featured.csv")

features = ["school", "sex", "age", "studytime", "failures", "absences", "G1", "G2"]
X = pd.get_dummies(df[features], drop_first=True)

# 2. Load the saved Random Forest classifier
model = joblib.load("models/random_forest_classifier.pkl")

# 3. Create a table of feature names and their importance scores
importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("Feature Importance:")
print(importance_df.to_string(index=False))

# 4. Plot a horizontal bar chart
plt.figure(figsize=(8, 5))
plt.barh(importance_df["Feature"], importance_df["Importance"], color="steelblue")
plt.gca().invert_yaxis()  # most important feature on top
plt.xlabel("Importance Score")
plt.title("Feature Importance (Random Forest Classifier)")
plt.tight_layout()

# 5. Save the graph and the table
plt.savefig("visualizations/feature_importance.png", dpi=150)
plt.close()
importance_df.to_csv("reports/feature_importance.csv", index=False)

print("\nGraph saved to: visualizations/feature_importance.png")
print("Table saved to: reports/feature_importance.csv")