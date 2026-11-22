"""Scoring logic for GreenSpec AI.

Kept separate from the web app so it can be tested and explained on its own.
All material scores are per 1 kg of material, on a 1-10 scale:
  - Carbon Impact: 10 = worst (highest emissions)
  - Recyclability: 10 = best (easiest to recycle)
  - Energy Impact: 10 = worst (highest production energy)
"""
import pandas as pd

COL_MATERIAL = "Material"
COL_CARBON = "Carbon Impact (10=worst)"
COL_RECYCLE = "Recyclability (10=best)"
COL_ENERGY = "Energy Impact (10=worst)"

# Weights must add up to 1. Change them here and the whole app updates.
WEIGHTS = {"carbon": 0.4, "recyclability": 0.3, "energy": 0.3}
assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9, "Weights must add up to 1"


def load_materials(path="materials.csv"):
    """Load the materials database and strip stray spaces from headers and names."""
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    df[COL_MATERIAL] = df[COL_MATERIAL].astype(str).str.strip()
    return df


def get_material_row(df, name):
    """Find a material by name (ignores case and extra spaces). Returns a row or None."""
    match = df[df[COL_MATERIAL].str.lower() == str(name).strip().lower()]
    if match.empty:
        return None
    return match.iloc[0]


def calculate_score(carbon, recyclability, energy, weights=WEIGHTS):
    """Return a sustainability score out of 100 (higher = better).

    Carbon and energy are impacts (higher = worse), so they are inverted
    with (10 - value) before weighting.
    """
    carbon_good = 10 - carbon
    energy_good = 10 - energy
    total = (
        weights["carbon"] * carbon_good
        + weights["recyclability"] * recyclability
        + weights["energy"] * energy_good
    )
    return round(total * 10, 1)


def rating_label(score):
    """Turn the score into a plain-English rating."""
    if score >= 70:
        return "Good"
    if score >= 50:
        return "Moderate"
    return "Poor"
