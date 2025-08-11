# 🚗 Used Car Price Prediction – India Market

This project explores and models pricing trends in the Indian used car market using a dataset of nearly 15,000 listings. It combines **data engineering**, **data cleaning**, **SQL ETL**, **Power BI dashboards**, and a **machine learning regression model** to predict the resale value of a vehicle based on features such as brand, model, age, kilometers driven, fuel type, and ownership.

---

## 📦 Dataset Overview

- **Source**: Collected from Indian used car listings
- **Size**: ~15,000 entries, 11 attributes
- **Features**:
  - `Brand`, `Model`, `Year`, `Age`
  - `kmDriven`, `FuelType`, `Transmission`, `Owner`
  - `PostedDate`, `AskPrice`, `AdditionalInfo`

---

## 🛠️ Project Highlights

### 🔄 ETL Pipeline
- Cleaned raw data (handled ₹ symbols, commas, "km" units)
- Converted to proper numeric types (`ask_price`, `distance_travelled_km`)
- Loaded into **PostgreSQL** using Python + SQLAlchemy

### 📊 Power BI Dashboard
- Created a dynamic dashboard to explore:
  - Brand & model performance hierarchy
  - Fuel type distribution
  - Transmission preferences
  - Price vs. Age & Distance correlation
- Included custom KPIs for market insights

### 🤖 Machine Learning Model
- Feature engineering using one-hot encoding
- Trained a **Linear Regression** model on cleaned data
- Evaluation Metrics:
  - R² score
  - MAE (Mean Absolute Error)
  - RMSE (Root Mean Squared Error)

---

## 📂 File Structure

Used_Cars_Price_Prediction <br />
├── used_cars_dataset_v2.csv # Raw dataset <br />
├── used_cars_cleaned.csv # Cleaned dataset (numeric & standardized) <br />
├── clean_used_cars.py # Script to clean and preprocess raw data <br />
├── etl_used_cars.py # Load cleaned data to PostgreSQL <br />
├── price_predictor.py # Model training and evaluation script <br />
├── requirements.txt # Python dependencies <br />
├── README.md # Project documentation

##📊 MODEL EVALUATION <br />
R² Score: 0.6906 <br />
MAE (₹): 304,241 <br />
RMSE (₹): 674,834,105,868
