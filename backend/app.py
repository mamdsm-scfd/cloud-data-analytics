from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import numpy as np
from scipy import stats
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins="*")

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)


@app.route('/upload', methods=['POST'])
def upload_file():
    # تحقق من وجود ملف
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Only CSV files are allowed'}), 400

    # احفظ الملف مؤقتًا
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # اقرأ الملف باستخدام pandas
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        return jsonify({'error': f'Error reading file: {str(e)}'}), 500

    # تأكد أن فيه أعمدة رقمية
    numeric_columns = df.select_dtypes(include=np.number).columns.tolist()
    if not numeric_columns:
        return jsonify({'error': 'No numeric columns found in the CSV'}), 400

    # تحليل البيانات
    analysis = {}
    for col in numeric_columns:
        mean = df[col].mean()
        median = df[col].median()
        mode = df[col].mode().iloc[0] if not df[col].mode().empty else 'N/A'

        analysis[col] = {
            'mean': float(round(mean, 2)),
            'median': float(round(median, 2)),
            'mode': float(mode) if isinstance(mode, (np.integer, np.floating)) else mode
        }

    return jsonify({'analysis': analysis})


if __name__ == '__main__':
    app.run(debug=True)


