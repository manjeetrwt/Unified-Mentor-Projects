import os
import pandas as pd


# STEP 0: DYNAMIC PATH RESOLUTION (FIXED)

# This gets the absolute directory where data_cleaning.py is saved
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Move up one level out of 'Notebook' and look for the 'data' folder
RAW_DATA_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "data", "APL_Logistics.csv"))
CLEANED_DATA_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "data", "APL_Logistics_Cleaned.csv"))
ANOMALY_LOG_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "data", "APL_Logistics_Anomalies.csv"))

print("--- Loading raw APL Logistics dataset ---")
print(f"Looking for file at: {RAW_DATA_PATH}")

# Load dataset
try:
    df = pd.read_csv(RAW_DATA_PATH, encoding="utf-8")
except FileNotFoundError:
    print(f"\n[ERROR] File not found! Please check that your file name is spelled exactly 'APL_Logistics.csv' and is dropped inside this folder:\n{os.path.join(SCRIPT_DIR, '..', 'data')}")
    exit(1)
except UnicodeDecodeError:
    df = pd.read_csv(RAW_DATA_PATH, encoding="latin1")

print(f"Dataset successfully loaded. Shape: {df.shape[0]} rows, {df.shape[1]} columns.\n")


# STEP 2.1: INITIAL AUDIT & STRUCTURAL CHECK

print("--- Step 2.1: Executing Initial Structural Audit ---")

# Strip spaces from column names immediately to prevent KeyErrors
df.columns = df.columns.str.strip()

# Check for missing values in critical columns
missing_summary = df.isnull().sum()
print("\nMissing values detected per critical column:")
print(missing_summary[missing_summary > 0] if missing_summary.sum() > 0 else "None")

# Check for duplicate transactions
duplicate_count = df.duplicated(subset=['Customer Id', 'Product Name'], keep='first').sum() if 'Customer Id' in df.columns else df.duplicated().sum()
print(f"Duplicate records identified: {duplicate_count}")


# STEP 2.2: TEXT & ID FIELDS NORMALIZATION

print("\n--- Step 2.2: Normalizing Text & ID Fields ---")

df['Customer Fname'] = df['Customer Fname'].fillna('').astype(str).str.strip()
df['Customer Lname'] = df['Customer Lname'].fillna('').astype(str).str.strip()
df['Customer_Name'] = (df['Customer Fname'] + ' ' + df['Customer Lname']).str.strip()

df.drop(columns=['Customer Fname', 'Customer Lname'], errors='ignore', inplace=True)

categorical_cols = ['Customer City', 'Customer State', 'Customer Segment', 'Product Name', 'Category Name']
for col in categorical_cols:
    if col in df.columns:
        df[col] = df[col].fillna("Unknown").astype(str).str.strip()

print("Text fields standardized and merged into 'Customer_Name'.")


# STEP 2.3: FINANCIAL VALIDATION LOGIC

print("\n--- Step 2.3: Applying Margin Intelligence Validation ---")

tolerance = 0.01

calculated_total = df['Sales'] - df['Order Item Discount']
math_anomaly_condition = (calculated_total - df['Order Item Total']).abs() > tolerance

impossible_data_condition = (
    (df['Sales'] < 0) | 
    (df['Order Item Quantity'] <= 0) | 
    (df['Order Item Product Price'] <= 0)
)

non_revenue_status = ['SUSPECTED_FRAUD', 'CANCELED']
status_exclusion_condition = df['Order Status'].isin(non_revenue_status)

all_anomalies_mask = math_anomaly_condition | impossible_data_condition | status_exclusion_condition

df_anomalies = df[all_anomalies_mask].copy()
df_cleaned = df[~all_anomalies_mask].copy()

df_anomalies['Anomaly_Reason'] = "Operational Flag/Status"
df_anomalies.loc[math_anomaly_condition, 'Anomaly_Reason'] = "Financial Calculation Error"
df_anomalies.loc[impossible_data_condition, 'Anomaly_Reason'] = "Negative/Impossible Value"


# STEP 4: EXPORT & REPORT OUTCOMES

print("\n--- Phase 2 Validation Complete. Exporting Files ---")

df_cleaned.to_csv(CLEANED_DATA_PATH, index=False)
df_anomalies.to_csv(ANOMALY_LOG_PATH, index=False)

print(f"Success! Cleaned Dataset Saved: {df_cleaned.shape[0]} rows remaining.")
print(f"Anomaly Log Saved: {df_anomalies.shape[0]} flawed/cancelled rows isolated.")