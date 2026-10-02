import pandas as pd
import sqlite3


# --------------------------------------------------
# 1. CONNECT TO THE HR DATABASE
# --------------------------------------------------

connection = sqlite3.connect(
    "data/aurora_hr.db"
)


# --------------------------------------------------
# 2. FIND OVERDUE MANDATORY TRAINING
# --------------------------------------------------

query = """
SELECT
    t.TrainingID,
    e.EmployeeNumber,
    e.JobRole,
    e.Department,
    h.HotelName,
    h.Country,
    h.Region,
    t.CourseName,
    t.AssignedDate,
    t.DueDate,
    t.Status

FROM training AS t

JOIN employees AS e
    ON t.EmployeeNumber = e.EmployeeNumber

JOIN hotels AS h
    ON e.HotelID = h.HotelID

WHERE t.ComplianceRisk = 1
"""


alerts = pd.read_sql_query(
    query,
    connection
)

connection.close()


# --------------------------------------------------
# 3. CHECK THE RESULTS
# --------------------------------------------------

print("--- COMPLIANCE ALERTS ---")

print(f"\nTotal alerts: {len(alerts)}")

print("\nFirst 10 alerts:")
print(alerts.head(10))


# --------------------------------------------------
# 4. CALCULATE DAYS OVERDUE
# --------------------------------------------------

# Date the HR compliance check is being run
check_date = pd.Timestamp("2026-10-02")

# Convert DueDate into a proper date
alerts["DueDate"] = pd.to_datetime(
    alerts["DueDate"]
)

# Calculate how many days the training
# has been overdue
alerts["DaysOverdue"] = (
    check_date
    - alerts["DueDate"]
).dt.days


# --------------------------------------------------
# 5. ASSIGN ALERT PRIORITY
# --------------------------------------------------

def assign_priority(days):

    if days >= 365:
        return "Critical"

    elif days >= 180:
        return "High"

    elif days >= 90:
        return "Medium"

    else:
        return "Low"


# Apply the priority rule to every alert
alerts["Priority"] = (
    alerts["DaysOverdue"]
    .apply(assign_priority)
)


# --------------------------------------------------
# 6. SHOW PRIORITY SUMMARY
# --------------------------------------------------

print("\n--- ALERT PRIORITIES ---")

print(
    alerts["Priority"]
    .value_counts()
)


# --------------------------------------------------
# 7. SHOW HIGHEST PRIORITY CASES
# --------------------------------------------------

print("\nHighest priority cases:")

priority_alerts = (
    alerts[
        [
            "EmployeeNumber",
            "HotelName",
            "CourseName",
            "DueDate",
            "DaysOverdue",
            "Priority"
        ]
    ]
    .sort_values(
        "DaysOverdue",
        ascending=False
    )
)

print(
    priority_alerts.head(10)
)

# --------------------------------------------------
# 8. ASSIGN HR ACTION
# --------------------------------------------------

def assign_action(priority):

    if priority == "Critical":
        return "Escalate to HR Manager"

    elif priority == "High":
        return "Notify HR Team"

    elif priority == "Medium":
        return "Notify Line Manager"

    else:
        return "Send Employee Reminder"


alerts["RecommendedAction"] = (
    alerts["Priority"]
    .apply(assign_action)
)
# --------------------------------------------------
# 9. GENERATE HR ACTION REPORT
# --------------------------------------------------

# Define the order in which HR should handle alerts
priority_order = {
    "Critical": 1,
    "High": 2,
    "Medium": 3,
    "Low": 4
}

# Create a temporary numeric ranking for sorting
alerts["PriorityRank"] = (
    alerts["Priority"]
    .map(priority_order)
)

# Sort by priority first, then by days overdue
action_report = alerts.sort_values(
    by=["PriorityRank", "DaysOverdue"],
    ascending=[True, False]
)

# Remove the temporary sorting column
action_report = action_report.drop(
    columns=["PriorityRank"]
)

# Save the report
action_report.to_csv(
    "data/processed/compliance_action_report.csv",
    index=False
)

print("\n--- HR ACTION REPORT ---")
print(
    f"Report generated with "
    f"{len(action_report)} cases."
)

print(
    "Saved to: "
    "data/processed/compliance_action_report.csv"
)
# --------------------------------------------------
# 10. GENERATE MANAGEMENT SUMMARY
# --------------------------------------------------

total_alerts = len(action_report)

critical_alerts = (
    action_report["Priority"] == "Critical"
).sum()

high_alerts = (
    action_report["Priority"] == "High"
).sum()

# Find hotels with the most compliance risks
hotel_risks = (
    action_report
    .groupby("HotelName")
    .size()
    .sort_values(ascending=False)
)

print("\n--- MANAGEMENT SUMMARY ---")

print(f"Total compliance risks: {total_alerts}")
print(f"Critical risks: {critical_alerts}")
print(f"High risks: {high_alerts}")

print("\nHotels with most compliance risks:")
print(hotel_risks.head(5))