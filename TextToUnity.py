from flask import Flask, Response, jsonify
import requests

app = Flask(__name__)

# URL to your raw file on GitHub
GITHUB_RAW_FILE_URL = 'https://raw.githubusercontent.com/jeannieshe/simpathy/main/caption.txt'

@app.route('/download_file', methods=['GET'])
def download_file():
    try:
        # Fetch the file from GitHub
        response = requests.get(GITHUB_RAW_FILE_URL)
        response.raise_for_status()  # Raise an error for bad responses

        # Return the file content as a response
        return Response(
            response.content,
            mimetype='text/plain',
            headers={'Content-Disposition': 'attachment; filename=filename.txt'}
        )
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
