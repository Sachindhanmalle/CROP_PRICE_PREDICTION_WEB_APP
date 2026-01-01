import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer


# 1. Load dataset
df = pd.read_csv("crop.csv")

# 2. Date processing
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day

# 3. Features & target
X = df[['Amc_Name', 'Crop', 'Month', 'Day']]
y = df[['Minimum', 'Maximum']]

# 4. Preprocessing: one-hot encode categorical features, keep Month/Day numeric
cat_features = ['Amc_Name', 'Crop']
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features)
    ],
    remainder='passthrough'
)

X_transformed = preprocessor.fit_transform(X)

# feature names after transform
try:
    feature_names = preprocessor.get_feature_names_out(X.columns)
except Exception:
    # Fallback if older sklearn version
    feature_names = None

# Save preprocessing artifacts
joblib.dump(preprocessor, "encoder.pkl")
joblib.dump(feature_names, "training_columns.pkl")

# 5. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_transformed, y, test_size=0.2, random_state=42
)

# 6. Train model (supports multi-output)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 7. Save model
joblib.dump(model, "price_predictor.pkl")

print("✅ Model training complete!")
print("✅ Saved: price_predictor.pkl, encoder.pkl, training_columns.pkl")
