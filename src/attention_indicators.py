import pandas as pd

# 1. Load the feature-engineered dataset
df = pd.read_csv("data/processed/student-mat-featured.csv")

# 2. Define the limit for "high absences" (top 25% of students)
absence_limit = df["absences"].quantile(0.75)

# 3. Create the four indicators (1 = indicator present, 0 = not present)
df["low_recent_grade"] = (df["G2"] < 10).astype(int)
df["grade_drop"] = ((df["G1"] - df["G2"]) >= 2).astype(int)
df["past_failures"] = (df["failures"] >= 1).astype(int)
df["high_absences"] = (df["absences"] > absence_limit).astype(int)

indicators = ["low_recent_grade", "grade_drop", "past_failures", "high_absences"]

# 4. Count indicators per student and suggest a review if 2 or more are present
df["indicator_count"] = df[indicators].sum(axis=1)
df["review_suggested"] = (df["indicator_count"] >= 2).astype(int)

# 5. Print a summary
print("Absence limit (75th percentile):", absence_limit)

print("\nStudents per indicator:")
print(df[indicators].sum().to_string())

print("\nNumber of indicators per student:")
print(df["indicator_count"].value_counts().sort_index().to_string())

flagged = df["review_suggested"].sum()
print(f"\nStudents with review suggested: {flagged} out of {len(df)} "
      f"({round(flagged / len(df) * 100, 1)}%)")

# 6. Save the result (student_id = row number in the dataset)
df.insert(0, "student_id", df.index + 1)
columns_to_save = ["student_id", "G1", "G2", "failures", "absences"] + indicators + [
    "indicator_count", "review_suggested", "performance_level"
]
df[columns_to_save].to_csv("reports/attention_indicators.csv", index=False)

print("\nNote: These are analytical indicators, not final judgements about students.")
print("Saved to: reports/attention_indicators.csv")