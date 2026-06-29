# -*- coding: utf-8 -*-
"""Section 5 — Unsupervised Clustering on Well Log Data

Standalone version of section 5, converted from the Colab notebook.
Loads xeek_train_subset.csv itself, builds KMeans + GMM facies, and saves
the elbow / silhouette / well-plot / crossplot / pairplot figures.

NOTES — bugs fixed from the notebook:
  1. NaN before clustering. The notebook fitted the SilhouetteVisualizer
     and ran the silhouette sweep BEFORE calling workingdf.dropna(), so
     scikit-learn raised "ValueError: Input contains NaN". Here dropna()
     runs first, then every model is fitted on clean data.
  2. KMeans n_init. n_init is set explicitly (=10) so behaviour is
     identical across scikit-learn versions and no FutureWarning prints.
  3. The colormap length in create_plot is taken as int(max)+1 so the
     number of colours matches the number of classes and slicing never
     fails on a numpy float.
  4. Filename sanitization. Real well names like '16/10-1' contain '/',
     which the OS reads as a folder separator -> FileNotFoundError when
     saving. safe_name() replaces unsafe characters before saving.
  5. OpenMP guard. Sets KMP_DUPLICATE_LIB_OK before numeric imports and
     silences threadpoolctl's duplicate-OpenMP warning (a conda env quirk).

Run:  python section5.py
"""

import os
# ── conda/OpenMP guard ───────────────────────────────────────────────────────
# Some conda envs load TWO OpenMP runtimes at once (Intel 'libiomp' from MKL +
# LLVM 'libomp'), which threadpoolctl warns about and can rarely crash/deadlock.
# Setting this BEFORE importing numpy/scikit-learn makes runs safe and quiet.
# This is a mitigation; the clean fix is a single-channel env (see file footer).
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import re
import warnings
# silence threadpoolctl's duplicate-OpenMP FYI so the console stays readable
warnings.filterwarnings("ignore", category=RuntimeWarning, module="threadpoolctl")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import seaborn as sns

OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)

DATA_FILE = "xeek_train_subset.csv"


def safe_name(text):
    """Make a string safe to use as a filename.

    Well names like '16/10-1' contain '/', which the OS treats as a folder
    separator -> writing 's05_wellplot_16/10-1.jpg' fails with FileNotFoundError.
    Replace anything that isn't a letter/number/dot/dash/underscore with '_'.
    """
    return re.sub(r"[^A-Za-z0-9._-]", "_", str(text))


def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=200, bbox_inches="tight", format="jpg")
    plt.show()
    print(f"  -> saved {path}")


# ── helper: full multi-track well plot ───────────────────────────────────────
def create_plot(wellname, dataframe, curves_to_plot, depth_curve,
                log_curves=None, facies_curves=None):
    if log_curves is None:
        log_curves = []
    if facies_curves is None:
        facies_curves = []

    num_tracks = len(curves_to_plot)
    facies_color = [
        "#F4D03F", "#F5B041", "#DC7633", "#6E2C00",
        "#1B4F72", "#2E86C1", "#AED6F1", "#A569BD",
        "#196F3D", "red", "black", "blue",
    ]

    fig, ax = plt.subplots(1, num_tracks, figsize=(num_tracks * 2, 10))
    fig.suptitle(wellname, fontsize=20, y=1.05)

    cmap_f = None
    for i, curve in enumerate(curves_to_plot):
        if curve in facies_curves:
            # number of colours = number of classes (int, +1 so max is included)
            n_classes = int(dataframe[curve].max()) + 1
            cmap_f = colors.ListedColormap(facies_color[0:n_classes], "indexed")
            cluster = np.repeat(
                np.expand_dims(dataframe[curve].values, 1), 100, 1)
            ax[i].imshow(
                cluster, interpolation="none", cmap=cmap_f, aspect="auto",
                vmin=dataframe[curve].min(), vmax=dataframe[curve].max(),
                extent=[0, 20, depth_curve.max(), depth_curve.min()])
        else:
            ax[i].plot(dataframe[curve], depth_curve)

        ax[i].set_title(curve, fontsize=14, fontweight="bold")
        ax[i].grid(which="major", color="lightgrey", linestyle="-")
        ax[i].set_ylim(depth_curve.max(), depth_curve.min())

        if i == 0:
            ax[i].set_ylabel("DEPTH (m)", fontsize=18, fontweight="bold")
        else:
            plt.setp(ax[i].get_yticklabels(), visible=False)

        if curve in log_curves:
            ax[i].set_xscale("log")
            ax[i].grid(which="minor", color="lightgrey", linestyle="-")

    plt.tight_layout()
    save(fig, f"s05_wellplot_{safe_name(wellname)}.jpg")
    return cmap_f


