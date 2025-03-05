from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Allows frontend to communicate with backend

# File to store appointment data
data_file = "appointments.xlsx"

@app.route("/")
def home():
    return "Chatbot Backend is Running!"

@app.route("/save", methods=["POST"])
def save_data():
    try:
        data = request.json
        df = pd.DataFrame([data])  # Convert JSON to DataFrame

        # Check if file exists, append or create new
        if os.path.exists(data_file):
            existing_df = pd.read_excel(data_file)
            df = pd.concat([existing_df, df], ignore_index=True)
        
        df.to_excel(data_file, index=False)
        
        return jsonify({"message": "Data saved successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
