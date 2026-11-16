 # Kenda S Breish                  #
 # November 16, 2026               #
 # Script: script.py #
 # kendabreish@usf.edu             #

 # DESCRIPTION:
 # Analyzes CDC NHANES cardiovascular disease estimates
 # from 1999-2000 through 2017-2018. Compares male and
 # female prevalence across cardiovascular conditions,
 # summarizes the data, and creates graphs.

 # ======================
 # IMPORT LIBRARIES
 # ======================

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# =======================
# SET UP FILE LOCATIONS
# =======================

PROJECT_FOLDER = Path(__file__).resolve().parent
DATA_FOLDER = PROJECT_FOLDER / "data"
RESULTS_FOLDER = PROJECT_FOLDER / "results"

RESULTS_FOLDER.mkdir(exist_ok=True)

DATA_FILE = Path("nhanes_cardiovascular_data.csv")

# =========================
# LOAD AND EXPLORE THE DATA
# =========================

def load_data(file_path: Path) -> pd.DataFrame:
    """Load the original CDC cardiovascular dataset."""

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    data = pd.read_csv(file_path)

    print("Dataset shape:", data.shape)
    print("\nColumn names:")
    print(data.columns.tolist())

    print("\nMissing values:")
    print(data.isnull().sum())

    return data

# ==========================
# CLEAN AND SELECT THE DATA
# ===========================

def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """Select male and female cardiovascular estimates"""

    required_columns = [
        "YearStart",
        "Topic",
        "Data_Value_Type",
        "Data_Value",
        "Break_Out",
        "Break_Out_Category"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {missing_columns}"
        )

    cleaned = data.copy()

    # Convert prevalence estimates to numeric values.
    cleaned["Data_Value"] = pd.to_numeric(
        cleaned["Data_Value"], errors="coerce"
    )

    # Keep gender-specific records.
    cleaned = cleaned[
        cleaned["Break_Out_Category"].str.contains(
            "sex|gender", case=False, na=False
        )
    ].copy()

    cleaned = cleaned[
        cleaned["Break_Out"].str.strip().str.lower().isin(
            ["male", "female"]
        )
    ].copy()

    # Keep age-standardized estimates when available
    cleaned = cleaned[
        cleaned["Data_Value_Type"].str.contains(
            "age-standardized", case=False, na=False
        )
    ].copy()

    # Remove records without a usable estimate.
    cleaned = cleaned.dropna(subset=["Data_Value"])

    # Save the cleaned dataset.
    cleaned.to_csv(
        RESULTS_FOLDER / "cleaned_cardiovascular_data.csv",
        index=False
    )

    print("\nCleaned dataset shape:", cleaned.shape)

    return cleaned

# =============================
# SUMMARIZE THE DATA
# =============================

def summarize_data(cleaned: pd.DataFrame) -> pd.DataFrame:
    """Calculate descriptive statistics by topic and sex."""

    summary = (
        cleaned.groupby(["Topic", "Break_Out"])["Data_Value"]
        .agg(["count","mean", "std", "min", "max"])
        .reset_index()
    )

    summary.to_csv(
        RESULTS_FOLDER / "descriptive_summary.csv",
        index=False
    )

    print("\nDescriptive statistics:")
    print(summary.to_string(index=False))

    return summary

# ==========================
# COMPARE MALES AND FEMALES
# ==========================

def compare_gender(cleaned: pd.DataFrame) -> pd.DataFrame:
    """Compare male and female prevalence estimates by year and topic."""

    comparison = cleaned.pivot_table(
        index=["YearStart", "Topic"],
        columns="Break_Out",
        values="Data_Value",
        aggfunc="mean"
    ).reset_index()

    comparison.columns.name = None

    if "Male" in comparison.columns and "Female" in comparison.columns:
        comparison["Difference_Male_Minus_Female"] = (
            comparison["Male"] - comparison["Female"]
    )

    comparison.to_csv(
        RESULTS_FOLDER / "gender_comparisons.csv",
        index=False
    )

    print("\nGender comparisons:")
    print(comparison.to_string(index=False))
    return comparison

# ==========================
# CREATE THE PRIMARY GRAPH
# ==========================

def create_primary_graph(cleaned: pd.DataFrame) -> None:
    """Graph cardiovascular prevalence by sex over time."""

    print("\nAvailable cardiovascular topic:")
    print(cleaned["Topic"].dropna().unique())

    # Select the main heart disease topic from the dataset
    primary_data = cleaned[
        cleaned["Topic"] == "Major Cardiovascular Disease"
    ].copy()

    if primary_data.empty:
        print("No matching heart disease topic was found.")
        return

    primary_data = (
        primary_data.groupby(
            ["YearStart", "Break_Out"], as_index=False
        )["Data_Value"].mean()
    )

    for gender in ["Male", "Female"]:
        gender_data = primary_data[
            primary_data["Break_Out"].str.lower() == gender.lower()
        ].sort_values("YearStart")

        plt.plot(
            gender_data["YearStart"],
            gender_data["Data_Value"],
            marker="o",
            label=gender,
        )

        plt.title("Heart Disease Prevalence by sex")
        plt.xlabel("Survey Year")
        plt.ylabel("Age-Standardized Prevalence (%)")
        plt.xticks(rotation=45)
        plt.legend(title="Sex")
        plt.grid(alpha=0.3)
        plt.tight_layout()

        plt.savefig(
            RESULTS_FOLDER / "heart_disease_by_sex.png",
            dpi=300,
        )

        plt.show()

# =========================
# CREATE SECONDARY GRAPHS
# =========================

def create_secondary_graphs(cleaned: pd.DataFrame) -> None:
    """Create separte graph for available cardiovascular topics."""

    secondary_topics = [
        "heart attack",
        "coronary heart disease",
        "heart failure",
    ]

    for topic in secondary_topics:
        topic_data = cleaned[
            cleaned["Topic"].str.contains(
                topic, case=False, na=False
            )
        ]

        if topic_data.empty:
            continue

        plt.figure(figsize=(9, 5))

        for gender in ["Male", "Female"]:
            gender_data = topic_data[
                topic_data["Break_Out"].str.lower() == gender.lower()
            ].sort_values("YearStart")

            plt.plot(
                gender_data["YearStart"],
                gender_data["Data_Value"],
                marker="o",
                label=gender,
            )
        plt.title(f"{topic.title()} Prevalence by Sex")
        plt.xlabel("Survey Year")
        plt.ylabel("Age-Standardized Prevalence (%)")
        plt.xticks(rotation=45)
        plt.legend(title="Sex")
        plt.grid(alpha=0.3)
        plt.tight_layout()

        file_name = topic.replace(" ", "_")
        plt.savefig(
            RESULTS_FOLDER / f"{file_name}.png",
            dpi=300,
        )

        plt.show()

# =============================
# RUN THE ANALYSIS
# =============================

def main() -> None:
    """ Run the complete cardiovascular disease analysis."""

    original_data = load_data(DATA_FILE)

    cleaned_data = clean_data(original_data)

    summarize_data(cleaned_data)

    compare_gender(cleaned_data)

    create_primary_graph(cleaned_data)

    create_secondary_graphs(cleaned_data)

    print("\nAnalysis complete successfully.")
    print("Results saved in the results folder:")

if __name__ == "__main__":
    main()