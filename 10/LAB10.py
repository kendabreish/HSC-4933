#########################################################
# kaplan Meier Log rate and Cox PH tests                #
# Kenda S Breish # HSC4933.005 # 11/1/2026              #
# This script uses two heart failure dataset to perform #
# a Keplan Meir log rate test and Cox proportional      #
# hazards regression. it compares hospital readmission  #
#########################################################

import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import logrank_test

# PART 1. KAPLAN-MEIER AND LOG-RANK ANALYSIS

# Import the Kaplan-Meier dataset
km_data = pd.read_csv("km_logrank_readmission.csv")

# Review the dataset
print("Kaplan_Meier Dataset:")
print(km_data.head())
print(km_data.dtypes)

# Remove records with missing information
km_data.dropna(
    subset=["treatment_group", "time_days", "readmitted", "sex"],
    inplace=True
)

# Remove extra spaces from group names
km_data["treatment_group"] = km_data["treatment_group"].str.strip()

# Divide patients by treatment type
standard = km_data[
    km_data["treatment_group"].str.contains("Standard",case=False, na=False)
]

telehealth = km_data[
    km_data["treatment_group"].str.contains("TeleHealth",case=False, na=False)
]

# Print the number of patients in each group
print("\nNumber of Standard Care Patients:",len(standard))
print("Number of TeleHealth Patients:",len(telehealth))

# Compare readmission times between treatment groups
treatment_test = logrank_test(
    standard["time_days"],
    telehealth["time_days"],
    event_observed_A=standard["readmitted"],
    event_observed_B=telehealth["readmitted"],
)

print("\nLog-Rank Results: Standard vs Telehealth")
print(treatment_test.summary)

# Compare readmission times by sex
male = km_data[km_data["sex"] == "Male"]
female = km_data[km_data["sex"] == "Female"]

gender_test = logrank_test(
    male["time_days"],
    female["time_days"],
    event_observed_A=male["readmitted"],
    event_observed_B=female["readmitted"],
)

print("\nLog-Rank Results: Male vs Female")
print(gender_test.summary)

# Plot Kaplan-Meier survival curves
kmf = KaplanMeierFitter()

plt.figure(figsize=(9, 6))

# Standard care survival curve
kmf.fit(
    durations=standard["time_days"],
    event_observed=standard["readmitted"],
    label="Standard Care",
)
kmf.plot_survival_function(ci_show=True)

# Telehealth survival curve
kmf.fit(
    durations=telehealth["time_days"],
    event_observed=telehealth["readmitted"],
    label="TeleHealth Follow-up",
)
kmf.plot_survival_function(ci_show=True)

plt.title("Kaplan Meier: Time to Hospital Readmission")
plt.xlabel("Days After Discharge")
plt.ylabel("Probability of No Readmission")
plt.xlim(0, 180)
plt.ylim(0, 1)
plt.grid()
plt.tight_layout()

# Export the Kaplan-Meier graph
plt.savefig("kaplan_meier_logrank.png", dpi=300)
plt.show()

# PART2: COX PROPORTIONAL HAZARDS MODEL

# Import the Cox regression dataset
cox_data = pd.read_csv("cox_ph_heart_failure_survival.csv")

# Display the dataset information
print("\nCox PH Dataset:")
print(cox_data.head())
print(cox_data.dtypes)

# Change sex categories into numeric values
cox_data["sex"] = cox_data["sex"].map({
    "Male": 1,
    "Female": 0
})

# Keep the variables needed for the analysis
selected_columns = [
    "time_months",
    "death",
    "age",
    "sex",
    "bmi",
    "systolic_bp",
    "ejection_fraction",
    "diabetes",
    "smoker",
    "chronic_kidney_disease",
    "nyha_class",
    "beta_blocker"
]

cox_data = cox_data[selected_columns]

# Remove incomplete records
cox_data = cox_data.dropna()

# Build and run the Cox regression model
cox_model = CoxPHFitter()

cox_model.fit(
    cox_data,
    duration_col="time_months",
    event_col="death",
)

# Show the regression output
print("\nCox Proportional Hazards Model Summary:")
cox_model.print_summary()

# Display the hazard ratio graph
plt.figure(figsize=(10, 7))

cox_model.plot(hazard_ratios=True)

plt.title("Cox PH Model: Heart Failure Survival")
plt.xlabel("Hazard Ratio")
plt.grid()
plt.tight_layout()

# Save the Cox regression graph
plt.savefig("cox.proportional_hazard.png", dpi=300)
plt.show()

# Finish the analysis
print("\nBoth analyses finished successfully.")
print("The two graphs were saved.")