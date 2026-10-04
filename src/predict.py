import pandas as pd
import joblib

# 1. Load the saved Random Forest classifier
model = joblib.load("models/random_forest_classifier.pkl")


def predict_performance(school, sex, age, studytime, failures, absences, G1, G2):
    """Predict performance level (Low / Average / High) for one student."""

    # 2. Put the student's data into a one-row table
    student = pd.DataFrame([{
        "age": age,
        "studytime": studytime,
        "failures": failures,
        "absences": absences,
        "G1": G1,
        "G2": G2,
        "school_MS": 1 if school == "MS" else 0,  # same encoding as training
        "sex_M": 1 if sex == "M" else 0,
    }])

    # 3. Arrange columns in the same order the model was trained with
    student = student[model.feature_names_in_]

    # 4. Predict the level and the probability of each level
    level = model.predict(student)[0]
    probabilities = dict(zip(model.classes_, model.predict_proba(student)[0]))

    return level, probabilities


# 5. Test with three sample students
if __name__ == "__main__":
    samples = [
        ("GP", "F", 17, 2, 2, 10, 6, 5),
        ("GP", "M", 16, 2, 0, 4, 11, 12),
        ("MS", "F", 16, 3, 0, 2, 17, 18),
    ]

    for i, s in enumerate(samples, start=1):
        level, probs = predict_performance(*s)
        print(f"Student {i}: {level}")
        for name, p in probs.items():
            print(f"   {name}: {round(p * 100, 1)}%")