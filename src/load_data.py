import pandas as pd

# Dataset path
file_path = "data/raw/student-mat.csv"

# Load dataset
df = pd.read_csv(file_path, sep=";")

# Display basic information
print("Dataset loaded successfully!")
print("Shape of dataset:", df.shape)

print("\nFirst 5 rows:")
print(df.head())

print("\nColumn names:")
print(df.columns.tolist())
print("\nDataset Information:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nStatistical Summary:")
print(df.describe())