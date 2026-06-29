# Hari 3 — Sesi 1: Unsupervised Learning Singkat

> **Waktu:** 09.00 – 09.45 (45 menit)
> **Fokus:** Clustering, segmentasi data, pengenalan pola tanpa label
> **Catatan fasilitator:** Sesi ini singkat dan padat. Tujuannya *bukan* membuat peserta jadi ahli clustering, tapi memberi intuisi + 1 alur kerja yang bisa langsung dipakai di mini project sore nanti.

---

## 🎯 Tujuan Sesi

Setelah sesi ini, peserta bisa:

1. Menjelaskan beda **supervised** vs **unsupervised learning** dengan bahasa sendiri.
2. Memahami cara kerja **KMeans** secara intuitif (tanpa matematika berat).
3. Menjalankan clustering pada data well log dan menempelkan label cluster ke dataframe.
4. Memilih jumlah cluster (`K`) memakai **Elbow** dan **Silhouette**.
5. Tahu kapan pakai **GMM** sebagai alternatif yang lebih "lembut".

---

## 1. Apa itu Unsupervised Learning?

Ingat di Hari 2 kita pakai **supervised learning** — kita punya **target/label** (misalnya litologi tiap kedalaman), lalu model belajar memprediksinya.

**Unsupervised learning kebalikannya: tidak ada label sama sekali.** Kita serahkan ke algoritma untuk *menemukan sendiri* pola atau kelompok di dalam data.

> **Analogi:** Bayangkan kamu masuk ke gudang penuh baut dan mur yang tercampur, tanpa ada yang memberi tahu kategorinya.
> - **Supervised** = ada orang yang sudah menempelkan label "ini M6, ini M8" di tiap baut → kamu tinggal hafal aturannya.
> - **Unsupervised** = tidak ada label apa pun → kamu kelompokkan sendiri berdasarkan *kemiripan* (ukuran, bentuk, panjang), lalu *baru* kamu kasih nama tiap tumpukan.

| | Supervised | Unsupervised |
|---|---|---|
| Butuh label? | ✅ Ya | ❌ Tidak |
| Pertanyaan | "Prediksi Y dari X" | "Pola apa yang ada di X?" |
| Contoh tugas | Klasifikasi, regresi | **Clustering**, segmentasi, deteksi anomali |
| Contoh di well log | Prediksi litologi (ada label FACIES) | Temukan **electrofacies** (tanpa label) |

---

## 2. Clustering & KMeans

**Clustering** = mengelompokkan data sehingga titik dalam satu kelompok (*cluster*) saling mirip, dan beda dari kelompok lain.

**KMeans** adalah algoritma clustering paling populer. Cara kerjanya seperti permainan tarik-menarik:

1. **Tentukan K** (jumlah cluster yang kita mau, misal 5).
2. **Taruh K titik pusat** (*centroid*) secara acak.
3. **Assign:** tiap data menempel ke centroid **terdekat**.
4. **Update:** tiap centroid pindah ke *rata-rata* posisi anggotanya.
5. Ulangi langkah 3–4 sampai centroid berhenti bergerak (konvergen).

> **Kata kunci penting:** KMeans bekerja berdasarkan **jarak** (Euclidean). Inilah kenapa **scaling** wajib (lihat bagian praktik di bawah).

---

## 3. Kenapa Relevan untuk Well Log?

Di lapangan, kita sering punya **data log lengkap tapi tanpa label litologi** (karena core/cutting mahal dan tidak tersedia di semua kedalaman).

Dengan clustering, kita biarkan algoritma mengelompokkan kedalaman yang punya **respons log mirip** (GR, RHOB, NPHI, DTC). Kelompok hasil clustering ini disebut **electrofacies** — bukan litologi resmi, tapi "kelompok batuan dengan tanda tangan log yang sama" yang sangat berguna untuk segmentasi cepat.

---

## 4. Praktik: KMeans Langkah demi Langkah

### Langkah 1 — Load data & pilih fitur

```python
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("well.csv")

# pilih kolom log numerik sebagai fitur
features = df[["GR", "RHOB", "NPHI", "DTC"]].dropna()
```

**Penjelasan bagian:**
- `df[["GR", "RHOB", "NPHI", "DTC"]]` → ambil 4 kurva log sebagai input clustering.
- `.dropna()` → **buang baris yang ada NaN**. Ini WAJIB sebelum clustering — scikit-learn akan error `ValueError: Input contains NaN` kalau ada nilai kosong. (Ingat bug ini dari latihan sebelumnya!)

### Langkah 2 — Scaling (jangan dilewati!)

```python
scaler = StandardScaler()
X = scaler.fit_transform(features)
```

**Penjelasan bagian — kenapa ini KRUSIAL:**

KMeans mengukur jarak antar titik. Tapi lihat skala kurva log kita:

