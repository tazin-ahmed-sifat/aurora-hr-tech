import pandas as pd
import sqlite3


# Load the processed datasets
employees = pd.read_csv("data/processed/employees.csv")

hotels = pd.read_csv("data/processed/hotels.csv")

recruitment = pd.read_csv("data/processed/recruitment.csv")

training = pd.read_csv("data/processed/training.csv")


# Create/connect to the Aurora HR database
connection = sqlite3.connect("data/aurora_hr.db")


# Create employee table
employees.to_sql("employees", connection, if_exists="replace", index=False)


# Create hotel table
hotels.to_sql("hotels", connection, if_exists="replace", index=False)


# Create recruitment table
recruitment.to_sql("recruitment", connection, if_exists="replace", index=False)


# Create training table
training.to_sql("training", connection, if_exists="replace", index=False)


# Close the database connection
connection.close()

print("Aurora HR database created successfully.")
