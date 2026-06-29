# -*- coding: utf-8 -*-
"""Well Log Analysis & Unsupervised Clustering
Generates all plots and saves each as JPG in the output/ folder.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import seaborn as sns
from matplotlib.ticker import FuncFormatter
from mpl_toolkits.mplot3d import Axes3D

# ── output folder ──────────────────────────────────────────────────────────
OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)


def save(fig, name):
    """Save figure to JPG and show it."""
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=200, bbox_inches="tight", format="jpg")
    plt.show()
    print(f"  → saved {path}")


# =============================================================================
# Section 1: Loading and Displaying Well Data From CSV
# =============================================================================
def section1():
    print("\n" + "=" * 60)
    print("Section 1 — Loading & Displaying Well Data")
    print("=" * 60)

    well = pd.read_csv("L0509WellData.csv", header=0)
    print(well.head())
    print(well.describe())

    well.replace(-999, np.nan, inplace=True)
    print(well.describe())
    print(well.head())
    print(well.head(20))

    # Line plot: GR vs DEPTH
    fig, ax = plt.subplots(figsize=(6, 8))
    well.plot(x="DEPTH", y="GR", ax=ax)
    ax.set_title("GR vs DEPTH")
    save(fig, "s01_gr_vs_depth.jpg")

    # Scatter plot: NPHI vs RHOB
    fig, ax = plt.subplots(figsize=(6, 6))
    well.plot(kind="scatter", x="NPHI", y="RHOB", ylim=(3, 2), ax=ax)
    ax.set_title("NPHI vs RHOB")
    save(fig, "s01_nphi_vs_rhob.jpg")

    # Scatter plot: NPHI vs RHOB coloured by GR
    fig, ax = plt.subplots(figsize=(6, 6))
    well.plot(kind="scatter", x="NPHI", y="RHOB", c="GR",
              colormap="jet", ylim=(3, 2), ax=ax)
    ax.set_title("NPHI vs RHOB (coloured by GR)")
    save(fig, "s01_nphi_vs_rhob_gr.jpg")

    # Histogram GR
    fig, ax = plt.subplots(figsize=(6, 4))
    well["GR"].plot(kind="hist", bins=30, ax=ax, edgecolor="black")
    ax.set_title("GR Histogram")
    save(fig, "s01_gr_hist.jpg")

    # KDE plot GR
    fig, ax = plt.subplots(figsize=(6, 4))
    well["GR"].plot(kind="kde", xlim=(0, 200), ax=ax)
    ax.set_title("GR KDE")
    save(fig, "s01_gr_kde.jpg")

    return well


# =============================================================================
# Section 2: Displaying a Well Plot with Matplotlib
# =============================================================================
def section2(well):
    print("\n" + "=" * 60)
    print("Section 2 — Well Plot (simple)")
    print("=" * 60)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 10))

    ax1.plot("GR", "DEPTH", data=well, color="green")
    ax1.set_title("Gamma")
    ax1.set_xlim(0, 200)
    ax1.set_ylim(4850, 4600)
    ax1.grid()

    ax2.plot("RHOB", "DEPTH", data=well, color="red")
    ax2.set_title("Density")
    ax2.set_xlim(1.95, 2.95)
    ax2.set_ylim(4850, 4600)
    ax2.grid()

    ax3.plot("DT", "DEPTH", data=well, color="purple")
    ax3.set_title("Sonic")
    ax3.set_xlim(140, 40)
    ax3.set_ylim(4850, 4600)
    ax3.grid()

    save(fig, "s02_well_plot_simple.jpg")

    # ── advanced version with Neutron twin ──
    print("  Advanced well plot …")
    fig, ax = plt.subplots(figsize=(10, 10))

    ax1 = plt.subplot2grid((1, 3), (0, 0))
    ax2 = plt.subplot2grid((1, 3), (0, 1))
    ax3 = plt.subplot2grid((1, 3), (0, 2))
    ax4 = ax2.twiny()

    # hidden top borders
    for a in [ax1, ax2, ax3]:
        t = a.twiny()
        t.xaxis.set_visible(False)

    # Gamma Ray
    ax1.plot("GR", "DEPTH", data=well, color="green")
    ax1.set_xlabel("Gamma");  ax1.xaxis.label.set_color("green")
    ax1.set_xlim(0, 200);     ax1.set_ylabel("Depth (m)")
    ax1.tick_params(axis="x", colors="green")
    ax1.spines["top"].set_edgecolor("green")
    ax1.set_xticks([0, 50, 100, 150, 200])

    # Density
    ax2.plot("RHOB", "DEPTH", data=well, color="red")
    ax2.set_xlabel("Density"); ax2.xaxis.label.set_color("red")
    ax2.set_xlim(1.95, 2.95)
    ax2.tick_params(axis="x", colors="red")
    ax2.spines["top"].set_edgecolor("red")
    ax2.set_xticks([1.95, 2.2, 2.45, 2.7, 2.95])

    # Sonic
    ax3.plot("DT", "DEPTH", data=well, color="purple")
    ax3.set_xlabel("Sonic");   ax3.xaxis.label.set_color("purple")
    ax3.set_xlim(140, 40)
    ax3.tick_params(axis="x", colors="purple")
    ax3.spines["top"].set_edgecolor("purple")

    # Neutron (twin of Density)
    ax4.plot("NPHI", "DEPTH", data=well, color="blue")
    ax4.set_xlabel("Neutron"); ax4.xaxis.label.set_color("blue")
    ax4.set_xlim(0.45, -0.15); ax4.set_ylim(4850, 4600)
    ax4.tick_params(axis="x", colors="blue")
    ax4.spines["top"].set_position(("axes", 1.08))
    ax4.spines["top"].set_visible(True)
    ax4.spines["top"].set_edgecolor("blue")
    ax4.set_xticks([0.45, 0.3, 0.15, 0, -0.15])

    for a in [ax1, ax2, ax3]:
        a.set_ylim(4850, 4600)
        a.grid(which="major", color="lightgrey", linestyle="-")
        a.xaxis.set_ticks_position("top")
        a.xaxis.set_label_position("top")
        a.spines["top"].set_position(("axes", 1.02))

    plt.tight_layout()
    save(fig, "s02_well_plot_advanced.jpg")


# =============================================================================
# Section 3: Displaying Histograms and Crossplots
# =============================================================================
def section3(well):
    print("\n" + "=" * 60)
    print("Section 3 — Histograms & Crossplots")
    print("=" * 60)

    mean = well["GR"].mean()
    p5 = well["GR"].quantile(0.05)
    p95 = well["GR"].quantile(0.95)

    # GR histogram with stats lines
    fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
    well["GR"].plot(kind="hist", bins=30, color="red", alpha=0.5,
                    edgecolor="black", ax=ax)
    ax.axvline(mean, color="blue",   label="mean")
    ax.axvline(p5,   color="green",  label="5th Percentile")
    ax.axvline(p95,  color="purple", label="95th Percentile")
    ax.set_xlabel("Gamma Ray", fontsize=14)
    ax.set_ylabel("Frequency", fontsize=14)
    ax.set_xlim(0, 200)
    ax.legend()
    save(fig, "s03_gr_hist_stats.jpg")

    # All-column histograms (3×2 grid)
    cols_to_plot = [c for c in well.columns if c != "DEPTH"]
    rows, cols = 3, 2
    fig = plt.figure(figsize=(10, 10))
    for i, feature in enumerate(cols_to_plot):
        ax = fig.add_subplot(rows, cols, i + 1)
        well[feature].hist(bins=20, ax=ax, facecolor="green", alpha=0.6)
        ax.set_title(feature + " Distribution")
        ax.set_axisbelow(True)
        ax.grid(color="whitesmoke")
    plt.tight_layout()
    save(fig, "s03_all_distributions.jpg")

    # NPHI vs RHOB coloured by GR (YlOrRd_r)
    fig, ax = plt.subplots(figsize=(6, 6))
    well.plot(kind="scatter", x="NPHI", y="RHOB", c="GR",
              colormap="YlOrRd_r", ylim=(3, 2), ax=ax)
    ax.set_title("NPHI vs RHOB (YlOrRd_r)")
    save(fig, "s03_nphi_rhob_ylordr.jpg")

    # 3D scatter
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(well["NPHI"], well["RHOB"], well["GR"], alpha=0.3, c="r")
    ax.set_xlabel("NPHI"); ax.set_ylabel("RHOB"); ax.set_zlabel("GR")
    save(fig, "s03_3d_scatter.jpg")

    # 4-panel crossplots
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    panels = [
        (axes[0, 0], "NPHI", "RHOB", "s", "NPHI (dec)", "RHOB (g/cc)"),
        (axes[0, 1], "GR",   "RHOB", "p", "GR (API)",   "RHOB (g/cc)"),
        (axes[1, 0], "DT",   "RHOB", "*", "DT (us/ft)", "RHOB (g/cc)"),
        (axes[1, 1], "GR",   "DT",   "D", "GR (API)",   "DT (us/ft)"),
    ]
    for ax, xcol, ycol, marker, xlabel, ylabel in panels:
        ax.scatter(x=xcol, y=ycol, data=well, marker=marker, alpha=0.2)
        ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
        if ycol == "RHOB":
            ax.set_ylim(3, 1.8)
        ax.grid()
    plt.tight_layout()
    save(fig, "s03_four_panel_crossplots.jpg")


# =============================================================================
# Section 4: Displaying Core Data & Deriving a Poro-Perm Relationship
# =============================================================================
def section4():
    print("\n" + "=" * 60)
    print("Section 4 — Core Data & Poro-Perm Relationship")
    print("=" * 60)

    import statsmodels.api as sm

    core_data = pd.read_csv("15_9-19A-CORE.csv", na_values=[" ", -999.25])
    print(core_data.head())
    print(core_data.describe())

    # Scatter CPOR vs CKHG (linear)
    fig, ax = plt.subplots(figsize=(6, 5))
    core_data.plot(kind="scatter", x="CPOR", y="CKHG", ax=ax)
    ax.set_title("CPOR vs CKHG")
    save(fig, "s04_poro_perm_linear.jpg")

    # Scatter CPOR vs CKHG (log y)
    fig, ax = plt.subplots(figsize=(6, 5))
    core_data.plot(kind="scatter", x="CPOR", y="CKHG", ax=ax)
    ax.set_yscale("log"); ax.grid(True)
    ax.set_title("CPOR vs CKHG (log y)")
    save(fig, "s04_poro_perm_logy.jpg")

    # Polished porosity-perm plot
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(0, 40); ax.set_ylim(0.01, 100000)
    ax.plot(core_data["CPOR"], core_data["CKHG"], "bo")
    ax.set_yscale("log"); ax.grid(True)
    ax.set_ylabel("Core Perm (mD)"); ax.set_xlabel("Core Porosity (%)")
    for axis in [ax.yaxis, ax.xaxis]:
        axis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:.16g}"))
    save(fig, "s04_poro_perm_polished.jpg")

    # OLS regression
    x_ols = core_data["CPOR"]
    y_ols = np.log10(core_data["CKHG"])
    model = sm.OLS(y_ols, x_ols, missing="drop")
    results = model.fit()
    print(results.summary())

    # Polyfit degree 1
    coeffs = np.polyfit(core_data["CPOR"], np.log10(core_data["CKHG"]), 1)
    print(f"  Slope={coeffs[0]:.6f}  Intercept={coeffs[1]:.6f}")

    # Data + regression line
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(0, 30); ax.set_ylim(0.01, 10000)
    ax.semilogy(core_data["CPOR"], core_data["CKHG"], "bo")
    ax.semilogy(core_data["CPOR"],
                10 ** (coeffs[0] * core_data["CPOR"] + coeffs[1]), "r-")
    ax.grid(True)
    ax.set_ylabel("Core Perm (mD)"); ax.set_xlabel("Core Porosity (%)")
    for axis in [ax.yaxis, ax.xaxis]:
        axis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:.16g}"))
    save(fig, "s04_poro_perm_regression.jpg")

    # Predicted permeability
    core_data["PRED_PERM"] = 10 ** (coeffs[0] * core_data["CPOR"] + coeffs[1])
    print(core_data.describe())

    # Log-log: measured vs predicted
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0.01, 10000); ax.set_ylim(0.01, 10000)
    ax.loglog(core_data["CKHG"], core_data["PRED_PERM"], "bo")
    ax.loglog([0.01, 10000], [0.01, 10000], "r-")
    ax.set_xlabel("Measured Perm (mD)"); ax.set_ylabel("Predicted Perm (mD)")
    ax.set_title("Measured vs Predicted Permeability")
    ax.grid(True, which="both")
    save(fig, "s04_measured_vs_predicted.jpg")

    return core_data


# =============================================================================
# Section 5: Unsupervised Clustering on Well Log Data
# =============================================================================
def section5():
    print("\n" + "=" * 60)
    print("Section 5 — Unsupervised Clustering")
    print("=" * 60)

    from sklearn.cluster import KMeans
    from sklearn.mixture import GaussianMixture
    from sklearn.metrics import silhouette_score
    from yellowbrick.cluster import SilhouetteVisualizer

    # ── helper: create_plot ──────────────────────────────────────────────
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

        fig, ax = plt.subplots(1, num_tracks,
                               figsize=(num_tracks * 2, 10))
        fig.suptitle(wellname, fontsize=20, y=1.05)

        for i, curve in enumerate(curves_to_plot):
            if curve in facies_curves:
                cmap_f = colors.ListedColormap(
                    facies_color[0: dataframe[curve].max()], "indexed")
                cluster = np.repeat(
                    np.expand_dims(dataframe[curve].values, 1), 100, 1)
                ax[i].imshow(
                    cluster, interpolation="none", cmap=cmap_f,
                    aspect="auto",
                    vmin=dataframe[curve].min(),
                    vmax=dataframe[curve].max(),
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
        save(fig, f"s05_wellplot_{wellname.replace(' ', '_')}.jpg")

        # return cmap so callers can reuse it
        try:
            return cmap_f
        except NameError:
            return None

    # ── helper: well_splitter ────────────────────────────────────────────
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

    # ── helper: elbow method ─────────────────────────────────────────────
    def optimise_k_means(data, max_k):
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

    # ── helper: silhouette score plot ────────────────────────────────────
    def optimise_k_means_silhouette(data, max_k):
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
        ax.set_title("Silhouette Analysis For KMeans",
                      fontsize=14, fontweight="bold")
        ax.grid(True)
        save(fig, "s05_silhouette_scores.jpg")

    # ── Load & prepare data ──────────────────────────────────────────────
    df = pd.read_csv("xeek_train_subset.csv")
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
    g.fig.suptitle("NPHI vs RHOB by Lithology", y=1.02, fontsize=16)
    save(g.fig, "s05_facetgrid_lithology.jpg")

    # Split per well
    grouped_wells, grouped_names = well_splitter(workingdf, "WELL")

    # Drop NaN
    workingdf.dropna(inplace=True)
    print(workingdf.describe())

    # ── Elbow & Silhouette ───────────────────────────────────────────────
    features = workingdf[["GR", "RHOB", "NPHI", "DTC"]]
    optimise_k_means(features, 30)
    optimise_k_means_silhouette(features, 5)

    # Silhouette visualizer (yellowbrick)
    km10 = KMeans(n_clusters=10, n_init=10)
    vis = SilhouetteVisualizer(km10, colors="yellowbrick")
    vis.fit(features)
    vis.show()
    fig_sil = vis.fig_
    save(fig_sil, "s05_silhouette_visualizer_k10.jpg")

    # ── KMeans k=5 ──────────────────────────────────────────────────────
    kmeans = KMeans(n_clusters=5, n_init=10)
    kmeans.fit(features)
    workingdf["KMeans"] = kmeans.labels_

    # ── GMM n_components=5 ──────────────────────────────────────────────
    gmm = GaussianMixture(n_components=5)
    gmm.fit(features)
    workingdf["GMM"] = gmm.predict(features)

    # ── Visualise per well ──────────────────────────────────────────────
    dfs_wells, wellnames = well_splitter(workingdf, "WELL")

    curves  = ["GR", "RHOB", "NPHI", "DTC", "LITH_SI", "KMeans", "GMM"]
    log_cur = ["RDEP"]
    fac_cur = ["KMeans", "GMM", "LITH_SI"]

    well_idx = 4
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

    # Pairplot — KMeans
    g1 = sns.pairplot(
        dfs_wells[well_idx], vars=["GR", "RHOB", "NPHI", "DTC"],
        hue="KMeans", palette="Dark2", diag_kind="kde",
        plot_kws={"s": 15, "marker": "o", "alpha": 1})
    g1.fig.suptitle("Pairplot — KMeans", y=1.02, fontsize=16)
    save(g1.fig, "s05_pairplot_kmeans.jpg")

    # Pairplot — GMM
    g2 = sns.pairplot(
        dfs_wells[well_idx], vars=["GR", "RHOB", "NPHI", "DTC"],
        hue="GMM", palette="Dark2", diag_kind="kde",
        plot_kws={"s": 15, "marker": "o", "alpha": 1})
    g2.fig.suptitle("Pairplot — GMM", y=1.02, fontsize=16)
    save(g2.fig, "s05_pairplot_gmm.jpg")


# =============================================================================
# Main
# =============================================================================
def main():
    well      = section1()
    section2(well)
    section3(well)
    section4()
    section5()
    print("\n✅  All done. JPGs are in the", OUT_DIR, "folder.")


if __name__ == "__main__":
    main()