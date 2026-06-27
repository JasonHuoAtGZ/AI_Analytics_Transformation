# Dummy Data Generation Requirement — wealth_segment_pivot.xlsx

> Created: 2026-06-27
> Status: Specification
> Output: `data/generated/wealth_segment_pivot.xlsx`

## Overview

Generate a single Excel file containing aggregated, pivot-ready dummy data for
wealth segment analysis. The data represents customer counts and annual premiums
across life insurance customer dimensions.

**Format**: One flat table with 12 columns, all combinations populated (~57,600 rows).

---

## Column Specification

| # | Column Name | Type | Possible Values | Count |
|---|---|---|---|---|
| 1 | `life_stage` | Text | `young single`, `young couple`, `matured adult`, `matured family with kid`, `matured family without kid`, `golden age` | 6 |
| 2 | `wealth_segment` | Text | `High-net-worth`, `Affluent`, `Mass` | 3 |
| 3 | `customer_tenure` | Text | `>= 1 year`, `1-3 years`, `3-6 years`, `6-10 years`, `>10 years` | 5 |
| 4 | `new_or_existing` | Text | `New`, `Existing` | 2 |
| 5 | `market` | Text | `PHKL`, `PACS`, `PAMB`, `PBTB`, `PLAI`, `PSLA`, `PLUK`, `PVA`, `PLT`, `PCALT` | 10 |
| 6 | `saving_holding` | Text | `Yes`, `No` | 2 |
| 7 | `investment_holding` | Text | `Yes`, `No` | 2 |
| 8 | `medical_holding` | Text | `Yes`, `No` | 2 |
| 9 | `critical_illness_holding` | Text | `Yes`, `No` | 2 |
| 10 | `others_health_and_protection_holding` | Text | `Yes`, `No` | 2 |
| 11 | `customer_count` | Integer | `> 0` | — |
| 12 | `annual_premium` | Float | `> 0` | — |

**Total combinations**: 6 × 3 × 5 × 2 × 10 × 2 × 2 × 2 × 2 × 2 = **57,600 rows**

---

## Generation Rules

### R1 — Completeness

The dataset must include **every combination** of columns 1 through 10.
No missing rows. No duplicate rows for the same combination.

### R2 — Market-Level Customer Count

For each market in column 5, the sum of `customer_count` (column 11) must
fall within: **500,000 to 1,500,000**.

```
FOR EACH market:
    500,000 ≤ SUM(customer_count) ≤ 1,500,000
```

### R3 — Market-Level Annual Premium

For each market in column 5, the sum of `annual_premium` (column 12) must
fall within: **20,000,000 to 5,000,000,000**.

```
FOR EACH market:
    20,000,000 ≤ SUM(annual_premium) ≤ 5,000,000,000
```

### R4 — HNW Customer Count Proportion

For each market, High-net-worth customers must account for **3% to 15%**
of total `customer_count`.

```
FOR EACH market:
    0.03 ≤ SUM(HNW customer_count) / SUM(all customer_count) ≤ 0.15
```

### R5 — HNW Annual Premium Proportion

For each market, High-net-worth customers must account for **20% to 70%**
of total `annual_premium`. This is intentionally higher than the customer count
proportion — HNW customers contribute disproportionately more premium.

```
FOR EACH market:
    0.20 ≤ SUM(HNW annual_premium) / SUM(all annual_premium) ≤ 0.70
```

### R6 — Affluent Customer Count Proportion

For each market, Affluent customers must account for **50% to 70%**
of total `customer_count`.

```
FOR EACH market:
    0.50 ≤ SUM(Affluent customer_count) / SUM(all customer_count) ≤ 0.70
```

### R7 — Affluent Annual Premium Proportion

For each market, Affluent customers must account for **15% to 30%**
of total `annual_premium`.

```
FOR EACH market:
    0.15 ≤ SUM(Affluent annual_premium) / SUM(all annual_premium) ≤ 0.30
```

### R8 — Remaining Data Distribution

For all combinations not constrained by R4-R7 (i.e., individual rows under `Mass`
segment and all rows beyond the wealth segment proportions), values for
`customer_count` and `annual_premium` should be randomly generated following a
**Normal Distribution** whose parameters are derived from the residual totals.

**Allocation logic**:

1. For each market, determine the target totals (R2, R3).
2. Allocate HNW share (R4, R5) and Affluent share (R6, R7).
3. The remaining `Mass` segment gets the residual.
4. Within each wealth segment, distribute across the other 9 dimensions
   (life_stage, tenure, new/existing, 5 × holding flags) using Normal
   Distribution with reasonable variance.
5. Ensure no individual `customer_count` or `annual_premium` is ≤ 0.

---

## Proportionality Summary

Per market, the target wealth segment breakdown:

| Wealth Segment | % of Customer Count | % of Annual Premium |
|---|---|---|
| High-net-worth | 3% – 15% | 20% – 70% |
| Affluent | 50% – 70% | 15% – 30% |
| Mass | Remainder (15% – 47%) | Remainder (0% – 65%) |

Note: Mass is the residual — it has no direct proportion constraint.

---

## Output

| Property | Value |
|---|---|
| File | `data/generated/wealth_segment_pivot.xlsx` |
| Format | Single sheet, header row, no merged cells |
| Rows | 57,600 |
| Columns | 12 |
| Random seed | Fixed (e.g., 42) for reproducibility |

---

## Validation Checklist

- [ ] All 57,600 unique combinations present (no missing, no duplicates)
- [ ] Per market customer_count total in [500K, 1.5M]
- [ ] Per market annual_premium total in [20M, 5B]
- [ ] Per market HNW customer_count % in [3%, 15%]
- [ ] Per market HNW annual_premium % in [20%, 70%]
- [ ] Per market Affluent customer_count % in [50%, 70%]
- [ ] Per market Affluent annual_premium % in [15%, 30%]
- [ ] All customer_count values > 0
- [ ] All annual_premium values > 0
- [ ] Fixed random seed produces identical output on re-run
