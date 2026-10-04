import pandas as pd

# Load cleaned dataset
file_path = "data/processed/student-mat-cleaned.csv"
df = pd.read_csv(file_path)

print("Original dataset shape:", df.shape)

# Create Performance Level based on final grade (G3)
def classify_performance(grade):
    if grade < 10:
        return "Low"
    elif grade < 15:
        return "Average"
    else:
        return "High"

df["performance_level"] = df["G3"].apply(classify_performance)

# Display performance distribution
print("\nPerformance Level Distribution:")
print(df["performance_level"].value_counts())

# Save feature-engineered dataset
output_path = "data/processed/student-mat-featured.csv"
df.to_csv(output_path, index=False)

print("\nFeature engineering completed successfully!")
print("Saved to:", output_path)