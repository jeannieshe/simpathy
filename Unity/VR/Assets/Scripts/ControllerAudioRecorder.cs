using UnityEngine;
using System.IO;
using System;

public class AudioRecorder : MonoBehaviour
{
    private AudioClip audioClip;
    private string microphoneDevice;
    private bool isRecording = false;

    void Start()
    {
        // Check if any microphones are available
        if (Microphone.devices.Length > 0)
        {
            // Get the first available microphone device
            microphoneDevice = Microphone.devices[0];
            Debug.Log("Using microphone: " + microphoneDevice);
        }
        else
        {
            Debug.LogError("No microphone devices found!");
        }
    }

    public void StartRecording()
    {
        if (isRecording || microphoneDevice == null)
        {
            Debug.LogWarning("Recording is already in progress or no microphone available.");
            return;
        }

        // Start recording, no looping, record for 10 seconds, sample rate of 44100 Hz
        audioClip = Microphone.Start(microphoneDevice, false, 10, 44100);
        isRecording = true;
        Debug.Log("Recording started...");
    }

    // public void StopRecordingAndSave()
    // {
    //     if (!isRecording)
    //     {
    //         Debug.LogWarning("No recording to stop.");
    //         return;
    //     }

    //     // Stop recording
    //     Microphone.End(microphoneDevice);
    //     isRecording = false;
    //     Debug.Log("Recording stopped.");

    //     // Save the recorded AudioClip as a .wav file
    //     SaveAudioClip(audioClip);
    // }

    public void StopRecordingAndSave()
{
    if (!isRecording)
    {
        Debug.LogWarning("No recording to stop.");
        return;
    }

    // Stop recording
    Microphone.End(microphoneDevice);
    isRecording = false;
    Debug.Log("Recording stopped.");

    // Save the recorded AudioClip as a .wav file
    string filePath = Path.Combine(Application.persistentDataPath, "recording.wav");
    SaveAudioClip(audioClip, filePath);

    // Send the saved .wav file to the Flask backend
    StartCoroutine(SendAudioToFlask(filePath));
}

private IEnumerator SendAudioToFlask(string filePath)
{
    // Read the saved .wav file into a byte array
    byte[] audioData = File.ReadAllBytes(filePath);

    // Create a form to hold the file data
    WWWForm form = new WWWForm();
    form.AddBinaryData("audio_file", audioData, "recording.wav", "audio/wav");

    // Send the request to Flask using UnityWebRequest
    UnityWebRequest www = UnityWebRequest.Post("http://localhost:3000/message", form); // Update with your Flask server URL

    // Wait for the request to complete
    yield return www.SendWebRequest();

    // Check for errors
    if (www.result == UnityWebRequest.Result.ConnectionError || www.result == UnityWebRequest.Result.ProtocolError)
{
    Debug.LogError("Error sending audio to Flask: " + www.error);
}
else
{
    Debug.Log("Audio successfully sent to Flask. Response: " + www.downloadHandler.text);

    // Assuming Flask returns JSON (e.g., {"terminate": false, "filepath": "path_to_file.wav"})
    var jsonResponse = JsonUtility.FromJson<FlaskResponse>(www.downloadHandler.text);
    if (!jsonResponse.terminate && !string.IsNullOrEmpty(jsonResponse.filepath))
    {
        StartCoroutine(DownloadProcessedAudio(jsonResponse.filepath));
    }
    else
    {
        Debug.Log("Conversation terminated or no audio file returned.");
    }
}
}

[Serializable]
private class FlaskResponse
{
    public bool terminate;
    public string filepath;
}



private IEnumerator DownloadProcessedAudio(string fileUrl)
{
    UnityWebRequest www = UnityWebRequestMultimedia.GetAudioClip(fileUrl, AudioType.WAV);
    yield return www.SendWebRequest();

    if (www.result == UnityWebRequest.Result.ConnectionError || www.result == UnityWebRequest.Result.ProtocolError)
    {
        Debug.LogError("Error downloading processed audio: " + www.error);
    }
    else
    {
        AudioClip clip = DownloadHandlerAudioClip.GetContent(www);
        PlayAudioClip(clip);
    }
}

private void PlayAudioClip(AudioClip clip)
{
    AudioSource audioSource = GetComponent<AudioSource>();
    audioSource.clip = clip;
    audioSource.Play();
}


