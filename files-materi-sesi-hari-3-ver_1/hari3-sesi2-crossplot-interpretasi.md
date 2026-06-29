# Hari 3 — Sesi 2: Crossplot & Interpretasi

> **Waktu:** 09.45 – 11.00 (75 menit)
> **Fokus:** Crossplot Neutron-Density, Gamma Ray-Resistivity, (opsional) pseudo-Van Krevelen
> **Catatan fasilitator:** Ini sesi yang menggabungkan **domain (petrofisika)** + **coding**. Untuk peserta dengan latar AI/Data Science, jelaskan konteks geologinya pelan-pelan — crossplot adalah cara domain ini "membaca" data, bukan sekadar scatter plot biasa.

---

## 🎯 Tujuan Sesi

Setelah sesi ini, peserta bisa:

1. Menjelaskan **apa itu crossplot** dan kenapa industri migas memakainya.
2. Membuat & membaca **crossplot Neutron-Density (NPHI–RHOB)** — crossplot paling penting.
3. Membuat **crossplot Gamma Ray–Resistivity** untuk indikasi fluida.
4. Menambahkan **dimensi ke-3** lewat pewarnaan (color by GR / by cluster).
5. (Opsional) Memahami ide **pseudo-Van Krevelen** untuk source rock.

---

## 1. Apa itu Crossplot?

**Crossplot = scatter plot dua pengukuran log**, dipakai untuk mengidentifikasi **litologi** dan **fluida**.

> **Analogi:** Satu kurva log (misal GR saja) seperti melihat orang dari satu sudut. **Crossplot menggabungkan dua kurva**, seperti melihat orang dari depan + samping sekaligus — pola yang tadinya tersembunyi jadi kelihatan.

Kenapa bukan cuma lihat kurva satu per satu? Karena **litologi punya "tanda tangan" di kombinasi dua pengukuran**. Misalnya batupasir dan batugamping bisa punya GR mirip, tapi posisinya beda di crossplot Neutron-Density.

---

## 2. Crossplot Neutron-Density (NPHI–RHOB) — Sang Andalan

Ini crossplot **paling sering dipakai** untuk menentukan litologi.

- Sumbu-X: **NPHI** (Neutron Porosity)
- Sumbu-Y: **RHOB** (Bulk Density, g/cc) — **dibalik** (nilai kecil di atas)

### Kode dasar

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 7))
sc = ax.scatter(df["NPHI"], df["RHOB"],
                c=df["GR"], cmap="jet", s=12, alpha=0.6)

ax.set_xlim(-0.05, 0.45)
ax.set_ylim(2.95, 1.95)          # PERHATIKAN: dibalik!
ax.set_xlabel("NPHI (Neutron Porosity, dec)")
ax.set_ylabel("RHOB (Bulk Density, g/cc)")
ax.set_title("Crossplot Neutron-Density")
ax.grid(True, alpha=0.3)

cbar = plt.colorbar(sc)
cbar.set_label("GR (API)")
plt.show()
```

**Penjelasan bagian:**
- `ax.set_ylim(2.95, 1.95)` → sumbu Y **dibalik** (besar ke kecil). Ini **konvensi petrofisika**: batuan padat (density tinggi) digambar di bawah, batuan porous (density rendah) di atas. Pemula sering lupa ini → plot jadi "terbalik".
- `c=df["GR"]` → titik **diwarnai** berdasarkan GR. Ini menambahkan **dimensi ketiga**: sekarang kita lihat NPHI vs RHOB *sekaligus* shaliness (GR tinggi = shale).
- `cmap="jet"` → skema warna. (Untuk produksi, `viridis`/`YlOrRd` lebih disarankan, tapi `jet` umum di industri.)

### Cara membaca (interpretasi)

| Posisi di crossplot | Indikasi |
|---|---|
| Garis litologi: kiri-atas → kanan-bawah | Sandstone → Limestone → Dolomite |
| **Crossover** (NPHI rendah, RHOB rendah, titik "naik") | **Efek gas** ⚡ |
| GR tinggi (warna), titik bergeser kanan-bawah | **Shale** |
| Sebaran sepanjang garis matriks | Variasi porositas |

> **Poin kunci:** Lokasi titik = litologi; *trend*-nya = porositas; warnanya (GR) = kandungan shale; pergeseran tak wajar ke atas = kemungkinan gas.

### Menempelkan cluster dari Sesi 1

Sekarang kita uji apakah electrofacies hasil clustering punya makna:

```python
fig, ax = plt.subplots(figsize=(7, 7))
sc = ax.scatter(df["NPHI"], df["RHOB"],
                c=df["cluster"], cmap="tab10", s=12, alpha=0.7)
