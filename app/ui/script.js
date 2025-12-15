// File: app/ui/script.js (Final & Clean for 3 Pages)

// --- 1. FITUR WARNA REAL-TIME & KLASIFIKASI ---
function determineColorName(r, g, b) {
    if (r < 50 && g < 50 && b < 50) return "Gelap / Hitam";
    if (g > r + 40) return "Hijau Pekat (Mentah)";
    if (r > 200 && g > 200 && Math.abs(r - g) < 30) return "Kuning Emas (Optimal)";
    if (r > 160 && g > 160 && Math.abs(r - g) < 30) return "Kuning Pucat / Krem";
    if (r > g + 20) return "Cokelat / Kering";
    if (g >= r) return "Hijau Kekuningan (Mengkal)";
    return "Warna Tidak Terdefinisi";
}

function updateColorPreview() {
    const rInput = document.querySelector('input[name="R"]');
    if (!rInput) return;
    
    const r = parseInt(rInput.value) || 0;
    const g = parseInt(document.querySelector('input[name="G"]').value) || 0;
    const b = parseInt(document.querySelector('input[name="B"]').value) || 0;
    
    const colorBox = document.getElementById('colorPreview');
    const colorText = document.getElementById('colorText');
    
    if (colorBox) colorBox.style.backgroundColor = `rgb(${r}, ${g}, ${b})`;

    if (colorText) {
        const colorName = determineColorName(r, g, b);
        colorText.innerHTML = `<strong>${colorName}</strong> <small style="opacity:0.6;">(R${r} G${g} B${b})</small>`;
        
        if(colorName.includes("Mentah")) colorText.style.color = "#d32f2f"; 
        else if(colorName.includes("Optimal")) colorText.style.color = "#2e7d32";
        else colorText.style.color = "#555";
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.rgb-group input').forEach(input => {
        input.addEventListener('input', updateColorPreview);
    });
    updateColorPreview();
});


// --- 2. ANALISIS KE API (Port 8080) - Hanya di index.html ---
document.addEventListener('DOMContentLoaded', () => {
    const harvestForm = document.getElementById('harvestForm');
    if (harvestForm) {
        harvestForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = document.querySelector('.btn-analyze');
            const originalText = btn.innerHTML;
            
            btn.innerHTML = '<span class="icon">⏳</span> Memproses AI...';
            btn.disabled = true;

            document.querySelector('.result-placeholder').classList.remove('hidden');
            document.querySelector('.result-content').classList.add('hidden');
            document.getElementById('resultCard').className = 'card result-card';

            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData.entries());
            for (let key in data) { if(key !== 'tobacco_variety') data[key] = parseFloat(data[key]); }

            try {
                const res = await fetch('http://localhost:8080/predict', { 
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });

                if (!res.ok) {
                    const errorBody = await res.json().catch(() => ({'error': 'Gagal koneksi API'}));
                    throw new Error(errorBody.error || `Error HTTP: ${res.status}`);
                }

                const result = await res.json();
                
                setTimeout(() => {
                    document.querySelector('.result-placeholder').classList.add('hidden');
                    document.querySelector('.result-content').classList.remove('hidden');
                    
                    document.getElementById('statusBadge').innerText = result.status_panen;
                    document.getElementById('mainInstruction').innerText = result.instruction;
                    document.getElementById('confidenceVal').innerText = result.confidence_score;
                    document.getElementById('primingVal').innerText = "Priming " + result.priming_position;

                    const card = document.getElementById('resultCard');
                    card.classList.remove('is-optimal', 'is-suboptimal');
                    if(result.status_panen.includes("Optimal") && !result.status_panen.includes("Sub")) {
                        card.classList.add('is-optimal');
                    } else {
                        card.classList.add('is-suboptimal');
                    }

                    updateColorPreview();
                }, 600);

            } catch(err) {
                alert("Gagal koneksi API atau Server Error. Pastikan Flask berjalan di http://localhost:8080. Detail: " + err.message);
            } finally {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }
        });
    }
});


// --- 3. CONFIG LOGIC (Untuk config.html) ---

window.loadConfig = async function() {
    const formElement = document.getElementById('configForm');
    if (!formElement) return;

    const inputs = formElement.querySelectorAll('input, select');
    inputs.forEach(input => input.disabled = true);
    
    try {
        const res = await fetch('http://localhost:8080/config'); 
        
        if (!res.ok) {
            const errorBody = await res.json().catch(() => ({'error': 'Gagal memuat konfigurasi'}));
            throw new Error(errorBody.error || `Error HTTP: ${res.status}`);
        }
        
        const config = await res.json();
        
        // Isi nilai-nilai form (semua field baru)
        document.getElementById('strict_mode').value = config.strict_mode.toString();
        document.getElementById('min_temp_virginia').value = config.min_temp_virginia;
        document.getElementById('min_temp_burley').value = config.min_temp_burley;
        document.getElementById('min_temp_oriental').value = config.min_temp_oriental; // BARU
        document.getElementById('max_humidity').value = config.max_humidity; 
        document.getElementById('optimal_R_min').value = config.optimal_R_min;       // BARU
        document.getElementById('optimal_G_min').value = config.optimal_G_min;       // BARU
        document.getElementById('optimal_B_max').value = config.optimal_B_max;       // BARU
        document.getElementById('rgb_ratio_tolerance').value = config.rgb_ratio_tolerance; // BARU
        document.getElementById('texture_optimal_min').value = config.texture_optimal_min; // BARU
        document.getElementById('texture_optimal_max').value = config.texture_optimal_max; // BARU

        
    } catch(e) { 
         alert(`❌ Gagal memuat data konfigurasi: ${e.message}. Cek koneksi API dan Database.`);
    } finally {
         inputs.forEach(input => input.disabled = false);
    }
}

