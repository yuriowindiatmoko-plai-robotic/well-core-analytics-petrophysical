# Hari 3 — Sesi 6: Presentasi & Post-test

> **Waktu:** 15.30 – 16.30 (60 menit)
> **Fokus:** Peserta mempresentasikan hasil mini project, evaluasi, diskusi lanjutan
> **Catatan fasilitator:** Sesi penutup. Sebagian besar **fasilitasi**, bukan materi baru. Bahan di bawah: panduan presentasi, rubrik penilaian, post-test + kunci jawaban, prompt diskusi, dan langkah lanjutan.

---

## 🎯 Tujuan Sesi

1. Tiap peserta/kelompok **mendemokan** mini project Streamlit-nya.
2. Peserta **menjelaskan interpretasi** hasil (bukan cuma "appnya jalan").
3. Mengukur pemahaman lewat **post-test** singkat.
4. Menutup dengan **diskusi & arah belajar selanjutnya**.

---

## ⏱️ Pembagian Waktu (saran)

| Menit | Aktivitas |
|---|---|
| 15.30 – 16.00 (30') | Presentasi peserta (~3–4 menit per orang/kelompok) |
| 16.00 – 16.15 (15') | Post-test |
| 16.15 – 16.30 (15') | Pembahasan post-test + diskusi + penutup |

> Kalau peserta banyak, batasi 2–3 menit per presentasi dan pilih beberapa untuk demo penuh.

---

## 1. Panduan Presentasi (bagikan ke peserta)

Tiap presentasi (3–4 menit) sebaiknya menjawab 5 hal:

1. **Problem** — apa yang app-mu selesaikan? (1 kalimat)
2. **Data** — dataset apa, kolom/kurva apa yang dipakai?
3. **Pipeline** — alur app: upload → preprocess → clustering → output. Highlight 1 keputusan teknis (mis. kenapa pilih K tertentu, kenapa pakai scaling).
4. **Demo** — tunjukkan app jalan: upload → hasil crossplot.
5. **Interpretasi** — **bagian terpenting:** "Cluster ini kemungkinan litologi apa, dan kenapa?" Hubungkan ke crossplot Sesi 2.

> **Pesan ke peserta:** Nilai tertinggi bukan untuk app paling rapi, tapi untuk yang bisa **menjelaskan makna** hasilnya. Tools tanpa interpretasi = setengah jadi.

---

## 2. Rubrik Penilaian

Skala 1–5 tiap kriteria (5 = sangat baik).

| Kriteria | Bobot | Yang dinilai |
|---|---|---|
| **Fungsionalitas** | 25% | App jalan: upload → proses → output tanpa crash |
| **Kualitas kode/pipeline** | 20% | Fungsi terpisah, ada validasi, tidak "notebook ditempel" |
| **Visualisasi** | 20% | Plot benar (sumbu, colormap, label) & informatif |
| **Interpretasi** | 25% | Bisa menjelaskan makna cluster, hubungkan ke geologi |
| **Presentasi** | 10% | Jelas, terstruktur, sesuai waktu |

**Contoh deskriptor "Interpretasi":**
- *5* — menjelaskan tiap cluster + bukti dari crossplot + sadar keterbatasan.
- *3* — menjelaskan beberapa cluster secara umum.
- *1* — hanya "appnya jalan", tidak ada interpretasi.

---

## 3. Post-test (15 menit)

> Campuran pilihan ganda + isian singkat. Sasaran: konsep inti Hari 1–3 dengan penekanan Hari 3. **Kunci jawaban ada di bawah** (jangan dibagikan dulu).

### Bagian A — Pilihan Ganda

**1.** Perbedaan utama supervised vs unsupervised learning adalah:
- a) Supervised lebih cepat
- b) Supervised butuh label/target, unsupervised tidak
- c) Unsupervised selalu lebih akurat
- d) Tidak ada bedanya

**2.** Sebelum menjalankan KMeans pada data well log, langkah yang WAJIB dilakukan:
- a) Mengurutkan data berdasarkan kedalaman
- b) Mengubah ke format Excel
- c) Membuang NaN (`dropna`) dan melakukan scaling
- d) Menghapus kolom DEPTH

**3.** Kenapa scaling penting untuk KMeans tapi tidak untuk Decision Tree?
- a) Decision Tree tidak bisa baca angka besar
- b) KMeans pakai jarak Euclidean (sensitif skala); Decision Tree memisah per threshold
- c) Scaling mempercepat Decision Tree
- d) KMeans tidak butuh angka

**4.** Pada crossplot Neutron-Density, sumbu RHOB digambar terbalik (besar di bawah) karena:
- a) Bug di Matplotlib
- b) Konvensi petrofisika (batuan padat di bawah)
- c) Supaya lebih indah
- d) Wajib untuk semua scatter plot

**5.** Elbow method dipakai untuk:
- a) Membersihkan data
- b) Memilih jumlah cluster (K) yang optimal
- c) Menghitung akurasi
- d) Menggambar peta

