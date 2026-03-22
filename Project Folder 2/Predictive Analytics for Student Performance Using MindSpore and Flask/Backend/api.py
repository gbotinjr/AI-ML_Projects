from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load model and scaler with proper path handling
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "../Model/Model_File/model.pkl")
scaler_path = os.path.join(base_dir, "../Model/Model_File/scaler.pkl")

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

print(f"Model loaded from: {model_path}")
print(f"Scaler loaded from: {scaler_path}")

def ph_to_uci(grade):
    return grade / 5

def uci_to_ph(grade):
    return grade * 5

def validate_ph_grade(value, field_name):
    if not isinstance(value, (int, float)):
        raise ValueError(f"{field_name} must be a number")
    if value < 0 or value > 100:
        raise ValueError(f"{field_name} must be between 0 and 100")

@app.route('/')
def home():
    return "Student Performance API Running"


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        validate_ph_grade(data['G1'], "G1")
        validate_ph_grade(data['G2'], "G2")

        G1 = ph_to_uci(data['G1'])
        G2 = ph_to_uci(data['G2'])
        
        studytime = data['studytime']
        failures = data['failures']
        absences = data['absences']

        input_data = np.array([[G1, G2, studytime, failures, absences]])

        scaled_data = scaler.transform(input_data)

        prediction = model.predict(scaled_data)

        # Convert prediction back to PH grading system
        predicted_g3_ph = uci_to_ph(prediction[0])

        # Enforce PH grading bounds
        predicted_g3_ph = np.clip(predicted_g3_ph, 0, 100)

        return jsonify({
        "Predicted_G3": round(float(predicted_g3_ph), 2),
        "success": True
        })
    
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
    }), 400

    except KeyError as e:
        return jsonify({
            "success": False,
            "error": f"Missing required field: {e.args[0]}"
        }), 400

    except Exception as e:
        print(f"Error in predict: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)