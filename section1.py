# -*- coding: utf-8 -*-
"""Section 1 — Loading and Displaying Well Data From CSV

Standalone version of section 1, converted from the Colab notebook.
Reads L0509WellData.csv from the current folder and saves every plot
as a JPG inside ./output/.

Run:  python section1.py
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ── output folder ────────────────────────────────────────────────────────────
OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)

DATA_FILE = "L0509WellData.csv"


def save(fig, name):
    """Save a figure to JPG (inside output/) and show it."""
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=200, bbox_inches="tight", format="jpg")
    plt.show()
    print(f"  -> saved {path}")


def load_well(path=DATA_FILE):
    """Load the well-log CSV and replace the -999 null sentinel with NaN."""
    well = pd.read_csv(path, header=0)
    well.replace(-999, np.nan, inplace=True)
    return well


def section1():
    print("\n" + "=" * 60)
    print("Section 1 - Loading & Displaying Well Data")
    print("=" * 60)

    well = pd.read_csv(DATA_FILE, header=0)
    print(well.head())
    print(well.describe())

    # The dataset uses -999 as a "no value" flag; turn it into NaN.
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


if __name__ == "__main__":
    section1()
    print("\nDone. JPGs are in the", OUT_DIR, "folder.")
