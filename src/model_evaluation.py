# Model evaluation
import joblib
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)).rsplit(os.sep, 1)[0])
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from src.training_script import train_model

def evaluate_model():
    """Mengukur kinerja prediktif model menggunakan metrik klasifikasi standar."""
    
    # Pastikan model dilatih/dimuat
    try:
        model = joblib.load('model/trained_random_forest.pkl')
        # Anggap data pengujian sudah tersedia dari proses training_script
        _, X_test, y_test = train_model() 
    except FileNotFoundError:
        print("Model belum dilatih. Menjalankan skrip pelatihan...")
        model, X_test, y_test = train_model()
    
    # Prediksi pada set pengujian
    y_pred = model.predict(X_test)
    
    # [cite_start]Menghitung metrik evaluasi [cite: 32]
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    conf_matrix = confusion_matrix(y_test, y_pred)
    
    print("\n--- Hasil Evaluasi Model Random Forest ---")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f}")
    print("\nConfusion Matrix:\n", conf_matrix)
    print("------------------------------------------")
    
    # [cite_start]Contoh analisis Feature Importance [cite: 43]
    feature_names = ['R', 'G', 'B', 'texture_lbp', 'priming_position', 'local_temp', 'local_humidity', 'tobacco_variety_Burley', 'tobacco_variety_Virginia']
    importances = model.feature_importances_
    sorted_idx = importances.argsort()[::-1]

    print("\nFeature Importance (Faktor Penentu Utama Kematangan):")
    for i in sorted_idx:
        if i < len(feature_names):
            print(f"- {feature_names[i]}: {importances[i]:.4f}")

if __name__ == '__main__':
    evaluate_model()