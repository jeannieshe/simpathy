import tkinter as tk
import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import threading
import numpy as np

# Audio settings
fs = 44100  # Sample rate
recording = None
is_recording = False  # Flag to check if currently recording
output_file = "output.wav"  # Output WAV file

# Initialize the Whisper model
model = whisper.load_model("base")

# Function to start recording
def start_recording():
    global recording, is_recording
    is_recording = True
    threading.Thread(target=record_audio).start()  # Start the recording in a separate thread

def record_audio():
    global recording, is_recording
    print("Recording started... Press 'Stop' to finish.")
    recording = []  # Reset recording
    with sd.InputStream(samplerate=fs, channels=1, callback=audio_callback):
        while is_recording:
            sd.sleep(100)  # Sleep while recording
    
    # After recording is stopped, save the file and transcribe
    print("Recording stopped. Saving file and transcribing...")
    recording_array = np.concatenate(recording, axis=0)
    write(output_file, fs, recording_array)  # Save the recording as WAV
    transcribe_audio()

# Callback function for sounddevice to handle chunks of audio data
def audio_callback(indata, frames, time, status):
    global recording
    recording.append(indata.copy())  # Append the recorded chunk to the list

# Function to stop recording
def stop_recording():
    global is_recording
    is_recording = False  # This will stop the recording loop

# Function to transcribe the saved audio using Whisper
def transcribe_audio():
    # Transcribe the audio file
    result = model.transcribe(output_file)
    print("Transcription: ", result['text'])  # Print the transcription to the terminal

# Create the Tkinter GUI
window = tk.Tk()
window.title("Voice to Text")
window.geometry("300x150")

# Button to start recording
record_button = tk.Button(window, text="Record", command=start_recording, width=10)
record_button.pack(pady=20)

# Button to stop recording
stop_button = tk.Button(window, text="Stop", command=stop_recording, width=10)
stop_button.pack(pady=10)

# Start the Tkinter event loop
window.mainloop()
