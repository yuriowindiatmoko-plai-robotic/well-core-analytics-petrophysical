# Hari 3 — Sesi 3: Visualisasi Matplotlib & Seaborn

> **Waktu:** 11.00 – 12.00 (60 menit)
> **Fokus:** Scatter plot, color map, label zona, visualisasi interaktif sederhana
> **Catatan fasilitator:** Banyak pemula "asal jalan" pakai Matplotlib tanpa paham strukturnya, lalu bingung saat plot rumit. Habiskan 10 menit pertama untuk mental model **Figure vs Axes** — ini investasi yang terbayar di seluruh sisa hari.

---

## 🎯 Tujuan Sesi

Setelah sesi ini, peserta bisa:

1. Memahami struktur Matplotlib: **Figure vs Axes** (pondasi semua plot).
2. Membuat plot **multi-panel** yang rapi (subplots).
3. Memilih **colormap** yang tepat (sequential / diverging / categorical).
4. Memberi **label zona** pada plot (shading + anotasi).
5. Memakai **Seaborn** untuk plot statistik cepat (pairplot, FacetGrid).
6. Membuat **visualisasi interaktif sederhana** (ipywidgets / Plotly).

---

## 1. Mental Model: Figure vs Axes

Ini konsep yang **wajib** dipahami.

> **Analogi:**
> - **Figure** = kanvas/bingkai kosong (keseluruhan gambar).
> - **Axes** = satu area plot di dalam kanvas (punya sumbu-x, sumbu-y, judul sendiri).
> - Satu Figure bisa berisi **banyak Axes** (multi-panel).

```python
import matplotlib.pyplot as plt

# pola yang DIANJURKAN: bikin Figure + Axes secara eksplisit
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot([1, 2, 3], [4, 5, 6])
ax.set_title("Satu Axes di dalam satu Figure")
ax.set_xlabel("x"); ax.set_ylabel("y")
plt.show()
```

**Penjelasan bagian:**
- `fig, ax = plt.subplots()` → membuat **Figure** (`fig`) dan **Axes** (`ax`) sekaligus. Ini cara yang bersih dan bisa dikontrol (beda dengan `plt.plot()` yang "ajaib" dan susah saat plot rumit).
- Semua perintah menggambar lewat `ax.` → eksplisit titik gambarnya di mana.

> **Aturan praktis:** Selalu pakai pola `fig, ax = plt.subplots(...)`. Hindari mencampur `plt.plot()` dengan `ax.plot()` di plot yang sama — ini sumber bug umum (ingat masalah `fig = plt.subplots()` yang menghasilkan tuple di latihan sebelumnya).

---

## 2. Plot Multi-Panel (Subplots)

Untuk well log, kita sering butuh **beberapa track berdampingan**.

```python
fig, axes = plt.subplots(1, 3, figsize=(10, 8), sharey=True)

# axes adalah array: axes[0], axes[1], axes[2]
axes[0].plot(df["GR"],   df["DEPTH"], color="green")
axes[0].set_title("GR"); axes[0].set_xlim(0, 200)

axes[1].plot(df["RHOB"], df["DEPTH"], color="red")
axes[1].set_title("RHOB"); axes[1].set_xlim(1.95, 2.95)

axes[2].plot(df["NPHI"], df["DEPTH"], color="blue")
axes[2].set_title("NPHI"); axes[2].set_xlim(0.45, -0.15)

for ax in axes:
    ax.invert_yaxis()            # kedalaman: kecil di atas
    ax.grid(True, alpha=0.3)

axes[0].set_ylabel("DEPTH (m)")
plt.tight_layout()
plt.show()
```

**Penjelasan bagian:**
- `plt.subplots(1, 3)` → 1 baris, 3 kolom → `axes` jadi array 3 Axes.
- `sharey=True` → ketiga track **berbagi sumbu kedalaman** (rapi, hemat ruang).
- `for ax in axes:` → loop untuk hal yang sama di semua track (grid, invert) → **hindari copy-paste**.
- `ax.invert_yaxis()` → balik sumbu kedalaman (konvensi log).
- `plt.tight_layout()` → rapikan jarak antar panel otomatis.

---

## 3. Memilih Colormap yang Tepat

Colormap salah = interpretasi salah. Ada 3 jenis utama:

| Jenis | Kapan dipakai | Contoh |
|---|---|---|
| **Sequential** | data berurut rendah→tinggi (porositas, GR) | `viridis`, `YlOrRd`, `Blues` |
| **Diverging** | ada titik tengah penting (deviasi +/-) | `RdBu`, `coolwarm` |
| **Categorical** | label/kelas (cluster, litologi) | `tab10`, `Set1` |

```python
# BENAR: cluster (kategori) pakai colormap categorical
plt.scatter(df["NPHI"], df["RHOB"], c=df["cluster"], cmap="tab10")

# BENAR: GR (nilai kontinu) pakai sequential
plt.scatter(df["NPHI"], df["RHOB"], c=df["GR"], cmap="viridis")
```

