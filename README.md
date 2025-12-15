# 🍂 SmartHarvestSystem

**Sistem Cerdas Prediktif untuk Manajemen Panen Tembakau Presisi Tinggi**

Sistem ini menggunakan *Machine Learning* (Algoritma Random Forest) untuk mengklasifikasikan status panen daun tembakau secara individual. Sistem mengintegrasikan data visual (Warna RGB, Tekstur LBP) dan data lingkungan (Suhu, Kelembaban) untuk memberikan rekomendasi presisi: **'Siap Optimal'** atau **'Sub-Optimal'**.

---

## 💡 Konsep Teknologi Inti

Sistem SmartHarvest didukung oleh Machine Learning (ML), yang memungkinkannya belajar dari data historis daun untuk mengambil keputusan prediktif.

### 🤖 Machine Learning

Machine Learning (ML) adalah cabang dari kecerdasan buatan (AI) yang memungkinkan sistem komputer untuk **belajar dari data** tanpa diprogram secara eksplisit. Prosesnya meliputi:

1.  **Pelatihan (Training):** Algoritma menganalisis data Input (RGB, Suhu, dll.) dan Output yang sudah diketahui (*Label* "Optimal"), membangun hubungan pola.
2.  **Prediksi:** Model yang telah dilatih kemudian digunakan untuk memproses data sensor baru dan membuat prediksi status panen.

### 🌳 Algoritma Random Forest

Random Forest adalah algoritma ML yang populer dan kuat untuk tugas klasifikasi. Cara kerjanya adalah dengan membangun banyak pohon keputusan secara acak, dan keputusan akhirnya diambil berdasarkan *voting* mayoritas dari semua pohon yang ada di dalam hutan.

---

## 🚀 Cara Menjalankan (Quick Start)

Ikuti langkah ini secara berurutan agar sistem berjalan tanpa error:

1.  **Persiapan Folder & Data** (Wajib dijalankan pertama kali)
    ```bash
    python setup_project.py
    python generate_full_data.py
    ```
    *(Script ini akan membuat struktur folder dan men-generate 2.000 data latih realistis)*

2.  **Training Model AI**
    ```bash
    python src/training_script.py
    ```
    *(Melatih otak AI 'Random Forest' dan menyimpannya ke folder `model/`)*

3.  **Jalankan Backend API**
    ```bash
    python app/api/prediction_service.py
    ```
    *(Biarkan terminal ini tetap terbuka)*

4.  **Buka Dashboard**
    Buka file `app/ui/index.html` menggunakan browser Anda (Chrome/Edge).

---

## 📖 Panduan Simulasi & Logika Panen

Gunakan panduan ini untuk menguji Dashboard. Masukkan angka-angka berikut untuk mensimulasikan berbagai kondisi daun dan melihat respon AI.

### 1. Varietas VIRGINIA (Tembakau Oven / Flue-Cured)

**Karakteristik:** Kualitas premium dinilai dari kadar gula tinggi. Daun matang harus berwarna **Kuning Emas Cerah** atau Oranye. AI sangat ketat pada warna dan posisi daun.

#### ✅ KONDISI: SIAP OPTIMAL (PETIK)

*Masukkan kombinasi angka ini untuk hasil Hijau:*

* **Posisi Priming:** `4` s.d. `8` (Daun Tengah - Atas).
* **Warna (RGB):** Harus Tinggi & Cerah (Kuning Emas).
    * **R:** `220` - `240`
    * **G:** `225` - `245` (Seimbang dengan R)
    * **B:** `40` - `80` (Rendah)
* **Tekstur (LBP):** `45.0` - `55.0` (Tegas/Matang).
* **Suhu:** `26°C` - `30°C` (Hangat).

#### ❌ KONDISI: SUB-OPTIMAL (JANGAN PETIK)

* **Kasus 1: Masih Mentah (Hijau)**
    * *Input:* Priming `5`, R=`80`, G=`220`.
    * *Analisis AI:* "Klorofil terlalu tinggi, gula belum naik."
* **Kasus 2: Posisi Buruk (Daun Pasir)**
    * *Input:* Priming `1` atau `2`.
    * *Analisis AI:* "Posisi terlalu bawah, daun kotor/rusak, nilai jual rendah."

---

