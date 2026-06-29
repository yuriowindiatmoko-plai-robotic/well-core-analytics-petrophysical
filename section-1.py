# -*- coding: utf-8 -*-
"""Well Log Analysis & Unsupervised Clustering"""

# =============================================================================
# Section 1: Loading and Displaying Well Data From CSV
# =============================================================================

# Import library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import seaborn as sns
import os

OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)

def save(fig, name):
    """Save figure to JPG and show it."""
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=200, bbox_inches="tight", format="jpg")
    plt.show()
    print(f"  → saved {path}")

def main():
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

if __name__ == '__main__':
    main()
    # well.plot(x='DEPTH', y='GR')