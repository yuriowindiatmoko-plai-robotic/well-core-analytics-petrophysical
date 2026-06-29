# -*- coding: utf-8 -*-
"""Section 3 — Displaying Histograms and Crossplots

Standalone version of section 3, converted from the Colab notebook.
Loads L0509WellData.csv itself and saves the GR histogram with stats,
the per-column distribution grid, a coloured crossplot, a 3-D scatter
and the 4-panel crossplot set.

Run:  python section3.py
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (enables 3-D projection)

OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)

DATA_FILE = "L0509WellData.csv"


def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=200, bbox_inches="tight", format="jpg")
    plt.show()
    print(f"  -> saved {path}")


def load_well(path=DATA_FILE):
    """Load the well-log CSV and replace the -999 null sentinel with NaN."""
    well = pd.read_csv(path, header=0)
    well.replace(-999, np.nan, inplace=True)
    return well


def section3(well=None):
    print("\n" + "=" * 60)
    print("Section 3 - Histograms & Crossplots")
    print("=" * 60)

    if well is None:
        well = load_well()

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

    # All-column histograms (3x2 grid)
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

    # 3-D scatter
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


if __name__ == "__main__":
    section3()
    print("\nDone. JPGs are in the", OUT_DIR, "folder.")
