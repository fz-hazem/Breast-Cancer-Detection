import os
import numpy as np
import pickle
from flask import Flask, request, render_template

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'models', 'model.pkl')
scaler_path = os.path.join(BASE_DIR, 'models', 'scaler.pkl')

try:
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    with open(scaler_path, 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
    print("SUCCESS: Model and Scaler loaded successfully!")
except FileNotFoundError:
    model = None
    scaler = None
    print("Error: Model files are missing in the 'models/' folder.")

@app.route('/')
def home():
    return render_template('index.html', message=None, image_file=None)

@app.route('/predict', methods=['POST'])
def predict():
    raw_input = request.form.get('feature', '').strip()

    # Frontend Test Bypass
    if raw_input.lower() == 'test_safe':
        return render_template('index.html', message="Not Cancrouse", image_file="okay_img.jpg")
    elif raw_input.lower() == 'test_danger':
        return render_template('index.html', message="Cancrouse", image_file="alert_imge.png")

    if not model or not scaler:
        return render_template('index.html', message="Error: Model components not loaded.", image_file=None)

    try:
        if not raw_input:
            return render_template('index.html', message="Please enter feature values.", image_file=None)

        # Nettoyage et conversion des données en floats
        feature_list = [float(x.strip()) for x in raw_input.split(',') if x.strip()]
        
        # Si un ID de contrôle (comme 842302) est présent au début (31 valeurs), on le retire
        if len(feature_list) == 31:
            feature_list = feature_list[1:]
        
        # Validation finale des 30 caractéristiques
        if len(feature_list) != 30:
            return render_template('index.html', message=f"Expected 30 features, received {len(feature_list)}.", image_file=None)

        input_array = np.array([feature_list])
        scaled_features = scaler.transform(input_array)
        prediction = model.predict(scaled_features)
        
        if prediction[0] == 0:
            result_str = "Not Cancrouse"
            image_file = "okay_img.jpg"
        else:
            result_str = "Cancrouse"
            image_file = "alert_imge.png"
            
        return render_template('index.html', message=result_str, image_file=image_file)

    except Exception as e:
        return render_template('index.html', message=f"Error parsing data: {str(e)}", image_file=None)

if __name__ == '__main__':
    app.run(debug=True)