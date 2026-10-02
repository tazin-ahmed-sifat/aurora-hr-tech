import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score
)


# --------------------------------------------------
# 1. LOAD EMPLOYEE DATA
# --------------------------------------------------

employees = pd.read_csv(
    "data/processed/employees.csv"
)

print(f"Employees loaded: {len(employees)}")


# --------------------------------------------------
# 2. DEFINE TARGET
# --------------------------------------------------

# Convert Attrition from Yes/No into 1/0
# 0 = stayed
# 1 = left
employees["AttritionTarget"] = (
    employees["Attrition"]
    .map({
        "No": 0,
        "Yes": 1
    })
)

print("\nAttrition distribution:")
print(
    employees["AttritionTarget"]
    .value_counts()
)

print("\nAttrition rate:")
print(
    employees["AttritionTarget"]
    .mean()
)


# --------------------------------------------------
# 3. SELECT MODEL FEATURES
# --------------------------------------------------

features = [
    "Age",
    "BusinessTravel",
    "Department",
    "DistanceFromHome",
    "EnvironmentSatisfaction",
    "JobInvolvement",
    "JobLevel",
    "JobRole",
    "JobSatisfaction",
    "MonthlyIncome",
    "NumCompaniesWorked",
    "OverTime",
    "PercentSalaryHike",
    "RelationshipSatisfaction",
    "StockOptionLevel",
    "TotalWorkingYears",
    "TrainingTimesLastYear",
    "WorkLifeBalance",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "YearsWithCurrManager"
]

# X = information the model learns from
X = employees[features]

# y = outcome we want the model to predict
y = employees["AttritionTarget"]


# --------------------------------------------------
# 4. CHECK MODEL DATA
# --------------------------------------------------

print("\nFeature dataset shape:")
print(X.shape)

print("\nTarget shape:")
print(y.shape)

print("\nFeature types:")
print(X.dtypes)


# --------------------------------------------------
# 5. SPLIT DATA INTO TRAINING AND TEST SETS
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,

    # Keep roughly the same attrition percentage
    # in both training and testing data
    stratify=y
)

print("\nTraining employees:")
print(len(X_train))

print("\nTesting employees:")
print(len(X_test))


# --------------------------------------------------
# 6. DEFINE FEATURE TYPES
# --------------------------------------------------

# Text/category columns
categorical_features = [
    "BusinessTravel",
    "Department",
    "JobRole",
    "OverTime"
]

# Numerical columns
numerical_features = [
    "Age",
    "DistanceFromHome",
    "EnvironmentSatisfaction",
    "JobInvolvement",
    "JobLevel",
    "JobSatisfaction",
    "MonthlyIncome",
    "NumCompaniesWorked",
    "PercentSalaryHike",
    "RelationshipSatisfaction",
    "StockOptionLevel",
    "TotalWorkingYears",
    "TrainingTimesLastYear",
    "WorkLifeBalance",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "YearsWithCurrManager"
]


# --------------------------------------------------
# 7. PREPROCESS MODEL FEATURES
# --------------------------------------------------

preprocessor = ColumnTransformer(
    transformers=[

        # Convert text categories into numerical columns
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        ),

        # Standardise numerical variables
        (
            "numerical",
            StandardScaler(),
            numerical_features
        )
    ]
)

print("\nPreprocessor created successfully.")


# --------------------------------------------------
# 8. BUILD ATTRITION MODEL
# --------------------------------------------------

# Pipeline automatically:
# 1. Preprocesses the data
# 2. Sends the processed data into the model

model = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,

                # Attrition cases are much less common
                # than employees who stayed
                class_weight="balanced"
            )
        )
    ]
)

print("\nModel created successfully.")


# --------------------------------------------------
# 9. TRAIN MODEL
# --------------------------------------------------

model.fit(
    X_train,
    y_train
)

print("\nModel trained successfully.")


# --------------------------------------------------
# 10. MAKE PREDICTIONS
# --------------------------------------------------

# Predict whether employees stayed or left
y_pred = model.predict(
    X_test
)

# Get the predicted probability of attrition
y_probability = (
    model.predict_proba(X_test)[:, 1]
)


# --------------------------------------------------
# 11. EVALUATE MODEL
# --------------------------------------------------

print("\n--- MODEL PERFORMANCE ---")

print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_test,
        y_pred
    )
)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred
    )
)

print("ROC-AUC Score:")
print(
    round(
        roc_auc_score(
            y_test,
            y_probability
        ),
        3
    )
)


