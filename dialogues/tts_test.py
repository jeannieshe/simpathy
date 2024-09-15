# import torch
import gtts

# Get device
# device = "cuda" if torch.cuda.is_available() else "cpu"

# List available TTS models
# print(TTS().list_models())

# Initialize TTS model
# model_path = "tts_models/en/ljspeech/tacotron2-DDC"  # Example model that doesn't require a speaker file
# tts = TTS(model_path).to(device)

# # Run TTS and save output to file
# text = "Hello world, this is an ai generated audio file!"
# output_file = "output.wav"

# Generate speech and save to file
# tts.tts_to_file(text=text, file_path=output_file)

# print(f"Generated speech saved to {output_file}")

def textToSpeech(input):
    """
    Produces text to speech using the Coqui TTS package.
    Input: input is a string containing the text which we wish to turn into audio.
    Returns: the file path of the .wav file that is produced.
    """

    print(input)

    output_file = "AI_to_speech.mp3"
    # tts.tts_to_file(text=input, file_path=output_file)
    tts = gtts.gTTS(input)
    tts.save(output_file)

    # print(f"Generated speech saved to {output_file}")
    return output_file