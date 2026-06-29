# -*- coding: utf-8 -*-
"""Section 2 — Displaying a Well Plot with Matplotlib

Standalone version of section 2, converted from the Colab notebook.
Loads L0509WellData.csv itself (so it runs on its own) and saves both
the simple 3-track plot and the advanced version with a Neutron twin.

Run:  python section2.py
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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


def section2(well=None):
    print("\n" + "=" * 60)
    print("Section 2 - Well Plot (simple + advanced)")
    print("=" * 60)

    if well is None:
        well = load_well()

    # ── simple 3-track plot ──────────────────────────────────────────────
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

    # ── advanced version with Neutron twin ──────────────────────────────
    print("  Advanced well plot ...")
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
    ax1.set_xlabel("Gamma"); ax1.xaxis.label.set_color("green")
    ax1.set_xlim(0, 200); ax1.set_ylabel("Depth (m)")
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
    ax3.set_xlabel("Sonic"); ax3.xaxis.label.set_color("purple")
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


if __name__ == "__main__":
    section2()
    print("\nDone. JPGs are in the", OUT_DIR, "folder.")
