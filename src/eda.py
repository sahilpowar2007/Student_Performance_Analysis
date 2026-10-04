import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned dataset
file_path = "data/processed/student-mat-cleaned.csv"
df = pd.read_csv(file_path)

print("Cleaned dataset loaded successfully!")
print("Dataset shape:", df.shape)

# Display basic statistics
print("\nStatistical Summary:")
print(df.describe())

# -----------------------------
# 1. Final Grade Distribution
# -----------------------------

plt.figure(figsize=(8, 5))
sns.histplot(df["G3"], bins=11, kde=True)
plt.title("Distribution of Final Grades (G3)")
plt.xlabel("Final Grade")
plt.ylabel("Number of Students")
plt.savefig("visualizations/final_grade_distribution.png")
plt.show()


# -----------------------------
# 2. Study Time vs Final Grade
# -----------------------------

plt.figure(figsize=(8, 5))
sns.boxplot(x="studytime", y="G3", data=df)
plt.title("Study Time vs Final Grade")
plt.xlabel("Study Time")
plt.ylabel("Final Grade")
plt.savefig("visualizations/studytime_vs_grade.png")
plt.show()


# -----------------------------
# 3. Failures vs Final Grade
# -----------------------------

plt.figure(figsize=(8, 5))
sns.boxplot(x="failures", y="G3", data=df)
plt.title("Previous Failures vs Final Grade")
plt.xlabel("Number of Failures")
plt.ylabel("Final Grade")
plt.savefig("visualizations/failures_vs_grade.png")
plt.show()


# -----------------------------
# 4. Absences vs Final Grade
# -----------------------------

plt.figure(figsize=(8, 5))
sns.scatterplot(x="absences", y="G3", data=df)
plt.title("Absences vs Final Grade")
plt.xlabel("Number of Absences")
plt.ylabel("Final Grade")
plt.savefig("visualizations/absences_vs_grade.png")
plt.show()


print("\nEDA completed successfully!")
print("Graphs saved in visualizations folder.")