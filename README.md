# Student Performance Analysis System

## 1. Project Overview

The Student Performance Analysis System is a Data Science based mini project developed to analyze student academic performance, identify important performance-related factors, classify students into performance levels, and predict student performance using Machine Learning.

The system also provides analytical indicators to identify students who may require academic review.

A Streamlit dashboard is developed to present the analysis, predictions, visualizations, and model results in an interactive way.

---

## 2. Objectives

- Collect and organize student academic performance data.
- Clean and preprocess the dataset.
- Perform Exploratory Data Analysis (EDA).
- Analyze factors related to student performance.
- Perform student-wise and performance-level analysis.
- Visualize important patterns using graphs and charts.
- Classify students into Low, Average, and High performance levels.
- Apply Machine Learning models for prediction.
- Identify analytical indicators for students who may require academic review.
- Provide an interactive Streamlit dashboard.
- Generate data-driven insights and reports.

---

## 3. Dataset

The project uses the UCI Student Performance dataset.

Dataset file:

`student-mat.csv`

Dataset size:

- 395 students
- 33 columns

Target variable:

`G3` - Final grade

Performance levels are created from G3:

- Low: G3 < 10
- Average: 10 <= G3 < 15
- High: G3 >= 15

### Important Dataset Limitation

The UCI Student Performance dataset does not contain:

- Attendance percentage
- Assignment marks
- Practical marks

Therefore, these variables are not artificially added to the analysis.

Instead, the project uses available variables such as:

- Study time
- Failures
- Absences
- G1
- G2
- Age
- Sex
- School

---

## 4. Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Streamlit
- Joblib
- CSV / Excel

---

## 5. Project Workflow

```text
Data Collection
      ↓
Data Cleaning
      ↓
Data Preprocessing
      ↓
Exploratory Data Analysis
      ↓
Feature Engineering
      ↓
Train-Test Split
      ↓
Machine Learning
      ↓
Model Evaluation
      ↓
Performance Classification
      ↓
Prediction
      ↓
Attention Indicators
      ↓
Visualization Dashboard
      ↓
Reports and Insights