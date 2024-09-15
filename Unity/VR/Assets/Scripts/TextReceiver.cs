using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using System.IO;
using TMPro;  // Import TextMeshPro namespace

public class TextReceiver : MonoBehaviour
{
    // URL to your Flask server to download the file
    private string url = "http://localhost:3000/file?filename=caption.txt";

    // Variable to store the last downloaded content
    private string lastFileContent = "";

    // Path to save the file in the Unity Assets folder
    private string filePath;

    // Reference to the TextMeshPro component
    public TextMeshProUGUI textMeshPro;

    void Start()
    {
        // Set the path to the Assets folder (You can choose a specific subfolder inside Assets if needed)
        filePath = Application.dataPath + "/DownloadedFiles/updated_file.txt";  // Ensure this folder exists

        // Start the polling coroutine
        StartCoroutine(PollForFileUpdates());
    }

    // Coroutine to continuously poll for file updates
    IEnumerator PollForFileUpdates()
    {
        // Infinite loop to poll every few seconds
        while (true)
        {
            // Fetch the file and check for changes
            yield return StartCoroutine(FetchFile());

            // Wait for 5 seconds before the next poll (or adjust as needed)
            yield return new WaitForSeconds(5);
        }
    }

    // Coroutine to fetch the file
    IEnumerator FetchFile()
    {
        UnityWebRequest www = UnityWebRequest.Get(url);
        yield return www.SendWebRequest();

        // Check for network errors
        if (www.result == UnityWebRequest.Result.ConnectionError || www.result == UnityWebRequest.Result.ProtocolError)
        {
            Debug.LogError(www.error);
        }
        else
        {
            // Get the file content
            string currentFileContent = www.downloadHandler.text;

            // Check if the content has changed
            if (currentFileContent != lastFileContent)
            {
                Debug.Log("File content has changed.");
                lastFileContent = currentFileContent;

                // Save the updated content in the Assets folder
                SaveFileToAssets(currentFileContent);

                // Update TextMeshPro with the new content
                UpdateTextMeshPro(currentFileContent);
            }
            else
            {
                Debug.Log("File content is the same, no update needed.");
            }
        }
    }

    // Method to save the file to the Assets folder
    void SaveFileToAssets(string content)
    {
        // Ensure the directory exists (if not, create it)
        string directory = Path.GetDirectoryName(filePath);
        if (!Directory.Exists(directory))
        {
            Directory.CreateDirectory(directory);
        }

        // Write the content to the file
        File.WriteAllText(filePath, content);
        Debug.Log("File saved at: " + filePath);

        // Refresh the Unity Asset Database to ensure the file shows up in the editor
        #if UNITY_EDITOR
        UnityEditor.AssetDatabase.Refresh();
        #endif
    }

    // Method to update TextMeshPro component with new content
    void UpdateTextMeshPro(string content)
    {
        if (textMeshPro != null)
        {
            textMeshPro.text = content;  // Update the TextMeshPro component
            Debug.Log("TextMeshPro updated with new content.");
        }
        else
        {
            Debug.LogError("TextMeshPro component is not assigned.");
        }
    }
}
