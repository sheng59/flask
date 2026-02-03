from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os
import json

app = Flask(__name__)
CORS(app)

if os.getenv('FLASK_ENV') == 'production':
    from dotenv import load_dotenv
    load_dotenv()
    
CHANNEL_ACCESS_TOKEN = os.environ.get('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET')  # 如果需要的话

@app.route("/") 
def home():
    return "Hello Flask"

@app.route("/sendmessage", methods=['POST'])
def send_message():
    try:
        order_data = request.json
        
        required_fields = ['userId', 'message']
        
        for field in required_fields:
            if field not in order_data:
                return jsonify({
                    "error": f"Missing required field: {field}",
                    "message": "Please provide all required order information"
                }), 400
                
        formatted_message = order_data['message']
        
        headers = {
            'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        body = {
            'to': order_data['userId'],
            'messages': [{
                'type': 'text',
                'text': formatted_message
            }]
        }
        
        response = requests.post(
            'https://api.line.me/v2/bot/message/push',
            #'https://api.line.me/v2/bot/message/broadcast',
            headers=headers,
            json=body
        )
        
        return jsonify({
            "status": "success",
            "message": "Message sent to LINE",
            "formatted_message": formatted_message
        }), response.status_code
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "發送失敗"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)