# ── helper: split a dataframe into one frame per well ────────────────────────
def well_splitter(dataframe, groupby_column):
    grouped = dataframe.groupby(groupby_column)
    dfs, names = [], []
    for name, data in grouped:
        dfs.append(data)
        names.append(name)
    print("index  wellname")
    for i, n in enumerate(names):
        print(f"{i}      {n}")
    return dfs, names


# ── helper: elbow method ─────────────────────────────────────────────────────
def optimise_k_means(data, max_k):
    from sklearn.cluster import KMeans
    inertias = []
    ks = list(range(1, max_k))
    for k in ks:
        km = KMeans(n_clusters=k, n_init=10)
        km.fit(data)
        inertias.append(km.inertia_)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(ks, inertias, "o-")
    ax.set_xlabel("Number of Clusters")
    ax.set_ylabel("Inertia")
    ax.grid(True)
    save(fig, "s05_elbow_method.jpg")


# ── helper: silhouette score sweep ───────────────────────────────────────────
def optimise_k_means_silhouette(data, max_k):
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    range_n = list(range(2, max_k))
    sil_scores = []
    for k in range_n:
        km = KMeans(n_clusters=k, n_init=10)
        km.fit(data)
        sil_scores.append(silhouette_score(data, km.labels_))
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(range_n, sil_scores, "bo-")
    ax.set_xlabel("Number of Clusters")
    ax.set_ylabel("Silhouette Score")
    ax.set_title("Silhouette Analysis For KMeans", fontsize=14, fontweight="bold")
    ax.grid(True)
    save(fig, "s05_silhouette_scores.jpg")


