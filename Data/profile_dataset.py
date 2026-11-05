
import pandas as pd
import html

file_path = "procurement_dataset.csv"

df = pd.read_csv(file_path)

# Sütun adlarını ve metin değerlerini temizle
df.columns = [
    html.unescape(col.replace("*", "")).strip()
    for col in df.columns
]

for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].apply(
        lambda x: html.unescape(x.replace("*", "").strip())
        if isinstance(x, str) else x
    )

print("\n--- DATASET INFO ---")
print("Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- DUPLICATE RECORDS ---")
print(df.duplicated().sum())

print("\n--- ORDER STATUS ---")
print(df["Order_Status"].value_counts(dropna=False))

print("\n--- SUPPLIERS ---")
print(df["Supplier"].value_counts(dropna=False))

print("\n--- ITEM CATEGORIES ---")
print(df["Item_Category"].value_counts(dropna=False))

print("\n--- NUMERIC SUMMARY ---")
print(df.describe(include="all").to_string())

print("\n--- DATE VALIDATION ---")
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
df["Delivery_Date"] = pd.to_datetime(df["Delivery_Date"], errors="coerce")

print(
    "Delivery before order:",
    (df["Delivery_Date"] < df["Order_Date"]).sum()
)

print("\n--- STATUS / DELIVERY DATE CHECK ---")
print(pd.crosstab(
    df["Order_Status"],
    df["Delivery_Date"].isna(),
    margins=True
))

# Analiz çıktısını dosyaya kaydet
with open("dataset_profile.txt", "w", encoding="utf-8") as f:
    f.write(f"Dataset shape: {df.shape}\n\n")
    f.write("Missing values:\n")
    f.write(df.isnull().sum().to_string())
    f.write("\n\nOrder status:\n")
    f.write(df["Order_Status"].value_counts(dropna=False).to_string())
    f.write("\n\nSupplier:\n")
    f.write(df["Supplier"].value_counts(dropna=False).to_string())
    f.write("\n\nNumeric summary:\n")
    f.write(df.describe(include="all").to_string())
    f.write("\n\nStatus / Delivery Date:\n")
    f.write(pd.crosstab(
        df["Order_Status"],
        df["Delivery_Date"].isna(),
        margins=True
    ).to_string())

print("\nProfile saved: dataset_profile.txt")
