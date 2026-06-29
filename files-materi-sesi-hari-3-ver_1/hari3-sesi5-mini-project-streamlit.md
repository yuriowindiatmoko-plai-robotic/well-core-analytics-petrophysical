# Hari 3 — Sesi 5: Mini Project — Web App dengan Streamlit

> **Waktu:** 14.00 – 15.30 (90 menit)
> **Fokus:** Membuat aplikasi sederhana dengan Streamlit: upload CSV → tampilkan data → plot kurva → jalankan model
> **Catatan fasilitator:** ⚠️ **Sesi paling rawan overrun.** 90 menit untuk membangun app dari nol itu mepet untuk pemula. **Strategi:** jangan suruh mengetik dari kosong. Bagikan **kerangka isi-bagian-kosong** (`app_scaffold.py`) + sediakan **versi lengkap** (`app.py`) sebagai referensi. Peserta merangkai, bukan mengarang.

---

## 🎯 Tujuan Sesi

Setelah sesi ini, peserta bisa:

1. Memahami apa itu Streamlit & model "script jadi web app".
2. Memakai komponen inti: `file_uploader`, `dataframe`, `slider`, `multiselect`, `button`, `pyplot`.
3. Menyambungkan UI ke **`pipeline.py`** dari Sesi 4.
4. Memakai **caching** agar app cepat.
5. Menjalankan app: `streamlit run app.py`.

---

## 1. Apa itu Streamlit?

**Streamlit** mengubah **script Python biasa** menjadi **aplikasi web interaktif** — tanpa HTML, CSS, atau JavaScript.

> **Analogi:** Biasanya bikin web butuh "front-end" (HTML/CSS/JS) + "back-end" (Python). Streamlit menggabungnya: kamu nulis Python, Streamlit yang menggambar UI-nya.

**Model mental Streamlit yang WAJIB dipahami:**
> Setiap kali user berinteraksi (klik tombol, geser slider), **seluruh script dijalankan ulang dari atas ke bawah.**

Ini terasa aneh awalnya, tapi bikin kodenya sangat sederhana — kamu cukup tulis script linear, Streamlit urus sisanya. (Caching di bagian 5 mengatasi "kerja berat yang diulang".)

### Install

```bash
pip install streamlit
```

### "Hello World"

```python
# hello.py
import streamlit as st

st.title("Halo Streamlit 👋")
nama = st.text_input("Siapa nama kamu?")
if nama:
    st.write(f"Halo, {nama}!")
```

Jalankan:
```bash
streamlit run hello.py
```
Browser otomatis terbuka di `http://localhost:8501`.

---

## 2. Komponen Inti Streamlit

| Komponen | Fungsi |
|---|---|
| `st.title()` / `st.header()` / `st.write()` | teks & judul |
| `st.file_uploader()` | tombol upload file |
| `st.dataframe()` / `st.table()` | tampilkan tabel |
| `st.multiselect()` | pilih banyak opsi |
| `st.slider()` | geser angka |
| `st.button()` | tombol aksi |
| `st.pyplot(fig)` | tampilkan plot Matplotlib |
| `st.metric()` | tampilkan angka KPI |
| `st.columns()` | layout berdampingan |

---

## 3. Kerangka Isi-Bagian-Kosong (bagikan ke peserta)

> Beri file ini ke peserta. Mereka mengisi bagian `# TODO`. Pasangkan dengan `pipeline.py` dari Sesi 4 di folder yang sama.

```python
# app_scaffold.py  — ISI bagian bertanda TODO
import streamlit as st
import pandas as pd
from pipeline import load_data, preprocess, run_clustering, make_crossplot

st.title("🛢️ Well Log Clustering App")
st.write("Upload data well log, lalu kelompokkan jadi electrofacies.")

# 1) Upload CSV
uploaded = st.file_uploader("Upload file CSV", type="csv")

if uploaded is not None:
    # 2) Load & tampilkan data
    df = load_data(uploaded)
    st.subheader("Pratinjau Data")
    st.dataframe(df.head())          # TODO: tampilkan juga df.describe()

    # 3) Pilih fitur untuk clustering
    kolom_numerik = df.select_dtypes("number").columns.tolist()
    features = st.multiselect(
        "Pilih fitur (kurva log):",
        options=kolom_numerik,
        default=["GR", "RHOB", "NPHI", "DTC"],   # TODO: sesuaikan dgn data
    )

    # 4) Pilih jumlah cluster
    k = st.slider("Jumlah cluster", min_value=2, max_value=10, value=5)

    # 5) Tombol jalankan
    if st.button("Jalankan Clustering"):
        # TODO: panggil preprocess() -> run_clustering() -> make_crossplot()
        # TODO: tempel label ke dataframe lalu st.pyplot(fig)
        pass
```

---

## 4. Versi Lengkap (referensi fasilitator)

> Tampilkan ini setelah peserta mencoba, atau pakai untuk peserta yang sudah cepat.

