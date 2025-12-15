# File: generate_full_data.py
import pandas as pd
import random
import os

def generate_tobacco_data(num_rows=2000):
    print(f"🔄 Sedang men-generate {num_rows} baris data sensor realistis...")
    
    rows = []
    varieties = ['Virginia', 'Burley', 'Oriental']
    plant_ids = [f"P{str(i).zfill(3)}" for i in range(1, 101)] # P001 - P100

    for i in range(num_rows):
        plant_id = random.choice(plant_ids)
        leaf_id = random.randint(1, 20)
        variety = random.choice(varieties)
        
        # --- Simulasi Variabel Lingkungan ---
        # Suhu optimal tembakau: 20-30 C
        local_temp = round(random.uniform(18.0, 38.0), 1) 
        # Kelembaban: 50-90%
        local_humidity = random.randint(50, 95)
        
        # --- Simulasi Fisik Daun ---
        priming_pos = random.randint(1, 10) # 1 (Bawah) - 10 (Atas)
        
        # Warna (RGB). Daun matang biasanya Kuning-Hijau (R tinggi, G tinggi), Mentah (G dominan)
        # Kita buat pola: Semakin tinggi priming, butuh waktu lebih lama.
        G = random.randint(100, 255)
        R = random.randint(50, 240)
        B = random.randint(0, 100)
        
        # Tekstur (LBP). Semakin matang, tekstur biasanya lebih halus/rata (nilai lebih rendah) atau spesifik
        texture = round(random.uniform(20.0, 80.0), 2)

        # --- LOGIKA PENENTUAN LABEL (RULE OF THUMB PETANI) ---
        # Logika ini mengajarkan AI pola panen yang "benar"
        is_optimal = 0
        
        # Kriteria 1: Posisi Priming Tengah (3-7) seringkali kualitas terbaik
        # Kriteria 2: Warna Matang (Kuning kehijauan -> R mendekati G)
        # Kriteria 3: Suhu & Kelembaban mendukung
        
        color_ratio = R / G if G > 0 else 0
        
        if (3 <= priming_pos <= 8):
            # Jika priming bagus, cek warna dan lingkungan
            if (0.8 <= color_ratio <= 1.1) and (24 <= local_temp <= 32):
                is_optimal = 1
        elif (priming_pos > 8):
            # Daun pucuk butuh warna sangat spesifik (sangat matang)
            if (color_ratio > 0.95) and (local_temp > 26):
                is_optimal = 1
        
        # Tambahkan noise sedikit (human error) agar model belajar robust
        if random.random() < 0.05: # 5% kemungkinan salah label
            is_optimal = 1 - is_optimal

        rows.append([plant_id, leaf_id, R, G, B, texture, priming_pos, local_temp, local_humidity, variety, is_optimal])

    # Buat DataFrame
    columns = ['plant_id', 'leaf_id', 'R', 'G', 'B', 'texture_lbp', 'priming_position', 'local_temp', 'local_humidity', 'tobacco_variety', 'ripeness_class']
    df = pd.DataFrame(rows, columns=columns)
    
    # Simpan
    os.makedirs('data/raw', exist_ok=True)
    output_path = 'data/raw/raw_sensor_data.csv'
    df.to_csv(output_path, index=False)
    print(f"✅ SUKSES! Data disimpan di: {output_path}")
    print("   Sekarang jalankan: python src/training_script.py")

if __name__ == "__main__":
    generate_tobacco_data()