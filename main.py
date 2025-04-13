from flask_cors import CORS
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configure the Google Generative AI API
genai.configure(api_key="AIzaSyAqN9T7P_ldExMNL2KN592bnEzCPlKSuH8")

@app.route('/')
def home():
    return "Flask server is running on the root!"

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json  # Get JSON data from the request
    user_input = data.get('input', '')
    category = data.get('category', '')

    if not user_input or not category:
        return jsonify({'error': 'Missing input or category'}), 400

    # Define the prompts for different sections
    prompts = []
    if category == "Disease":
        prompts = [
            f"Please provide details about the symptoms of the disease: {user_input} (Response size = max 50 words!)",
            f"Please provide the cure for the disease: {user_input} (Response size = max 50 words!)",
            f"Please provide the prevention methods for the disease: {user_input} (Response size = max 50 words!)"
        ]
    elif category == "Symptoms":
        prompts = [
            f"Provide possible diseases related to the symptoms mentioned: {user_input} (Response size = max 50 words!)",
            f"Please provide the cure for the diseases related to the symptoms: {user_input} (Response size = max 50 words!)",
            f"Please provide the prevention methods for the diseases related to the symptoms: {user_input} (Response size = max 50 words!)"
        ]
    else:
        return jsonify({'error': 'Invalid category selected'}), 400

    # Generate the responses for each part
    try:
        # List to store the responses for Symptoms, Cure, and Prevention
        responses = {}
        sections = ["symptoms", "cure", "prevention"]

        for i, section in enumerate(sections):
            # Use the Generative AI model to get a response for each section
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompts[i])
            responses[section] = response.text.strip()

        # Format the response into a structured HTML format
        formatted_response = format_response(responses, category)

        return jsonify({'response': formatted_response})  # Return the AI's structured and formatted response

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def format_response(responses, category):
    if category == "Disease":
        formatted = f"""
        <div>
            <h2>Disease Details</h2>
            <h3>Symptoms</h3>
            <p>{responses['symptoms']}</p><br>
            
            <h3>Cure</h3>
            <p>{responses['cure']}</p><br>
            
            <h3>Prevention</h3>
            <p>{responses['prevention']}</p>
        </div>
        """
    elif category == "Symptoms":
        formatted = f"""
        <div>
            <h2>Possible Disease Information</h2>
            <h3>Possible Disease</h3>
            <p>{responses['symptoms']}</p><br>

            <h3>Cure</h3>
            <p>{responses['cure']}</p><br>

            <h3>Prevention</h3>
            <p>{responses['prevention']}</p>
        </div>
        """
    return formatted

if __name__ == "__main__":
    app.run(debug=True)
