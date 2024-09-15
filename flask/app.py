#run `pip install flask` to install flask
from flask import Flask

app = Flask(__name__)

@app.route('/processAI', methods=['POST'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)