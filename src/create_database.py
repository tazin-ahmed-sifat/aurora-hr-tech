import pandas as pd
import sqlite3


# --------------------------------------------------
# 1. LOAD PROCESSED DATA
# --------------------------------------------------

employees = pd.read_csv(
    "data/processed/employees.csv"
)

hotels = pd.read_csv(
    "data/processed/hotels.csv"
)

recruitment = pd.read_csv(
    "data/processed/recruitment.csv"
)

training = pd.read_csv(
    "data/processed/training.csv"
)

attrition_risk = pd.read_csv(
    "data/processed/attrition_risk.csv"
)


# --------------------------------------------------
# 2. CONNECT TO SQLITE DATABASE
# --------------------------------------------------

connection = sqlite3.connect(
    "data/aurora_hr.db"
)


# --------------------------------------------------
# 3. CREATE DATABASE TABLES
# --------------------------------------------------

employees.to_sql(
    "employees",
    connection,
    if_exists="replace",
    index=False
)

hotels.to_sql(
    "hotels",
    connection,
    if_exists="replace",
    index=False
)

recruitment.to_sql(
    "recruitment",
    connection,
    if_exists="replace",
    index=False
)

training.to_sql(
    "training",
    connection,
    if_exists="replace",
    index=False
)

attrition_risk.to_sql(
    "attrition_risk",
    connection,
    if_exists="replace",
    index=False
)


# --------------------------------------------------
# 4. CLOSE DATABASE CONNECTION
# --------------------------------------------------

connection.close()

print("Aurora HR database created successfully.")