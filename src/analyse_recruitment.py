import pandas as pd

# Load the recruitment dataset
applications = pd.read_csv(
    "data/processed/recruitment.csv",
    parse_dates=[
        "ApplicationDate",
        "InterviewDate",
        "OfferDate",
        "HireDate"
    ]
)

# Check that the data loaded correctly
print("Recruitment dataset shape:")
print(applications.shape)

print("\nFirst 5 rows:")
print(applications.head())
# Total number of applications
total_applications = len(applications)

# Number who reached each recruitment stage
interviewed = applications["InterviewDate"].notna().sum()
offered = applications["OfferDate"].notna().sum()
hired = applications["HireDate"].notna().sum()

print("\n--- RECRUITMENT FUNNEL ---")

print(f"Applications: {total_applications}")
print(f"Interviewed: {interviewed}")
print(f"Offered: {offered}")
print(f"Hired: {hired}")


# Calculate recruitment conversion rates
application_to_interview = interviewed / total_applications * 100
interview_to_offer = offered / interviewed * 100
offer_to_hire = hired / offered * 100
overall_hire_rate = hired / total_applications * 100

print("\n--- CONVERSION RATES ---")

print(f"Application → Interview: {application_to_interview:.1f}%")
print(f"Interview → Offer: {interview_to_offer:.1f}%")
print(f"Offer → Hire: {offer_to_hire:.1f}%")
print(f"Overall Hire Rate: {overall_hire_rate:.1f}%")

# Count applications from each recruitment source
source_analysis = applications.groupby("Source").agg(
    Applications=("ApplicationID", "count"),
    Hires=("HireDate", "count")
)

print("\n--- RECRUITMENT SOURCE ANALYSIS ---")
print(source_analysis)

# Calculate hire rate for each recruitment source
source_analysis["HireRate"] = (
    source_analysis["Hires"]
    / source_analysis["Applications"]
    * 100
)

# Round to 1 decimal place
source_analysis["HireRate"] = source_analysis["HireRate"].round(1)

print("\n--- SOURCE PERFORMANCE ---")
print(source_analysis.sort_values("HireRate", ascending=False))



# Calculate average time to hire for each recruitment source
time_to_hire_by_source = (
    applications[
        applications["Status"] == "Hired"
    ]
    .groupby("Source")["TimeToHireDays"]
    .mean()
    .round(1)
)

print("\n--- AVERAGE TIME TO HIRE BY SOURCE ---")
print(
    time_to_hire_by_source
    .sort_values()
)