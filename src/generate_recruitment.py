import pandas as pd
import numpy as np


# --------------------------------------------------
# 1. SETUP
# --------------------------------------------------

# Make random generation reproducible
np.random.seed(42)

# Load Aurora employee and hotel data
employees = pd.read_csv("data/processed/employees.csv")
hotels = pd.read_csv("data/processed/hotels.csv")

print(f"Employees loaded: {len(employees)}")
print(f"Hotels loaded: {len(hotels)}")


# --------------------------------------------------
# 2. CREATE APPLICATION IDs
# --------------------------------------------------

# Number of job applications to simulate
num_applications = 5000

# Create unique application IDs:
# APP00001, APP00002, APP00003, etc.
application_ids = [
    f"APP{i:05d}"
    for i in range(1, num_applications + 1)
]

# Create the recruitment applications table
applications = pd.DataFrame({
    "ApplicationID": application_ids
})

print(f"\nTotal applications: {len(applications)}")


# --------------------------------------------------
# 3. ASSIGN APPLICATIONS TO HOTELS
# --------------------------------------------------

# Calculate each hotel's share of Aurora employees
hotel_weights = (
    employees["HotelID"]
    .value_counts(normalize=True)
    .reindex(hotels["HotelID"])
)

# Larger hotels receive proportionally more applications
applications["HotelID"] = np.random.choice(
    hotels["HotelID"],
    size=num_applications,
    p=hotel_weights
)

print("\nApplications per hotel:")
print(
    applications["HotelID"]
    .value_counts()
    .sort_index()
)


# --------------------------------------------------
# 4. ASSIGN JOB ROLES
# --------------------------------------------------

# --------------------------------------------------
# 4. ASSIGN JOB ROLES
# --------------------------------------------------

def assign_job_role(hotel_id):

    # Get employees who work at this hotel
    hotel_employees = employees[
        employees["HotelID"] == hotel_id
    ]

    # Calculate the job role distribution for this hotel
    role_weights = (
        hotel_employees["JobRole"]
        .value_counts(normalize=True)
    )

    # Choose a job role using this hotel's workforce distribution
    return np.random.choice(
        role_weights.index,
        p=role_weights.values
    )


# Assign a job role based on the application's hotel
applications["JobRole"] = (
    applications["HotelID"]
    .apply(assign_job_role)
)

print("\nApplications by job role:")
print(applications["JobRole"].value_counts())


# --------------------------------------------------
# 5. ASSIGN RECRUITMENT SOURCES
# --------------------------------------------------

# Recruitment channels candidates can apply through
recruitment_sources = [
    "Careers Website",
    "LinkedIn",
    "Employee Referral",
    "Recruitment Agency",
    "University",
    "Indeed"
]

# Probability of an application coming from each source
source_weights = [
    0.30,  # Careers Website
    0.25,  # LinkedIn
    0.15,  # Employee Referral
    0.10,  # Recruitment Agency
    0.08,  # University
    0.12   # Indeed
]

# Assign a recruitment source to every application
applications["Source"] = np.random.choice(
    recruitment_sources,
    size=num_applications,
    p=source_weights
)

print("\nApplications by recruitment source:")
print(applications["Source"].value_counts())


# --------------------------------------------------
# 6. GENERATE APPLICATION DATES
# --------------------------------------------------

# Applications are submitted between these dates
start_date = pd.Timestamp("2025-01-01")
end_date = pd.Timestamp("2026-09-30")

# Calculate number of possible days
date_range_days = (end_date - start_date).days

# Generate random number of days after start_date
random_days = np.random.randint(
    0,
    date_range_days + 1,
    size=num_applications
)

# Create application dates
applications["ApplicationDate"] = (
    start_date
    + pd.to_timedelta(random_days, unit="D")
)

print("\nApplication date range:")
print(applications["ApplicationDate"].min())
print(applications["ApplicationDate"].max())


# --------------------------------------------------
# 7. GENERATE RECRUITMENT OUTCOMES
# --------------------------------------------------

# Possible final outcomes
application_statuses = [
    "Rejected",
    "Withdrew",
    "Interviewed",
    "Offered",
    "Hired"
]

