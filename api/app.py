from flask import Flask, request, jsonify
import requests
import os
import logging
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# 从环境变量获取配置
LINE_TOKEN = os.getenv('LINE_BOT_TOKEN')
LINE_API_URL = 'https://api.line.me/v2/bot/message/push'

@app.route("/") 
def home():
    return "Hello Flask"

@app.route("/sendmessage", methods=['POST'])
def send_message():
    try:
        # 验证请求方法
        if request.method != 'POST':
            return jsonify({'error': 'Method not allowed'}), 405
        
        # 获取请求数据
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # 验证必要字段
        required_fields = ['to', 'messages']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # 构建请求头
        headers = {
            'Authorization': f'Bearer {LINE_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # 发送请求
        response = requests.post(
            LINE_API_URL,
            headers=headers,
            json=data  # 直接使用 json 参数，自动处理编码
        )
        
        # 记录日志
        logger.info(f"Sent message to {data.get('to')}, Status: {response.status_code}")
        
        # 返回响应
        if response.status_code == 200:
            return jsonify({
                'success': True,
                'message': 'Message sent successfully'
            }), 200
        else:
            logger.error(f"Failed to send message: {response.text}")
            return jsonify({
                'success': False,
                'error': response.text,
                'status_code': response.status_code
            }), response.status_code
            
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