    private void SaveAudioClip(AudioClip clip)
    {
        string filePath = Path.Combine(Application.persistentDataPath, "recording.wav");

        // Convert the AudioClip to WAV format
        byte[] wavFile = AudioClipToWav(clip);

        // Write the .wav file to disk
        File.WriteAllBytes(filePath, wavFile);
        Debug.Log("File saved at: " + filePath);
    }

    private byte[] AudioClipToWav(AudioClip clip)
    {
        using (MemoryStream stream = new MemoryStream())
        {
            int headerSize = 44; // Standard WAV header size
            int fileSize = clip.samples * clip.channels * 2 + headerSize;

            byte[] header = new byte[headerSize];
            byte[] audioData = new byte[clip.samples * clip.channels * 2];

            // Write WAV header
            WriteWavHeader(header, fileSize, clip.frequency, clip.channels);
            // Convert the audio clip data to bytes
            ConvertAudioClipSamplesToBytes(clip, audioData);

            // Combine header and audio data
            stream.Write(header, 0, header.Length);
            stream.Write(audioData, 0, audioData.Length);

            return stream.ToArray();
        }
    }

    private void WriteWavHeader(byte[] header, int fileSize, int frequency, int channels)
    {
        // Create a valid WAV header (44 bytes)
        // "RIFF" chunk descriptor
        header[0] = (byte)'R';
        header[1] = (byte)'I';
        header[2] = (byte)'F';
        header[3] = (byte)'F';

        // File size minus first 8 bytes of RIFF descriptor
        BitConverter.GetBytes(fileSize - 8).CopyTo(header, 4);

        // "WAVE" format
        header[8] = (byte)'W';
        header[9] = (byte)'A';
        header[10] = (byte)'V';
        header[11] = (byte)'E';

        // "fmt " subchunk
        header[12] = (byte)'f';
        header[13] = (byte)'m';
        header[14] = (byte)'t';
        header[15] = (byte)' ';

        // Subchunk1 size (16 for PCM)
        BitConverter.GetBytes(16).CopyTo(header, 16);

        // Audio format (1 = PCM)
        BitConverter.GetBytes((short)1).CopyTo(header, 20);

        // Number of channels
        BitConverter.GetBytes((short)channels).CopyTo(header, 22);

        // Sample rate
        BitConverter.GetBytes(frequency).CopyTo(header, 24);

        // Byte rate (SampleRate * NumChannels * BitsPerSample/8)
        BitConverter.GetBytes(frequency * channels * 2).CopyTo(header, 28);

        // Block align (NumChannels * BitsPerSample/8)
        BitConverter.GetBytes((short)(channels * 2)).CopyTo(header, 32);

        // Bits per sample (16 bits here)
        BitConverter.GetBytes((short)16).CopyTo(header, 34);

        // "data" subchunk
        header[36] = (byte)'d';
        header[37] = (byte)'a';
        header[38] = (byte)'t';
        header[39] = (byte)'a';

        // Data size (NumSamples * NumChannels * BitsPerSample/8)
        BitConverter.GetBytes(fileSize-44).CopyTo(header, 40);
    }

    private void ConvertAudioClipSamplesToBytes(AudioClip clip, byte[] audioData)
    {
        float[] samples = new float[clip.samples * clip.channels];
        clip.GetData(samples, 0);
        
        for (int i = 0; i < samples.Length; i++)
        {
            short sampleShort = (short)(samples[i] * short.MaxValue);
            byte[] bytes = BitConverter.GetBytes(sampleShort);
            bytes.CopyTo(audioData, i * 2); // 2 bytes per sample
        }
    }

    // For testing purposes, bind StartRecording() and StopRecordingAndSave() to keyboard inputs
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.R))
        {
            StartRecording();
        }

        if (Input.GetKeyDown(KeyCode.S))
        {
            StopRecordingAndSave();
        }
    }
}