from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# YAHAN APNI KEY DAALNI HAI
ASSEMBLY_AI_KEY = "45ea70952de74c0b9e54541a85cb136a" 

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    headers = {'authorization': ASSEMBLY_AI_KEY}

    # 1. Video AssemblyAI par bhej rahe hain
    upload_response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, data=file.read())
    audio_url = upload_response.json().get('upload_url')

    # 2. Captions generate karne ka command
    json_data = {'audio_url': audio_url}
    transcript_response = requests.post('https://api.assemblyai.com/v2/transcript', json=json_data, headers=headers)

    return jsonify(transcript_response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
