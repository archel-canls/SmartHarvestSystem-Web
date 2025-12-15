import os
import pandas as pd
import random

def create_structure():
    """Memastikan semua folder proyek tersedia."""
    folders = [
        'app/ui', 'app/api', 
        'data/raw', 'data/processed', 
        'model', 'src'
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"[OK] Folder dipastikan ada: {folder}")

def generate_tobacco_data(num_rows=2000):
    """Menghasilkan dataset sensor tembakau yang realistis."""
    print(f"🔄 Sedang men-generate {num_rows} baris data sensor realistis...")
    
    rows = []
    # Menggunakan 3 varietas agar lebih lengkap
    varieties = ['Virginia', 'Burley', 'Oriental'] 
    plant_ids = [f"P{str(i).zfill(3)}" for i in range(1, 101)] # P001 - P100

    for i in range(num_rows):
        plant_id = random.choice(plant_ids)
        leaf_id = random.randint(1, 20)
        variety = random.choice(varieties)
        
        # --- Simulasi Variabel Lingkungan ---
        local_temp = round(random.uniform(18.0, 38.0), 1) 
        local_humidity = random.randint(50, 95)
        
        # --- Simulasi Fisik Daun ---
        priming_pos = random.randint(1, 10) # 1 (Bawah) - 10 (Atas)
        
        # Warna (RGB)
        G = random.randint(100, 255)
        R = random.randint(50, 240)
        B = random.randint(0, 100)
        
        # Tekstur (LBP)
        texture = round(random.uniform(20.0, 80.0), 2)

        # --- LOGIKA PENENTUAN LABEL (RULE OF THUMB) ---
        is_optimal = 0
        color_ratio = R / G if G > 0 else 0
        
        # Logika panen berdasarkan posisi priming
        if (3 <= priming_pos <= 8):
            # Priming tengah butuh rasio warna seimbang dan suhu hangat
            if (0.8 <= color_ratio <= 1.1) and (24 <= local_temp <= 32):
                is_optimal = 1
        elif (priming_pos > 8):
            # Daun pucuk butuh warna sangat matang
            if (color_ratio > 0.95) and (local_temp > 26):
                is_optimal = 1
        
        # Tambahkan sedikit noise (human error 5%)
        if random.random() < 0.05:
            is_optimal = 1 - is_optimal

        rows.append([plant_id, leaf_id, R, G, B, texture, priming_pos, local_temp, local_humidity, variety, is_optimal])

    # Buat DataFrame
    columns = ['plant_id', 'leaf_id', 'R', 'G', 'B', 'texture_lbp', 'priming_position', 'local_temp', 'local_humidity', 'tobacco_variety', 'ripeness_class']
    df = pd.DataFrame(rows, columns=columns)
    
    # Simpan ke folder yang sudah dibuat oleh fungsi create_structure
    output_path = 'data/raw/raw_sensor_data.csv'
    df.to_csv(output_path, index=False)
    print(f"✅ SUKSES! {num_rows} data disimpan di: {output_path}")

if __name__ == "__main__":
    # 1. Buat Folder dulu
    create_structure()
    # 2. Langsung isi datanya
    generate_tobacco_data()
    print("\nSETUP SELESAI. Silakan lanjut ke: python src/training_script.py")