# Synthetic Aurora assumptions:
# different recruitment sources have different
# probabilities of reaching each final outcome.
#
# Order:
# Rejected, Withdrew, Interviewed, Offered, Hired
source_status_weights = {
    "Careers Website": [
        0.49, 0.10, 0.20, 0.08, 0.13
    ],

    "LinkedIn": [
        0.52, 0.10, 0.20, 0.08, 0.10
    ],

    "Employee Referral": [
        0.42, 0.08, 0.20, 0.10, 0.20
    ],

    "Recruitment Agency": [
        0.46, 0.09, 0.20, 0.10, 0.15
    ],

    "University": [
        0.48, 0.10, 0.20, 0.08, 0.14
    ],

    "Indeed": [
        0.56, 0.11, 0.18, 0.07, 0.08
    ]
}


# Function for assigning an outcome based on source
def assign_status(source):

    return np.random.choice(
        application_statuses,
        p=source_status_weights[source]
    )


# Apply the function to every application
applications["Status"] = (
    applications["Source"]
    .apply(assign_status)
)

print("\nRecruitment outcomes:")
print(applications["Status"].value_counts())

print("\nRecruitment outcome percentages:")
print(
    applications["Status"]
    .value_counts(normalize=True)
    .mul(100)
    .round(1)
)


# --------------------------------------------------
# 8. GENERATE INTERVIEW DATES
# --------------------------------------------------

# Start with empty date columns
applications["InterviewDate"] = pd.NaT
applications["OfferDate"] = pd.NaT
applications["HireDate"] = pd.NaT

# Candidates who reached at least interview stage
interview_mask = applications["Status"].isin([
    "Interviewed",
    "Offered",
    "Hired"
])

# Interviews happen 3–14 days after application
applications.loc[interview_mask, "InterviewDate"] = (
    applications.loc[
        interview_mask,
        "ApplicationDate"
    ]
    + pd.to_timedelta(
        np.random.randint(
            3,
            15,
            size=interview_mask.sum()
        ),
        unit="D"
    )
)


# --------------------------------------------------
# 9. GENERATE OFFER DATES
# --------------------------------------------------

# Candidates who reached at least offer stage
offer_mask = applications["Status"].isin([
    "Offered",
    "Hired"
])

# Offers happen 2–7 days after interview
applications.loc[offer_mask, "OfferDate"] = (
    applications.loc[
        offer_mask,
        "InterviewDate"
    ]
    + pd.to_timedelta(
        np.random.randint(
            2,
            8,
            size=offer_mask.sum()
        ),
        unit="D"
    )
)


# --------------------------------------------------
# 10. GENERATE HIRE DATES
# --------------------------------------------------

# Only successful candidates receive a hire date
hire_mask = applications["Status"] == "Hired"

# Hire/start date happens 7–30 days after offer
applications.loc[hire_mask, "HireDate"] = (
    applications.loc[
        hire_mask,
        "OfferDate"
    ]
    + pd.to_timedelta(
        np.random.randint(
            7,
            31,
            size=hire_mask.sum()
        ),
        unit="D"
    )
)


# --------------------------------------------------
# 11. CALCULATE TIME TO HIRE
# --------------------------------------------------

# Number of days from application to hire
applications["TimeToHireDays"] = (
    applications["HireDate"]
    - applications["ApplicationDate"]
).dt.days

average_time_to_hire = (
    applications["TimeToHireDays"].mean()
)

print(
    f"\nAverage time to hire: "
    f"{average_time_to_hire:.1f} days"
)


# --------------------------------------------------
# 12. FINAL DATA CHECK
# --------------------------------------------------

print("\nRecruitment dataset preview:")

print(
    applications[
        [
            "ApplicationID",
            "HotelID",
            "JobRole",
            "Source",
            "ApplicationDate",
            "Status",
            "InterviewDate",
            "OfferDate",
            "HireDate",
            "TimeToHireDays"
        ]
    ].head(10)
)

print("\nFinal dataset shape:")
print(applications.shape)


# --------------------------------------------------
# 13. SAVE DATASET
# --------------------------------------------------

applications.to_csv(
    "data/processed/recruitment.csv",
    index=False
)

print("\nSaved recruitment data.")