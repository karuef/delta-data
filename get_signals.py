import requests
import pandas as pd
from datetime import datetime

url = "https://www.deribit.com/api/v2/public/get_book_summary_by_currency"
params = {"currency": "BTC", "kind": "option"}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()["result"]
except Exception as e:
    print(f"❌ Deribit API hatası: {e}")
    exit(1)

records = []
for d in data:
    name = d["instrument_name"]
    mark_price = d["mark_price"]
    greeks = d.get("greeks", {})
    if not greeks:
        continue
    delta = greeks.get("delta")
    gamma = greeks.get("gamma")
    if delta is None or gamma is None:
        continue
    try:
        strike = int(name.split("-")[2])
    except:
        continue
    records.append({
        "instrument_name": name,
        "strike": strike,
        "delta": delta,
        "gamma": gamma,
        "mark_price": mark_price,
        "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    })

df = pd.DataFrame(records)

if not df.empty:
    df.to_csv("signals.csv", index=False)
    print("✅ signals.csv dosyası güncellendi.")
else:
    print("⚠️ Deribit verisi alınamadı, signals.csv oluşturulmadı.")
    exit(0)