async function handleConfigSubmit(e) {
    e.preventDefault();
    const btn = document.querySelector('#configForm .btn-analyze');
    const originalText = btn.innerHTML;
    btn.innerHTML = 'Menyimpan...';
    btn.disabled = true;

    const configData = {
        strict_mode: document.getElementById('strict_mode').value === 'true',
        min_temp_virginia: parseFloat(document.getElementById('min_temp_virginia').value),
        min_temp_burley: parseFloat(document.getElementById('min_temp_burley').value),
        min_temp_oriental: parseFloat(document.getElementById('min_temp_oriental').value), // BARU
        max_humidity: parseFloat(document.getElementById('max_humidity').value), 
        optimal_R_min: parseFloat(document.getElementById('optimal_R_min').value),       // BARU
        optimal_G_min: parseFloat(document.getElementById('optimal_G_min').value),       // BARU
        optimal_B_max: parseFloat(document.getElementById('optimal_B_max').value),       // BARU
        rgb_ratio_tolerance: parseFloat(document.getElementById('rgb_ratio_tolerance').value), // BARU
        texture_optimal_min: parseFloat(document.getElementById('texture_optimal_min').value), // BARU
        texture_optimal_max: parseFloat(document.getElementById('texture_optimal_max').value), // BARU
    };
    
    try {
        const res = await fetch('http://localhost:8080/config', { 
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(configData)
        });

        if (!res.ok) {
            const errorBody = await res.json().catch(() => ({'error': 'Server merespons non-OK'}));
            throw new Error(errorBody.error || `Error HTTP: ${res.status}`);
        }
        
        alert("✅ Konfigurasi Tersimpan!");

    } catch (e) {
        alert("Gagal menyimpan konfigurasi. Periksa koneksi API dan Database. Detail: " + e.message);
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
        window.loadConfig(); 
    }
}

async function handleConfigSubmit(e) {
    e.preventDefault();
    const btn = document.querySelector('#configForm .btn-analyze');
    const originalText = btn.innerHTML;
    btn.innerHTML = 'Menyimpan...';
    btn.disabled = true;

    const configData = {
        strict_mode: document.getElementById('strict_mode').value === 'true',
        min_temp_virginia: parseFloat(document.getElementById('min_temp_virginia').value),
        min_temp_burley: parseFloat(document.getElementById('min_temp_burley').value),
        max_humidity: parseFloat(document.getElementById('max_humidity').value), 
        texture_tolerance: parseFloat(document.getElementById('texture_tolerance').value), 
    };
    
    try {
        const res = await fetch('http://localhost:8080/config', { 
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(configData)
        });

        if (!res.ok) {
            const errorBody = await res.json().catch(() => ({'error': 'Server merespons non-OK'}));
            throw new Error(errorBody.error || `Error HTTP: ${res.status}`);
        }
        
        alert("✅ Konfigurasi Tersimpan!");

    } catch (e) {
        alert("Gagal menyimpan konfigurasi. Periksa koneksi API dan Database. Detail: " + e.message);
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
        window.loadConfig(); 
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const configForm = document.getElementById('configForm');
    if (configForm) {
        configForm.addEventListener('submit', handleConfigSubmit);
    }
});


// --- 4. HISTORY LOGIC (Untuk history.html) ---

window.loadHistory = async function() {
    const tbody = document.getElementById('historyTableBody');
    if (!tbody) return;
    
    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding: 20px;">⏳ Sedang memuat data riwayat...</td></tr>`;
    
    try {
        const res = await fetch('http://localhost:8080/history'); 
        
        if (!res.ok) {
             const errorBody = await res.json().catch(() => ({'error': 'Gagal memuat riwayat'}));
             throw new Error(errorBody.error || `Error HTTP: ${res.status}`);
        }

        const data = await res.json();
        tbody.innerHTML = '';
        
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding: 20px;">Database kosong. Lakukan Analisis pertama Anda.</td></tr>';
            return;
        }

        data.forEach(row => {
            const r = parseInt(row.rgb_r);
            const g = parseInt(row.rgb_g);
            const b = parseInt(row.rgb_b);
            
            const tr = document.createElement('tr');
            const statusClass = row.status.includes('Optimal') && !row.status.includes('Sub') ? 'status-optimal' : 'status-sub';
            const colorName = determineColorName(r, g, b);
            
            tr.innerHTML = `
                <td>${row.timestamp.split(' ')[1]}</td>
                <td>${row.variety}</td>
                <td>P-${row.priming}</td>
                <td>
                    <div style="display:flex; align-items:center; gap:5px;">
                        <span style="width:12px;height:12px;background:rgb(${r},${g},${b});border-radius:50%;border:1px solid #ccc;"></span>
                        <small>${colorName}</small>
                    </div>
                </td>
                <td><span class="${statusClass}">${row.status.split(' ')[0]}</span></td>
                <td>${row.instruction}</td>
            `;
            tbody.appendChild(tr);
        });

    } catch(e) { 
        tbody.innerHTML = `<tr><td colspan="6" style="color:red; text-align:center; padding: 20px;">❌ Gagal memuat riwayat: ${e.message}. Cek koneksi API/Database.</td></tr>`;
    }
}