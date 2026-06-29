# Hari 3 — Sesi 4: Arsitektur Web App Ringan

> **Waktu:** 13.00 – 14.00 (60 menit)
> **Fokus:** Konsep pipeline: upload file → preprocessing → inference → output grafik
> **Catatan fasilitator:** Sesi ini **lebih banyak konsep daripada nge-code**. Tujuannya mengubah cara berpikir peserta: dari "kode notebook yang jalan dari atas ke bawah" menjadi "fungsi-fungsi rapi yang bisa dirangkai jadi aplikasi". Kode di sini = kerangka yang langsung dipakai di mini project Sesi 5.

---

## 🎯 Tujuan Sesi

Setelah sesi ini, peserta bisa:

1. Memahami **pipeline data** sebagai rangkaian tahap: upload → preprocess → inference → output.
2. Memecah kode jadi **fungsi-fungsi terpisah** (separation of concerns).
3. Mengerti kenapa **kode notebook ≠ kode aplikasi**.
4. Menempatkan model ML di posisi yang benar (load sekali, pakai berkali-kali).
5. Menambahkan **validasi & error handling** di tiap tahap.

---

## 1. Notebook vs Aplikasi — Apa Bedanya?

> **Analogi:** Notebook itu seperti **catatan masak coret-coretan** — kamu yang tahu urutannya, boleh loncat-loncat, boleh berantakan.
> Aplikasi itu seperti **resep yang dipublikasikan** — orang lain harus bisa mengikuti tanpa kamu di sampingnya.

| Aspek | Kode Notebook | Kode Aplikasi |
|---|---|---|
| Urutan eksekusi | Bergantung urutan cell (rawan bug) | Jelas, lewat pemanggilan fungsi |
| State | Variabel global "nyangkut" antar cell | Dibungkus dalam fungsi, eksplisit |
| Input | Hard-coded (`pd.read_csv("file.csv")`) | Dari user (upload) |
| Reusability | Susah dipakai ulang | Tiap fungsi bisa dipanggil di mana saja |
| Testing | Hampir mustahil | Tiap fungsi bisa dites sendiri |

> 💡 **Ingat latihan kita sebelumnya:** notebook yang error karena clustering jalan *sebelum* `dropna()`, dan karena urutan cell. Saat kita ubah jadi fungsi-fungsi terpisah, bug itu hilang — karena alur jadi eksplisit dan tiap tahap punya tanggung jawab jelas. **Itulah inti sesi ini.**

---

## 2. Mental Model Pipeline

Hampir semua aplikasi data sederhana mengikuti alur yang sama:

```
┌──────────┐    ┌───────────────┐    ┌─────────────┐    ┌──────────────┐
│  UPLOAD  │ →  │  PREPROCESS   │ →  │  INFERENCE  │ →  │  OUTPUT      │
│  (CSV)   │    │ (clean,scale) │    │ (run model) │    │ (grafik/tabel│
└──────────┘    └───────────────┘    └─────────────┘    └──────────────┘
```

**Prinsip kunci: tiap kotak = satu fungsi.** Input jelas, output jelas. Kotak tidak peduli isi kotak lain — dia cuma terima input dan kembalikan output.

> **Kenapa dipisah begini?**
> - **Testable:** bisa tes `preprocess()` tanpa menjalankan model.
> - **Reusable:** fungsi yang sama dipakai di notebook, di app, di batch script.
> - **Swappable:** mau ganti KMeans jadi GMM? cukup ubah fungsi `inference`, sisanya tak tersentuh.
> - **Debuggable:** kalau error, langsung tahu di tahap mana.

---

## 3. Membangun Pipeline (kode kerangka)

Kita bikin file `pipeline.py` berisi 4 fungsi — satu per tahap. **File ini akan dipakai langsung di Sesi 5.**

```python
# pipeline.py
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# ── Tahap 1: LOAD ────────────────────────────────────────────────
def load_data(file) -> pd.DataFrame:
    """Baca CSV menjadi DataFrame. `file` bisa path ATAU objek upload."""
    df = pd.read_csv(file)
    return df


# ── Tahap 2: PREPROCESS ──────────────────────────────────────────
def preprocess(df: pd.DataFrame, features: list):
    """Pilih fitur, buang NaN, lalu scaling.
    Kembalikan X (siap model), clean (df bersih), scaler (untuk reuse).
    """
    # validasi: pastikan kolom yang diminta ada
    missing = [c for c in features if c not in df.columns]
    if missing:
        raise ValueError(f"Kolom tidak ditemukan: {missing}")

    clean = df[features].dropna().copy()
    scaler = StandardScaler()
    X = scaler.fit_transform(clean)
    return X, clean, scaler


# ── Tahap 3: INFERENCE ───────────────────────────────────────────
def run_clustering(X, n_clusters: int = 5):
    """Latih KMeans dan kembalikan label + model."""
    model = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    labels = model.fit_predict(X)
    return labels, model


# ── Tahap 4: OUTPUT ──────────────────────────────────────────────
def make_crossplot(clean: pd.DataFrame, x="NPHI", y="RHOB", color="cluster"):
    """Buat crossplot Neutron-Density diwarnai cluster. Kembalikan Figure."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 7))
    sc = ax.scatter(clean[x], clean[y], c=clean[color],
                    cmap="tab10", s=12, alpha=0.7)
    ax.set_xlabel(x); ax.set_ylabel(y)
    if y == "RHOB":
        ax.invert_yaxis()          # konvensi density
    ax.set_title("Crossplot diwarnai Cluster")
    fig.colorbar(sc, ax=ax, label=color)
    return fig
```

