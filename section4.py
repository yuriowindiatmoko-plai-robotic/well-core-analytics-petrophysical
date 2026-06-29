# -*- coding: utf-8 -*-
"""Section 4 — Displaying Core Data and Deriving a Poro-Perm Relationship

Standalone version of section 4, converted from the Colab notebook.
Loads 15_9-19A-CORE.csv itself, fits a porosity-permeability trend with
both statsmodels OLS and numpy.polyfit, and saves the crossplots.

NOTE — bugs fixed from the notebook:
    1. The notebook referenced a column called "CKH" in two plots
       (ax.semilogy(... 'CKH' ...) and ax.loglog(... 'CKH' ...)).
       That column does not exist — it is "CKHG" — so the notebook raised
       KeyError: 'CKH'. Both references below correctly use "CKHG".
    2. Real core data has gaps and zero/negative permeability values.
       np.log10 turns those into -inf / NaN, and np.polyfit / OLS cannot
       fit on -inf or NaN -> on MKL (conda) numpy this surfaces as the
       cryptic "Intel oneMKL ERROR ... DGELSD" / "SVD did not converge"
       crash. The regression below first keeps only rows where CPOR and
       CKHG are present and CKHG > 0, so the fit always gets clean input.

Run:  python section4.py
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)

DATA_FILE = "15_9-19A-CORE.csv"


def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=200, bbox_inches="tight", format="jpg")
    plt.show()
    print(f"  -> saved {path}")


def section4():
    print("\n" + "=" * 60)
    print("Section 4 - Core Data & Poro-Perm Relationship")
    print("=" * 60)

    import statsmodels.api as sm

    core_data = pd.read_csv(DATA_FILE, na_values=[" ", -999.25])
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

    # ── Clean subset for the log-log regression ──────────────────────────
    # np.log10 needs strictly positive perm: CKHG == 0 -> -inf,
    # CKHG < 0 (or an uncaught -999 null) -> NaN. Neither np.polyfit nor
    # statsmodels OLS can fit on NaN/Inf -- that is exactly what triggers
    # the "SVD did not converge" / Intel oneMKL DGELSD error on real data.
    # So keep only rows where CPOR and CKHG are present AND CKHG > 0.
    valid = (
        core_data["CPOR"].notna()
        & core_data["CKHG"].notna()
        & (core_data["CKHG"] > 0)
    )
    n_dropped = int((~valid).sum())
    if n_dropped:
        print(f"  (dropped {n_dropped} rows with missing/zero/negative "
              f"CPOR or CKHG before regression)")
    if int(valid.sum()) < 2:
        raise ValueError(
            "Tidak cukup data valid (butuh >=2 baris dengan CKHG > 0) "
            "untuk regresi poro-perm.")

    fit_df = core_data.loc[valid]
    x_fit = fit_df["CPOR"].to_numpy()
    y_fit = np.log10(fit_df["CKHG"].to_numpy())

    # OLS regression: log10(perm) vs porosity (on clean data)
    model = sm.OLS(y_fit, x_fit)
    results = model.fit()
    print(results.summary())

    # Polyfit degree 1 (on clean data)
    coeffs = np.polyfit(x_fit, y_fit, 1)
    print(f"  Slope={coeffs[0]:.6f}  Intercept={coeffs[1]:.6f}")

    # Data + regression line  (line drawn over a clean, sorted x-range)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(0, 30); ax.set_ylim(0.01, 10000)
    ax.semilogy(core_data["CPOR"], core_data["CKHG"], "bo")
    x_line = np.linspace(x_fit.min(), x_fit.max(), 100)
    ax.semilogy(x_line, 10 ** (coeffs[0] * x_line + coeffs[1]), "r-")
    ax.grid(True)
    ax.set_ylabel("Core Perm (mD)"); ax.set_xlabel("Core Porosity (%)")
    for axis in [ax.yaxis, ax.xaxis]:
        axis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:.16g}"))
    save(fig, "s04_poro_perm_regression.jpg")

    # Predicted permeability
    core_data["PRED_PERM"] = 10 ** (coeffs[0] * core_data["CPOR"] + coeffs[1])
    print(core_data.describe())

    # Log-log: measured vs predicted  (FIXED: was 'CKH', now 'CKHG')
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0.01, 10000); ax.set_ylim(0.01, 10000)
    ax.loglog(core_data["CKHG"], core_data["PRED_PERM"], "bo")
    ax.loglog([0.01, 10000], [0.01, 10000], "r-")
    ax.set_xlabel("Measured Perm (mD)"); ax.set_ylabel("Predicted Perm (mD)")
    ax.set_title("Measured vs Predicted Permeability")
    ax.grid(True, which="both")
    save(fig, "s04_measured_vs_predicted.jpg")

    return core_data


if __name__ == "__main__":
    section4()
    print("\nDone. JPGs are in the", OUT_DIR, "folder.")