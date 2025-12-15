# File: app/api/prediction_service.py
import joblib
import pandas as pd
import os
from flask import Flask, request, jsonify
from flask_cors import CORS 

# --- FIREBASE SETUP ---
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# --- KONFIGURASI ANDA YANG TERSIMPAN DALAM KODE ---
CREDENTIALS_FILENAME = 'smart-harvest-service-key.json' 
DB_URL = 'https://sistemcerdas-arc-default-rtdb.asia-southeast1.firebasedatabase.app/' 

CRED_PATH = os.path.join(os.path.dirname(__file__), CREDENTIALS_FILENAME)

DB_REF = None 

# Inisialisasi Firebase
try:
    if not firebase_admin._apps:
        if not os.path.exists(CRED_PATH):
             # Ganti ke FileNotFoundError agar error lebih spesifik
             raise FileNotFoundError(f"File kredensial tidak ditemukan di: {CRED_PATH}")
             
        cred = credentials.Certificate(CRED_PATH)
        firebase_admin.initialize_app(cred, {
            'databaseURL': DB_URL
        })
    DB_REF = db.reference('/')
    print("[OK] Firebase Connected.")
except Exception as e:
    print(f"ERROR Firebase Connection: {e}")
    print("WARNING: Fitur Konfigurasi dan Riwayat TIDAK akan berfungsi.")
    DB_REF = None 

# --- END FIREBASE SETUP ---

app = Flask(__name__)
CORS(app) 

# Load Model Sekali Saja saat Start
try:
    print("Loading model...")
    MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'model', 'trained_random_forest.pkl')
    PIPELINE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'model', 'feature_pipeline.pkl')

    MODEL = joblib.load(MODEL_PATH)
    PIPELINE = joblib.load(PIPELINE_PATH)
    print("[OK] Model Loaded.")
except Exception as e:
    print(f"ERROR Loading Model: {e}")
    MODEL = None
    PIPELINE = None


# --- KONFIGURASI ENDPOINTS (/config) ---

DEFAULT_CONFIG = {
    'strict_mode': False,
    # Suhu Minimum untuk 3 Varietas
    'min_temp_virginia': 25.0,
    'min_temp_burley': 23.0,
    'min_temp_oriental': 21.0,  # BARU: Oriental

    # Batas Lingkungan
    'max_humidity': 90,
    
    # Batas Warna (RGB) untuk Optimal
    'optimal_R_min': 180,       # BARU
    'optimal_G_min': 180,       # BARU
    'optimal_B_max': 120,       # BARU
    'rgb_ratio_tolerance': 0.15, # BARU: Toleransi R/G ratio dari 1.0 (e.g., 1.0 +/- 0.15)
    
    # Batas Tekstur
    'texture_optimal_min': 40.0, # BARU
    'texture_optimal_max': 60.0  # BARU
}

@app.route('/config', methods=['GET', 'POST'])
def handle_config():
    if DB_REF is None:
        return jsonify({'error': 'Koneksi database Firebase gagal'}), 503 

    config_ref = DB_REF.child('config')
    
    if request.method == 'GET':
        config = config_ref.get()
        if config is None:
            config_ref.set(DEFAULT_CONFIG)
            config = DEFAULT_CONFIG
        
        # Mengembalikan konfigurasi dengan default jika ada kunci yang hilang
        response_config = {**DEFAULT_CONFIG, **(config if config else {})}
        return jsonify(response_config)

    elif request.method == 'POST':
        data = request.json
        # Perbarui required_keys untuk mencakup semua field baru
        required_keys = [
            'strict_mode', 'min_temp_virginia', 'min_temp_burley', 'min_temp_oriental', 
            'max_humidity', 'optimal_R_min', 'optimal_G_min', 'optimal_B_max', 
            'rgb_ratio_tolerance', 'texture_optimal_min', 'texture_optimal_max'
        ]
        
        if not all(k in data for k in required_keys):
             return jsonify({'error': 'Data konfigurasi tidak lengkap'}), 400
             
        config_ref.update(data)
        return jsonify({'message': 'Konfigurasi berhasil disimpan'}), 200

# --- PREDICT ENDPOINT DENGAN LOGGING (/predict) ---

@app.route('/predict', methods=['POST'])
def predict():
    if not MODEL: 
        return jsonify({'error': 'Model belum dilatih atau gagal dimuat'}), 500

    try:
        data = request.json
        
        df = pd.DataFrame([data])
        processed_data = PIPELINE.transform(df)
        
        # Prediksi
        prediction = MODEL.predict(processed_data)[0]
        proba = MODEL.predict_proba(processed_data)[0].max() * 100
        
        result_status = "Siap Optimal" if prediction == 1 else "Sub-Optimal"
        instruction_text = "LAKUKAN PEMETIKAN" if prediction == 1 else "JANGAN PETIK"
        
        response = {
            'status_panen': result_status,
            'confidence_score': f"{proba:.2f}%",
            'priming_position': data['priming_position'],
            'instruction': instruction_text
        }

        # --- LOGGING KE HISTORY (Hanya jika DB_REF ada) ---
        if DB_REF: 
            history_ref = DB_REF.child('history')
            new_entry = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'variety': data['tobacco_variety'],
                'priming': data['priming_position'],
                'rgb_r': data['R'],
                'rgb_g': data['G'],
                'rgb_b': data['B'],
                'temp': data['local_temp'],
                'humidity': data['local_humidity'],
                'status': result_status,
                'instruction': instruction_text,
                'confidence': f"{proba:.2f}%"
            }
            history_ref.push(new_entry) 
        # --- END LOGGING ---
        
        return jsonify(response)

    except Exception as e:
        print(f"Error prediksi: {e}")
        return jsonify({'error': f"Processing Error: {str(e)}"}), 400


# --- HISTORY ENDPOINT (/history) ---

@app.route('/history', methods=['GET'])
def get_history():
    if DB_REF is None:
        return jsonify({'error': 'Koneksi database Firebase gagal'}), 503 # Mengembalikan 503

    try:
        history_ref = DB_REF.child('history')
        data = history_ref.order_by_key().limit_to_last(50).get()
        
        history_list = []
        if data:
            for key, entry in data.items():
                history_list.append(entry)
        
        history_list.reverse() 
        
        return jsonify(history_list)

    except Exception as e:
        print(f"Error memuat riwayat: {e}")
        return jsonify({'error': 'Gagal memuat data riwayat dari database'}), 500


if __name__ == '__main__':
    print("Server berjalan di http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=False)