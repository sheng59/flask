from flask import Flask, jsonify, request
import requests
import os
import json

app = Flask(__name__)

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
        
        if not order_data:
            return jsonify({"error": "No data provided"}), 400
        
        headers = {
            'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        body = {
            'to': order_data.get('userId'),  # 从 POST 数据获取 userId
            'messages': [{
                'type': 'text',
                'text': f"訂單資訊：\n{json.dumps(order_data, ensure_ascii=False, indent=2)}"
            }]
        }
        
        response = requests.post(
            'https://api.line.me/v2/bot/message/push',
            headers=headers,
            data=json.dumps(body).encode('utf-8')
        )
        
        return jsonify({
            "status": "success",
            "line_response": response.json(),
            "order_data": order_data
        }), response.status_code
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "發送失敗"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)