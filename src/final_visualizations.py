import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay

# 1. Load the data
df = pd.read_csv("data/processed/student-mat-featured.csv")
att = pd.read_csv("reports/attention_indicators.csv")

order = ["Low", "Average", "High"]
colors = ["#e74c3c", "#f1c40f", "#2ecc71"]

# Graph 1: Performance level distribution
counts = df["performance_level"].value_counts().reindex(order)
plt.figure(figsize=(6, 4))
bars = plt.bar(order, counts.values, color=colors)
plt.bar_label(bars)
plt.title("Performance Level Distribution")
plt.xlabel("Performance Level")
plt.ylabel("Number of Students")
plt.tight_layout()
plt.savefig("visualizations/performance_distribution.png", dpi=150)
plt.close()

# Graph 2: Number of students per indicator
indicators = ["low_recent_grade", "grade_drop", "past_failures", "high_absences"]
ind_counts = att[indicators].sum()
plt.figure(figsize=(7, 4))
bars = plt.bar(ind_counts.index, ind_counts.values, color="steelblue")
plt.bar_label(bars)
plt.title("Students per Academic Attention Indicator")
plt.ylabel("Number of Students")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("visualizations/indicator_counts.png", dpi=150)
plt.close()

# Graph 3: Review suggested by performance level
table = pd.crosstab(att["performance_level"], att["review_suggested"]).reindex(order)
table.columns = ["Not flagged", "Review suggested"]
table.plot(kind="bar", figsize=(7, 4), color=["#95a5a6", "#e67e22"])
plt.title("Review Suggested by Performance Level")
plt.xlabel("Performance Level")
plt.ylabel("Number of Students")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("visualizations/review_by_performance.png", dpi=150)
plt.close()

# Graph 4: Average final grade (G3) by study time
avg_g3 = df.groupby("studytime")["G3"].mean()
plt.figure(figsize=(6, 4))
bars = plt.bar(avg_g3.index.astype(str), avg_g3.values, color="teal")
plt.bar_label(bars, fmt="%.1f")
plt.title("Average Final Grade (G3) by Study Time")
plt.xlabel("Study Time (1 = lowest, 4 = highest)")
plt.ylabel("Average G3")
plt.tight_layout()
plt.savefig("visualizations/g3_by_studytime.png", dpi=150)
plt.close()

# Graph 5: Confusion matrix of the Random Forest classifier
features = ["school", "sex", "age", "studytime", "failures", "absences", "G1", "G2"]
X = pd.get_dummies(df[features], drop_first=True)
y = df["performance_level"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = joblib.load("models/random_forest_classifier.pkl")
ConfusionMatrixDisplay.from_estimator(
    model, X_test, y_test, labels=order, cmap="Blues"
)
plt.title("Confusion Matrix (Random Forest)")
plt.tight_layout()
plt.savefig("visualizations/confusion_matrix_rf.png", dpi=150)
plt.close()

print("All graphs saved in the visualizations folder:")
print("1. performance_distribution.png")
print("2. indicator_counts.png")
print("3. review_by_performance.png")
print("4. g3_by_studytime.png")
print("5. confusion_matrix_rf.png")