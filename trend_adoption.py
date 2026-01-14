# Style Signals: Trend ≠ Adoption

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import os

#  Beauty Trends:
FASHION_BEAUTY_TRENDS = [
    "coquette",
    "mobwife",
    "balletcore",
    "cleanlook",
    "oversizedblazer",
    "sneakers",
    "skincare",
    "hairtutorial",
    "minimalistmakeup",
    "neutralpalette"
]

WEEKS = list(range(1, 7))  # 6-week window

# Simulated TikTok Viral Behavior
# (Posting / visibility behavior)

tiktok_data = []

for trend in FASHION_BEAUTY_TRENDS:
    spike_base = random.randint(60, 200)

    for week in WEEKS:
        volatility = random.randint(-30, 60)
        count = max(spike_base + volatility, 0)

        tiktok_data.append({
            "trend": trend,
            "week": week,
            "video_count": count
        })

df_tiktok = pd.DataFrame(tiktok_data)


# Adoption Profiles 
ADOPTION_PROFILES = {
    "adopted": lambda: np.cumsum(np.random.randint(1, 3, size=6)) + 20,
    "performative": lambda: np.random.randint(18, 22, size=6),
    "burnout": lambda: np.array([30, 27, 24, 20, 17, 14]),
    "dormant": lambda: np.array([12, 13, 13, 14, 14, 15])
}


TREND_ADOPTION_TYPE = {
    "coquette": "performative",
    "mobwife": "burnout",
    "balletcore": "performative",
    "cleanlook": "adopted",
    "oversizedblazer": "adopted",
    "sneakers": "adopted",
    "skincare": "adopted",
    "hairtutorial": "performative",
    "minimalistmakeup": "dormant",
    "neutralpalette": "dormant"
}

# Adoption Signals

adoption_data = {}

for trend in FASHION_BEAUTY_TRENDS:
    profile = TREND_ADOPTION_TYPE[trend]
    adoption_data[trend] = ADOPTION_PROFILES[profile]()

#  Viral vs Adoption

os.makedirs("charts", exist_ok=True)

for trend in FASHION_BEAUTY_TRENDS:
    trend_df = df_tiktok[df_tiktok["trend"] == trend]
    adoption_signal = adoption_data[trend]

    plt.figure(figsize=(8, 5))
    plt.plot(
        trend_df["week"],
        trend_df["video_count"],
        marker="o",
        label="Viral Content (Posting)"
    )
    plt.plot(
        WEEKS,
        adoption_signal,
        marker="o",
        label="Adoption Signal (Wearing)"
    )

    plt.title(f"Style Signals: {trend}")
    plt.xlabel("Week")
    plt.ylabel("Relative Frequency")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"charts/{trend}_style_signal.png")
    plt.close()

print("✅ Charts saved in /charts folder")

# SIGNAL SCORE CALCULATION

signal_scores = []

for trend in FASHION_BEAUTY_TRENDS:
    trend_df = df_tiktok[df_tiktok["trend"] == trend]

    # Viral intensity (average posting volume)
    viral_avg = trend_df["video_count"].mean()

    # Adoption growth (% change)
    adoption = adoption_data[trend]
    adoption_growth = (adoption[-1] - adoption[0]) / adoption[0]

    signal_scores.append({
        "trend": trend,
        "viral_intensity": round(viral_avg, 1),
        "adoption_growth_pct": round(adoption_growth * 100, 1)
    })

signal_df = pd.DataFrame(signal_scores)

# Normalize virality
signal_df["viral_norm"] = (
    signal_df["viral_intensity"] / signal_df["viral_intensity"].max()
)

# Compute Signal Score
signal_df["signal_score"] = (
    signal_df["adoption_growth_pct"] / signal_df["viral_norm"]
).round(2)


# Signal Labels

def label_signal(score):
    if score > 40:
        return "Strong Signal"
    elif score > 15:
        return "Emerging Signal"
    elif score > 0:
        return "Noise"
    else:
        return "Burnout"

signal_df["signal_label"] = signal_df["signal_score"].apply(label_signal)

# Rank trends
signal_df = signal_df.sort_values(
    by="signal_score",
    ascending=False
).reset_index(drop=True)

print("\n📊 STYLE SIGNALS RANKING\n")
print(signal_df)

#  Save Outputs

df_tiktok.to_csv("style_signals_tiktok_weekly.csv", index=False)
signal_df.to_csv("style_signals_scores.csv", index=False)

print("CSVs saved")
print("- style_signals_tiktok_weekly.csv")
print("- style_signals_scores.csv")
