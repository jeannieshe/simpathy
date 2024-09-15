from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Directory to save the received audio files
UPLOAD_FOLDER = 'received_audio'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/processAudio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file found in the request"}), 400

    audio_file = request.files['audio']
    audio_path = os.path.join(UPLOAD_FOLDER, audio_file.filename)
    audio_file.save(audio_path)

    print(f"Audio file received and saved at {audio_path}")
    return jsonify({"message": "Audio received successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
