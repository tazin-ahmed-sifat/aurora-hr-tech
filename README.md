# Aurora HR Technology Platform

Aurora is a fictional hotel group's HR technology platform built to explore how data, automation and responsible AI can support HR operations across a multi-country organisation.

The project brings together workforce data, recruitment, learning and compliance into a single SQLite data layer. Python is used for data processing, workflow automation and machine learning, while SQL is used to analyse HR performance across hotels and regions.

## Project Goals

The project was designed to:

- Build an integrated HR data model across multiple HR processes
- Analyse recruitment performance and time-to-hire
- Monitor employee learning and mandatory training compliance
- Automate the identification and prioritisation of overdue compliance training
- Explore employee attrition patterns using interpretable machine learning
- Apply responsible AI principles to HR analytics
- Prepare management-level HR metrics for visualisation in Power BI

## Use of AI Tools

Large Language Models (LLMs) were used during the development of this project as a supporting tool for:

- Brainstorming and refining the project concept
- Discussing system architecture and implementation approaches
- Troubleshooting coding errors and development hurdles
- Explaining unfamiliar concepts and alternative solutions
- Reviewing and improving code during development

The project was developed iteratively, with implementation decisions, testing, debugging and validation carried out throughout the development process. AI-generated suggestions were reviewed and adapted rather than treated as automatically correct.

## System Architecture

Aurora follows a simple HR technology pipeline:

```text
HRIS / Workforce Data
        │
        ├── Recruitment Data
        │
        └── Learning & Training Data
        │
        ▼
Data Processing & Transformation
        │
        │  Python / pandas
        ▼
SQLite HR Database
        │
        ├── employees
        ├── hotels
        ├── recruitment
        ├── training
        └── attrition_risk
        │
        ▼
SQL Analytics
        │
        ├── Recruitment Performance
        ├── Training Compliance
        └── Workforce Risk
        │
        ├─────────────────────┐
        ▼                     ▼
Workflow Automation     Responsible AI
Compliance Alerts       Attrition Risk Model
        │                     │
        └──────────┬──────────┘
                   ▼
             Power BI
        Management Dashboard
```



## Core Modules

### 1. Workforce / HRIS

The workforce module provides the core employee dataset used throughout the platform. Employee records are transformed and assigned across 15 fictional Aurora hotels in the EMEA region.

It provides a common workforce layer that connects recruitment, learning, compliance and workforce analytics.

### 2. Recruitment Analytics

A recruitment dataset of 5,000 applications was created to model the hiring process across Aurora hotels.

The module supports analysis of:

- Recruitment funnel performance
- Applications and hires by recruitment source
- Source-level hire rates
- Time-to-hire
- Recruitment performance by hotel and region

Recruitment data is stored in SQLite and analysed using SQL and Python.

### 3. Learning & Compliance

The learning module contains employee training assignments across compliance, service, leadership and digital courses.

Training records track:

- Assigned and due dates
- Completion status
- Training scores and hours
- Mandatory training requirements
- Overdue compliance training

This allows compliance performance to be analysed across hotels and regions.

### 4. Compliance Automation

A Python workflow automatically identifies overdue mandatory training and calculates how long each case has been overdue.

Cases are classified into Low, Medium, High or Critical priority levels and mapped to recommended actions such as employee reminders, line-manager notifications or HR escalation.

The workflow generates a structured compliance action report for management reporting.

### 5. Responsible Attrition AI

An interpretable logistic regression model was developed to explore patterns associated with employee attrition.

On the held-out test set, the selected model achieved:

- ROC-AUC: **0.833**
- Attrition recall: **0.74**
- Attrition precision: **0.39**
- Attrition F1-score: **0.51**

The model is designed as a decision-support and workforce analytics tool rather than an automated employment decision system.

Age was evaluated during development and then removed from the final model. Predictive performance was maintained after its removal. Gender and marital status are also excluded from the prediction features.

Model coefficients are used to examine factors associated with predicted attrition risk. These relationships are treated as predictive associations rather than evidence of causation.

The platform uses a fictional 15-hotel EMEA organisation to demonstrate how information from different HR processes can be integrated into a common data model and used for reporting, automation and decision support.


## Technology Stack

- **Python** — data processing, automation and machine learning
- **pandas / NumPy** — data transformation and synthetic data generation
- **scikit-learn** — preprocessing, logistic regression and model evaluation
- **SQLite** — integrated HR data storage
- **SQL** — recruitment, compliance and workforce risk analysis
- **Git & GitHub** — version control and project management
- **Power BI** — management dashboards and visualisation *(planned)*

## Repository Structure

```text
aurora-hr-tech/
│
├── data/
│   ├── raw/                 # Source workforce dataset
│   └── processed/           # Generated and transformed datasets
│
├── src/
│   ├── explore_data.py
│   ├── transform_employees.py
│   ├── generate_hotels.py
│   ├── generate_recruitment.py
│   ├── analyse_recruitment.py
│   ├── generate_training.py
│   ├── compliance_alerts.py
│   ├── attrition_model.py
│   └── create_database.py
│
├── sql/
│   ├── 01_recruitment_analysis.sql
│   ├── 02_training_analysis.sql
│   └── 03_attrition_analysis.sql
│
├── dashboard/               # Power BI development
├── docs/                    # Project documentation
├── requirements.txt
└── README.md
```

Generated datasets and the local SQLite database are excluded from version control and can be recreated through the project scripts.