from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Load model and encoder
model = joblib.load("price_predictor.pkl")
encoder = joblib.load("encoder.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        amc_name = request.form["amc_name"]
        crop = request.form["crop"]
        date = pd.to_datetime(request.form["date"])

        # Extract month and day
        month = date.month
        day = date.day

        # Create DataFrame
        input_df = pd.DataFrame([[amc_name, crop, month, day]],
                                columns=["Amc_Name", "Crop", "Month", "Day"])

        # Encode input using saved encoder
        input_encoded = encoder.transform(input_df)

        # Predict
        prediction = model.predict(input_encoded)

        min_price = round(prediction[0][0], 2)
        max_price = round(prediction[0][1], 2)

        return jsonify({
            "min_price": min_price,
            "max_price": max_price
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