```python
# app.py  — versi lengkap
import streamlit as st
import pandas as pd
from pipeline import load_data, preprocess, run_clustering, make_crossplot

st.set_page_config(page_title="Well Log Clustering", page_icon="🛢️", layout="wide")

st.title("🛢️ Well Log Clustering App")
st.write("Upload data well log → pilih fitur → kelompokkan jadi electrofacies.")

uploaded = st.file_uploader("Upload file CSV", type="csv")

if uploaded is None:
    st.info("⬆️ Silakan upload file CSV well log untuk mulai.")
    st.stop()                         # hentikan script sampai ada file

# ── Load & tampilkan data ────────────────────────────────────────
df = load_data(uploaded)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Pratinjau Data")
    st.dataframe(df.head())
with col2:
    st.subheader("Statistik")
    st.dataframe(df.describe())

# ── Kontrol di sidebar ───────────────────────────────────────────
st.sidebar.header("⚙️ Pengaturan")
kolom_numerik = df.select_dtypes("number").columns.tolist()
default_fitur = [c for c in ["GR", "RHOB", "NPHI", "DTC"] if c in kolom_numerik]

features = st.sidebar.multiselect(
    "Fitur untuk clustering:", options=kolom_numerik, default=default_fitur
)
k = st.sidebar.slider("Jumlah cluster (K)", 2, 10, 5)

# ── Jalankan ─────────────────────────────────────────────────────
if st.sidebar.button("🚀 Jalankan Clustering"):
    if len(features) < 2:
        st.error("Pilih minimal 2 fitur.")
        st.stop()

    try:
        X, clean, scaler = preprocess(df, features)
        labels, model = run_clustering(X, n_clusters=k)
        clean["cluster"] = labels

        st.success(f"Selesai! {len(clean)} baris dikelompokkan jadi {k} cluster.")

        # tampilkan crossplot
        st.subheader("Crossplot (diwarnai cluster)")
        fig = make_crossplot(clean)
        st.pyplot(fig)

        # ringkasan tiap cluster
        st.subheader("Rata-rata fitur per cluster")
        st.dataframe(clean.groupby("cluster")[features].mean().round(2))

        # tombol download hasil
        csv = clean.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download hasil (CSV)", csv, "hasil_cluster.csv", "text/csv")

    except ValueError as e:
        st.error(f"Terjadi masalah: {e}")
```

**Penjelasan bagian-bagian penting:**

- **`st.set_page_config(...)`** → atur judul tab & layout lebar. Harus jadi perintah Streamlit **paling pertama**.
- **`st.stop()`** → menghentikan eksekusi script. Dipakai untuk *guard clause*: kalau belum ada file, jangan lanjut. Ini cara Streamlit yang rapi (ganti `if-else` bertingkat).
- **`st.columns(2)`** + **`with col1:`** → tata letak berdampingan (data di kiri, statistik di kanan).
- **`st.sidebar.xxx`** → taruh kontrol di panel samping → area utama bersih untuk hasil.
- **`if st.button(...)`** → blok di dalamnya **hanya jalan saat tombol diklik** (karena script re-run, tombol mengembalikan `True` hanya di run setelah diklik).
- **Validasi** (`if len(features) < 2`) + **`try/except ValueError`** → menangkap error dari `pipeline.py` dan menampilkannya ramah, bukan crash. (Buah dari error handling di Sesi 4.)
- **`st.download_button(...)`** → user bisa unduh hasil clustering → app jadi benar-benar berguna.

---

## 5. Caching: Bikin App Cepat

Ingat: script re-run **tiap interaksi**. Kalau load data 100 MB tiap kali geser slider → lambat. Solusinya **caching**.

```python
@st.cache_data
def load_data(file):
    return pd.read_csv(file)
```

| Dekorator | Untuk apa |
|---|---|
| `@st.cache_data` | hasil komputasi/data (DataFrame, hasil transform) |
| `@st.cache_resource` | objek "berat" yang dipakai ulang (model ML, koneksi DB) |

**Penjelasan:** dengan `@st.cache_data`, Streamlit **mengingat hasil** untuk input yang sama. Geser slider yang tak terkait? Data tidak di-load ulang → instan.

> Untuk workshop, taruh `@st.cache_data` di `load_data` saja sudah cukup terasa bedanya.

---

## 6. Checklist Mini Project

Peserta dianggap "selesai" kalau app-nya bisa:

- [ ] Upload file CSV
- [ ] Menampilkan pratinjau data + statistik
- [ ] Memilih fitur & jumlah cluster
- [ ] Menjalankan clustering saat tombol diklik
- [ ] Menampilkan crossplot diwarnai cluster
- [ ] (Bonus) Menampilkan ringkasan per cluster
- [ ] (Bonus) Tombol download hasil

---

## 📦 Struktur Folder Mini Project

```
mini-project/
├── pipeline.py     # dari Sesi 4 (load, preprocess, clustering, plot)
├── app.py          # UI Streamlit (Sesi 5)
└── well.csv        # data contoh (opsional, peserta bisa upload sendiri)
```

Jalankan dari dalam folder:
```bash
streamlit run app.py
```

---

## 🔗 Koneksi ke Sesi Berikutnya

App sudah jadi! Di **Sesi 6 (Presentasi & Post-test)** peserta mendemokan aplikasinya, menjelaskan interpretasi hasilnya, dan kita evaluasi pemahaman lewat post-test.
