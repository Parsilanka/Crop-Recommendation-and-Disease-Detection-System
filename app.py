from flask import Flask, request, render_template, jsonify
import numpy as np
import pandas
import sklearn
import pickle

model = pickle.load(open('model.pkl', 'rb'))
sc = pickle.load(open('standscaler.pkl', 'rb'))
mx = pickle.load(open('minmaxscaler.pkl', 'rb'))

app = Flask(__name__)

@app.route("/")
def home():
    """Serve the main page"""
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    try:
        # Get form data and convert to float
        N = float(request.form.get('nitrogen', 0))
        P = float(request.form.get('phosphorus', 0))
        K = float(request.form.get('potassium', 0))
        temp = float(request.form.get('temperature', 0))
        humidity = float(request.form.get('humidity', 0))
        ph = float(request.form.get('ph', 0))
        rainfall = float(request.form.get('rainfall', 0))
        
        # Validate inputs
        if N == 0 and P == 0 and K == 0:
            result = "Please provide valid input values for all fields."
            return render_template('index.html', result=result)
        
        feature_list = [N, P, K, temp, humidity, ph, rainfall]
        single_pred = np.array(feature_list).reshape(1, -1)
        
        # Apply transformations
        mx_features = mx.transform(single_pred)
        sc_mx_features = sc.transform(mx_features)
        prediction = model.predict(sc_mx_features)
        
        crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                     8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                     14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                     19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}
        
        if prediction[0] in crop_dict:
            crop = crop_dict[prediction[0]]
            result = f"{crop} is the best crop to be cultivated right there"
        else:
            result = "Sorry, we could not determine the best crop to be cultivated with the provided data."
            
    except ValueError as ve:
        result = "Invalid input: Please enter numeric values only."
        print(f"ValueError: {ve}")
    except Exception as e:
        result = "Sorry, we could not determine the best crop to be cultivated with the provided data."
        print(f"Error: {e}")
    
    return render_template('index.html', result=result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)