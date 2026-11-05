
import pandas as pd
import html

df = pd.read_csv("procurement_dataset.csv")

# Temizlik: ham dosyayı değiştirmeden DataFrame üzerinde çalış
df.columns = [
    html.unescape(c.replace("*", "")).strip()
    for c in df.columns
]

for col in df.select_dtypes(include=["object", "str"]).columns:
    df[col] = df[col].apply(
        lambda x: html.unescape(x.replace("*", "").strip())
        if isinstance(x, str) else x
    )

df["Order_Date"] = pd.to_datetime(
    df["Order_Date"], errors="coerce"
)
df["Delivery_Date"] = pd.to_datetime(
    df["Delivery_Date"], errors="coerce"
)

issues = []

def add_issue(condition, issue_name):
    temp = df.loc[condition].copy()
    temp["Issue"] = issue_name
    issues.append(temp)

# 1. Teslimat tarihi sipariş tarihinden önce
add_issue(
    df["Delivery_Date"] < df["Order_Date"],
    "Delivery before order"
)

# 2. Pending / Cancelled ama teslimat tarihi dolu
add_issue(
    df["Order_Status"].isin(["Pending", "Cancelled"])
    & df["Delivery_Date"].notna(),
    "Unexpected delivery date"
)

# 3. Delivered / Partially Delivered ama teslimat tarihi boş
add_issue(
    df["Order_Status"].isin(
        ["Delivered", "Partially Delivered"]
    )
    & df["Delivery_Date"].isna(),
    "Missing delivery date"
)

# 4. Kusurlu ürün sayısı sipariş miktarından fazla
add_issue(
    df["Defective_Units"].notna()
    & (df["Defective_Units"] > df["Quantity"]),
    "Defective units exceed quantity"
)

# 5. Negatif veya geçersiz fiyat / miktar
add_issue(
    (df["Quantity"] <= 0)
    | (df["Unit_Price"] <= 0)
    | (df["Negotiated_Price"] <= 0),
    "Invalid quantity or price"
)

# 6. Birleştir ve dışa aktar
if issues:
    result = pd.concat(issues).drop_duplicates(
        subset=["PO_ID", "Issue"]
    )
    result.to_csv(
        "data_quality_issues.csv",
        index=False,
        encoding="utf-8-sig"
    )
    print("Issue records:", len(result))
    print(result[["PO_ID", "Issue"]].to_string(index=False))
else:
    print("No issues found.")

# Detaylı tarih tutarsızlığı raporu

date_issues = df[
    (
        df["Order_Status"].isin(["Pending", "Cancelled"])
        & df["Delivery_Date"].notna()
    )
    |
    (
        df["Order_Status"].isin(
            ["Delivered", "Partially Delivered"]
        )
        & df["Delivery_Date"].isna()
    )
    |
    (
        df["Delivery_Date"] < df["Order_Date"]
    )
].copy()

print("\n--- DATE ISSUE SUMMARY ---")
print(date_issues["Order_Status"].value_counts())

print("\n--- ISSUE DETAILS ---")
print(
    date_issues[
        [
            "PO_ID",
            "Supplier",
            "Order_Status",
            "Order_Date",
            "Delivery_Date",
            "Quantity",
            "Defective_Units",
            "Compliance"
        ]
    ].sort_values("Order_Status").to_string(index=False)
)

date_issues.to_csv(
    "date_issue_details.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved: date_issue_details.csv")

print("\n--- DEFECTIVE UNITS BY STATUS ---")
print(
    df.groupby("Order_Status")["Defective_Units"]
    .agg(["count", "size"])
)

print("\n--- COMPLIANCE DISTRIBUTION ---")
print(df["Compliance"].value_counts(dropna=False))

print("\n--- NEGOTIATED PRICE CHECK ---")
print(
    "Negotiated price higher than unit price:",
    (df["Negotiated_Price"] > df["Unit_Price"]).sum()
)

print("\n--- DEFECTIVE UNITS CHECK ---")
print(
    "Defective units greater than quantity:",
    (
        df["Defective_Units"].notna()
        & (df["Defective_Units"] > df["Quantity"])
    ).sum()
)

print("\n--- QUALITY CHECK COMPLETED ---")
