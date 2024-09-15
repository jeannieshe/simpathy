using System.Collections;
using System.Collections.Generic;  // Add this for List<>
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.XR;
using System.IO;

public class ControllerAudioRecorder : MonoBehaviour
{
    private AudioClip recordedClip; // Store the recorded audio
    private bool isRecording = false; // Track recording state
    private string filePath = "recording.wav";
    private string directoryPath;
    private InputDevice rightHandController;

    // URL of the Flask backend API
    public string flaskApiUrl = "http://localhost:5000/processAudio"; // Update this to your Flask backend URL

    void Start()
    {
        // Set up the local directory path to save the recording
        directoryPath = Application.persistentDataPath + "/Recordings";
        if (!Directory.Exists(directoryPath))
        {
            Directory.CreateDirectory(directoryPath);
        }

        Debug.Log("Ready to record and send audio.");

        // Try to initialize the right-hand controller
        TryInitializeRightHandController();
    }

    void TryInitializeRightHandController()
    {
        List<InputDevice> devices = new List<InputDevice>();
        InputDeviceCharacteristics rightHandedControllerCharacteristics = InputDeviceCharacteristics.Right | InputDeviceCharacteristics.Controller;
        InputDevices.GetDevicesWithCharacteristics(rightHandedControllerCharacteristics, devices);

        if (devices.Count > 0)
        {
            rightHandController = devices[0]; // Assign the first detected right-hand controller
            Debug.Log("Right hand controller detected.");
        }
        else
        {
            Debug.LogError("Right hand controller not found! Please check the headset and controller connection.");
        }
    }

    void Update()
    {
        // Check if the right-hand controller is still valid
        if (!rightHandController.isValid)
        {
            TryInitializeRightHandController(); // Re-initialize if disconnected
        }

        // Record and send audio based on the trigger button press
        if (rightHandController.isValid)
        {
            bool triggerValue;
            if (rightHandController.TryGetFeatureValue(CommonUsages.triggerButton, out triggerValue))
            {
                if (triggerValue && !isRecording)
                {
                    StartRecording();
                }
                else if (!triggerValue && isRecording)
                {
                    StopRecordingAndSendToBackend();
                }
            }
        }
    }

    // Start recording audio from the microphone
    void StartRecording()
    {
        int sampleRate = 44100;
        recordedClip = Microphone.Start(null, true, 300, sampleRate); // Max 5 minutes recording
        isRecording = true;
        Debug.Log("Recording started...");
    }

    void SaveAudioClip(AudioClip clip)
    {
        string filePath = Path.Combine(Application.persistentDataPath, "recording.wav");

        // Convert audio clip to .wav file
        byte[] wavFile = AudioClipToWav(clip);

        // Write the file to disk
        File.WriteAllBytes(filePath, wavFile);
        Debug.Log("File saved at: " + filePath);
    }

    // Stop recording, trim the audio, save locally, and send to Flask backend
void StopRecordingAndSendToBackend()
{
    if (Microphone.IsRecording(null))
    {
        int recordingPosition = Microphone.GetPosition(null); // Get the current position of the recording
        Microphone.End(null); // Stop the recording
        isRecording = false;
        Debug.Log("Recording stopped, preparing to send to Flask...");
        SaveAudioClip(recordedClip)
        // Trim the audio clip to the actual recording length
        AudioClip trimmedClip = TrimAudioClip(recordedClip, recordingPosition);
        // Save the recording locally
        string fullPath = Path.Combine(directoryPath, filePath);
        WavUtility.Save(fullPath, trimmedClip);
        Debug.Log($"Recording saved locally at {fullPath}");

        // Send the audio file to Flask backend
        StartCoroutine(SendAudioToFlask(fullPath));
    }
}

// Function to trim the AudioClip
AudioClip TrimAudioClip(AudioClip clip, int recordingPosition)
{
    int samples = recordingPosition * clip.channels;
    float[] data = new float[samples];
    clip.GetData(data, 0); // Get the recorded samples up to the actual recorded position

    AudioClip trimmedClip = AudioClip.Create(clip.name + "_trimmed", samples, clip.channels, clip.frequency, false);
    trimmedClip.SetData(data, 0); // Set the trimmed data to the new clip

    return trimmedClip;
}



    // Coroutine to send the audio to Flask backend
    IEnumerator SendAudioToFlask(string audioFilePath)
    {
        byte[] audioData = File.ReadAllBytes(audioFilePath);
        WWWForm form = new WWWForm();
        form.AddBinaryData("audio", audioData, "userSpeech.wav", "audio/wav");

        using (UnityWebRequest request = UnityWebRequest.Post(flaskApiUrl, form))
        {
            yield return request.SendWebRequest();

            if (request.result == UnityWebRequest.Result.ConnectionError || request.result == UnityWebRequest.Result.ProtocolError)
            {
                Debug.LogError("Error sending audio to Flask: " + request.error);
            }
            else
            {
                Debug.Log("Audio successfully sent to Flask.");
            }
        }
    }
}
