"""Generate wealth_segment_pivot.xlsx with dummy customer analytics data.

Follows rules R1-R8 from dummy_data_gen_requirement.md.
57,600 rows = all combinations of 10 dimensions.
"""

import itertools
import random
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
np.random.seed(SEED)
random.seed(SEED)

LIFE_STAGES = [
    "young single", "young couple", "matured adult",
    "matured family with kid", "matured family without kid", "golden age",
]
WEALTH_SEGMENTS = ["High-net-worth", "Affluent", "Mass"]
CUSTOMER_TENURES = [">= 1 year", "1-3 years", "3-6 years", "6-10 years", ">10 years"]
NEW_OR_EXISTING = ["New", "Existing"]
MARKETS = ["PHKL", "PACS", "PAMB", "PBTB", "PLAI", "PSLA", "PLUK", "PVA", "PLT", "PCALT"]
HOLDING = ["Yes", "No"]

dims = [
    LIFE_STAGES, WEALTH_SEGMENTS, CUSTOMER_TENURES, NEW_OR_EXISTING, MARKETS,
    HOLDING, HOLDING, HOLDING, HOLDING, HOLDING,
]
columns = [
    "life_stage", "wealth_segment", "customer_tenure", "new_or_existing", "market",
    "saving_holding", "investment_holding", "medical_holding",
    "critical_illness_holding", "others_health_and_protection_holding",
]
df = pd.DataFrame(list(itertools.product(*dims)), columns=columns)
df["customer_count"] = 0
df["annual_premium"] = 0.0

print(f"Combinations: {len(df)} rows  (expected 57600)")


def distribute_normal(n_rows: int, total: float) -> np.ndarray:
    """Distribute `total` across `n_rows` values using normal distribution.
    Ensures every value >= 1 (for counts) or > 0 (for premiums)."""
    mean = total / n_rows
    std = mean * 0.5
    vals = np.random.normal(mean, std, n_rows)
    vals = np.clip(vals, mean * 0.01, None)
    # Rescale to exact total
    vals = vals * (total / vals.sum())
    return vals


for market in MARKETS:
    mask_market = df["market"] == market

    total_cust = round(random.uniform(500_000, 1_500_000))
    total_prem = random.uniform(20_000_000, 5_000_000_000)

    hnw_cust_pct = random.uniform(0.03, 0.15)
    hnw_prem_pct = random.uniform(0.20, 0.70)
    aff_cust_pct = random.uniform(0.50, 0.70)
    aff_prem_pct = random.uniform(0.15, 0.30)

    mass_cust_pct = 1.0 - hnw_cust_pct - aff_cust_pct
    mass_prem_pct = 1.0 - hnw_prem_pct - aff_prem_pct

    segments_cfg = {
        "High-net-worth": {"cust_total": total_cust * hnw_cust_pct,
                           "prem_total": total_prem * hnw_prem_pct},
        "Affluent":       {"cust_total": total_cust * aff_cust_pct,
                           "prem_total": total_prem * aff_prem_pct},
        "Mass":           {"cust_total": total_cust * mass_cust_pct,
                           "prem_total": total_prem * mass_prem_pct},
    }

    for seg in WEALTH_SEGMENTS:
        mask_seg = mask_market & (df["wealth_segment"] == seg)
        n_seg = mask_seg.sum()
        cfg = segments_cfg[seg]

        cust_vals = distribute_normal(n_seg, cfg["cust_total"])
        prem_vals = distribute_normal(n_seg, cfg["prem_total"])

        # Round customer_count to int, floor at 1
        cust_int = np.maximum(np.round(cust_vals).astype(int), 1)
        # Rebalance to maintain exact total
        diff = cust_int.sum() - round(cfg["cust_total"])
        if diff != 0:
            # Adjust largest values to absorb the difference
            order = np.argsort(cust_int)[::-1]
            i = 0
            while diff != 0:
                idx = order[i % n_seg]
                if diff > 0 and cust_int[idx] > 1:
                    cust_int[idx] -= 1
                    diff -= 1
                elif diff < 0:
                    cust_int[idx] += 1
                    diff += 1
                i += 1
                if i > n_seg * 10:
                    break

        df.loc[mask_seg, "customer_count"] = cust_int
        df.loc[mask_seg, "annual_premium"] = prem_vals

    tc = df.loc[mask_market, "customer_count"].sum()
    tp = df.loc[mask_market, "annual_premium"].sum()
    mhnw = mask_market & (df["wealth_segment"] == "High-net-worth")
    maff = mask_market & (df["wealth_segment"] == "Affluent")
    hnw_c = df.loc[mhnw, "customer_count"].sum() / tc
    hnw_p = df.loc[mhnw, "annual_premium"].sum() / tp
    aff_c = df.loc[maff, "customer_count"].sum() / tc
    aff_p = df.loc[maff, "annual_premium"].sum() / tp
    print(
        f"  {market:6s}  cust={tc:>10,}  prem={tp:>14,.0f}"
        f"  HNW={hnw_c:.1%}/{hnw_p:.0%}  Aff={aff_c:.0%}/{aff_p:.0%}"
    )

# ── Final checks ────────────────────────────────────────────────────────
print(f"\nRows: {len(df)}")
print(f"customer_count min={df['customer_count'].min()}  max={df['customer_count'].max()}")
print(f"annual_premium min={df['annual_premium'].min():.0f}  max={df['annual_premium'].max():.0f}")

# ── Save ────────────────────────────────────────────────────────────────
output_dir = Path("data/generated")
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "wealth_segment_pivot.xlsx"
df.to_excel(output_path, index=False, engine="openpyxl")
print(f"\nSaved: {output_path.resolve()}")
print(f"Size: {output_path.stat().st_size / 1_048_576:.1f} MB")
