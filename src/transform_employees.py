import pandas as pd
import random
import numpy as np

np.random.seed(42)

# Makes synthetic data reproducible
random.seed(42)

# Load the original IBM HR dataset
employees = pd.read_csv("data/raw/employees.csv")


# Create a copy so we never modify the raw dataset
aurora_employees = employees.copy()

print(aurora_employees.head())

# Convert IBM departments into hospitality departments
department_map = {
    "Research & Development": "Hotel Operations",
    "Sales": "Commercial",
    "Human Resources": "Human Resources"
}

aurora_employees["Department"] = (
    aurora_employees["Department"].replace(department_map)
)

# Check the new departments
print("\nAurora departments:")
print(aurora_employees["Department"].value_counts())

# Possible job roles for each Aurora department
job_roles = {
    "Hotel Operations": [
        "Front Office Associate",
        "Food & Beverage Associate",
        "Guest Services Associate",
        "Housekeeping Associate",
        "Operations Supervisor",
        "Hotel Operations Manager"
    ],

    "Commercial": [
        "Sales Executive",
        "Sales Representative",
        "Marketing Executive",
        "Revenue Analyst"
    ],

    "Human Resources": [
        "HR Specialist",
        "HR Coordinator",
        "HR Manager"
    ]
}

# Assign a realistic job role based on department and seniority
def assign_job_role(row):

    department = row["Department"]
    level = row["JobLevel"]

    if department == "Hotel Operations":
        if level == 1:
            return random.choice([
                "Front Office Associate",
                "Food & Beverage Associate",
                "Housekeeping Associate",
                "Guest Services Associate"
    ])
        elif level == 2:
            return "Operations Supervisor"
        elif level == 3:
            return "Assistant Hotel Manager"
        else:
            return "Hotel Manager"

    elif department == "Commercial":
        if level == 1:
            return "Sales Representative"
        elif level == 2:
            return "Sales Executive"
        elif level == 3:
            return "Revenue Manager"
        else:
            return "Commercial Director"

    elif department == "Human Resources":
        if level == 1:
            return "HR Coordinator"
        elif level == 2:
            return "HR Specialist"
        elif level == 3:
            return "HR Manager"
        else:
            return "HR Director"


# Apply the job role function to every employee
aurora_employees["JobRole"] = aurora_employees.apply(
    assign_job_role,
    axis=1
)

# Check the new job roles
print("\nAurora job roles:")
print(aurora_employees["JobRole"].value_counts())


# Assign employees to Aurora hotel properties

hotel_ids = [
    "AH001", "AH002", "AH003", "AH004", "AH005",
    "AH006", "AH007", "AH008", "AH009", "AH010",
    "AH011", "AH012", "AH013", "AH014", "AH015"
]

# Larger properties receive a larger share of employees
hotel_weights = [
    0.12, 0.07, 0.06, 0.09, 0.08,
    0.06, 0.06, 0.06, 0.10, 0.06,
    0.05, 0.06, 0.05, 0.04, 0.04
]

aurora_employees["HotelID"] = np.random.choice(
    hotel_ids,
    size=len(aurora_employees),
    p=hotel_weights
)

print("\nEmployees per hotel:")
print(
    aurora_employees["HotelID"]
    .value_counts()
    .sort_index()
)

size=len(aurora_employees)


# Save the transformed Aurora employee dataset
aurora_employees.to_csv(
    "data/processed/employees.csv",
    index=False
)

print("\nSaved transformed employee data.")