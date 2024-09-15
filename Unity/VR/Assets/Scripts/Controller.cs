using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class AudioLoader : MonoBehaviour
{
    public string apiUrl = "http://localhost:5000/get-audio"; 

 
    public AudioSource audioSource;

    void Start()
    {
          StartCoroutine(GetAudioFromApi());
    }

    IEnumerator GetAudioFromApi()
    {
        
        UnityWebRequest request = UnityWebRequestMultimedia.GetAudioClip(apiUrl, AudioType.WAV);
        yield return request.SendWebRequest(
);

        if (request.result == UnityWebRequest.Result.ConnectionError || request.result == UnityWebRequest.Result.ProtocolError)
        {
            Debug.LogError("Error downloading audio: " + request.error);
        }
        else
        {
            
            AudioClip clip = DownloadHandlerAudioClip.GetContent(request);
            audioSource.clip = clip;
            audioSource.Play();
        }
    }
}