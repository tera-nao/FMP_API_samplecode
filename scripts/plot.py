import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams
rcParams['font.family'] = 'Noto Sans CJK JP'

from pathlib import Path

DIR = Path(__file__).resolve().parent
DATA_DIR = DIR / "../data"
OUTPUT_DIR = DIR / "../output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CSV_PATH = DATA_DIR / "FMP_sector_20240927000000to20260927000000.csv"

HIGHLIGHT = {
    "Consumer Cyclical": ("tab:blue","一般消費財（自動車含む）"),
    "Technology": ("tab:red","テクノロジー（半導体含む）")
}

df = pd.read_csv(CSV_PATH)

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").set_index("date")

# データは日ごとの変化率（Daily return）なので，累積の変化率（cumulative performance）に変換する
# 開始時点はデータ開始1日前で100としておく
# 欠損値(NaN)は0として扱う．（証券取引所の休業日に対応している気がするが今のところ原因不明）
df = df.fillna(0)
cumulative = (1 + df / 100).cumprod() * 100

base_date = cumulative.index.min() - pd.offsets.BDay(1)
cumulative.loc[base_date] = 100
cumulative = cumulative.sort_index()

#===== plot =====

fig, ax = plt.subplots(figsize=(8, 4))

for sector in cumulative.columns:

    if sector not in HIGHLIGHT:
        ax.plot(
            cumulative.index,
            cumulative[sector],
            color="gray",
            linewidth=0.7,
            alpha=0.30,
            zorder=1,
        )

for sector, color_ja_label in HIGHLIGHT.items():

    if sector in cumulative.columns:
        ax.plot(
            cumulative.index,
            cumulative[sector],
            label=color_ja_label[1],
            color=color_ja_label[0],
            linewidth=1.5,
            alpha=1.0,
            zorder=3,
        )

ax.axhline(
    100,
    color="black",
    linestyle="--",
    linewidth=0.7,
    alpha=0.5,
    zorder=0,
)

ax.xaxis.set_major_locator(
    mdates.MonthLocator(interval=1)
)

ax.xaxis.set_major_formatter(
    mdates.DateFormatter("%Y-%m")
)

plt.setp(
    ax.get_xticklabels(),
    rotation=45,
    ha="right",
)

ax.set_xlabel("日付", fontsize=12)
ax.set_ylabel("株価の累積変化量（$t_{0}=100$）", fontsize=12)

ax.grid(
    True,
    linestyle="--",
    linewidth=0.5,
    alpha=0.25,
)

ax.legend(
    frameon=False,
    fontsize=11,
    loc="upper left",
)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()

#学会発表の原稿（予稿）や論文執筆ではeps等のベクター画像が望ましい．
plt.savefig(OUTPUT_DIR / "sector_cumulative_performance.eps", bbox_inches="tight")
plt.savefig(OUTPUT_DIR / "sector_cumulative_performance.png",dpi=300,bbox_inches="tight")

plt.show()