# File: src/training_script.py
import joblib
import os
import sys
from sklearn.ensemble import RandomForestClassifier

# Pastikan python bisa menemukan modul src
sys.path.append(os.getcwd())

from src.data_preparation import prepare_data

def train_model():
    print("--- MULAI PROSES TRAINING ---")
    
    # 1. Ambil data
    X_train, X_test, y_train, y_test = prepare_data()
    
    if X_train is None:
        print("GAGAL: Data kosong.")
        return None, None, None, None # Mengembalikan 4 nilai None jika gagal!

    # 2. Inisialisasi Model Random Forest
    print("Melatih Random Forest...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    # 3. Simpan
    os.makedirs('model', exist_ok=True)
    joblib.dump(rf_model, 'model/trained_random_forest.pkl')
    print("[OK] Model disimpan di model/trained_random_forest.pkl")
    print("--- TRAINING SELESAI ---")
    
    # 4. TAMBAHKAN RETURN VALUE AGAR model_evaluation.py BISA MENGGUNAKAN DATA TEST
    return rf_model, X_test, y_test # Mengembalikan model, data test, dan label test
                                     # (Catatan: X_train tidak diperlukan oleh evaluation)

if __name__ == '__main__':
    train_model()