ax.set_xlim(-0.05, 0.45)
ax.set_ylim(2.95, 1.95)
ax.set_xlabel("NPHI"); ax.set_ylabel("RHOB")
ax.set_title("Crossplot diwarnai berdasarkan Cluster (KMeans)")
plt.colorbar(sc, label="cluster")
plt.show()
```

**Interpretasi:** kalau tiap cluster menempati **zona yang berbeda dan rapi** di crossplot, berarti clustering berhasil menangkap perbedaan litologi yang nyata. Kalau warnanya tercampur acak → cluster kurang bermakna (mungkin perlu scaling, ganti K, atau tambah fitur).

---

## 3. Crossplot Gamma Ray – Resistivity

Crossplot ini untuk **indikasi fluida** (hidrokarbon vs air).

- **GR** → indikator shale (tinggi = shale, rendah = reservoir bersih).
- **Resistivity (RDEP)** → indikator fluida (tinggi = hidrokarbon, rendah = air asin).

```python
fig, ax = plt.subplots(figsize=(7, 6))
ax.scatter(df["GR"], df["RDEP"], s=12, alpha=0.5, c="steelblue")

ax.set_yscale("log")             # resistivity SELALU skala log
ax.set_xlabel("GR (API)")
ax.set_ylabel("Resistivity (ohm.m)")
ax.set_title("Crossplot Gamma Ray - Resistivity")

# garis bantu "rule of thumb" dari Hari 2
ax.axvline(50, color="green", linestyle="--", label="GR = 50 (zona bersih)")
ax.axhline(5,  color="red",   linestyle="--", label="Res = 5 (potensi HC)")
ax.legend()
ax.grid(True, which="both", alpha=0.3)
plt.show()
```

**Penjelasan bagian:**
- `ax.set_yscale("log")` → resistivity rentangnya sangat lebar (0.2 sampai ratusan ohm.m), jadi **wajib log scale** supaya pola kelihatan.
- `axvline(50)` & `axhline(5)` → garis aturan praktis dari Hari 2: **GR < 50 DAN Resistivity > 5** = kandidat zona reservoir berisi hidrokarbon (pojok kanan-atas di sumbu yang sudah dibalik logikanya: GR rendah + Res tinggi).

> **Zona menarik = GR rendah + Resistivity tinggi** = reservoir bersih yang kemungkinan berisi hidrokarbon (bukan air).

---

## 4. (Opsional / Advanced) pseudo-Van Krevelen

> ⚠️ **Materi advanced** — boleh dilewati kalau audiens lebih ke AI/DS atau waktu mepet.

Diagram **Van Krevelen** asalnya dari geokimia untuk menentukan **tipe kerogen** (material organik sumber minyak/gas). Sumbunya:
- **HI (Hydrogen Index)** vs **OI (Oxygen Index)**.

Disebut **"pseudo"** kalau parameternya **diturunkan dari log** (bukan dari lab Rock-Eval). Idenya: identifikasi **source rock** dan potensinya.

```python
# ilustrasi konsep (butuh kolom HI & OI dari analisis geokimia/log)
fig, ax = plt.subplots(figsize=(7, 6))
ax.scatter(df["OI"], df["HI"], s=15, alpha=0.6)
ax.set_xlabel("Oxygen Index (OI)")
ax.set_ylabel("Hydrogen Index (HI)")
ax.set_title("pseudo-Van Krevelen (tipe kerogen)")
# Tipe I (atas, prone minyak) → Tipe III (bawah, prone gas)
ax.grid(True, alpha=0.3)
plt.show()
```

**Intinya untuk peserta:** konsepnya **sama persis dengan crossplot lain** — dua sumbu, baca posisi titik untuk klasifikasi. Yang beda cuma *domain*-nya (geokimia source rock, bukan litologi reservoir).

---

## ✅ Latihan (10 menit)

Beri peserta dataset well log dan minta:

1. Buat crossplot Neutron-Density, **warnai dengan GR**. Tunjuk: mana yang kemungkinan shale?
2. Buat crossplot GR-Resistivity dengan garis bantu GR=50 & Res=5. Berapa banyak titik di "zona menarik"?
3. Warnai crossplot Neutron-Density dengan **cluster** dari Sesi 1. Apakah cluster terpisah rapi?

---

## 🔗 Koneksi ke Sesi Berikutnya

Kita sudah membuat crossplot "ala kadarnya". Di **Sesi 3 (Visualisasi Matplotlib & Seaborn)** kita akan **naik level**: memahami struktur Matplotlib (Figure vs Axes), memilih colormap yang tepat, memberi label zona, dan membuat plot multi-panel yang rapi dan interaktif.
