from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

if os.getenv('FLASK_ENV') == 'development':
    from dotenv import load_dotenv
    load_dotenv()
    
CHANNEL_ACCESS_TOKEN = os.environ.get('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET')  # 如果需要的话

@app.route("/") 
def home():
    return "Hello Flask"

@app.route("/sendmessage")
def send_message():
    return jsonify({
        "token_exists": CHANNEL_ACCESS_TOKEN is not None,
        "token_length": len(CHANNEL_ACCESS_TOKEN) if CHANNEL_ACCESS_TOKEN else 0,
        "flask_env": os.getenv('FLASK_ENV')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)