import subprocess
import sys

# --------------------------------------------------
# AURORA HR TECHNOLOGY PLATFORM
# Full data platform build pipeline
# --------------------------------------------------

scripts = [
    "src/transform_employees.py",
    "src/generate_hotels.py",
    "src/generate_recruitment.py",
    "src/generate_training.py",
    "src/attrition_model.py",
    "src/create_database.py",
    "src/compliance_alerts.py",
]

print("\n========================================")
print("   AURORA HR PLATFORM BUILD STARTED")
print("========================================\n")

for script in scripts:

    print(f"Running: {script}")

    subprocess.run(
        [sys.executable, script],
        check=True
    )

    print(f"Completed: {script}\n")

print("========================================")
print("   AURORA BUILD COMPLETED SUCCESSFULLY")
print("========================================")