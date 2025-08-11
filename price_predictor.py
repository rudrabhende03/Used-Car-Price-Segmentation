import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
# from sqlalchemy import create_engine  # Uncomment if loading from DB

# --------------------------------------
# STEP 1: LOAD DATA
# --------------------------------------
# Option A: Load cleaned CSV
DF_PATH = r"P:\Projects\Used_Cars\used_cars_cleaned.csv"  # update if needed
df = pd.read_csv(DF_PATH)

# Option B: Load from PostgreSQL instead (uncomment + configure)
# engine = create_engine("postgresql+psycopg2://username:password@localhost:5432/Used_Cars")
# df = pd.read_sql_table("used_cars_cleaned", engine)

# --------------------------------------
# STEP 2: CLEAN/ENSURE NUMERICS (robust guardrails)
# --------------------------------------
# ask_price numeric
df["ask_price"] = (
    df["ask_price"]
    .astype(str)
    .str.replace("₹", "", case=False)
    .str.replace(",", "")
    .str.strip()
)
df["ask_price"] = pd.to_numeric(df["ask_price"], errors="coerce")

# distance_travelled_km numeric
df["distance_travelled_km"] = (
    df["distance_travelled_km"]
    .astype(str)
    .str.replace("km", "", case=False)
    .str.replace(",", "")
    .str.strip()
)
df["distance_travelled_km"] = pd.to_numeric(df["distance_travelled_km"], errors="coerce")

# Drop rows with missing critical fields
required = ["brand", "model", "age", "distance_travelled_km", "fuel_type", "transmission", "owner", "ask_price"]
df = df.dropna(subset=required)

# --------------------------------------
# STEP 3: FEATURE ENGINEERING
# --------------------------------------
features = ["brand", "model", "age", "distance_travelled_km", "fuel_type", "transmission", "owner"]
target = "ask_price"

X = df[features].copy()
y = df[target].copy()

# One-hot encoding for categoricals
X_encoded = pd.get_dummies(
    X,
    columns=["brand", "model", "fuel_type", "transmission", "owner"],
    drop_first=True
)

# Final safety: drop any lingering NaNs and align y
X_encoded.dropna(inplace=True)
y = y.loc[X_encoded.index]

# --------------------------------------
# STEP 4: SPLIT
# --------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42
)

# --------------------------------------
# STEP 5: TRAIN (Linear Regression baseline)
# --------------------------------------
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# --------------------------------------
# STEP 6: EVALUATE
# --------------------------------------
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))  # compatible with older sklearn
r2 = r2_score(y_test, y_pred)

print("📊 MODEL EVALUATION")
print(f"R² Score        : {r2:.4f}")
print(f"MAE (₹)         : {mae:,.0f}")
print(f"RMSE (₹)        : {rmse:,.0f}")

# --------------------------------------
# (Optional) SAVE MODEL for reuse
# --------------------------------------
# import joblib
# joblib.dump(model, "models/used_car_price_model.pkl")
# print("💾 Model saved to models/used_car_price_model.pkl")
