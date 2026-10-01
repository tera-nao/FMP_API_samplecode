#src/main.py
import os
import requests
import pandas as pd

from pathlib  import Path
from datetime import date
from dateutil.relativedelta import relativedelta
from time import sleep

# .env 読み込み
from dotenv import load_dotenv
load_dotenv()

DIR = Path(__file__).resolve().parent
DATA_DIR = DIR / "../data"

# Financial Modeling Prep (FMP) の API 設定
API_KEY = os.getenv("YOUR_API_KEY")
BASE_URL = "https://financialmodelingprep.com/stable/historical-sector-performance"

#米国株のセクタ（11種）
SECTORS = [
    "Technology",
    "Healthcare",
    "Financial Services",
    "Consumer Cyclical",
    "Consumer Defensive",
    "Industrials",
    "Energy",
    "Basic Materials",
    "Communication Services",
    "Real Estate",
    "Utilities",
]

# 取得期間は過去2年とする
to_date = date.today()
from_date = to_date - relativedelta(years=2)


dfs = []

for i, sector in enumerate(SECTORS, start=1):
    params = {
        "sector": sector,
        "from": from_date.isoformat(),
        "to": to_date.isoformat(),
        "apikey": API_KEY,
    }

    print(f"[{i}/{len(SECTORS)}] Fetching: {sector}")

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()

    if not isinstance(data, list):
        print(f"Unexpected response for {sector}:")
        print(data)
        continue

    if len(data) == 0:
        print(f"No data: {sector}")
        continue

    df_sector = pd.DataFrame(data)

    # APIレスポンス側にsector列がなくても識別できるよう追加
    df_sector["sector"] = sector

    dfs.append(df_sector)

    # APIへの連続アクセスを少し緩める
    sleep(0.1)

# 全セクターを縦結合
if not dfs:
    raise RuntimeError("No sector data was retrieved.")

df = pd.concat(dfs, ignore_index=True)

# dateをdatetimeに
df["date"] = pd.to_datetime(df["date"])

# 日付 → セクター順
df = (
    df
    .sort_values(["date", "sector"])
    .reset_index(drop=True)
)


print("\nRows:", len(df))
print("Date range:", df["date"].min(), "->", df["date"].max())
print("Sectors:", df["sector"].nunique())
print("API calls:", len(SECTORS))

sector_returns = df.pivot_table(
    index="date",
    columns="sector",
    values="averageChange",
    aggfunc="first",
)

sector_returns = sector_returns.sort_index()

print(sector_returns.head())

save_path = DATA_DIR / f"FMP_sector_{from_date.strftime("%Y%m%d%H%M%S")}to{to_date.strftime("%Y%m%d%H%M%S")}.csv"

sector_returns.to_csv(
    save_path,
    encoding="utf-8-sig",
)

print("saved csv data")