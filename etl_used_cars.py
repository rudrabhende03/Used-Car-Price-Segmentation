import pandas as pd
from sqlalchemy import create_engine

# ---------------------------
# CONFIG
# ---------------------------
# CSV source (raw or semi-clean)
CSV_FILE_PATH = r"P:\Data Tools\Datasets\used_cars_dataset_v2.csv"

# PostgreSQL connection (edit these)
DB_USER = "your_username"         # e.g. "postgres"
DB_PASSWORD = "your_password"     # e.g. "admin"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "Used_Cars"

# Destination table
TABLE_NAME = "used_cars_cleaned"

# ---------------------------
# EXTRACT
# ---------------------------
print("Reading CSV...")
df = pd.read_csv(CSV_FILE_PATH)

# ---------------------------
# TRANSFORM
# ---------------------------
# 1) Standardize column names to snake_case
df = df.rename(columns={
    "Brand": "brand",
    "Model": "model",
    "Year": "year",
    "Age": "age",
    "kmDriven": "distance_travelled_km",
    "Transmission": "transmission",
    "Owner": "owner",
    "FuelType": "fuel_type",
    "PostedDate": "posted_date",
    "AdditionalInfo": "additional_info",
    "AskPrice": "ask_price",
    # In case your CSV already had spaced labels, map them too:
    "Distance Travelled (Km)": "distance_travelled_km",
    "Fuel Type": "fuel_type",
    "Posted Date": "posted_date",
    "Additional Info": "additional_info",
    "Ask Price": "ask_price",
})

# 2) Clean numeric columns
# ask_price => numeric (strip ₹, commas, spaces)
if "ask_price" in df.columns:
    df["ask_price"] = (
        df["ask_price"]
        .astype(str)
        .str.replace("₹", "", case=False)
        .str.replace(",", "")
        .str.strip()
    )
    # coerce errors to NaN, then we can drop later
    df["ask_price"] = pd.to_numeric(df["ask_price"], errors="coerce")

# distance_travelled_km => numeric (strip "km", commas, spaces)
if "distance_travelled_km" in df.columns:
    df["distance_travelled_km"] = (
        df["distance_travelled_km"]
        .astype(str)
        .str.replace("km", "", case=False)
        .str.replace(",", "")
        .str.strip()
    )
    df["distance_travelled_km"] = pd.to_numeric(df["distance_travelled_km"], errors="coerce")

# 3) Basic trimming for text columns if present
for col in ["brand", "model", "fuel_type", "transmission", "owner", "posted_date", "additional_info"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# 4) Drop rows missing critical fields for downstream use
needed = ["brand", "model", "age", "distance_travelled_km", "fuel_type", "transmission", "owner", "ask_price"]
present_needed = [c for c in needed if c in df.columns]
df = df.dropna(subset=present_needed)

# ---------------------------
# LOAD
# ---------------------------
print("Connecting to PostgreSQL...")
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

print(f"Writing {len(df):,} rows to table '{TABLE_NAME}'...")
df.to_sql(TABLE_NAME, engine, if_exists="replace", index=False)

print("✅ ETL complete.")
