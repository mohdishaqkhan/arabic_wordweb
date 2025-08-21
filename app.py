import os
import json
import requests
from flask import Flask, jsonify, request # Import 'request' object
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/api/data', methods=['POST']) # Set the method to POST
def get_data():
    # Get the API key from the environment variable
    gm_api_key = os.environ.get('GM_API_KEY')
    if not gm_api_key:
        return jsonify({"error": "API key not found."}), 500

    # Ensure the request is a JSON POST request
    if not request.json:
        return jsonify({"error": "Request body must be JSON."}), 400

    # Get the user prompt from the JSON body
    user_prompt = request.json.get('prompt')
    if not user_prompt:
        return jsonify({"error": "No 'prompt' field in the request body."}), 400

    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gm_api_key}'
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": user_prompt}
                ]
            }
        ],
        # Add generationConfig for JSON output, as you had in your original JS
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    
    try:
        # Make the request to the Gemini API
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        # Parse the JSON response from the Gemini API
        gemini_response_data = response.json()
        
        # Extract the text part of the response
        if 'candidates' in gemini_response_data and len(gemini_response_data['candidates']) > 0:
            generated_content = gemini_response_data['candidates'][0]['content']['parts'][0]['text']
            
            # The generated content is a stringified JSON, so parse it
            parsed_data = json.loads(generated_content)
            
            # Return the parsed data to the client
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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
