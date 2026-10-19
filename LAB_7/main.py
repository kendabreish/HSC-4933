


#name: Amani Fargham
#assignment: Lab 7
#description: Load a CSV dataset, clean column names,
#create scatterplots, and calculate an OLS regression.

import re
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def clean_column_name(column_name):
    """Convert a column name to snake_case."""
    column_name = column_name.strip()

    #separate words written in CamelCase.
    column_name = re.sub(
        r"([A-Z]+)([A-Z][a-z])", r"\1_\2", column_name
    )
    column_name = re.sub(
        r"([a-z0-9])([A-Z])", r"\1_\2", column_name
    )

    #replace spaces and other punctuation with underscores.
    column_name = re.sub(r"[^a-zA-Z0-9]+", "_", column_name)

    return column_name.lower().strip("_")


def save_plot(figure, base_folder):
    """Ask whether to save the figure with a custom filename."""
    answer = input("Would you like to save this plot? (yes/no): ")
    answer = answer.strip().lower()

    if answer in ["yes", "y"]:
        filename = input(
            "Enter a filename or folder path, including .png: "
        ).strip()

        if not filename:
            print("No filename entered. Plot was not saved.")
            return

        save_path = Path(filename).expanduser()

        if not save_path.is_absolute():
            save_path = base_folder / save_path

        if save_path.suffix.lower() != ".png":
            save_path = save_path.with_suffix(".png")

        #create the folders if they do not already exist.
        save_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(save_path, dpi=300, bbox_inches="tight")
        print("Saved:", save_path)


def main():
    #look for files in the same folder as this script.
    base_folder = Path(__file__).resolve().parent

    dataset_name = input(
        "Enter the dataset filename, including .csv: "
    ).strip()

    dataset_path = Path(dataset_name).expanduser()

    if not dataset_path.is_absolute():
        dataset_path = base_folder / dataset_path

    try:
        data = pd.read_csv(dataset_path)
    except (OSError, pd.errors.ParserError, pd.errors.EmptyDataError) as error:
        print("Could not load the dataset:", error)
        return

    #clean and display the column names.
    data.columns = [
        clean_column_name(column) for column in data.columns
    ]

    if data.columns.duplicated().any():
        print("Some column names became duplicates after cleaning.")
        return

    print("\nAvailable columns:")
    for column in data.columns:
        print(column)

    x_column = input("\nEnter the X column name: ").strip()
    y_column = input("Enter the Y column name: ").strip()

    if x_column not in data.columns or y_column not in data.columns:
        print("Please run again and enter names from the column list.")
        return

    if x_column == y_column:
        print("Please choose two different columns.")
        return

    #convert the chosen columns to numbers.
    # Remove commas from values such as 14,369.
    x_values = pd.to_numeric(
        data[x_column].astype(str).str.replace(",", "", regex=False),
        errors="coerce"
    )
    y_values = pd.to_numeric(
        data[y_column].astype(str).str.replace(",", "", regex=False),
        errors="coerce"
    )

    regression_data = pd.DataFrame({
        "x": x_values,
        "y": y_values
    })

    #remove missing, nonnumeric, or infinite values.
    regression_data = regression_data.replace(
        [float("inf"), float("-inf")], float("nan")
    )
    regression_data = regression_data.dropna(subset=["x", "y"])

    print("\nRows used:", len(regression_data))
    print("Rows removed:", len(data) - len(regression_data))

    if len(regression_data) < 2:
        print("At least two complete numeric rows are needed.")
        return

    x = regression_data["x"]
    y = regression_data["y"]
    point_color = input("Enter point color (blue, green, purple): ").strip()
    line_color =  input("Enter regression line color (red, black, green): ").strip()
    line_width = float(input("Enter regression line width (1-5): "))
    show_grid = input("Show gridlines? (yes/no): ").strip().lower()
    plot_title = input("Enter plot title: ").strip()
    minimum = input("Enter minimum X value, or press Enter to skip: ").strip()
    maximum = input("Enter maximum X value, or press Enter to skip: ").strip()

    if minimum and maximum:
        minimum = float(minimum)
        maximum = float(maximum)

        if minimum > maximum:
            print("Minimum X value cannot be greater than maximum.")
            return

        regression_data = regression_data[
            (regression_data["x"] >= minimum)
            & (regression_data["x"] <= maximum)
        ]

        x = regression_data["x"]
        y = regression_data["y"]
        if len(regression_data) < 2:
            print("Not enough rows in this range.")
            return
    if x.nunique() < 2:
        print("X must contain at least two different values.")
        return

    #create the scatterplot without a regression line.
    figure, axes = plt.subplots(figsize=(8, 5))
    axes.scatter(x, y, alpha=0.5, color=point_color)
    axes.grid(show_grid in ["yes", "y"])
    axes.set_xlabel(x_column)
    axes.set_ylabel(y_column)
    axes.set_title(plot_title or f"{y_column} vs. {x_column}")
    figure.tight_layout()

    print("\nScatterplot without regression")
    plt.show(block=False)
    plt.pause(0.1)
    save_plot(figure, base_folder)

    #calculate the OLS slope and intercept.
    x_mean = x.mean()
    y_mean = y.mean()

    beta_1 = (
        ((x - x_mean) * (y - y_mean)).sum()
        / ((x - x_mean) ** 2).sum()
    )
    beta_0 = y_mean - beta_1 * x_mean

    # Calculate predicted Y values and R squared.
    predicted_y = beta_0 + beta_1 * x
    residual_sum = ((y - predicted_y) ** 2).sum()
    total_sum = ((y - y_mean) ** 2).sum()

    print(f"\nIntercept (beta_0): {beta_0:.8f}")
    print(f"Slope (beta_1): {beta_1:.8f}")

    if total_sum == 0:
        print("R squared: undefined because all Y values are equal.")
    else:
        r_squared = 1 - residual_sum / total_sum
        print(f"R squared: {r_squared:.8f}")

    # Sort X so the regression line is drawn in order.
    sorted_x = x.sort_values()
    regression_line = beta_0 + beta_1 * sorted_x

    axes.plot(
        sorted_x,
        regression_line,
        color=line_color,
        linewidth=line_width,
        label="OLS regression line"
    )
    axes.grid(show_grid in ["yes", "y"])

    axes.set_title(
        plot_title or f"{y_column} vs. {x_column} with OLS regression"
    )
    axes.legend()
    figure.tight_layout()

    print("\nScatterplot with regression")
    plt.show(block=False)
    plt.pause(0.1)
    save_plot(figure, base_folder)

    plt.show()


if __name__ == "__main__":
    main()