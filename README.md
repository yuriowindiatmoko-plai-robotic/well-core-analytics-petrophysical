# Well Core Analytics & Petrophysical

Project untuk analisis **well log & core data** petrofisika, lengkap dengan
**unsupervised clustering** (KMeans & GMM). Semua plot disimpan otomatis sebagai
JPG di folder `output/`.

Dikembangkan dari notebook Colab asli menjadi script Python yang bisa dijalankan
per section (section 1–5) atau sekaligus (`all-section.py`).

---

## Project Structure

```
.
├── all-section.py                              # Run semua section (1–5) sekaligus
├── section1.py                                 # Section 1 — Load & display well data
├── section2.py                                 # Section 2 — Well plot (matplotlib)
├── section3.py                                 # Section 3 — Histograms & crossplots
├── section4.py                                 # Section 4 — Core data + poro-perm relationship
├── section5.py                                 # Section 5 — Unsupervised clustering
├── section-1.py                                # (Legacy) salinan section 1 dari notebook
├── salinan_dari_salinan_dari_untitled7.py      # (Legacy) export notebook Colab asli
├── L0509WellData.csv                           # Dataset well log (Section 1–3)
├── 15_9-19A-CORE.csv                           # Dataset core data (Section 4)
├── xeek_train_subset.csv                       # Dataset FORCE 2020 (Section 5)
├── output/                                     # Semua figure JPG hasil run
├── output-log/                                 # Log tiap run section
└── files-materi-sesi-hari-3-ver_1/             # Materi pendukung (markdown)
```

---

## Prasyarat (Prerequisites)

- [**Miniconda**](https://docs.conda.io/projects/miniconda/) — sudah ter-install & di `PATH`.
- [**PyCharm**](https://www.jetbrains.com/pycharm/) (Community atau Professional).

---

## Setup Mudah via PyCharm + Conda

Cara paling aman & mudah: bikin **conda environment baru** lewat PyCharm, jadi
env `base` miniconda tetap bersih dan **tidak akan rusak** kalau ada dependency conflict.

1. **Buka PyCharm** → `File` ▸ `New Project`.
2. Isi **Location** = folder project ini.
3. Bagian **Python Interpreter**, pilih type **Conda**.
4. Pilih **Python version: `3.13`**.
5. Pilih **New environment** (bukan Existing), isi nama environment: `well-core`.
6. Klik **Create**. PyCharm akan membuat env conda baru bernama `well-core`.
7. Buka **Terminal** bawaan PyCharm (kiri bawah). Env `well-core` sudah
   **otomatis aktif** — ditandai prompt `(well-core)`.

---

## Install Dependencies

Jalankan perintah ini di Terminal PyCharm (env `well-core` aktif):

```bash
conda install pandas numpy matplotlib yellowbrick seaborn statsmodels scikit-learn -c districtdatalabs -c conda-forge
```

> Urutan channel `-c districtdatalabs -c conda-forge` penting karena
> `yellowbrick` tersedia di channel `districtdatalabs`.

---

## Cara Menjalankan Setiap Section

> Penting: **jalankan dari root folder project** (folder yang berisi file `.csv`),
> supaya path dataset & folder `output/` terbaca dengan benar.

| Section | Apa yang dilakukan | Command | Contoh output |
|---|---|---|---|
| **All (1–5)** | Run semua section sekaligus | `python all-section.py` | semua `s0*_<...>.jpg` |
| **Section 1** | Load & display well data dari CSV | `python section1.py` | `s01_gr_vs_depth.jpg`, `s01_nphi_vs_rhob.jpg`, dll |
| **Section 2** | Well plot simple + advanced (matplotlib) | `python section2.py` | `s02_well_plot_simple.jpg`, `s02_well_plot_advanced.jpg` |
| **Section 3** | Histograms & crossplots (2D / 3D) | `python section3.py` | `s03_gr_hist_stats.jpg`, `s03_four_panel_crossplots.jpg`, dll |
| **Section 4** | Core data + Poro-Perm relationship (OLS regression) | `python section4.py` | `s04_poro_perm_regression.jpg`, `s04_measured_vs_predicted.jpg`, dll |
| **Section 5** | Unsupervised clustering (KMeans & GMM) | `python section5.py` | `s05_elbow_method.jpg`, `s05_wellplot_*.jpg`, `s05_pairplot_*.jpg`, dll |

Contoh run satu section:

```bash
python section4.py
```

Contoh run semua section sekaligus:

```bash
python all-section.py
```

---

## Output

- **Figure JPG** (DPI 200) → otomatis tersimpan di folder `output/`.
- **Run log** tiap section → tersimpan di folder `output-log/`.

---

## Dataset

| Dataset | Dipakai di | Keterangan |
|---|---|---|
| `L0509WellData.csv` | Section 1, 2, 3 | Well log standar (GR, RHOB, NPHI, DT). Null flag `-999` otomatis diubah ke `NaN`. |
| `15_9-19A-CORE.csv` | Section 4 | Core data (CPOR, CKHG) untuk derive poro-perm relationship. |
| `xeek_train_subset.csv` | Section 5 | Subset dataset FORCE 2020 lithofacies untuk clustering. |

---

## Catatan Legacy (jangan di-run)

File berikut adalah **export asli dari notebook Colab** dan disimpan hanya sebagai
referensi riwayat — **gunakan `section1.py` … `section5.py` / `all-section.py`** untuk
menjalankan analisis:

- `section-1.py` — salinan lama section 1.
- `salinan_dari_salinan_dari_untitled7.py` — export mentah notebook Colab (masih ada
  `google.colab` call, tidak bisa jalan langsung di lokal).

---

## Troubleshooting

- **`FileNotFoundError: ...csv`** → kamu belum run dari root folder project. Pastikan
  `cd` ke folder yang berisi file `.csv`, lalu run ulang.
- **`KeyError` / `ValueError: Input contains NaN`** di notebook asli → sudah diperbaiki
  di `section4.py` & `section5.py` (lihat header docstring tiap file).
- **`yellowbrick` tidak ketemu saat `conda install`** → pastikan channel
  `-c districtdatalabs` ikut ditulis di command.
- **Plot tidak muncul (macOS)** → script memanggil `plt.show()`; pastikan backend
  matplotlib GUI terpasang, atau cukup lihat hasilnya di folder `output/`.