**6.** Pada crossplot GR-Resistivity, kandidat zona reservoir berisi hidrokarbon ada di:
- a) GR tinggi + Resistivity rendah
- b) GR rendah + Resistivity tinggi
- c) GR tinggi + Resistivity tinggi
- d) GR rendah + Resistivity rendah

**7.** Di Streamlit, apa yang terjadi setiap kali user menggeser slider?
- a) Hanya bagian slider yang update
- b) Seluruh script dijalankan ulang dari atas ke bawah
- c) App restart total
- d) Tidak terjadi apa-apa

**8.** Fungsi `make_crossplot` sebaiknya `return fig` daripada langsung `plt.show()` karena:
- a) `plt.show()` error
- b) Supaya fleksibel (bisa dipakai di notebook, Streamlit, atau disimpan ke file)
- c) Lebih cepat
- d) Wajib di Python

### Bagian B — Isian Singkat

**9.** Sebutkan 4 tahap pada pipeline aplikasi data sederhana (sesuai diagram Sesi 4).

**10.** Sebutkan 1 perbedaan antara KMeans (hard clustering) dan GMM (soft clustering).

**11.** Kamu punya 4 fitur dengan rentang sangat berbeda (GR 0–200, RHOB ~2). Apa yang terjadi pada KMeans kalau kamu TIDAK scaling? Jelaskan singkat.

**12.** Sebutkan 2 colormap yang cocok untuk data **kategori** (cluster) dan 2 yang cocok untuk data **kontinu** (GR).

---

## 4. Kunci Jawaban (fasilitator)

**Pilihan Ganda:**
1. **b** — supervised butuh label, unsupervised tidak.
2. **c** — dropna + scaling.
3. **b** — KMeans jarak Euclidean; Decision Tree pakai threshold per fitur.
4. **b** — konvensi petrofisika.
5. **b** — memilih K optimal.
6. **b** — GR rendah (reservoir bersih) + Resistivity tinggi (hidrokarbon).
7. **b** — seluruh script re-run.
8. **b** — fleksibilitas penggunaan figure.

**Isian Singkat:**
9. **Upload → Preprocess → Inference → Output.**
10. KMeans: tiap titik masuk **tepat satu** cluster. GMM: tiap titik dapat **probabilitas** keanggotaan ke tiap cluster (soft). (Jawaban lain yang benar: GMM cocok untuk batas gradual.)
11. Fitur dengan rentang besar (**GR**) akan **mendominasi perhitungan jarak**, sehingga fitur lain (RHOB, NPHI) hampir diabaikan → cluster jadi praktis hanya berdasarkan GR / kurang bermakna.
12. **Kategori:** `tab10`, `Set1` (atau `tab20`, `Dark2`). **Kontinu:** `viridis`, `YlOrRd` (atau `Blues`, `plasma`). *(Catatan: `jet` sebaiknya dihindari untuk kontinu.)*

---

## 5. Prompt Diskusi Lanjutan (jika ada waktu)

Pancing diskusi dengan pertanyaan terbuka:

1. **Keterbatasan:** Cluster ≠ litologi resmi. Apa risikonya kalau kita anggap cluster langsung sebagai litologi tanpa validasi core?
2. **Memilih K:** Elbow bilang K=4, silhouette bilang K=6. Mana yang dipilih? Apa peran pengetahuan geologi di sini?
3. **Fitur:** Kalau kita tambahkan kurva PEF atau Resistivity ke clustering, apakah hasil membaik? Kenapa?
4. **Produksi:** Apa yang kurang dari mini project ini supaya layak dipakai sungguhan? (validasi data lebih ketat, simpan model, multi-well, autentikasi, dll.)

---

## 6. Arah Belajar Selanjutnya (next steps)

Bagikan ke peserta sebagai "mau ke mana setelah ini":

- **Perdalam ML:** evaluasi clustering (silhouette, Davies-Bouldin), feature engineering, dimensionality reduction (PCA, UMAP) sebelum clustering.
- **Supervised vs unsupervised:** gabungkan — pakai cluster sebagai fitur untuk model supervised.
- **Web app lanjut:** tambah multi-page Streamlit, simpan/load model (`joblib`), deploy ke Streamlit Community Cloud (gratis).
- **Domain:** dalami interpretasi log (buku *Crain's Petrophysical Handbook*, dataset publik FORCE 2020 Lithology).
- **Engineering:** ubah pipeline jadi package, tambah unit test (`pytest`), version control (Git).

---

## 7. Checklist Penutup (fasilitator)

- [ ] Semua peserta sempat demo (atau minimal sampel)
- [ ] Post-test terkumpul & dibahas
- [ ] Rubrik penilaian terisi
- [ ] Bagikan materi (file markdown + dataset + kode) ke peserta
- [ ] Sampaikan arah belajar lanjutan & cara kontak
- [ ] Apresiasi peserta 🎉

---

## ✅ Output Hari 3 (tercapai jika...)

> Sesuai rundown: **"peserta memiliki mini aplikasi/pipeline sederhana untuk analisis data tabular/well log."**

Peserta pulang membawa: (1) app Streamlit yang jalan, (2) pemahaman alur upload→preprocess→inference→output, (3) kemampuan membaca crossplot & menjelaskan hasil clustering.