| Kurva | Rentang khas |
|---|---|
| GR | 0 – 200 |
| RHOB | 1.95 – 2.95 |
| NPHI | -0.15 – 0.45 |
| DTC | 40 – 160 |

Tanpa scaling, perbedaan **1 unit GR** dianggap sama besar dengan **1 unit RHOB** — padahal GR rentangnya ratusan, RHOB cuma ~1. Akibatnya **GR mendominasi total** dan kurva lain nyaris diabaikan.

`StandardScaler` mengubah tiap kolom jadi **mean 0, std 1**, sehingga semua kurva "punya suara yang setara". Ini langkah kecil tapi sering jadi pembeda antara cluster yang masuk akal vs hasil acak.

### Langkah 3 — Jalankan KMeans

```python
kmeans = KMeans(n_clusters=5, n_init=10, random_state=42)
labels = kmeans.fit_predict(X)

features = features.copy()
features["cluster"] = labels
print(features.head())
```

**Penjelasan bagian:**
- `n_clusters=5` → kita minta 5 electrofacies.
- `n_init=10` → KMeans diulang 10 kali dengan centroid awal berbeda, lalu ambil hasil terbaik. **Selalu set ini eksplisit** supaya hasil konsisten di semua versi scikit-learn dan tidak muncul `FutureWarning`.
- `random_state=42` → bikin hasil **reproducible** (sama tiap kali dijalankan).
- `fit_predict(X)` → latih model **dan** langsung kembalikan label cluster (0–4) untuk tiap baris.

---

## 5. Memilih Jumlah Cluster (K)

K tidak ada "jawaban benar" mutlak — tapi ada dua alat bantu.

### Elbow Method (inertia)

```python
import matplotlib.pyplot as plt

inertias = []
K_range = range(1, 11)
for k in K_range:
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    km.fit(X)
    inertias.append(km.inertia_)

plt.plot(list(K_range), inertias, "o-")
plt.xlabel("Jumlah Cluster (K)")
plt.ylabel("Inertia (total jarak ke centroid)")
plt.title("Elbow Method")
plt.grid(True)
plt.show()
```

**Cara baca:** `inertia` selalu turun saat K naik. Cari titik **"siku" (elbow)** — tempat penurunan mulai melandai. Itu kandidat K yang bagus (menambah cluster setelahnya cuma sedikit membantu).

### Silhouette Score

```python
from sklearn.metrics import silhouette_score

for k in range(2, 7):
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    lab = km.fit_predict(X)
    score = silhouette_score(X, lab)
    print(f"K={k} → silhouette = {score:.3f}")
```

**Cara baca:** skor antara **-1 dan 1**. Makin **mendekati 1** makin bagus (cluster rapat & terpisah jelas). Pilih K dengan skor tertinggi yang masih masuk akal secara geologi.

---

## 6. Alternatif: GMM (Soft Clustering)

KMeans itu **hard**: tiap titik masuk **tepat satu** cluster. **Gaussian Mixture Model (GMM)** itu **soft/probabilistik**: tiap titik dapat *probabilitas* keanggotaan ke tiap cluster.

```python
from sklearn.mixture import GaussianMixture

gmm = GaussianMixture(n_components=5, random_state=42)
gmm_labels = gmm.fit_predict(X)

# probabilitas keanggotaan (bukan cuma label)
probs = gmm.predict_proba(X)
print(probs[:5].round(2))   # tiap baris menjumlah ke 1.0
```

**Kapan pakai GMM?**
- Saat batas antar litologi **gradual** (tidak tegas) → cocok dengan sifat batuan yang sering bercampur.
- Saat kamu butuh **tingkat keyakinan**, bukan cuma label keras.

> **Catatan:** KMeans cocok untuk demo cepat & intuitif. GMM lebih realistis untuk transisi geologi yang halus. Untuk mini project sore, KMeans sudah cukup.

---

## ✅ Checkpoint (5 menit)

Minta peserta jawab cepat:

1. Kenapa kita `.dropna()` sebelum KMeans?
2. Kenapa scaling penting di KMeans tapi tidak di Decision Tree (Hari 2)?
3. Pada Elbow plot, "siku" itu menandakan apa?

<details>
<summary>Kunci jawaban</summary>

1. scikit-learn error kalau ada NaN; clustering butuh data lengkap.
2. KMeans pakai jarak Euclidean (sensitif skala); Decision Tree memisah per fitur dengan threshold (tidak terpengaruh skala).
3. Titik di mana menambah cluster hanya sedikit menurunkan inertia → kandidat K optimal.

</details>

---

## 🔗 Koneksi ke Sesi Berikutnya

Sekarang kita punya **label cluster** menempel di tiap kedalaman. Di **Sesi 2 (Crossplot & Interpretasi)** kita akan **memvisualisasikan** cluster ini di atas crossplot Neutron-Density untuk melihat apakah kelompok hasil algoritma benar-benar punya makna geologi.
