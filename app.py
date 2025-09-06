import json
import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---- DIRECTLY SET YOUR GEMINI API KEY HERE ----
GM_API_KEY = "AIzaSyDgKgG3__XCgA9d1tkaIa-oM1aCPT_eShE"  # <-- Replace with your actual Gemini API key

@app.route('/')
def serve_index():
    """Serves the index.html file."""
    return render_template('index.html')

@app.route('/api/data', methods=['POST'])
def get_data():
    """
    Handles POST requests to the /api/data endpoint.
    It takes a prompt from the frontend, sends it to the Gemini API,
    and returns a JSON response.
    """
    if not GM_API_KEY or GM_API_KEY == "AIzaSyDgKgG3__XCgA9d1tkaIa-oM1aCPT_eShE":
        return jsonify({"error": "Please set your Gemini API key in app.py."}), 500

    if not request.json:
        return jsonify({"error": "Request body must be JSON."}), 400

    user_prompt = request.json.get('prompt')
    if not user_prompt:
        return jsonify({"error": "No 'prompt' field in the request body."}), 400

    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GM_API_KEY}'

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": user_prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        gemini_response_data = response.json()

        if 'candidates' in gemini_response_data and len(gemini_response_data['candidates']) > 0:
            generated_content = gemini_response_data['candidates'][0]['content']['parts'][0]['text']
            parsed_data = json.loads(generated_content)
            return jsonify(parsed_data)
        else:
            return jsonify({"error": "Gemini API did not return a valid response."}), 500

    except requests.exceptions.RequestException as e:
        print(f"Request to Gemini API failed: {e}")
        return jsonify({"error": "Failed to connect to the Gemini API."}), 500
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error parsing Gemini response: {e}")
        return jsonify({"error": "Invalid or malformed JSON response from Gemini API."}), 500

if __name__ == '__main__':
    port = 5000
    app.run(host='0.0.0.0', port=port, debug=True)
