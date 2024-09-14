import tkinter as tk
import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import threading

#Audio recording settings
fs = 16000  #Sample rate
seconds = 5  #Duration of recording
output_file = "output.wav"

#Initialize Whisper model
model = whisper.load_model("base")

# Function to start recording
def start_recording():
    #Start a new thread to avoid freezing the GUI
    threading.Thread(target=record_audio).start()

def record_audio():
    global myrecording
    transcription_text.set("Recording started...")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    write(output_file, fs, myrecording)  # Save as WAV file

    transcribe_audio()

# Function to stop recording
def stop_recording():
    transcription_text.set("Recording stopped.")
    transcription_text.set("Recording finished. Now transcribing...")
    sd.stop()

# Function to transcribe the audio using Whisper
def transcribe_audio():
    # Run the transcription in a separate thread to avoid freezing the GUI
    threading.Thread(target=transcribe_thread).start()

def transcribe_thread():
    # Load the recorded file and transcribe using Whisper
    result = model.transcribe(output_file)
    
    # Update the transcription label in the GUI with the result
    transcription_text.set(result['text'])

# Create a Tkinter window (For testing only)
window = tk.Tk()
window.title("Voice to Text")
window.geometry("400x300")

# Record button to start recording
record_button = tk.Button(window, text="Record", command=start_recording, width=10)
record_button.pack(pady=20)

# Stop button to stop recording (not needed in this setup, but included)
stop_button = tk.Button(window, text="Stop", command=stop_recording, width=10)
stop_button.pack(pady=10)

# Label to display the transcription
transcription_text = tk.StringVar()
transcription_label = tk.Label(window, textvariable=transcription_text, wraplength=350)
transcription_label.pack(pady=20)

# Set an initial value for the transcription text
transcription_text.set("Transcription will appear here.")

# Start the Tkinter event loop
window.mainloop()
