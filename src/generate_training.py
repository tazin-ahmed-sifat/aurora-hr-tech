import pandas as pd
import numpy as np

# --------------------------------------------------
# 1. SET RANDOM SEED
# --------------------------------------------------

# Makes our randomly generated data reproducible
np.random.seed(42)


# --------------------------------------------------
# 2. LOAD EMPLOYEE DATA
# --------------------------------------------------

employees = pd.read_csv("data/processed/employees.csv")

print(f"Employees loaded: {len(employees)}")


# --------------------------------------------------
# 3. DEFINE TRAINING COURSES
# --------------------------------------------------

training_courses = {
    "Data Protection & GDPR": "Compliance",
    "Health & Safety": "Compliance",
    "Cybersecurity Awareness": "Compliance",
    "Equality & Inclusion": "Compliance",
    "Customer Service Excellence": "Service",
    "Complaint Handling": "Service",
    "Leadership Essentials": "Leadership",
    "People Management": "Leadership",
    "Excel & Data Skills": "Digital",
    "HR Systems Training": "Digital"
}

print("\nAvailable training courses:")

for course, category in training_courses.items():
    print(f"{course} - {category}")


# --------------------------------------------------
# 4. GENERATE TRAINING RECORDS
# --------------------------------------------------

training_records = []

training_id = 1

for _, employee in employees.iterrows():

    # Each employee is assigned between 2 and 6 courses
    number_of_courses = np.random.randint(2, 7)

    # Select courses without giving the same course twice
    selected_courses = np.random.choice(
        list(training_courses.keys()),
        size=number_of_courses,
        replace=False
    )

    for course in selected_courses:

        training_records.append({
            "TrainingID": f"TRN{training_id:05d}",
            "EmployeeNumber": employee["EmployeeNumber"],
            "CourseName": course,
            "CourseCategory": training_courses[course]
        })

        training_id += 1


# Convert the generated records into a DataFrame
training = pd.DataFrame(training_records)

print("\nTraining records:")
print(training.head(10))

print(f"\nTotal training records: {len(training)}")


# --------------------------------------------------
# 5. ASSIGN TRAINING DATES
# --------------------------------------------------

start_date = pd.Timestamp("2025-01-01")
end_date = pd.Timestamp("2026-09-30")

date_range_days = (end_date - start_date).days

random_days = np.random.randint(
    0,
    date_range_days + 1,
    size=len(training)
)

training["AssignedDate"] = (
    start_date
    + pd.to_timedelta(random_days, unit="D")
)


# --------------------------------------------------
# 6. SET TRAINING DUE DATE
# --------------------------------------------------

# Employees have 30 days to complete assigned training
training["DueDate"] = (
    training["AssignedDate"]
    + pd.to_timedelta(30, unit="D")
)


# --------------------------------------------------
# 7. DECIDE WHICH TRAINING IS COMPLETED
# --------------------------------------------------

# Around 72% of training records are completed
completed_mask = (
    np.random.random(len(training)) < 0.72
)

training["CompletionDate"] = pd.NaT


# Completed training is finished between 1 and 30 days
# after it was assigned
training.loc[completed_mask, "CompletionDate"] = (
    training.loc[completed_mask, "AssignedDate"]
    + pd.to_timedelta(
        np.random.randint(
            1,
            31,
            size=completed_mask.sum()
        ),
        unit="D"
    )
)


# --------------------------------------------------
# 8. DETERMINE TRAINING STATUS
# --------------------------------------------------

# This represents the date our HR system checks compliance
check_date = pd.Timestamp("2026-10-02")

training["Status"] = "In Progress"

# Completed courses
training.loc[
    training["CompletionDate"].notna(),
    "Status"
] = "Completed"

# Not completed AND past the due date = overdue
overdue_mask = (
    training["CompletionDate"].isna()
    & (training["DueDate"] < check_date)
)

training.loc[
    overdue_mask,
    "Status"
] = "Overdue"


# --------------------------------------------------
# 9. GENERATE TRAINING SCORES
# --------------------------------------------------

training["Score"] = np.nan

training.loc[completed_mask, "Score"] = (
    np.random.randint(
        60,
        101,
        size=completed_mask.sum()
    )
)


# --------------------------------------------------
# 10. ADD TRAINING HOURS
# --------------------------------------------------

course_hours = {
    "Data Protection & GDPR": 2,
    "Health & Safety": 3,
    "Cybersecurity Awareness": 2,
    "Equality & Inclusion": 2,
    "Customer Service Excellence": 4,
    "Complaint Handling": 3,
    "Leadership Essentials": 6,
    "People Management": 6,
    "Excel & Data Skills": 5,
    "HR Systems Training": 4
}

training["TrainingHours"] = (
    training["CourseName"].map(course_hours)
)


# --------------------------------------------------
# 11. IDENTIFY MANDATORY TRAINING
# --------------------------------------------------

mandatory_courses = [
    "Data Protection & GDPR",
    "Health & Safety",
    "Cybersecurity Awareness",
    "Equality & Inclusion"
]

training["Mandatory"] = (
    training["CourseName"]
    .isin(mandatory_courses)
)


# --------------------------------------------------
# 12. IDENTIFY COMPLIANCE RISKS
# --------------------------------------------------

# A compliance risk exists when mandatory training
# has passed its due date and has not been completed
training["ComplianceRisk"] = (
    (training["Mandatory"] == True)
    & (training["Status"] == "Overdue")
)


# --------------------------------------------------
# 13. CHECK GENERATED DATA
# --------------------------------------------------

print("\nTraining status:")
print(training["Status"].value_counts())

print("\nCompliance risks:")
print(training["ComplianceRisk"].value_counts())

print("\nSample:")
print(
    training[
        [
            "TrainingID",
            "EmployeeNumber",
            "CourseName",
            "AssignedDate",
            "DueDate",
            "CompletionDate",
            "Status",
            "Mandatory",
            "ComplianceRisk"
        ]
    ].head(10)
)


# --------------------------------------------------
# 14. SAVE PROCESSED TRAINING DATA
# --------------------------------------------------

training.to_csv(
    "data/processed/training.csv",
    index=False
)

print("\nSaved training data.")
print(f"Final training dataset shape: {training.shape}")