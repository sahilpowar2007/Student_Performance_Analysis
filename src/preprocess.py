import pandas as pd

# Load dataset
file_path = "data/raw/student-mat.csv"
df = pd.read_csv(file_path, sep=";")

print("Original dataset shape:", df.shape)

# Check missing values
print("\nMissing Values:", df.isnull().sum().sum())

# Check duplicate rows
duplicate_count = df.duplicated().sum()
print("\nDuplicate Rows:", duplicate_count)

# Remove duplicate rows
df = df.drop_duplicates()

print("\nShape after removing duplicates:", df.shape)

# Save cleaned dataset
output_path = "data/processed/student-mat-cleaned.csv"
df.to_csv(output_path, index=False)

print("\nCleaned dataset saved successfully!")
print("Saved to:", output_path)