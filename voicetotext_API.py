from flask import request, send_file
from flask import Flask, jsonify
# import sounddevice as sd
import whisper
# import numpy as np
# from scipy.io.wavfile import write
# import threading
# import torch
# from TTS.api import TTS
from dialogues.tts_test import textToSpeech
from dialogues.gemini_api import geminiInteraction
import whisper

# Initialize Whisper model
model = whisper.load_model("base")

app = Flask(__name__)

# fs = 44100  # Sample rate
# output_file = "output.wav"
# recording = []
# is_recording = False

# # Callback function to capture audio chunks
# def audio_callback(indata, frames, time, status):
#     recording.append(indata.copy())

# Start recording
# @app.route('/start_recording', methods=['GET'])
# def start_recording():
#     global recording, is_recording
#     recording = []
#     is_recording = True
#     threading.Thread(target=record_audio).start()
#     return jsonify({"message": "Recording started"})

# # Stop recording and transcribe the audio
# @app.route('/stop_recording', methods=['GET'])
# def stop_recording():
#     global is_recording
#     is_recording = False
#     return jsonify({"message": "Recording stopped. Transcribing..."})

# send starting message to VR for captions

@app.route('/message', methods=['PUT'])
def generateMessage():
    """
    Takes in a .wav file, turns it into text, sends it to Gemini, receive a Gemini response,
    turns response to .wav file. Sends boolean describing termination screen, and if not
    terminated, the filepath of .wav output.

    Input: no arguments, but will be a .wav file from the VR

    Returns: json object with two keys: "terminate": (boolean of whether or not the simulation has ended),
    and "filepath": (of output .wav)
    """
    # Save file
    f = request.files['audio_file']
    f.save('user_input.wav')

    # Generate transcription
    result = model.transcribe('user_input.wav')

    user_input_text = result['text']
    # Generate response from Gemini
    model_output_text = geminiInteraction(user_input_text)
    if model_output_text == "terminate":
        return jsonify({ "terminate": True, "filepath": "" })

    # Generate a wav file from text
    model_output_audio_filepath = textToSpeech(model_output_text)

    return jsonify({ "terminate": False, "filepath": model_output_audio_filepath })

@app.route('/file', methods=['GET'])
def getFile():
    # print(request)
    filename = request.args.get('filename') # receive filepath from VR
    return send_file(filename, as_attachment=True) # send .wav file to VR


# Function to handle the recording process
# def record_audio():
#     global recording
#     with sd.InputStream(samplerate=fs, channels=1, callback=audio_callback):
#         while is_recording:
#             sd.sleep(100)  # Keep recording
    
#     # Save the recording as a WAV file
#     audio_data = np.concatenate(recording, axis=0)
#     write(output_file, fs, audio_data)
    
#     # Transcribe the saved audio file
#     result = model.transcribe(output_file)
#     print("Transcription:", result['text'])

#     return result['text']

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
