import pandas as pd

# Load the raw employee dataset
employees = pd.read_csv("data/raw/employees.csv")

# Dataset dimensions
print("Dataset shape:")
print(employees.shape)

# Column names
print("\nColumns:")
print(employees.columns.tolist())

# First 5 employees
print("\nFirst 5 rows:")
print(employees.head())

# Data types and missing values
print("\nDataset information:")
employees.info()




# Explore categorical HR variables
categorical_columns = [
    "Attrition",
    "BusinessTravel",
    "Department",
    "EducationField",
    "Gender",
    "JobRole",
    "MaritalStatus",
    "OverTime"
]

print("\n--- CATEGORICAL VARIABLES ---")

for column in categorical_columns:
    print(f"\n{column}:")
    print(employees[column].value_counts())