from flask import Flask, request, jsonify
from job import MetalPriceJob
import os

app = Flask(__name__)

# Додаємо маршрут для кореневого шляху
@app.route('/')
def index():
    return "Flask сервер працює, все готово!"

@app.route('/process', methods=['POST'])
def process_request():
    try:
        data = request.get_json()
        if not data or 'date' not in data or 'feature' not in data:
            return jsonify({"error": "Invalid request format"}), 400

        raw_dir = os.path.join(os.getcwd(), 'raw')
        job = MetalPriceJob(raw_dir=raw_dir)
        result = job.run(data['date'], data['feature'])
        
        return jsonify({"message": "Data processed", "files": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=8081, debug=True)