> **Jebakan umum:** memakai `jet`/`rainbow` untuk data kontinu. Mata manusia salah menafsir gradasinya (efek "banding" palsu). `viridis` jauh lebih jujur secara persepsi.

---

## 4. Memberi Label Zona

Sering kita mau menandai **zona of interest** (misal reservoir di kedalaman tertentu).

```python
fig, ax = plt.subplots(figsize=(4, 8))
ax.plot(df["GR"], df["DEPTH"], color="green")
ax.invert_yaxis()
ax.set_xlabel("GR (API)"); ax.set_ylabel("DEPTH (m)")

# shading zona reservoir (misal kedalaman 4700-4750 m)
ax.axhspan(4700, 4750, color="yellow", alpha=0.3)

# anotasi teks + panah
ax.annotate("Zona Reservoir",
            xy=(150, 4725), xytext=(160, 4680),
            arrowprops=dict(arrowstyle="->", color="black"))
plt.show()
```

**Penjelasan bagian:**
- `ax.axhspan(y1, y2, ...)` → arsir **pita horizontal** antara dua kedalaman (`axvspan` untuk pita vertikal).
- `ax.annotate(...)` → tambah teks + panah; `xy` = titik yang ditunjuk, `xytext` = posisi teks.

---

## 5. Seaborn: Plot Statistik Cepat

Seaborn = lapisan di atas Matplotlib, fokus ke **visualisasi statistik** dengan kode singkat.

### Pairplot — lihat semua hubungan sekaligus

```python
import seaborn as sns

sns.pairplot(
    df, vars=["GR", "RHOB", "NPHI", "DTC"],
    hue="cluster",                 # warnai per cluster (dari Sesi 1)
    palette="Dark2",
    diag_kind="kde",
    plot_kws={"s": 15, "alpha": 0.6},
)
plt.show()
```

**Penjelasan bagian:**
- `vars=[...]` → kurva yang mau dibandingkan satu-lawan-satu (matriks scatter).
- `hue="cluster"` → setiap cluster warna beda → langsung kelihatan apakah cluster terpisah di pasangan fitur mana pun.
- `diag_kind="kde"` → diagonal menampilkan distribusi (kurva kepadatan) tiap fitur.

> **Kekuatan pairplot:** dalam satu perintah, kamu melihat *semua* crossplot pasangan fitur + distribusinya. Sempurna untuk eksplorasi awal.

### FacetGrid — pisahkan per kategori

```python
g = sns.FacetGrid(df, col="LITH", col_wrap=4, height=3)
g.map(sns.scatterplot, "NPHI", "RHOB", alpha=0.5)
g.set(xlim=(-0.15, 0.45), ylim=(2.95, 1.95))
plt.show()
```

**Penjelasan:** buat **satu panel kecil per litologi** → bandingkan sebaran NPHI-RHOB tiap litologi secara berdampingan.

---

## 6. Visualisasi Interaktif Sederhana

### Opsi A — ipywidgets (di Jupyter/Colab)

```python
import ipywidgets as widgets
from IPython.display import display

def plot_zona(kedalaman_atas, kedalaman_bawah):
    fig, ax = plt.subplots(figsize=(4, 8))
    ax.plot(df["GR"], df["DEPTH"], color="green")
    ax.axhspan(kedalaman_atas, kedalaman_bawah, color="yellow", alpha=0.3)
    ax.invert_yaxis()
    plt.show()

widgets.interact(
    plot_zona,
    kedalaman_atas=(4600, 4800, 10),
    kedalaman_bawah=(4600, 4850, 10),
)
```

**Penjelasan:** `widgets.interact` otomatis membuat **slider** untuk tiap argumen fungsi. Geser slider → plot update real-time. Bagus untuk eksplorasi zona.

### Opsi B — Plotly (hover & zoom)

```python
import plotly.express as px

fig = px.scatter(
    df, x="NPHI", y="RHOB", color="GR",
    hover_data=["DEPTH", "cluster"],
)
fig.update_yaxes(autorange="reversed")    # balik sumbu density
fig.show()
```

**Penjelasan:** Plotly bikin plot **interaktif** (hover lihat nilai, zoom, pan) tanpa kode tambahan. Cocok kalau mau plot yang bisa "dipegang" peserta. Ini juga jembatan ke web app di Sesi 5.

---

## ✅ Latihan (10 menit)

1. Buat figure 1×3 track (GR, RHOB, NPHI) dengan sumbu kedalaman dibalik dan `sharey=True`.
2. Buat pairplot 4 fitur log, warnai dengan `cluster`. Di pasangan fitur mana cluster paling terpisah?
3. Tambahkan `axhspan` untuk menyorot satu zona menarik + anotasi panah.

---

## 🔗 Koneksi ke Sesi Berikutnya

Kita sudah jago membuat plot. Tapi semua ini masih di notebook. Di **Sesi 4 (Arsitektur Web App Ringan)** kita belajar **cara menyusun kode** supaya bisa berubah dari "notebook berantakan" menjadi "aplikasi rapi" — fondasi sebelum membangun mini project Streamlit.
