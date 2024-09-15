# SIMPATHY project at HackMIT 2024!

### A VR simulation to practice compassion in tough medical scenarios for doctors-to-be!

## Inspiration
Our project provides a VR simulation to train residents and future medical students with 10 different tricky medical situations, inspired by the MMI test in Canada. The user will attempt to connect with the VR-animated patient to practice their interpersonal skills. At the end of the conversation, Google Gemini AI will send an evaluation for the user’s performance on a scale from 0 to 10 on Empathy, Professionalism, and Medical skill.

## Techstack
The model and animations are created by Blender and imported into Unity, and Unity will record and send the voice recordings made by the user to the Flask backend in our file voicetotext_API.py. The Flask backend would then transcribe the user voice using OpenAI Whisper for the Google Gemini API to generate a response based on the character and the situation, and then the AI character generated response will be turned to voice using Python TTS which will be played back to the user.

## Challenges
Our members have little to no knowledge about VR Development, therefore we do not have knowledge developing Unity in C#. We also ran into some trouble integrating the separate AI models together with Unity, as well as activating the record and stop function on Unity and generating the .Wav file to send to the backend. Developing the Google Gemini API to consistently act as the patient instead of the doctor took quite a bit of debugging as well.

## Accomplishments
We are extremely proud of all we have learned as a beginner team. For some of us, within the 24 hours of the hackathon, we both learned what an API was and implemented them. For all of us, this was our first time carrying out a software/VR idea from start to finish. We had so much fun meeting each other, learning about each other’s skillsets, and practicing good teamwork skills over the course of the hackathon.

## Takeaways
We learn how to transcribe texts from voices using OpenAI Whisper, as well as utilizing Flask as a backend for the Unity application. We learned how to record audio input from the MetaQuest 2 microphone and produce a .wav file, which was later sent via an API request to our Flask backend pipeline. We learned how to create a pipeline that connects all three of our AIs together: taking as input a .wav file (the user input) and generating text, returning an appropriate generative AI response, and then translating text to a .wav file to be heard by the user.

## What's next?
More characters with more unique situations and better animations for the characters, i.e incorporate face emotions!

## [Check out our presentation here!](https://docs.google.com/presentation/d/1GhTf6ybHQ1rYUBNUPsyxLyXtUSu0VUYRH_obkCJZHi4/edit?usp=sharing)
