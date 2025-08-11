import pandas as pd

# Load CSV file
df = pd.read_csv(r"P:/Projects/Used_Cars/used_cars_cleaned.csv")  # Update path if needed

# Clean ask_price column
df['ask_price'] = (
    df['ask_price']
    .astype(str)
    .str.replace('₹', '', case=False)
    .str.replace(',', '')
    .str.strip()
    .astype(float)
)

# Clean distance_travelled_km (remove commas, 'km', etc.)
df['distance_travelled_km'] = (
    df['distance_travelled_km']
    .astype(str)
    .str.replace(',', '')
    .str.replace('km', '', case=False)
    .str.strip()
    .astype(float)
)

# Drop rows with missing values in required fields
df.dropna(subset=[
    'brand', 'model', 'age', 'distance_travelled_km',
    'fuel_type', 'transmission', 'owner', 'ask_price'
], inplace=True)
