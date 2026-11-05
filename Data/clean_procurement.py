
import pandas as pd
import html
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "procurement_dataset.csv"
OUTPUT_FILE = BASE_DIR / "cleaned_procurement.csv"
QUALITY_FILE = BASE_DIR / "procurement_quality_report.csv"

# 1. Load raw data
df = pd.read_csv(INPUT_FILE)

initial_count = len(df)

# 2. Normalize column names
df.columns = [
    html.unescape(col.replace("*", "")).strip()
    for col in df.columns
]

# 3. Clean text fields
for col in df.select_dtypes(include=["object", "str"]).columns:
    df[col] = df[col].apply(
        lambda x: html.unescape(x.replace("*", "").strip())
        if isinstance(x, str) else x
    )

# 4. Convert data types
df["Order_Date"] = pd.to_datetime(
    df["Order_Date"], errors="coerce"
)

df["Delivery_Date"] = pd.to_datetime(
    df["Delivery_Date"], errors="coerce"
)

for col in [
    "Quantity",
    "Unit_Price",
    "Negotiated_Price",
    "Defective_Units"
]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 5. Validate business rules
df["data_quality_issue"] = ""

def add_issue(condition, message):
    mask = condition.fillna(False)
    existing = df.loc[mask, "data_quality_issue"]

    df.loc[mask, "data_quality_issue"] = existing.apply(
        lambda x: f"{x}; {message}" if x else message
    )

add_issue(
    df["Order_Status"].isin(["Pending", "Cancelled"])
    & df["Delivery_Date"].notna(),
    "Unexpected delivery date"
)

add_issue(
    df["Order_Status"].isin(
        ["Delivered", "Partially Delivered"]
    )
    & df["Delivery_Date"].isna(),
    "Missing delivery date"
)

add_issue(
    df["Delivery_Date"] < df["Order_Date"],
    "Delivery before order"
)

add_issue(
    df["Defective_Units"].notna()
    & (df["Defective_Units"] > df["Quantity"]),
    "Defective units exceed quantity"
)

add_issue(
    df["Quantity"] <= 0,
    "Invalid quantity"
)

add_issue(
    df["Unit_Price"] <= 0,
    "Invalid unit price"
)

add_issue(
    df["Negotiated_Price"] <= 0,
    "Invalid negotiated price"
)

# 6. Quality status
df["data_quality_status"] = df[
    "data_quality_issue"
].apply(
    lambda x: "REVIEW_REQUIRED" if x else "VALID"
)

# 7. Save outputs
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

df.loc[
    df["data_quality_status"] == "REVIEW_REQUIRED"
].to_csv(
    QUALITY_FILE,
    index=False,
    encoding="utf-8-sig"
)

# 8. Summary
print("ETL CLEANING COMPLETED")
print("----------------------")
print("Initial records:", initial_count)
print("Output records:", len(df))
print("Records preserved:", initial_count == len(df))
print(
    "Valid records:",
    (df["data_quality_status"] == "VALID").sum()
)
print(
    "Records requiring review:",
    (df["data_quality_status"] == "REVIEW_REQUIRED").sum()
)
print("Cleaned file:", OUTPUT_FILE)
print("Quality report:", QUALITY_FILE)
