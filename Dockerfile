# File: Dockerfile

# Menggunakan image base Python yang ringan (slim)
FROM python:3.13-slim

# Menetapkan direktori kerja di dalam container
WORKDIR /app

# Menyalin file requirements.txt dan menginstal dependensi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin sisa kode proyek ke direktori kerja
# Ini termasuk app/, model/, data/, Procfile, dll.
COPY . .

# Menggunakan Procfile untuk menentukan perintah awal
# CMD akan menjalankan Gunicorn (Procfile: web: gunicorn app.api.prediction_service:app)
CMD ["gunicorn", "app.api.prediction_service:app", "-b", "0.0.0.0:8080"]

# Ekspos port 8080 (port yang digunakan Flask/Gunicorn)
EXPOSE 8080