def section5():
    print("\n" + "=" * 60)
    print("Section 5 - Unsupervised Clustering")
    print("=" * 60)

    from sklearn.cluster import KMeans
    from sklearn.mixture import GaussianMixture

    # ── Load & prepare data ──────────────────────────────────────────────
    df = pd.read_csv(DATA_FILE)
    print(df.describe())

    workingdf = df[["WELL", "DEPTH_MD", "RDEP", "RHOB", "GR", "NPHI",
                    "PEF", "DTC",
                    "FORCE_2020_LITHOFACIES_LITHOLOGY"]].copy()
    workingdf.rename(
        columns={"FORCE_2020_LITHOFACIES_LITHOLOGY": "FACIES"}, inplace=True)

    lithology_numbers = {
        30000: "Sandstone",       65030: "Sandstone/Shale",
        65000: "Shale",           80000: "Marl",
        74000: "Dolomite",        70000: "Limestone",
        70032: "Chalk",           88000: "Halite",
        86000: "Anhydrite",       99000: "Tuff",
        90000: "Coal",            93000: "Basement",
    }
    simple_lithology_numbers = {
        30000: 1,  65030: 2,  65000: 3,  80000: 4,
        74000: 5,  70000: 6,  70032: 7,  88000: 8,
        86000: 9,  99000: 10, 90000: 11, 93000: 12,
    }

    workingdf["LITH"]    = workingdf["FACIES"].map(lithology_numbers)
    workingdf["LITH_SI"] = workingdf["FACIES"].map(simple_lithology_numbers)

    # FacetGrid per lithology
    g = sns.FacetGrid(workingdf, col="LITH", col_wrap=4)
    g.map(sns.scatterplot, "NPHI", "RHOB", alpha=0.5)
    g.set(xlim=(-0.15, 1), ylim=(3, 1))
    g.figure.suptitle("NPHI vs RHOB by Lithology", y=1.02, fontsize=16)
    save(g.figure, "s05_facetgrid_lithology.jpg")

    # Inspect the per-well split (before dropping NaNs)
    well_splitter(workingdf, "WELL")

    # ── FIX: drop NaNs BEFORE any clustering happens ─────────────────────
    # The notebook clustered first and crashed with "Input contains NaN".
    workingdf.dropna(inplace=True)
    print(workingdf.describe())

    features = workingdf[["GR", "RHOB", "NPHI", "DTC"]]

    # ── Elbow & silhouette diagnostics (now on clean data) ───────────────
    optimise_k_means(features, 30)
    optimise_k_means_silhouette(features, 5)

    # Silhouette visualizer (yellowbrick). Wrapped so a version mismatch in
    # the optional yellowbrick dependency can't take down the whole section.
    try:
        from yellowbrick.cluster import SilhouetteVisualizer
        km10 = KMeans(n_clusters=10, n_init=10)
        # scikit-learn >= 1.8 dropped the ._estimator_type attribute that
        # yellowbrick 1.5 still checks; add it back so KMeans is accepted.
        if not hasattr(km10, "_estimator_type"):
            km10._estimator_type = "clusterer"
        vis = SilhouetteVisualizer(km10, colors="yellowbrick")
        vis.fit(features)
        vis.finalize()
        # newer yellowbrick has no .fig_; pull the figure off the axes instead
        save(vis.ax.get_figure(), "s05_silhouette_visualizer_k10.jpg")
    except Exception as exc:  # pragma: no cover - optional dependency
        print(f"  (skipped yellowbrick SilhouetteVisualizer: {exc})")

    # ── KMeans k=5 ───────────────────────────────────────────────────────
    kmeans = KMeans(n_clusters=5, n_init=10)
    kmeans.fit(features)
    workingdf["KMeans"] = kmeans.labels_

    # ── GMM n_components=5 ───────────────────────────────────────────────
    gmm = GaussianMixture(n_components=5)
    gmm.fit(features)
    workingdf["GMM"] = gmm.predict(features)

    # ── Visualise per well ───────────────────────────────────────────────
    dfs_wells, wellnames = well_splitter(workingdf, "WELL")

    curves  = ["GR", "RHOB", "NPHI", "DTC", "LITH_SI", "KMeans", "GMM"]
    log_cur = ["RDEP"]
    fac_cur = ["KMeans", "GMM", "LITH_SI"]

    # pick an example well to plot; clamp so it never overruns the list
    # (which wells survive dropna() is data-dependent)
    well_idx = min(4, len(wellnames) - 1)
    cmap_facies = create_plot(
        wellnames[well_idx], dfs_wells[well_idx],
        curves, dfs_wells[well_idx]["DEPTH_MD"],
        log_cur, fac_cur)

    # 3-panel crossplot: KMeans / GMM / Lithology
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 10))
    d = dfs_wells[well_idx]

    ax1.scatter(d["NPHI"], d["RHOB"], c=d["KMeans"], s=8, cmap=cmap_facies)
    ax1.set_title("KMeans", fontsize=22, y=1.05)

    ax2.scatter(d["NPHI"], d["RHOB"], c=d["GMM"], s=8)
    ax2.set_title("GMM", fontsize=22, y=1.05)

    ax3.scatter(d["NPHI"], d["RHOB"], c=d["LITH_SI"], s=8)
    ax3.set_title("Lithology (Supplied)", fontsize=22, y=1.05)

    for a in [ax1, ax2, ax3]:
        a.set_xlim(0, 0.7); a.set_ylim(3, 1.5)
        a.set_ylabel("RHOB", fontsize=18, labelpad=30)
        a.set_xlabel("NPHI", fontsize=18, labelpad=30)
        a.grid(); a.set_axisbelow(True)
        a.tick_params(axis="both", labelsize=14)
    plt.tight_layout()
    save(fig, "s05_crossplot_kmeans_gmm_lith.jpg")

    # Pairplot - KMeans
    g1 = sns.pairplot(
        dfs_wells[well_idx], vars=["GR", "RHOB", "NPHI", "DTC"],
        hue="KMeans", palette="Dark2", diag_kind="kde",
        plot_kws={"s": 15, "marker": "o", "alpha": 1})
    g1.figure.suptitle("Pairplot - KMeans", y=1.02, fontsize=16)
    save(g1.figure, "s05_pairplot_kmeans.jpg")

    # Pairplot - GMM
    g2 = sns.pairplot(
        dfs_wells[well_idx], vars=["GR", "RHOB", "NPHI", "DTC"],
        hue="GMM", palette="Dark2", diag_kind="kde",
        plot_kws={"s": 15, "marker": "o", "alpha": 1})
    g2.figure.suptitle("Pairplot - GMM", y=1.02, fontsize=16)
    save(g2.figure, "s05_pairplot_gmm.jpg")


if __name__ == "__main__":
    section5()
    print("\nDone. JPGs are in the", OUT_DIR, "folder.")