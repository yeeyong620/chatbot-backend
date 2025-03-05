from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Sample route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Chatbot backend is running!"})

# API to receive and store general form responses
@app.route("/submit", methods=["POST"])
def submit_data():
    try:
        data = request.json  # Get JSON data from request
        df = pd.DataFrame([data])  # Convert JSON to Pandas DataFrame

        # Define the Excel file path
        excel_file = "responses.xlsx"

        # Check if file exists, if yes, append data
        if os.path.exists(excel_file):
            existing_df = pd.read_excel(excel_file)
            df = pd.concat([existing_df, df], ignore_index=True)

        # Save DataFrame to Excel
        df.to_excel(excel_file, index=False)

        return jsonify({"message": "Data saved successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# New API to handle 'Tukar Temu Janji' requests
@app.route("/save_appointment", methods=["POST"])
def save_appointment():
    try:
        data = request.json  # Get JSON data from request
        df = pd.DataFrame([{
            "Nama": data.get("userName"),
            "IC": data.get("userIC"),
            "Tarikh Lama": data.get("oldDate"),
            "Tarikh Baru": data.get("newDate")
        }])

        # Define the Excel file path for appointments
        excel_file = "appointments.xlsx"

        # Append data if file exists
        if os.path.exists(excel_file):
            existing_df = pd.read_excel(excel_file)
            df = pd.concat([existing_df, df], ignore_index=True)

        # Save DataFrame to Excel
        df.to_excel(excel_file, index=False)

        return jsonify({"message": "Appointment data saved successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get the PORT from environment variables (default to 10000)
port = int(os.environ.get("PORT", 10000))

# Run the app on 0.0.0.0 to make it accessible on Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

