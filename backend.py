from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

try:
    model = joblib.load("price_predictor.pkl")
    encoder = joblib.load("encoder.pkl")
    training_columns = joblib.load("training_columns.pkl")
except Exception as e:
    raise RuntimeError(f"Failed to load model artifacts: {e}")


class PredictRequest(BaseModel):
    Amc_Name: str
    Crop: str
    Month: int
    Day: int


@app.post("/predict")
def predict(req: PredictRequest):
    try:
        X_df = pd.DataFrame([
            [req.Amc_Name, req.Crop, req.Month, req.Day]
        ], columns=["Amc_Name", "Crop", "Month", "Day"])

        X_encoded = encoder.transform(X_df)
        pred = model.predict(X_encoded)

        # model predicts two targets: Minimum and Maximum
        return {"Minimum": float(pred[0][0]), "Maximum": float(pred[0][1])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}
