# CROP_PRICE_PREDICTION_model

Simple FastAPI + Streamlit project to predict crop prices.

How to run locally

1. Install dependencies:
```
pip install -r requirements.txt
```
2. Train model (if not present):
```
python train_model.py
```
3. Start FastAPI backend:
```
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
4. Start Streamlit UI:
```
streamlit run streamlit_app.py
```

API endpoints

- `GET /health` — health check
- `POST /predict` — predict Minimum/Maximum (JSON: `Amc_Name`, `Crop`, `Month`, `Day`)
