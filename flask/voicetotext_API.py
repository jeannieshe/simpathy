from flask import Flask, jsonify
import sounddevice as sd
import whisper
import numpy as np
from scipy.io.wavfile import write
import threading

# Initialize Whisper model
model = whisper.load_model("base")

app = Flask(__name__)

fs = 44100  # Sample rate
output_file = "output.wav"
recording = []
is_recording = False

# Callback function to capture audio chunks
def audio_callback(indata, frames, time, status):
    recording.append(indata.copy())

# Start recording
@app.route('/start_recording', methods=['GET'])
def start_recording():
    global recording, is_recording
    recording = []
    is_recording = True
    threading.Thread(target=record_audio).start()
    return jsonify({"message": "Recording started"})

# Stop recording and transcribe the audio
@app.route('/stop_recording', methods=['GET'])
def stop_recording():
    global is_recording
    is_recording = False
    return jsonify({"message": "Recording stopped. Transcribing..."})

# Function to handle the recording process
def record_audio():
    global recording
    with sd.InputStream(samplerate=fs, channels=1, callback=audio_callback):
        while is_recording:
            sd.sleep(100)  # Keep recording
    
    # Save the recording as a WAV file
    audio_data = np.concatenate(recording, axis=0)
    write(output_file, fs, audio_data)
    
    # Transcribe the saved audio file
    result = model.transcribe(output_file)
    print("Transcription:", result['text'])

    return result['text']

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
