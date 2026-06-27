"""
Global Healthcare & Pharma Analysis (2010–2026)
================================================
Exploratory data analysis across 5 real-world datasets:
  - Biotech funding deals (1,208 deals)
  - Clinical trials (599 trials)
  - Disease burden by region (3,310 rows)
  - Drug approvals (722 approvals)
  - Pharma company financials (30 companies, 17 years)
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Load data ──────────────────────────────────────────────────────────────────
funding  = pd.read_csv("data/biotech_funding.csv", parse_dates=["date"])
trials   = pd.read_csv("data/clinical_trials.csv", parse_dates=["completion_date"])
burden   = pd.read_csv("data/disease_burden.csv")
approvals= pd.read_csv("data/drug_approvals.csv", parse_dates=["approval_date"])
financials= pd.read_csv("data/pharma_companies_financials.csv")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 1 — Biotech funding by year and deal type
# ══════════════════════════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Total funding value per year
yearly_funding = funding.groupby("year")["value_usd_bn"].sum().reset_index()
ax1.bar(yearly_funding["year"], yearly_funding["value_usd_bn"],
        color="#4C9BE8", edgecolor="white")
ax1.set_title("Total Biotech Funding by Year ($bn)", fontsize=13, fontweight="bold")
ax1.set_xlabel("Year")
ax1.set_ylabel("Total Deal Value ($bn)")
ax1.grid(axis="y", linestyle="--", alpha=0.4)
ax1.set_axisbelow(True)

# Deal type breakdown
deal_type = funding.groupby("deal_type")["value_usd_bn"].sum().sort_values(ascending=True)
colors = ["#4C9BE8","#1A5F9E","#7BB8F0","#A8D1F5","#D0E8FB"]
ax2.barh(deal_type.index, deal_type.values, color=colors[:len(deal_type)])
ax2.set_title("Total Funding by Deal Type ($bn)", fontsize=13, fontweight="bold")
ax2.set_xlabel("Total Value ($bn)")
ax2.grid(axis="x", linestyle="--", alpha=0.4)
ax2.set_axisbelow(True)

plt.suptitle("Biotech Funding Overview", fontsize=15, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/01_biotech_funding.png", dpi=150, bbox_inches="tight")
plt.close()
print("✔ Saved 01_biotech_funding.png")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 2 — Clinical trial success rates by therapy area and phase
# ══════════════════════════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Success rate by therapy area
success_by_area = (
    trials.groupby("therapy_area")["is_success"]
    .agg(["sum", "count"])
    .assign(success_rate=lambda x: 100 * x["sum"] / x["count"])
    .sort_values("success_rate", ascending=True)
)
colors = ["#E87070" if r < 40 else "#F2C94C" if r < 60 else "#6FCF97"
          for r in success_by_area["success_rate"]]
ax1.barh(success_by_area.index, success_by_area["success_rate"],
         color=colors, edgecolor="white")
ax1.axvline(50, color="gray", linestyle="--", linewidth=1, alpha=0.6)
ax1.set_title("Clinical Trial Success Rate\nby Therapy Area (%)", fontsize=13, fontweight="bold")
ax1.set_xlabel("Success Rate (%)")
ax1.grid(axis="x", linestyle="--", alpha=0.4)
ax1.set_axisbelow(True)

# Success rate by phase
success_by_phase = (
    trials.groupby("phase")["is_success"]
    .agg(["sum", "count"])
    .assign(success_rate=lambda x: 100 * x["sum"] / x["count"])
    .reindex(["Phase 1", "Phase 2", "Phase 3", "Phase 4"])
    .dropna()
)
phase_colors = ["#A8D1F5", "#4C9BE8", "#1A5F9E", "#0D3B6E"]
bars = ax2.bar(success_by_phase.index, success_by_phase["success_rate"],
               color=phase_colors[:len(success_by_phase)], edgecolor="white")
for bar, val in zip(bars, success_by_phase["success_rate"]):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f"{val:.0f}%", ha="center", fontsize=10, fontweight="bold")
ax2.set_title("Clinical Trial Success Rate\nby Phase (%)", fontsize=13, fontweight="bold")
ax2.set_xlabel("Trial Phase")
ax2.set_ylabel("Success Rate (%)")
ax2.grid(axis="y", linestyle="--", alpha=0.4)
ax2.set_axisbelow(True)

plt.suptitle("Clinical Trial Analysis", fontsize=15, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/02_clinical_trials.png", dpi=150, bbox_inches="tight")
plt.close()
print("✔ Saved 02_clinical_trials.png")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 3 — Disease burden by region over time
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(13, 6))

top_diseases = burden.groupby("disease")["dalys_millions"].sum().nlargest(5).index
burden_top = burden[burden["disease"].isin(top_diseases)]
disease_colors = ["#E87070","#4C9BE8","#F2C94C","#6FCF97","#BB6BD9"]

for i, disease in enumerate(top_diseases):
    d = burden_top[burden_top["disease"] == disease].groupby("year")["dalys_millions"].sum()
    ax.plot(d.index, d.values, linewidth=2.2, label=disease,
            color=disease_colors[i], marker="o", markersize=3)

ax.set_title("Global Disease Burden Over Time — Top 5 Diseases (DALYs, millions)",
             fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Year")
ax.set_ylabel("DALYs (millions)")
ax.legend(fontsize=9, loc="upper right")
ax.grid(linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/03_disease_burden.png", dpi=150)
plt.close()
print("✔ Saved 03_disease_burden.png")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 4 — Drug approvals: blockbusters by therapy area + trend
# ══════════════════════════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Approvals per year
approvals_by_year = approvals.groupby("year").size()
blockbusters_by_year = approvals[approvals["is_blockbuster"] == 1].groupby("year").size()

ax1.bar(approvals_by_year.index, approvals_by_year.values,
        color="#A8D1F5", label="All approvals", edgecolor="white")
ax1.bar(blockbusters_by_year.index, blockbusters_by_year.values,
        color="#1A5F9E", label="Blockbusters", edgecolor="white")
ax1.set_title("FDA Drug Approvals per Year", fontsize=13, fontweight="bold")
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Approvals")
ax1.legend(fontsize=9)
ax1.grid(axis="y", linestyle="--", alpha=0.4)
ax1.set_axisbelow(True)

# Blockbuster rate by therapy area
bb_by_area = (
    approvals.groupby("therapy_area")
    .agg(total=("approval_id","count"), blockbusters=("is_blockbuster","sum"))
    .assign(bb_rate=lambda x: 100 * x["blockbusters"] / x["total"])
    .sort_values("bb_rate", ascending=True)
)
ax2.barh(bb_by_area.index, bb_by_area["bb_rate"],
         color="#4C9BE8", edgecolor="white")
ax2.set_title("Blockbuster Rate by Therapy Area (%)", fontsize=13, fontweight="bold")
ax2.set_xlabel("Blockbuster Rate (%)")
ax2.grid(axis="x", linestyle="--", alpha=0.4)
ax2.set_axisbelow(True)

plt.suptitle("Drug Approvals Analysis", fontsize=15, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/04_drug_approvals.png", dpi=150, bbox_inches="tight")
plt.close()
print("✔ Saved 04_drug_approvals.png")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 5 — Pharma financials: revenue vs R&D spend
# ══════════════════════════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Top 8 companies by avg revenue
top_companies = (
    financials.groupby("company_name")["revenue_usd_bn"]
    .mean().nlargest(8).index
)
fin_top = financials[financials["company_name"].isin(top_companies)]

# Revenue trend for top companies
company_colors = plt.cm.tab10(np.linspace(0, 1, 8))
for i, company in enumerate(top_companies):
    d = fin_top[fin_top["company_name"] == company].sort_values("year")
    ax1.plot(d["year"], d["revenue_usd_bn"], linewidth=2,
             label=company, color=company_colors[i])
ax1.set_title("Revenue Trend — Top 8 Pharma Companies ($bn)",
              fontsize=12, fontweight="bold")
ax1.set_xlabel("Year")
ax1.set_ylabel("Revenue ($bn)")
ax1.legend(fontsize=7, loc="upper left")
ax1.grid(linestyle="--", alpha=0.4)

# R&D spend vs operating margin (scatter)
avg_fin = financials.groupby("company_name").agg(
    avg_rd=("rd_spend_usd_bn","mean"),
    avg_margin=("operating_margin_pct","mean"),
    avg_revenue=("revenue_usd_bn","mean")
).reset_index()

scatter = ax2.scatter(avg_fin["avg_rd"], avg_fin["avg_margin"],
                      s=avg_fin["avg_revenue"] * 2,
                      alpha=0.6, color="#4C9BE8", edgecolors="white", linewidth=0.5)
for _, row in avg_fin.iterrows():
    ax2.annotate(row["company_name"].split()[0],
                 (row["avg_rd"], row["avg_margin"]),
                 fontsize=6.5, ha="center", va="bottom")
ax2.set_title("R&D Spend vs Operating Margin\n(bubble size = revenue)",
              fontsize=12, fontweight="bold")
ax2.set_xlabel("Avg R&D Spend ($bn)")
ax2.set_ylabel("Avg Operating Margin (%)")
ax2.grid(linestyle="--", alpha=0.4)

plt.suptitle("Pharma Company Financials", fontsize=15, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/05_pharma_financials.png", dpi=150, bbox_inches="tight")
plt.close()
print("✔ Saved 05_pharma_financials.png")

# ── Print key findings ─────────────────────────────────────────────────────────
print("\n" + "="*55)
print("  GLOBAL PHARMA — KEY FINDINGS")
print("="*55)

total_funding = funding["value_usd_bn"].sum()
biggest_deal = funding.loc[funding["value_usd_bn"].idxmax()]
print(f"\n💰 Biotech Funding")
print(f"   Total deal value  : ${total_funding:.1f}bn across {len(funding):,} deals")
print(f"   Largest deal      : {biggest_deal['target_or_company']} (${biggest_deal['value_usd_bn']:.1f}bn, {biggest_deal['year']})")
print(f"   Megadeals         : {funding['is_megadeal'].sum()} ({100*funding['is_megadeal'].mean():.1f}% of all deals)")

success_rate = 100 * trials["is_success"].mean()
best_phase = trials.groupby("phase")["is_success"].mean().idxmax()
print(f"\n🔬 Clinical Trials")
print(f"   Overall success   : {success_rate:.1f}%")
print(f"   Best phase        : {best_phase}")
print(f"   Avg enrollment    : {trials['enrollment_n'].mean():.0f} patients")

total_approvals = len(approvals)
blockbuster_rate = 100 * approvals["is_blockbuster"].mean()
print(f"\n💊 Drug Approvals")
print(f"   Total approvals   : {total_approvals}")
print(f"   Blockbuster rate  : {blockbuster_rate:.1f}%")
print(f"   Top therapy area  : {approvals.groupby('therapy_area').size().idxmax()}")

top_company = financials.groupby("company_name")["revenue_usd_bn"].mean().idxmax()
top_rd = financials.groupby("company_name")["rd_spend_usd_bn"].mean().idxmax()
print(f"\n🏢 Pharma Financials")
print(f"   Highest avg revenue : {top_company}")
print(f"   Highest avg R&D     : {top_rd}")

print("\n✅ All charts saved to /output/")
