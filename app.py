
from flask import Flask, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
import os
@app.route('/api/data')
def get_data():
    gm_api_key = os.environ.get('GM_API_KEY')
    # Example API call (replace with your API)
    # response = requests.get('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}')
    # data = response.json()
    user_prompt = request.json.get('prompt', '')  # Get prompt from frontend
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gm_api_key}'
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": user_prompt}
                ]
            }
        ]
    }
    response = requests.post(url, json=payload)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