**Penjelasan tiap bagian:**

- **`load_data(file)`** — perhatikan `file` bukan nama file hard-coded. Bisa diisi path (`"well.csv"`) **atau** objek upload dari Streamlit. Inilah yang membuat fungsi ini siap untuk web app.
- **`preprocess(...)`** — menggabungkan 3 hal: validasi kolom, `dropna()`, dan scaling. Mengembalikan **3 hal**: `X` (untuk model), `clean` (df bersih untuk plot), dan `scaler` (kalau perlu transform data baru nanti). Ini contoh **kontrak fungsi yang jelas**.
- **`run_clustering(X, n_clusters)`** — *hanya* mengurus model. Tidak tahu-menahu soal file atau plot. `n_clusters` jadi parameter → mudah diubah dari UI (slider di Sesi 5).
- **`make_crossplot(...)`** — *hanya* mengurus visual. Mengembalikan `fig` (bukan langsung `plt.show()`) supaya pemanggil bebas mau menampilkan di mana (notebook, Streamlit, simpan ke file).

> **Pola penting:** fungsi output **mengembalikan `fig`**, tidak memanggil `plt.show()` sendiri. Ini membuat fungsi fleksibel — di Streamlit kita pakai `st.pyplot(fig)`, di notebook kita `plt.show()`, di batch kita `fig.savefig()`.

---

## 4. Merangkai Pipeline

Begini cara keempat fungsi bekerja sama (ini "lem"-nya):

```python
# orchestrator.py — merangkai pipeline jadi satu alur
from pipeline import load_data, preprocess, run_clustering, make_crossplot

def jalankan_pipeline(file, features, n_clusters=5):
    df = load_data(file)                          # 1. upload
    X, clean, scaler = preprocess(df, features)   # 2. preprocess
    labels, model = run_clustering(X, n_clusters) # 3. inference
    clean["cluster"] = labels
    fig = make_crossplot(clean)                   # 4. output
    return df, clean, fig, model
```

**Penjelasan:** Lihat betapa **mudah dibaca**-nya — alurnya literal mengikuti diagram pipeline. Tiap baris = satu tahap. Kalau ada error, traceback langsung menunjuk fungsi mana yang bermasalah.

---

## 5. Error Handling & Validasi

Aplikasi yang dipakai orang **harus tahan input jelek**. Tambahkan pengecekan di tahap rawan:

```python
def load_data(file) -> pd.DataFrame:
    try:
        df = pd.read_csv(file)
    except Exception as e:
        raise ValueError(f"Gagal membaca CSV: {e}")

    if df.empty:
        raise ValueError("File CSV kosong.")
    return df
```

**Tahap-tahap yang perlu dijaga:**
- **Upload:** file kosong? bukan CSV? encoding aneh?
- **Preprocess:** kolom yang diminta tidak ada? semua baris NaN setelah dropna?
- **Inference:** jumlah data < jumlah cluster? (KMeans error kalau `n_samples < n_clusters`).

> **Prinsip:** "Gagal dengan pesan jelas" jauh lebih baik daripada "crash dengan traceback misterius" — apalagi kalau penggunanya bukan programmer.

---

## 6. Di Mana Model "Tinggal"?

Model ML sebaiknya **dimuat sekali**, bukan tiap kali ada interaksi. Di notebook ini tidak terasa, tapi di web app (yang sering re-run) ini penting untuk kecepatan.

```python
# konsep: model di-load sekali, di-cache
# (di Streamlit Sesi 5, kita pakai @st.cache_resource untuk ini)

# untuk clustering yang dilatih on-the-fly dari data upload,
# tidak perlu load model dari disk — tapi konsepnya sama:
# pekerjaan berat jangan diulang kalau tidak berubah.
```

Kita akan implementasi caching-nya secara konkret di Sesi 5 dengan dekorator Streamlit.

---

## ✅ Diskusi (10 menit)

Lempar pertanyaan ke peserta:

1. Kalau kita mau ganti KMeans jadi GMM, **fungsi mana saja** yang perlu diubah? (Jawab: cukup `run_clustering`.)
2. Kenapa `make_crossplot` mengembalikan `fig` dan tidak langsung `plt.show()`?
3. Apa bedanya `load_data("well.csv")` (path) dengan `load_data(uploaded_file)` (objek upload)? Kenapa fungsi yang sama bisa terima dua-duanya? (Jawab: `pd.read_csv` menerima path string maupun file-like object.)

---

## 🔗 Koneksi ke Sesi Berikutnya

Kita sudah punya `pipeline.py` yang bersih dan rapi. Di **Sesi 5 (Mini Project Streamlit)** kita tinggal **menambahkan "wajah" (UI)** di atas pipeline ini — upload, slider, tombol, tampilkan grafik — dan jadilah aplikasi web sungguhan tanpa nulis satu baris HTML pun.
