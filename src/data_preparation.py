import pandas as pd
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import joblib

def prepare_data():
    input_path = 'data/raw/raw_sensor_data.csv'
    output_csv_path = 'data/processed/final_dataset.csv' # Path file output
    
    # 1. Cek apakah file raw ada
    if not os.path.exists(input_path):
        print(f"ERROR: File {input_path} tidak ditemukan. Jalankan setup_project.py dulu.")
        return None, None, None, None

    print(f"Loading data dari {input_path}...")
    data = pd.read_csv(input_path)
    
    # 2. Filter Kolom yang dipakai (Mengabaikan plant_id/leaf_id jika ada)
    # Kolom fitur (X) dan Target (y)
    X = data[['R', 'G', 'B', 'texture_lbp', 'priming_position', 'local_temp', 'local_humidity', 'tobacco_variety']]
    y = data['ripeness_class']

    # 3. Split Data (80% Training, 20% Testing)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Pipeline Preprocessing
    numerical_features = ['R', 'G', 'B', 'texture_lbp', 'priming_position', 'local_temp', 'local_humidity']
    categorical_features = ['tobacco_variety']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)]) 
            # sparse_output=False agar hasil bisa disimpan ke CSV dengan mudah

    print("Melakukan fitting dan transformasi data...")
    # Proses data menjadi angka murni (termasuk mengubah Virginia/Burley jadi 0/1)
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    
    # 5. [BARU] Simpan Final Dataset ke CSV (agar folder processed tidak kosong)
    # Kita simpan data training yang sudah diproses
    os.makedirs('data/processed', exist_ok=True)
    
    # Mengonversi array numpy ke DataFrame agar bisa disave ke CSV
    # Nama kolom tidak lagi R, G, B asli karena sudah di-encode, jadi kita pakai index saja
    df_processed = pd.DataFrame(X_train_processed)
    df_processed['target_class'] = y_train.values # Tempelkan label targetnya
    
    df_processed.to_csv(output_csv_path, index=False)
    print(f"[OK] Final dataset disimpan di: {output_csv_path}")

    # 6. Simpan pipeline
    os.makedirs('model', exist_ok=True)
    joblib.dump(preprocessor, 'model/feature_pipeline.pkl')
    print("[OK] Pipeline disimpan di model/feature_pipeline.pkl")
    
    return X_train_processed, X_test_processed, y_train, y_test

if __name__ == "__main__":
    prepare_data()