### 2. Varietas BURLEY (Tembakau Angin / Air-Cured)

**Karakteristik:** Rendah gula, tinggi nikotin. Warna matang Burley **tidak secerah Virginia**. Matangnya cenderung **Krem, Putih Kekuningan, atau Hijau Pucat**. Teksturnya lebih kasar/tebal.

#### ✅ KONDISI: SIAP OPTIMAL (PETIK)

*Masukkan kombinasi angka ini untuk hasil Hijau:*

* **Posisi Priming:** `3` s.d. `7` (Daun Tengah).
* **Warna (RGB):** Lebih Pucat/Pudar dibanding Virginia.
    * **R:** `170` - `200` (Lebih rendah dari Virginia)
    * **G:** `180` - `210`
    * **B:** `80` - `120` (Unsur putih/pucat lebih tinggi)
* **Tekstur (LBP):** `50.0` - `60.0` (Lebih kasar dari Virginia).
* **Suhu:** `24°C` - `29°C`.

#### ❌ KONDISI: SUB-OPTIMAL (JANGAN PETIK)

* **Kasus 1: Lewat Matang (Gosong/Kering)**
    * *Input:* Priming `6`, R=`180`, G=`100`, B=`50`.
    * *Analisis AI:* "Daun sudah mengering di batang (Senescence)."
* **Kasus 2: Pucuk Muda (Over-Fertilized)**
    * *Input:* Priming `9` atau `10`. Warna Hijau Gelap (R=`100`, G=`200`), Tekstur Halus (`35.0`).
    * *Analisis AI:* "Daun pucuk belum waktunya, nikotin belum maksimal."

---

### 3. Varietas ORIENTAL (Tembakau Jemur / Sun-Cured)

**Karakteristik:** Daun berukuran kecil, sangat aromatik. Sering dipetik saat warnanya **Hijau Kekuningan** (belum kuning total seperti Virginia). Sangat sensitif terhadap matahari (suhu).

#### ✅ KONDISI: SIAP OPTIMAL (PETIK)

*Masukkan kombinasi angka ini untuk hasil Hijau:*

* **Posisi Priming:** `4` s.d. `9` (Daun Tengah sampai agak Atas).
* **Warna (RGB):** Toleransi hijau sedikit lebih tinggi.
    * **R:** `190` - `210`
    * **G:** `210` - `230` (Sedikit lebih tinggi dari R)
    * **B:** `50` - `90`
* **Tekstur (LBP):** `40.0` - `50.0` (Daun kecil cenderung halus tapi lengket).
* **Suhu:** `28°C` - `34°C` (Butuh panas matahari langsung).

#### ❌ KONDISI: SUB-OPTIMAL (JANGAN PETIK)

* **Kasus 1: Kurang Sinar Matahari (Dingin)**
    * *Input:* Priming `5`, Warna OKE (R=`200`, G=`210`), tapi Suhu `20°C`.
    * *Analisis AI:* "Mikroklimat tidak mendukung fermentasi aromatik."
* **Kasus 2: Daun Bawah (Tanah)**
    * *Input:* Priming `1`, Warna Pucat (R=`150`, G=`160`).
    * *Analisis AI:* "Daun Oriental bawah tidak memiliki aroma (hambar)."

---

## 🔑 Rangkuman Perbedaan Utama

Agar simulasi terlihat canggih, perhatikan perbedaan kunci ini saat input data di Dashboard:

1.  **Warna Matang (RGB):**
    * **Virginia:** Input R & G tinggi (> 220) → *Kuning Silau*.
    * **Burley:** Input R & G sedang (180-200) → *Kuning Pucat*.
    * **Oriental:** Input G sedikit lebih tinggi dari R → *Hijau-Kuning*.

2.  **Sensitivitas Posisi (Priming):**
    Semua varietas akan menolak **Priming 1 & 2** (Sub-Optimal) kecuali kondisinya sangat sempurna, karena AI belajar bahwa daun bawah adalah kualitas terendah.

3.  **Sensitivitas Tekstur (LBP):**
    Jika memasukkan LBP di bawah **30.0** (Sangat Halus), AI akan mendeteksi sebagai **Daun Mentah/Muda** untuk semua jenis varietas.

---

**Teknologi:** Python 3, Flask, Scikit-Learn (Random Forest), Pandas