# --------------------------------------------------
# 12. EXPLAIN MODEL PREDICTIONS
# --------------------------------------------------

# Get the names of all features after preprocessing
feature_names = (
    model
    .named_steps["preprocessor"]
    .get_feature_names_out()
)

# Get the coefficients learned by Logistic Regression
coefficients = (
    model
    .named_steps["classifier"]
    .coef_[0]
)

# Put feature names and coefficients into a dataframe
feature_importance = pd.DataFrame({
    "Feature": feature_names,
    "Coefficient": coefficients
})

# Sort from strongest positive association
# to strongest negative association
feature_importance = (
    feature_importance
    .sort_values(
        "Coefficient",
        ascending=False
    )
)

print("\n--- FEATURES ASSOCIATED WITH HIGHER ATTRITION ---")

print(
    feature_importance.head(10)
)

print("\n--- FEATURES ASSOCIATED WITH LOWER ATTRITION ---")

print(
    feature_importance.tail(10)
    .sort_values("Coefficient")
)
# --------------------------------------------------
# 13. RESPONSIBLE AI TEST - REMOVE AGE
# --------------------------------------------------

# Create a second feature set without Age
features_without_age = [
    feature for feature in features
    if feature != "Age"
]

X_no_age = employees[features_without_age]

# Split the data again using the same settings
X_train_no_age, X_test_no_age, y_train_no_age, y_test_no_age = train_test_split(
    X_no_age,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# Numerical features without Age
numerical_features_no_age = [
    feature for feature in numerical_features
    if feature != "Age"
]


# Create preprocessing for the no-age model
preprocessor_no_age = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        ),
        (
            "numerical",
            StandardScaler(),
            numerical_features_no_age
        )
    ]
)


# Build the second model
model_no_age = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor_no_age
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced"
            )
        )
    ]
)


# Train the model
model_no_age.fit(
    X_train_no_age,
    y_train_no_age
)


# Get predictions
y_pred_no_age = model_no_age.predict(
    X_test_no_age
)

y_probability_no_age = (
    model_no_age.predict_proba(X_test_no_age)[:, 1]
)


# --------------------------------------------------
# 14. COMPARE MODELS
# --------------------------------------------------

auc_with_age = roc_auc_score(
    y_test,
    y_probability
)

auc_without_age = roc_auc_score(
    y_test_no_age,
    y_probability_no_age
)

print("\n--- RESPONSIBLE AI: AGE COMPARISON ---")

print(
    f"ROC-AUC with Age:    {auc_with_age:.3f}"
)

print(
    f"ROC-AUC without Age: {auc_without_age:.3f}"
)

print("\nNo-Age Model Classification Report:")

print(
    classification_report(
        y_test_no_age,
        y_pred_no_age
    )
)


# --------------------------------------------------
# 15. TRAIN FINAL APPROVED MODEL
# --------------------------------------------------

# The no-age model is our approved model because
# removing Age maintained predictive performance.

final_model = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor_no_age
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced"
            )
        )
    ]
)

# Train using all available employee records
final_model.fit(
    X_no_age,
    y
)

print("\nFinal no-age model trained successfully.")


# --------------------------------------------------
# 16. GENERATE ATTRITION RISK OUTPUT
# --------------------------------------------------

# Get attrition probability for every employee
risk_probabilities = (
    final_model.predict_proba(X_no_age)[:, 1]
)

# Create an output table with useful HR information
attrition_risk = employees[
    [
        "EmployeeNumber",
        "HotelID",
        "Department",
        "JobRole"
    ]
].copy()

# Add predicted attrition probability
attrition_risk["AttritionRisk"] = (
    risk_probabilities.round(3)
)


# --------------------------------------------------
# 17. CREATE RISK BANDS
# --------------------------------------------------

def assign_risk_band(probability):

    if probability >= 0.70:
        return "High"

    elif probability >= 0.40:
        return "Medium"

    else:
        return "Low"


attrition_risk["RiskBand"] = (
    attrition_risk["AttritionRisk"]
    .apply(assign_risk_band)
)


# --------------------------------------------------
# 18. SAVE RISK REPORT
# --------------------------------------------------

attrition_risk.to_csv(
    "data/processed/attrition_risk.csv",
    index=False
)

print("\n--- ATTRITION RISK OUTPUT ---")

print(
    attrition_risk["RiskBand"]
    .value_counts()
)

print("\nHighest predicted risk patterns:")

print(
    attrition_risk
    .sort_values(
        "AttritionRisk",
        ascending=False
    )
    .head(10)
)

print(
    "\nAttrition risk report saved successfully."
)