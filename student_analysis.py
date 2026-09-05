import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ==========================================
# STUDENT PERFORMANCE ANALYSIS
# ==========================================

print("=" * 50)
print("STUDENT PERFORMANCE ANALYSIS")
print("=" * 50)

# Create output folder for graphs
os.makedirs("outputs", exist_ok=True)

# ------------------------------------------
# 1. LOAD DATASET
# ------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "students.csv")

try:
    df = pd.read_csv(csv_path)
    print("\nDataset loaded successfully!")
except FileNotFoundError:
    print("\nERROR: students.csv was not found.")
    print("Make sure students.csv is in the same folder as this Python file.")
    exit()

# ------------------------------------------
# 2. BASIC DATASET INFORMATION
# ------------------------------------------

print("\n" + "=" * 50)
print("DATASET INFORMATION")
print("=" * 50)

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

# ------------------------------------------
# 3. CHECK MISSING VALUES
# ------------------------------------------

print("\n" + "=" * 50)
print("MISSING VALUES")
print("=" * 50)

missing_values = df.isnull().sum()
print(missing_values)

# Fill missing numerical values with median
numeric_columns = df.select_dtypes(include=np.number).columns

for column in numeric_columns:
    if df[column].isnull().sum() > 0:
        df[column] = df[column].fillna(df[column].median())

# Fill missing categorical values with mode
categorical_columns = df.select_dtypes(exclude=np.number).columns

for column in categorical_columns:
    if df[column].isnull().sum() > 0:
        mode_value = df[column].mode()

        if not mode_value.empty:
            df[column] = df[column].fillna(mode_value[0])

print("\nMissing values after cleaning:")
print(df.isnull().sum())

# ------------------------------------------
# 4. REMOVE DUPLICATE ROWS
# ------------------------------------------

duplicates_before = df.duplicated().sum()

df = df.drop_duplicates()

duplicates_after = df.duplicated().sum()

print("\n" + "=" * 50)
print("DUPLICATE CHECK")
print("=" * 50)

print("Duplicates before cleaning:", duplicates_before)
print("Duplicates after cleaning:", duplicates_after)

# ------------------------------------------
# 5. DESCRIPTIVE STATISTICS
# ------------------------------------------

print("\n" + "=" * 50)
print("DESCRIPTIVE STATISTICS")
print("=" * 50)

print(df.describe(include="all"))

# Save cleaned dataset
df.to_csv("outputs/cleaned_students.csv", index=False)

print("\nCleaned dataset saved as:")
print("outputs/cleaned_students.csv")

# ------------------------------------------
# 6. NUMERICAL DATA ANALYSIS
# ------------------------------------------

print("\n" + "=" * 50)
print("NUMERICAL DATA ANALYSIS")
print("=" * 50)

if len(numeric_columns) > 0:

    for column in numeric_columns:
        print(f"\n--- {column} ---")
        print("Mean:", round(df[column].mean(), 2))
        print("Median:", round(df[column].median(), 2))
        print("Minimum:", df[column].min())
        print("Maximum:", df[column].max())
        print("Standard Deviation:", round(df[column].std(), 2))

# ------------------------------------------
# 7. HISTOGRAMS
# ------------------------------------------

if len(numeric_columns) > 0:

    for column in numeric_columns:

        plt.figure(figsize=(8, 5))

        plt.hist(df[column].dropna(), bins=10, edgecolor="black")

        plt.title(f"Distribution of {column}")
        plt.xlabel(column)
        plt.ylabel("Number of Students")

        plt.tight_layout()

        filename = f"outputs/histogram_{column}.png"
        plt.savefig(filename)

        plt.show()

# ------------------------------------------
# 8. BAR CHART FOR CATEGORICAL DATA
# ------------------------------------------

if len(categorical_columns) > 0:

    for column in categorical_columns:

        # Avoid graphs with too many categories
        if df[column].nunique() <= 15:

            value_counts = df[column].value_counts()

            plt.figure(figsize=(8, 5))

            plt.bar(
                value_counts.index.astype(str),
                value_counts.values
            )

            plt.title(f"Student Distribution by {column}")
            plt.xlabel(column)
            plt.ylabel("Number of Students")

            plt.xticks(rotation=45)

            plt.tight_layout()

            filename = f"outputs/bar_chart_{column}.png"
            plt.savefig(filename)

            plt.show()

# ------------------------------------------
# 9. SCATTER PLOTS
# ------------------------------------------

if len(numeric_columns) >= 2:

    for i in range(len(numeric_columns) - 1):

        x_column = numeric_columns[i]
        y_column = numeric_columns[i + 1]

        plt.figure(figsize=(8, 5))

        plt.scatter(
            df[x_column],
            df[y_column]
        )

        plt.title(f"{x_column} vs {y_column}")
        plt.xlabel(x_column)
        plt.ylabel(y_column)

        plt.tight_layout()

        filename = f"outputs/scatter_{x_column}_vs_{y_column}.png"
        plt.savefig(filename)

        plt.show()

# ------------------------------------------
# 10. CORRELATION ANALYSIS
# ------------------------------------------

if len(numeric_columns) >= 2:

    print("\n" + "=" * 50)
    print("CORRELATION ANALYSIS")
    print("=" * 50)

    correlation_matrix = df[numeric_columns].corr()

    print(correlation_matrix)

    # Create correlation heatmap manually
    plt.figure(figsize=(10, 7))

    plt.imshow(correlation_matrix)

    plt.colorbar()

    plt.xticks(
        range(len(correlation_matrix.columns)),
        correlation_matrix.columns,
        rotation=45
    )

    plt.yticks(
        range(len(correlation_matrix.columns)),
        correlation_matrix.columns
    )

    plt.title("Correlation Matrix")

    plt.tight_layout()

    plt.savefig("outputs/correlation_matrix.png")

    plt.show()

# ------------------------------------------
# 11. SAVE ANALYSIS SUMMARY
# ------------------------------------------

with open("outputs/analysis_summary.txt", "w") as file:

    file.write("STUDENT PERFORMANCE ANALYSIS\n")
    file.write("=" * 50 + "\n\n")

    file.write(f"Total Students: {len(df)}\n")
    file.write(f"Total Columns: {len(df.columns)}\n\n")

    file.write("Column Names:\n")
    file.write(", ".join(df.columns) + "\n\n")

    file.write("Missing Values After Cleaning:\n")
    file.write(str(df.isnull().sum()) + "\n\n")

    if len(numeric_columns) > 0:
        file.write("Numerical Statistics:\n")
        file.write(str(df[numeric_columns].describe()))

print("\n" + "=" * 50)
print("ANALYSIS COMPLETED SUCCESSFULLY!")
print("=" * 50)

print("\nProject outputs have been saved in the 'outputs' folder.")