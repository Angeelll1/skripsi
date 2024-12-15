from flask import Flask, request, jsonify, send_file, url_for
from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path
import psycopg2
import os
import time
import json

# Inisialisasi Flask
app = Flask(__name__)

# Konfigurasi
db_config = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'admin'
}

IMAGE_FOLDER = 'static/images'
os.makedirs(IMAGE_FOLDER, exist_ok=True)


def save_to_database(subdist_id, chiller_id, path_image, send_date, detection):
    """Simpan informasi deteksi ke dalam database PostgreSQL."""
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        query = """
        INSERT INTO t_chiller_detection (subdist_id, chiller_id, path_image, send_date, detection)
        VALUES (%s, %s, %s, %s, %s)
        """
        detection_str = json.dumps(detection)
        cursor.execute(query, (subdist_id, chiller_id, path_image, send_date, detection_str))
        print('BERHASIL INSERT KE DB')

        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")


model_path = Path('C:/Users/PC/Documents/Angel/Kuliah/SKRIPSI/model_default_dataset12.pt')
model = YOLO(str(model_path))


@app.route('/predict', methods=['POST'])
def predict():
    # Ambil data dari form
    subdist_id = request.form.get('subdist_id')
    chiller_id = request.form.get('chiller_id')
    send_date = request.form.get('send_date')

    if not subdist_id or not chiller_id or not send_date:
        return jsonify({'error': 'Missing required form data'}), 400

    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Baca gambar
    np_img = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    # Panggil model YOLOv8
    results = model(img, conf=0.20, iou=0.4)
    detections = results[0].boxes
    label_count = {}

        # Hasil deteksi
    for detection in detections:
        x1, y1, x2, y2 = map(int, detection.xyxy[0])  # Bounding box
        conf = detection.conf.item()  # Confidence score
        class_idx = int(detection.cls[0])  # Index kelas
        original_label = model.names[class_idx]  # Nama kelas asli berdasarkan index

        # Modifikasi label dan warna berdasarkan confidence
        if conf < 0.6:
            label = "Produk Kompetitor"
            color = (0, 0, 255)  # Merah untuk produk kompetitor
        else:
            label = original_label
            color = (0, 255, 0)  # Hijau untuk kelas yang dikenali

        # Gambar bounding box dan label pada gambar
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img, f"{label} {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Hitung jumlah deteksi berdasarkan label
        if label not in label_count:
            label_count[label] = 0
        label_count[label] += 1


    # Simpan gambar di folder
    image_filename = f'{subdist_id}_{chiller_id}_{int(time.time())}.jpg'
    image_path = os.path.join(IMAGE_FOLDER, image_filename)
    cv2.imwrite(image_path, img)

    # Get URL
    image_url = url_for('static', filename=f'images/{image_filename}', _external=True)

    # Simpan ke database
    save_to_database(subdist_id, chiller_id, image_url, send_date, label_count)

    print('BERHASIL DETEKSI URL = %s' % image_url)

    # Kirim response
    return jsonify({
        'path': image_url,
        'detections': label_count
    }), 200


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_file(os.path.join('static', filename))


if __name__ == '__main__':
    # running
    app.run(host='10.10.61.114', port=5000, debug=True)
