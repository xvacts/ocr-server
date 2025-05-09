from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import pytesseract
import requests
from io import BytesIO

app = Flask(__name__)
CORS(app)  # 允许跨域

@app.route('/ocr', methods=['POST'])
def ocr_from_url():
    data = request.get_json()
    image_url = data.get('url')
    lang = data.get('lang', 'eng')  # 默认语言英文

    if not image_url:
        return jsonify({'error': 'Missing image URL'}), 400

    try:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        text = pytesseract.image_to_string(image, lang=lang)
        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return 'OCR Multilang Service is running!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
