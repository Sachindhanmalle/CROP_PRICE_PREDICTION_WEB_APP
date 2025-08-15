import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder

# ===============================
# 1. Load Dataset
# ===============================
df = pd.read_csv("crop.csv")  # make sure this file is in the same folder

# ===============================
# 2. Date Processing
# ===============================
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day

# ===============================
# 3. Features & Target
# ===============================
X = df[['Amc_Name', 'Crop', 'Month', 'Day']]  # features
y = df[['Minimum', 'Maximum']]                # targets

# ===============================
# 4. One-Hot Encode categorical features
# ===============================
encoder = OneHotEncoder(handle_unknown='ignore')
X_encoded = encoder.fit_transform(X)

# Save the training columns for later use in Flask
training_columns = encoder.get_feature_names_out(X.columns)
joblib.dump(training_columns, "training_columns.pkl")
joblib.dump(encoder, "encoder.pkl")  # Save encoder so Flask can use same encoding

# ===============================
# 5. Train-Test Split
# ===============================
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42
)

# ===============================
# 6. Train Model
# ===============================
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ===============================
# 7. Save Model
# ===============================
joblib.dump(model, "price_predictor.pkl")

print("✅ Model training complete!")
print("✅ price_predictor.pkl, encoder.pkl, and training_columns.pkl saved.")
