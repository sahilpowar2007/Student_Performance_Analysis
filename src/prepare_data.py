import pandas as pd
from sklearn.model_selection import train_test_split

# Load feature-engineered dataset
file_path = "data/processed/student-mat-featured.csv"
df = pd.read_csv(file_path)

print("Dataset shape:", df.shape)

# Select input features
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

print("\nSelected Features:")
print(X.columns.tolist())

print("\nTarget:")
print("G3 - Final Grade")

# Convert categorical columns into numeric columns
X = pd.get_dummies(X, drop_first=True)

# Split dataset into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining data shape:", X_train.shape)
print("Testing data shape:", X_test.shape)

print("\nData preparation completed successfully!")