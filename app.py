import os
from google import genai
from flask import Flask, request, jsonify, render_template
# Loads environment variables from .env file
from dotenv import load_dotenv 
# Load API keys / secrets into environment
load_dotenv()

# Create Flask app instance
app = Flask(__name__)

# Initialize Gemini client (uses GOOGLE_API_KEY from env automatically)
client =  genai.Client()

# =========================
# HOME ROUTE (UI PAGE)
# =========================
@app.route("/") 
def index(): 
    return render_template("index.html")



# =========================
# CODE REVIEW API ROUTE
# =========================
@app.route("/review", methods=["POST"])
def review_code():
    # Get JSON data sent from frontend
    data = request.get_json()
    # Extract the code string
    user_code = data.get('code')

    # Validate input (empty check)
    if not user_code or user_code.strip() == "":
        return jsonify({"error": "No code provided"}), 400

    try:
        # Send request to Gemini model
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            # Prompt engineering: defines AI behavior
            contents=f"You are an expert Senior Software Engineer. Provide a concise code review for the following snippet. Focus on bugs, security, and performance:\n\n{user_code}"
        )
        # Extract AI response text
        feedback = response.text
        # Return response to frontend
        return jsonify({"feedback": response.text})

    except Exception as e:
        # Debug error in terminal
        print(f"Error: {e}")
        # Return safe error message to frontend
        return jsonify({"error": "Failed to get review from Gemini."}), 500


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(debug=True)