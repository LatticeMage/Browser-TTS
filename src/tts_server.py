# tts_server.py

from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS extension
from tts_jp import speak_text  # Import your TTS function

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    text = data.get('text')

    if text:
        speak_text(text)  # Call your TTS function
        return jsonify({'status': 'speaking', 'text': text})
    else:
        return jsonify({'error': 'No text provided'}, 400)

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Or your preferred port